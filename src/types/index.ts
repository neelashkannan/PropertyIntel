export interface User {
  id: number;
  email: string;
  full_name: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  full_name: string;
}

export interface Property {
  id?: number;
  user_id?: number;
  house_number: string;
  street_name: string;
  postcode: string;
  property_type: string;
  bedrooms?: number;
  bathrooms?: number;
  size_sqft?: number;
  floor_number?: number;
  new_build?: string;
  solar_panels?: string;
  epc_rating?: string;
  council_tax_band?: string;
  parking?: string;
  parking_type?: string;
  garden?: string;
  garden_type?: string;
  lift_available?: string;
  sunroom?: boolean;
  basement?: boolean;
  loft?: boolean;
  parking_additional?: boolean;
  misc_notes?: string;
  datazone?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PropertyAnalysis {
  total_properties: number;
  avg_epc_rating?: string;
  total_value_estimate?: number;
  recommendations: string[];
  energy_efficiency_score?: number;
  investment_score?: number;
  risk_assessment: string;
}

export interface APIResponse<T> {
  data: T;
  message?: string;
}

export interface APIError {
  detail: string;
  status_code: number;
}
