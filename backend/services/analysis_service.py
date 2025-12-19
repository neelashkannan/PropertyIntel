from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import Property
import pandas as pd
import numpy as np
from collections import defaultdict
import statistics


class AnalysisService:
    """Service class for advanced property analysis and market insights"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def market_analysis(self, user_id: int, location_filter: Optional[str] = None) -> Dict[str, Any]:
        """Perform market analysis for user's portfolio"""
        properties = self.db.query(Property).filter(Property.user_id == user_id).all()
        
        if location_filter:
            properties = [p for p in properties if p.postcode and location_filter.upper() in p.postcode.upper()]
        
        if not properties:
            return {
                "market_trends": {},
                "price_analysis": {},
                "investment_metrics": {},
                "recommendations": []
            }
        
        # Market trends analysis
        market_trends = self._analyze_market_trends(properties)
        
        # Price analysis
        price_analysis = self._analyze_prices(properties)
        
        # Investment metrics
        investment_metrics = self._calculate_investment_metrics(properties)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(properties)
        
        return {
            "market_trends": market_trends,
            "price_analysis": price_analysis,
            "investment_metrics": investment_metrics,
            "recommendations": recommendations
        }
    
    def property_comparison(self, property_ids: List[int], user_id: int) -> Dict[str, Any]:
        """Compare multiple properties"""
        properties = self.db.query(Property).filter(
            Property.id.in_(property_ids),
            Property.user_id == user_id
        ).all()
        
        if len(properties) < 2:
            return {"error": "At least 2 properties required for comparison"}
        
        comparison_data = []
        for prop in properties:
            comparison_data.append({
                "id": prop.id,
                "address": f"{prop.house_number} {prop.street_name}",
                "postcode": prop.postcode,
                "property_type": prop.property_type,
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "size_sqft": prop.size_sqft,
                "estimated_value": prop.estimated_value,
                "epc_rating": prop.epc_rating,
                "features": {
                    "parking": prop.parking,
                    "garden": prop.garden,
                    "solar_panels": prop.solar_panels,
                    "new_build": prop.new_build
                }
            })
        
        # Calculate comparison metrics
        values = [p.estimated_value for p in properties if p.estimated_value]
        sizes = [p.size_sqft for p in properties if p.size_sqft]
        
        metrics = {
            "value_range": {"min": min(values), "max": max(values)} if values else {},
            "size_range": {"min": min(sizes), "max": max(sizes)} if sizes else {},
            "price_per_sqft": [v/s for v, s in zip(values, sizes) if v and s],
            "average_value": statistics.mean(values) if values else 0,
            "average_size": statistics.mean(sizes) if sizes else 0
        }
        
        return {
            "properties": comparison_data,
            "metrics": metrics,
            "insights": self._generate_comparison_insights(properties)
        }
    
    def portfolio_optimization(self, user_id: int) -> Dict[str, Any]:
        """Provide portfolio optimization suggestions"""
        properties = self.db.query(Property).filter(Property.user_id == user_id).all()
        
        if not properties:
            return {"message": "No properties found for optimization"}
        
        # Analyze current portfolio
        portfolio_stats = self._calculate_portfolio_stats(properties)
        
        # Identify gaps and opportunities
        gaps = self._identify_portfolio_gaps(properties)
        
        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(properties, portfolio_stats, gaps)
        
        return {
            "current_portfolio": portfolio_stats,
            "identified_gaps": gaps,
            "optimization_suggestions": suggestions,
            "risk_analysis": self._analyze_portfolio_risk(properties)
        }
    
    def _analyze_market_trends(self, properties: List[Property]) -> Dict[str, Any]:
        """Analyze market trends from property data"""
        # Group by property type
        type_analysis = defaultdict(list)
        for prop in properties:
            if prop.property_type and prop.estimated_value:
                type_analysis[prop.property_type].append(prop.estimated_value)
        
        trends = {}
        for prop_type, values in type_analysis.items():
            if values:
                trends[prop_type] = {
                    "average_value": statistics.mean(values),
                    "median_value": statistics.median(values),
                    "value_range": {"min": min(values), "max": max(values)},
                    "growth_potential": self._estimate_growth_potential(prop_type)
                }
        
        return trends
    
    def _analyze_prices(self, properties: List[Property]) -> Dict[str, Any]:
        """Analyze price patterns"""
        values = [p.estimated_value for p in properties if p.estimated_value]
        sizes = [p.size_sqft for p in properties if p.size_sqft]
        
        if not values:
            return {}
        
        # Price per square foot analysis
        price_per_sqft = []
        for prop in properties:
            if prop.estimated_value and prop.size_sqft:
                price_per_sqft.append(prop.estimated_value / prop.size_sqft)
        
        return {
            "value_statistics": {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                "range": {"min": min(values), "max": max(values)}
            },
            "price_per_sqft": {
                "mean": statistics.mean(price_per_sqft) if price_per_sqft else 0,
                "median": statistics.median(price_per_sqft) if price_per_sqft else 0,
                "range": {"min": min(price_per_sqft), "max": max(price_per_sqft)} if price_per_sqft else {}
            }
        }
    
    def _calculate_investment_metrics(self, properties: List[Property]) -> Dict[str, Any]:
        """Calculate investment performance metrics"""
        total_value = sum(p.estimated_value for p in properties if p.estimated_value)
        total_investment = sum(p.purchase_price for p in properties if p.purchase_price)
        
        if total_investment == 0:
            return {"message": "Purchase prices needed for investment analysis"}
        
        roi = ((total_value - total_investment) / total_investment) * 100
        
        # Estimate rental yields (simplified calculation)
        estimated_annual_rental = total_value * 0.05  # 5% yield assumption
        rental_yield = (estimated_annual_rental / total_value) * 100 if total_value > 0 else 0
        
        return {
            "total_investment": total_investment,
            "current_value": total_value,
            "total_return": total_value - total_investment,
            "roi_percentage": roi,
            "estimated_rental_yield": rental_yield,
            "portfolio_growth": roi > 0
        }
    
    def _generate_recommendations(self, properties: List[Property]) -> List[str]:
        """Generate investment recommendations"""
        recommendations = []
        
        # Analyze property types
        type_counts = defaultdict(int)
        for prop in properties:
            if prop.property_type:
                type_counts[prop.property_type] += 1
        
        # Diversification recommendations
        if len(type_counts) == 1:
            recommendations.append("Consider diversifying your portfolio with different property types")
        
        # EPC recommendations
        poor_epc = [p for p in properties if p.epc_rating in ['E', 'F', 'G']]
        if poor_epc:
            recommendations.append(f"Consider improving EPC ratings for {len(poor_epc)} properties to increase value")
        
        # Location analysis
        postcodes = [p.postcode for p in properties if p.postcode]
        if len(set(postcodes)) == 1:
            recommendations.append("Consider geographical diversification across different areas")
        
        # Solar panel opportunities
        no_solar = [p for p in properties if p.solar_panels == 'No']
        if len(no_solar) > len(properties) * 0.7:
            recommendations.append("Consider solar panel installations to improve sustainability and reduce costs")
        
        return recommendations
    
    def _calculate_portfolio_stats(self, properties: List[Property]) -> Dict[str, Any]:
        """Calculate current portfolio statistics"""
        return {
            "total_properties": len(properties),
            "property_types": dict(defaultdict(int, [(p.property_type, 1) for p in properties if p.property_type])),
            "average_bedrooms": statistics.mean([p.bedrooms for p in properties if p.bedrooms]),
            "locations": len(set([p.postcode for p in properties if p.postcode])),
            "epc_distribution": dict(defaultdict(int, [(p.epc_rating, 1) for p in properties if p.epc_rating]))
        }
    
    def _identify_portfolio_gaps(self, properties: List[Property]) -> List[str]:
        """Identify gaps in portfolio"""
        gaps = []
        
        # Check for missing property types
        current_types = set([p.property_type for p in properties if p.property_type])
        all_types = {'house', 'flat', 'detached', 'semi-detached', 'bungalow'}
        missing_types = all_types - current_types
        
        if missing_types:
            gaps.append(f"Missing property types: {', '.join(missing_types)}")
        
        # Check bedroom diversity
        bedrooms = [p.bedrooms for p in properties if p.bedrooms]
        if bedrooms and len(set(bedrooms)) < 3:
            gaps.append("Limited bedroom diversity - consider varied property sizes")
        
        return gaps
    
    def _generate_optimization_suggestions(self, properties: List[Property], stats: Dict, gaps: List[str]) -> List[str]:
        """Generate portfolio optimization suggestions"""
        suggestions = []
        
        # Size-based suggestions
        if stats['total_properties'] < 5:
            suggestions.append("Consider expanding portfolio to 5+ properties for better diversification")
        
        # Location suggestions
        if stats['locations'] < 3:
            suggestions.append("Consider investing in 2-3 additional locations for geographical diversification")
        
        # Value suggestions
        values = [p.estimated_value for p in properties if p.estimated_value]
        if values and len(set(values)) < 3:
            suggestions.append("Consider properties in different value brackets for balanced risk")
        
        return suggestions
    
    def _analyze_portfolio_risk(self, properties: List[Property]) -> Dict[str, Any]:
        """Analyze portfolio risk factors"""
        risks = []
        risk_score = 0
        
        # Concentration risk
        type_counts = defaultdict(int)
        for prop in properties:
            if prop.property_type:
                type_counts[prop.property_type] += 1
        
        max_concentration = max(type_counts.values()) / len(properties)
        if max_concentration > 0.7:
            risks.append("High concentration in single property type")
            risk_score += 2
        
        # Location concentration
        postcodes = [p.postcode for p in properties if p.postcode]
        if len(set(postcodes)) <= 2:
            risks.append("Limited geographical diversification")
            risk_score += 1
        
        # EPC risk
        poor_epc_count = len([p for p in properties if p.epc_rating in ['E', 'F', 'G']])
        if poor_epc_count > len(properties) * 0.3:
            risks.append("High proportion of poor EPC ratings")
            risk_score += 1
        
        return {
            "risk_factors": risks,
            "risk_score": min(risk_score, 5),  # Max 5
            "risk_level": "Low" if risk_score <= 1 else "Medium" if risk_score <= 3 else "High"
        }
    
    def _estimate_growth_potential(self, property_type: str) -> str:
        """Estimate growth potential for property type (simplified)"""
        growth_rates = {
            'flat': 'Medium',
            'house': 'High',
            'detached': 'High',
            'semi-detached': 'Medium',
            'bungalow': 'Medium'
        }
        return growth_rates.get(property_type, 'Medium')
    
    def _generate_comparison_insights(self, properties: List[Property]) -> List[str]:
        """Generate insights from property comparison"""
        insights = []
        
        values = [p.estimated_value for p in properties if p.estimated_value]
        if values:
            value_diff = max(values) - min(values)
            if value_diff > 100000:
                insights.append(f"Significant value difference: £{value_diff:,.0f}")
        
        # EPC comparison
        epc_ratings = [p.epc_rating for p in properties if p.epc_rating]
        if len(set(epc_ratings)) > 1:
            insights.append("Properties have different EPC ratings - consider improvements for lower-rated properties")
        
        return insights