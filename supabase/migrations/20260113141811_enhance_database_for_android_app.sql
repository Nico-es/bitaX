/*
  # Enhance Database Schema for Android App Integration
  
  ## Overview
  This migration adds essential features for the abitaX Android application,
  including geolocation support, booking system, notifications, and enhanced
  categorization.

  ## New Tables
  
  ### 1. service_categories
  - `id` (uuid, primary key)
  - `name` (text) - Category name (e.g., "Plomería", "Electricidad")
  - `name_en` (text) - English name for i18n
  - `icon` (text) - Icon name/url for the category
  - `description` (text) - Category description
  - `active` (boolean) - Whether category is active
  - `created_at` (timestamptz)
  
  ### 2. bookings
  - `id` (uuid, primary key)
  - `client_id` (uuid) - Reference to profiles
  - `professional_id` (uuid) - Reference to professionals
  - `service_id` (uuid, nullable) - Reference to services
  - `booking_date` (date) - Date of the booking
  - `booking_time` (time) - Time of the booking
  - `status` (text) - pending, confirmed, completed, cancelled
  - `location` (text) - Address for the service
  - `notes` (text, nullable) - Additional notes
  - `total_amount` (numeric, nullable)
  - `currency` (text)
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)
  
  ### 3. notifications
  - `id` (uuid, primary key)
  - `user_id` (uuid) - Reference to profiles
  - `title` (text) - Notification title
  - `body` (text) - Notification body
  - `type` (text) - booking, message, review, system
  - `reference_id` (uuid, nullable) - ID of related item
  - `read` (boolean) - Whether notification was read
  - `created_at` (timestamptz)
  
  ### 4. property_viewings
  - `id` (uuid, primary key)
  - `property_id` (uuid) - Reference to properties
  - `viewer_id` (uuid) - Reference to profiles
  - `viewing_date` (timestamptz)
  - `status` (text) - requested, confirmed, completed, cancelled
  - `notes` (text, nullable)
  - `created_at` (timestamptz)

  ## Table Modifications
  
  ### properties table
  - Add `latitude` (numeric) - GPS latitude
  - Add `longitude` (numeric) - GPS longitude
  - Add `featured` (boolean) - Featured listing flag
  - Add `views_count` (integer) - Number of views
  
  ### services table
  - Add `location` (text) - Service location/coverage area
  - Add `latitude` (numeric) - GPS latitude
  - Add `longitude` (numeric) - GPS longitude
  - Add `category_id` (uuid) - Reference to service_categories
  - Add `featured` (boolean) - Featured service flag
  
  ### professionals table
  - Add `location` (text) - Professional's location
  - Add `latitude` (numeric) - GPS latitude
  - Add `longitude` (numeric) - GPS longitude
  - Add `response_time_hours` (integer) - Average response time
  - Add `completion_rate` (numeric) - Job completion percentage
  
  ### profiles table
  - Add `fcm_token` (text) - Firebase Cloud Messaging token for push notifications
  - Add `notification_enabled` (boolean) - User notification preferences
  - Add `language` (text) - Preferred language (es, en, fr)
  
  ## Security
  - Enable RLS on all new tables
  - Add policies for authenticated user access
  - Ensure users can only access their own data
  
  ## Indexes
  - Add spatial indexes for latitude/longitude queries
  - Add indexes for foreign keys
  - Add indexes for frequently queried fields
*/

-- =====================================================
-- 1. CREATE SERVICE CATEGORIES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS service_categories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  name_en text NOT NULL,
  icon text,
  description text,
  active boolean NOT NULL DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- Add some default categories
INSERT INTO service_categories (name, name_en, icon, description) VALUES
  ('Plomería', 'Plumbing', 'wrench', 'Servicios de plomería y fontanería'),
  ('Electricidad', 'Electrical', 'zap', 'Servicios eléctricos y cableado'),
  ('Carpintería', 'Carpentry', 'hammer', 'Trabajos de madera y carpintería'),
  ('Limpieza', 'Cleaning', 'sparkles', 'Servicios de limpieza profesional'),
  ('Construcción', 'Construction', 'hard-hat', 'Construcción y remodelación'),
  ('Jardinería', 'Gardening', 'leaf', 'Mantenimiento de jardines y paisajismo'),
  ('Pintura', 'Painting', 'paint-brush', 'Servicios de pintura interior y exterior'),
  ('Mudanzas', 'Moving', 'truck', 'Servicios de mudanza y transporte'),
  ('Reparaciones', 'Repairs', 'tool', 'Reparaciones generales del hogar'),
  ('Tecnología', 'Technology', 'laptop', 'Servicios de TI y soporte técnico')
ON CONFLICT DO NOTHING;

-- =====================================================
-- 2. CREATE BOOKINGS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS bookings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  professional_id uuid NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
  service_id uuid REFERENCES services(id) ON DELETE SET NULL,
  booking_date date NOT NULL,
  booking_time time NOT NULL,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
  location text NOT NULL,
  latitude numeric,
  longitude numeric,
  notes text,
  total_amount numeric,
  currency text DEFAULT 'XAF',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- =====================================================
-- 3. CREATE NOTIFICATIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title text NOT NULL,
  body text NOT NULL,
  type text NOT NULL CHECK (type IN ('booking', 'message', 'review', 'system', 'property')),
  reference_id uuid,
  read boolean NOT NULL DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- =====================================================
-- 4. CREATE PROPERTY VIEWINGS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS property_viewings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  property_id uuid NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
  viewer_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  viewing_date timestamptz NOT NULL,
  status text NOT NULL DEFAULT 'requested' CHECK (status IN ('requested', 'confirmed', 'completed', 'cancelled')),
  notes text,
  created_at timestamptz DEFAULT now()
);

-- =====================================================
-- 5. ALTER PROPERTIES TABLE
-- =====================================================

DO $$
BEGIN
  -- Add latitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'properties' AND column_name = 'latitude'
  ) THEN
    ALTER TABLE properties ADD COLUMN latitude numeric;
  END IF;

  -- Add longitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'properties' AND column_name = 'longitude'
  ) THEN
    ALTER TABLE properties ADD COLUMN longitude numeric;
  END IF;

  -- Add featured column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'properties' AND column_name = 'featured'
  ) THEN
    ALTER TABLE properties ADD COLUMN featured boolean DEFAULT false;
  END IF;

  -- Add views_count column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'properties' AND column_name = 'views_count'
  ) THEN
    ALTER TABLE properties ADD COLUMN views_count integer DEFAULT 0;
  END IF;
END $$;

-- =====================================================
-- 6. ALTER SERVICES TABLE
-- =====================================================

DO $$
BEGIN
  -- Add location column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'services' AND column_name = 'location'
  ) THEN
    ALTER TABLE services ADD COLUMN location text;
  END IF;

  -- Add latitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'services' AND column_name = 'latitude'
  ) THEN
    ALTER TABLE services ADD COLUMN latitude numeric;
  END IF;

  -- Add longitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'services' AND column_name = 'longitude'
  ) THEN
    ALTER TABLE services ADD COLUMN longitude numeric;
  END IF;

  -- Add category_id column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'services' AND column_name = 'category_id'
  ) THEN
    ALTER TABLE services ADD COLUMN category_id uuid REFERENCES service_categories(id);
  END IF;

  -- Add featured column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'services' AND column_name = 'featured'
  ) THEN
    ALTER TABLE services ADD COLUMN featured boolean DEFAULT false;
  END IF;
END $$;

-- =====================================================
-- 7. ALTER PROFESSIONALS TABLE
-- =====================================================

DO $$
BEGIN
  -- Add location column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'professionals' AND column_name = 'location'
  ) THEN
    ALTER TABLE professionals ADD COLUMN location text;
  END IF;

  -- Add latitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'professionals' AND column_name = 'latitude'
  ) THEN
    ALTER TABLE professionals ADD COLUMN latitude numeric;
  END IF;

  -- Add longitude column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'professionals' AND column_name = 'longitude'
  ) THEN
    ALTER TABLE professionals ADD COLUMN longitude numeric;
  END IF;

  -- Add response_time_hours column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'professionals' AND column_name = 'response_time_hours'
  ) THEN
    ALTER TABLE professionals ADD COLUMN response_time_hours integer DEFAULT 24;
  END IF;

  -- Add completion_rate column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'professionals' AND column_name = 'completion_rate'
  ) THEN
    ALTER TABLE professionals ADD COLUMN completion_rate numeric DEFAULT 100.00 CHECK (completion_rate >= 0 AND completion_rate <= 100);
  END IF;
END $$;

-- =====================================================
-- 8. ALTER PROFILES TABLE
-- =====================================================

DO $$
BEGIN
  -- Add fcm_token column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'fcm_token'
  ) THEN
    ALTER TABLE profiles ADD COLUMN fcm_token text;
  END IF;

  -- Add notification_enabled column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'notification_enabled'
  ) THEN
    ALTER TABLE profiles ADD COLUMN notification_enabled boolean DEFAULT true;
  END IF;

  -- Add language column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'language'
  ) THEN
    ALTER TABLE profiles ADD COLUMN language text DEFAULT 'es' CHECK (language IN ('es', 'en', 'fr'));
  END IF;
END $$;

-- =====================================================
-- 9. CREATE INDEXES
-- =====================================================

-- Service categories indexes
CREATE INDEX IF NOT EXISTS idx_service_categories_active ON service_categories(active) WHERE active = true;

-- Bookings indexes
CREATE INDEX IF NOT EXISTS idx_bookings_client_id ON bookings(client_id);
CREATE INDEX IF NOT EXISTS idx_bookings_professional_id ON bookings(professional_id);
CREATE INDEX IF NOT EXISTS idx_bookings_service_id ON bookings(service_id);
CREATE INDEX IF NOT EXISTS idx_bookings_date ON bookings(booking_date);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_location ON bookings(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- Notifications indexes
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read) WHERE read = false;
CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at DESC);

-- Property viewings indexes
CREATE INDEX IF NOT EXISTS idx_property_viewings_property_id ON property_viewings(property_id);
CREATE INDEX IF NOT EXISTS idx_property_viewings_viewer_id ON property_viewings(viewer_id);
CREATE INDEX IF NOT EXISTS idx_property_viewings_date ON property_viewings(viewing_date);

-- Geolocation indexes for properties
CREATE INDEX IF NOT EXISTS idx_properties_location ON properties(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_properties_featured ON properties(featured) WHERE featured = true;

-- Geolocation indexes for services
CREATE INDEX IF NOT EXISTS idx_services_location ON services(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_services_category_id ON services(category_id);
CREATE INDEX IF NOT EXISTS idx_services_featured ON services(featured) WHERE featured = true;

-- Geolocation indexes for professionals
CREATE INDEX IF NOT EXISTS idx_professionals_location ON professionals(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- FCM token index for push notifications
CREATE INDEX IF NOT EXISTS idx_profiles_fcm_token ON profiles(fcm_token) WHERE fcm_token IS NOT NULL;

-- =====================================================
-- 10. ENABLE RLS ON NEW TABLES
-- =====================================================

ALTER TABLE service_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE property_viewings ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 11. CREATE RLS POLICIES - SERVICE_CATEGORIES
-- =====================================================

CREATE POLICY "Anyone can view active categories"
  ON service_categories
  FOR SELECT
  TO authenticated
  USING (active = true);

-- =====================================================
-- 12. CREATE RLS POLICIES - BOOKINGS
-- =====================================================

CREATE POLICY "Users can view their bookings as client"
  ON bookings
  FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = client_id);

CREATE POLICY "Professionals can view their bookings"
  ON bookings
  FOR SELECT
  TO authenticated
  USING (
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  );

CREATE POLICY "Clients can create bookings"
  ON bookings
  FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT auth.uid()) = client_id);

CREATE POLICY "Clients can update their bookings"
  ON bookings
  FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = client_id)
  WITH CHECK ((SELECT auth.uid()) = client_id);

CREATE POLICY "Professionals can update their bookings"
  ON bookings
  FOR UPDATE
  TO authenticated
  USING (
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  )
  WITH CHECK (
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  );

CREATE POLICY "Clients can delete their bookings"
  ON bookings
  FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = client_id);

-- =====================================================
-- 13. CREATE RLS POLICIES - NOTIFICATIONS
-- =====================================================

CREATE POLICY "Users can view their notifications"
  ON notifications
  FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can update their notifications"
  ON notifications
  FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can delete their notifications"
  ON notifications
  FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = user_id);

-- =====================================================
-- 14. CREATE RLS POLICIES - PROPERTY_VIEWINGS
-- =====================================================

CREATE POLICY "Viewers can view their viewing requests"
  ON property_viewings
  FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = viewer_id);

CREATE POLICY "Property owners can view requests for their properties"
  ON property_viewings
  FOR SELECT
  TO authenticated
  USING (
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  );

CREATE POLICY "Users can create viewing requests"
  ON property_viewings
  FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT auth.uid()) = viewer_id);

CREATE POLICY "Viewers can update their requests"
  ON property_viewings
  FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = viewer_id)
  WITH CHECK ((SELECT auth.uid()) = viewer_id);

CREATE POLICY "Property owners can update viewing status"
  ON property_viewings
  FOR UPDATE
  TO authenticated
  USING (
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  )
  WITH CHECK (
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  );

CREATE POLICY "Viewers can delete their requests"
  ON property_viewings
  FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = viewer_id);

-- =====================================================
-- 15. CREATE TRIGGER FOR UPDATED_AT
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger to bookings table
DROP TRIGGER IF EXISTS update_bookings_updated_at ON bookings;
CREATE TRIGGER update_bookings_updated_at
  BEFORE UPDATE ON bookings
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 16. ANALYZE TABLES
-- =====================================================

ANALYZE service_categories;
ANALYZE bookings;
ANALYZE notifications;
ANALYZE property_viewings;
ANALYZE properties;
ANALYZE services;
ANALYZE professionals;
ANALYZE profiles;
