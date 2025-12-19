from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models import Property
from schemas import PropertyCreate, PropertyUpdate, PropertyAnalysis
import statistics
from collections import defaultdict, Counter


class PropertyService:
    """Service class for property-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_property(self, property_data: PropertyCreate, user_id: int) -> Property:
        """Create a new property"""
        property_dict = property_data.model_dump()
        property_dict['user_id'] = user_id
        
        property_obj = Property(**property_dict)
        self.db.add(property_obj)
        self.db.commit()
        self.db.refresh(property_obj)
        return property_obj
    
    def get_property(self, property_id: int, user_id: int) -> Optional[Property]:
        """Get a property by ID for a specific user"""
        return self.db.query(Property).filter(
            Property.id == property_id,
            Property.user_id == user_id
        ).first()
    
    def get_properties(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Property]:
        """Get all properties for a user"""
        return self.db.query(Property).filter(
            Property.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def update_property(self, property_id: int, property_data: PropertyUpdate, user_id: int) -> Optional[Property]:
        """Update a property"""
        property_obj = self.get_property(property_id, user_id)
        if not property_obj:
            return None
        
        update_dict = property_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(property_obj, field, value)
        
        self.db.commit()
        self.db.refresh(property_obj)
        return property_obj
    
    def delete_property(self, property_id: int, user_id: int) -> bool:
        """Delete a property"""
        property_obj = self.get_property(property_id, user_id)
        if not property_obj:
            return False
        
        self.db.delete(property_obj)
        self.db.commit()
        return True
    
    def analyze_portfolio(self, user_id: int) -> PropertyAnalysis:
        """Analyze user's property portfolio and map to API schema"""
        properties = self.get_properties(user_id)

        if not properties:
            return PropertyAnalysis(
                total_properties=0,
                avg_epc_rating=None,
                total_value_estimate=None,
                recommendations=[],
                energy_efficiency_score=None,
                investment_score=None,
                risk_assessment="Low",
            )

        total_properties = len(properties)

        # EPC average as a letter (A best, G worst)
        epc_map = {"A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
        reverse_epc = {v: k for k, v in epc_map.items()}
        epc_values = [epc_map[e.upper()] for e in [p.epc_rating or "" for p in properties] if e and e.upper() in epc_map]
        avg_epc_rating = reverse_epc.get(round(sum(epc_values) / len(epc_values))) if epc_values else None

        # Naive total value estimate based on size if available
        # Assumes ~£250 per sqft as a rough placeholder
        per_sqft = 250
        size_estimates = [(p.size_sqft or 0) * per_sqft for p in properties if p.size_sqft]
        total_value_estimate = float(sum(size_estimates)) if size_estimates else None

        # Energy efficiency score (0-100) based on proportion of A-C ratings
        good_epc_count = len([p for p in properties if (p.epc_rating or "").upper() in {"A", "B", "C"}])
        energy_efficiency_score = round(100 * good_epc_count / total_properties, 2)

        # Investment score (0-100) using simple feature weights
        score = 0
        for p in properties:
            if (p.epc_rating or "").upper() in {"A", "B", "C"}:
                score += 20
            if p.solar_panels == "Yes":
                score += 15
            if p.garden == "Yes":
                score += 10
            if p.parking == "Yes":
                score += 10
            if p.new_build == "Yes":
                score += 15
        investment_score = min(round(score / total_properties), 100)

        # Risk assessment based on concentration and EPC distribution
        type_counts = Counter([p.property_type for p in properties if p.property_type])
        max_concentration = (max(type_counts.values()) / total_properties) if type_counts else 0
        poor_epc = len([p for p in properties if (p.epc_rating or "").upper() in {"E", "F", "G"}])
        risk_score = 0
        if max_concentration > 0.7:
            risk_score += 1
        if poor_epc > total_properties * 0.3:
            risk_score += 1
        risk_assessment = "Low" if risk_score == 0 else ("Medium" if risk_score == 1 else "High")

        # Recommendations
        recommendations: List[str] = []
        if poor_epc:
            recommendations.append(
                f"Consider improving EPC ratings for {poor_epc} properties"
            )
        if max_concentration > 0.7:
            recommendations.append("Diversify property types to reduce concentration risk")
        if not size_estimates:
            recommendations.append("Add property sizes to improve value estimates")

        return PropertyAnalysis(
            total_properties=total_properties,
            avg_epc_rating=avg_epc_rating,
            total_value_estimate=total_value_estimate,
            recommendations=recommendations,
            energy_efficiency_score=energy_efficiency_score,
            investment_score=investment_score,
            risk_assessment=risk_assessment,
        )
    
    def search_properties(self, user_id: int, query: str) -> List[Property]:
        """Search properties by address or postcode"""
        return self.db.query(Property).filter(
            Property.user_id == user_id,
            (Property.street_name.ilike(f"%{query}%")) |
            (Property.postcode.ilike(f"%{query}%")) |
            (Property.house_number.ilike(f"%{query}%"))
        ).all()
    
    def filter_properties(self, user_id: int, filters: Dict[str, Any]) -> List[Property]:
        """Filter properties based on criteria"""
        query = self.db.query(Property).filter(Property.user_id == user_id)
        
        if filters.get('property_type'):
            query = query.filter(Property.property_type == filters['property_type'])
        
        if filters.get('bedrooms'):
            query = query.filter(Property.bedrooms == filters['bedrooms'])
        
        if filters.get('epc_rating'):
            query = query.filter(Property.epc_rating == filters['epc_rating'])
        
        # Skip value-based filters as there's no persisted estimated value
        # Could be implemented via size_sqft heuristic if needed
        
        return query.all()
    
    def get_property_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get detailed property statistics"""
        properties = self.get_properties(user_id)
        
        if not properties:
            return {}
        
        # Value statistics via size heuristic (~£250/sqft)
        per_sqft = 250
        values = [p.size_sqft * per_sqft for p in properties if p.size_sqft]
        value_stats = {
            'min': min(values) if values else 0,
            'max': max(values) if values else 0,
            'median': statistics.median(values) if values else 0,
            'mean': statistics.mean(values) if values else 0
        }
        
        # Size statistics
        sizes = [p.size_sqft for p in properties if p.size_sqft]
        size_stats = {
            'min': min(sizes) if sizes else 0,
            'max': max(sizes) if sizes else 0,
            'median': statistics.median(sizes) if sizes else 0,
            'mean': statistics.mean(sizes) if sizes else 0
        }
        
        # Feature analysis
        features = {
            'parking': sum(1 for p in properties if p.parking == 'Yes'),
            'garden': sum(1 for p in properties if p.garden == 'Yes'),
            'solar_panels': sum(1 for p in properties if p.solar_panels == 'Yes'),
            'new_build': sum(1 for p in properties if p.new_build == 'Yes')
        }
        
        return {
            'value_statistics': value_stats,
            'size_statistics': size_stats,
            'feature_counts': features,
            'total_properties': len(properties)
        }
