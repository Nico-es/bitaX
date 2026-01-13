import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export type Profile = {
  id: string
  full_name: string
  phone?: string
  avatar_url?: string
  user_type: 'user' | 'professional'
  location?: { lat: number; lng: number }
  bio?: string
  created_at: string
  updated_at: string
}

export type Professional = {
  id: string
  user_id: string
  profession: string
  company_name?: string
  years_experience: number
  certifications: string[]
  rating: number
  total_reviews: number
  verified: boolean
  available: boolean
  created_at: string
}

export type Service = {
  id: string
  professional_id: string
  title: string
  description: string
  category: string
  price_from?: number
  price_to?: number
  currency: string
  location?: { lat: number; lng: number }
  images: string[]
  active: boolean
  created_at: string
  updated_at: string
}

export type Property = {
  id: string
  owner_id: string
  title: string
  description: string
  property_type: 'house' | 'apartment' | 'land' | 'commercial'
  listing_type: 'rent' | 'sale'
  price: number
  currency: string
  bedrooms?: number
  bathrooms?: number
  area_sqm?: number
  location: { lat: number; lng: number }
  address: string
  city: string
  images: string[]
  amenities: string[]
  available: boolean
  created_at: string
  updated_at: string
}

export type Review = {
  id: string
  reviewer_id: string
  professional_id: string
  service_id?: string
  rating: number
  comment?: string
  created_at: string
}
