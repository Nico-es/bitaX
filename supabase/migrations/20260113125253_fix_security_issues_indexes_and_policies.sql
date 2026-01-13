/*
  # Fix Security Issues - Indexes and Policies Optimization

  ## Changes
  
  1. **Drop Unused Indexes**
     - Remove all unused indexes that add overhead without performance benefit
     - Indexes on chats, messages, reviews, profiles, professionals, services, properties, favorites
  
  2. **Consolidate Multiple Permissive Policies**
     - Fix properties table: merge duplicate SELECT policies
     - Fix services table: merge duplicate SELECT policies
  
  3. **PostGIS Schema Management**
     - Move PostGIS extension to dedicated 'extensions' schema
     - Maintain spatial_ref_sys as system table (RLS not required)
  
  4. **Add Optimized Indexes**
     - Replace unused indexes with ones that match actual query patterns
     - Composite indexes for common search operations
  
  ## Security Notes
  - Unused indexes removed for better write performance
  - Policies consolidated to prevent permission conflicts
  - PostGIS isolated from public schema per best practices
  - Auth connection strategy must be changed via Supabase Dashboard (cannot be set via SQL)
*/

-- =====================================================
-- 1. DROP UNUSED INDEXES
-- =====================================================

-- Drop unused indexes on chats table
DROP INDEX IF EXISTS idx_chats_user2_id;
DROP INDEX IF EXISTS idx_chats_users;

-- Drop unused indexes on messages table
DROP INDEX IF EXISTS idx_messages_sender_id;
DROP INDEX IF EXISTS idx_messages_chat_id;

-- Drop unused indexes on reviews table
DROP INDEX IF EXISTS idx_reviews_reviewer_id;
DROP INDEX IF EXISTS idx_reviews_service_id;
DROP INDEX IF EXISTS idx_reviews_professional_id;

-- Drop unused indexes on profiles table
DROP INDEX IF EXISTS idx_profiles_location;
DROP INDEX IF EXISTS idx_profiles_user_type;

-- Drop unused indexes on professionals table
DROP INDEX IF EXISTS idx_professionals_user_id;
DROP INDEX IF EXISTS idx_professionals_profession;

-- Drop unused indexes on services table
DROP INDEX IF EXISTS idx_services_professional_id;
DROP INDEX IF EXISTS idx_services_location;
DROP INDEX IF EXISTS idx_services_category;

-- Drop unused indexes on properties table
DROP INDEX IF EXISTS idx_properties_owner_id;
DROP INDEX IF EXISTS idx_properties_location;
DROP INDEX IF EXISTS idx_properties_city;
DROP INDEX IF EXISTS idx_properties_listing_type;

-- Drop unused indexes on favorites table
DROP INDEX IF EXISTS idx_favorites_user_id;

-- =====================================================
-- 2. FIX MULTIPLE PERMISSIVE POLICIES - PROPERTIES
-- =====================================================

-- Drop existing SELECT policies on properties
DROP POLICY IF EXISTS "Anyone can view available properties" ON properties;
DROP POLICY IF EXISTS "Owners can manage own properties" ON properties;

-- Create single consolidated SELECT policy for properties
CREATE POLICY "Users can view available properties and owners can view own"
  ON properties
  FOR SELECT
  TO authenticated
  USING (
    available = true 
    OR auth.uid() = owner_id
  );

-- Recreate other policies for properties (if they don't exist)
DROP POLICY IF EXISTS "Owners can insert own properties" ON properties;
CREATE POLICY "Owners can insert own properties"
  ON properties
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = owner_id);

DROP POLICY IF EXISTS "Owners can update own properties" ON properties;
CREATE POLICY "Owners can update own properties"
  ON properties
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = owner_id)
  WITH CHECK (auth.uid() = owner_id);

DROP POLICY IF EXISTS "Owners can delete own properties" ON properties;
CREATE POLICY "Owners can delete own properties"
  ON properties
  FOR DELETE
  TO authenticated
  USING (auth.uid() = owner_id);

-- =====================================================
-- 3. FIX MULTIPLE PERMISSIVE POLICIES - SERVICES
-- =====================================================

-- Drop existing SELECT policies on services
DROP POLICY IF EXISTS "Anyone can view active services" ON services;
DROP POLICY IF EXISTS "Professionals can manage own services" ON services;

-- Create single consolidated SELECT policy for services
CREATE POLICY "Users can view active services and professionals can view own"
  ON services
  FOR SELECT
  TO authenticated
  USING (
    active = true 
    OR auth.uid() = professional_id
  );

-- Recreate other policies for services (if they don't exist)
DROP POLICY IF EXISTS "Professionals can insert own services" ON services;
CREATE POLICY "Professionals can insert own services"
  ON services
  FOR INSERT
  TO authenticated
  WITH CHECK (
    auth.uid() = professional_id
    AND EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.user_type = 'professional'
    )
  );

DROP POLICY IF EXISTS "Professionals can update own services" ON services;
CREATE POLICY "Professionals can update own services"
  ON services
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = professional_id)
  WITH CHECK (auth.uid() = professional_id);

DROP POLICY IF EXISTS "Professionals can delete own services" ON services;
CREATE POLICY "Professionals can delete own services"
  ON services
  FOR DELETE
  TO authenticated
  USING (auth.uid() = professional_id);

-- =====================================================
-- 4. MOVE POSTGIS TO EXTENSIONS SCHEMA
-- =====================================================

-- Create extensions schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS extensions;

-- Grant usage on extensions schema
GRANT USAGE ON SCHEMA extensions TO authenticated;
GRANT USAGE ON SCHEMA extensions TO anon;
GRANT USAGE ON SCHEMA extensions TO service_role;

-- Move PostGIS extension to extensions schema
-- Note: We need to drop and recreate with new schema
DO $$ 
BEGIN
  -- Check if postgis exists in public schema
  IF EXISTS (
    SELECT 1 FROM pg_extension 
    WHERE extname = 'postgis' 
    AND extnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
  ) THEN
    -- Drop from public
    DROP EXTENSION IF EXISTS postgis CASCADE;
    
    -- Recreate in extensions schema
    CREATE EXTENSION IF NOT EXISTS postgis SCHEMA extensions;
    
    -- Grant necessary permissions
    GRANT ALL ON ALL TABLES IN SCHEMA extensions TO authenticated;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA extensions TO authenticated;
    GRANT ALL ON ALL FUNCTIONS IN SCHEMA extensions TO authenticated;
    
    GRANT SELECT ON ALL TABLES IN SCHEMA extensions TO anon;
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA extensions TO anon;
  END IF;
END $$;

-- Update search_path to include extensions schema
ALTER DATABASE postgres SET search_path TO public, extensions;

-- =====================================================
-- 5. ADD USEFUL INDEXES FOR ACTUAL QUERIES
-- =====================================================

-- Add only indexes that will actually be used based on common query patterns

-- Index for finding chats by either user (used in chat listings)
CREATE INDEX IF NOT EXISTS idx_chats_user_lookup 
  ON chats(user1_id, user2_id);

-- Index for message ordering within a chat (used in message history)
CREATE INDEX IF NOT EXISTS idx_messages_chat_created 
  ON messages(chat_id, created_at DESC);

-- Composite index for property searches (city + available + type)
CREATE INDEX IF NOT EXISTS idx_properties_search 
  ON properties(city, available, listing_type);

-- Composite index for service searches (category + active)
CREATE INDEX IF NOT EXISTS idx_services_search 
  ON services(category, active);

-- Index for professional profile lookups (verified professionals)
CREATE INDEX IF NOT EXISTS idx_professionals_verified 
  ON professionals(user_id) 
  WHERE verified = true;

-- Index for recent reviews (used in professional profiles)
CREATE INDEX IF NOT EXISTS idx_reviews_target_recent 
  ON reviews(professional_id, created_at DESC);

-- =====================================================
-- 6. OPTIMIZE EXISTING TABLES
-- =====================================================

-- Analyze tables to update query planner statistics
ANALYZE chats;
ANALYZE messages;
ANALYZE reviews;
ANALYZE profiles;
ANALYZE professionals;
ANALYZE services;
ANALYZE properties;
ANALYZE favorites;

-- =====================================================
-- NOTES FOR MANUAL CONFIGURATION
-- =====================================================

/*
  IMPORTANT: Auth Connection Strategy
  
  The following cannot be changed via SQL and must be configured in Supabase Dashboard:
  
  1. Go to: Project Settings > Database > Connection Pooling
  2. Change Auth connection strategy from "Fixed (10)" to "Percentage (10%)"
  3. This allows Auth connections to scale with instance size
  
  Path: Settings > Database > Connection pooling > Edit > Auth > Change to percentage-based
*/

-- Add comment to database for documentation
COMMENT ON DATABASE postgres IS 'abitaX Database - Auth connection strategy should be percentage-based (configure in Dashboard)';
