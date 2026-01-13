/*
  # Fix Security and Performance Issues
  
  ## Overview
  This migration addresses security vulnerabilities and performance issues identified
  by the Supabase security advisor.
  
  ## Changes
  
  ### 1. Add Missing Foreign Key Indexes
  - `chats.user1_id` - Critical for chat lookup queries
  - `messages.chat_id` - Critical for message retrieval
  - `reviews.professional_id` - Important for professional review queries
  
  ### 2. Remove Redundant Indexes
  - Remove unused foreign key indexes that duplicate primary key indexes
  - Keep indexes that will be used by actual application queries
  
  ### 3. Fix Multiple Permissive Policies
  - Combine multiple SELECT policies into single policies with OR conditions
  - Combine multiple UPDATE policies appropriately
  - This improves performance and reduces policy evaluation overhead
  
  ### 4. Fix Function Security
  - Set immutable search_path on `update_updated_at_column` function
  - Prevents potential SQL injection through search_path manipulation
  
  ## Manual Configuration Required
  - Auth Connection Strategy: Set to percentage-based (10%) in Dashboard
  - Leaked Password Protection: Enable in Auth settings
  
  These cannot be configured via SQL and must be set in Supabase Dashboard.
*/

-- =====================================================
-- 1. ADD MISSING FOREIGN KEY INDEXES
-- =====================================================

-- Critical index for chats.user1_id foreign key
-- Used for queries like: "get all chats where user is participant 1"
CREATE INDEX IF NOT EXISTS idx_chats_user1_id_fk 
  ON chats(user1_id);

-- Critical index for messages.chat_id foreign key
-- Used for queries like: "get all messages in a chat"
CREATE INDEX IF NOT EXISTS idx_messages_chat_id_fk 
  ON messages(chat_id);

-- Important index for reviews.professional_id foreign key
-- Used for queries like: "get all reviews for a professional"
CREATE INDEX IF NOT EXISTS idx_reviews_professional_id_fk 
  ON reviews(professional_id);

-- =====================================================
-- 2. REMOVE REDUNDANT AND UNUSED INDEXES
-- =====================================================

-- These indexes were created in advance but are redundant or will not be used
-- We keep only indexes that will actually improve query performance

-- Remove redundant foreign key indexes (keeping the ones we just created above)
DROP INDEX IF EXISTS idx_chats_user2_id_fk;
DROP INDEX IF EXISTS idx_messages_sender_id_fk;
DROP INDEX IF EXISTS idx_properties_owner_id_fk;
DROP INDEX IF EXISTS idx_reviews_reviewer_id_fk;
DROP INDEX IF EXISTS idx_reviews_service_id_fk;
DROP INDEX IF EXISTS idx_services_professional_id_fk;

-- Remove unused feature indexes
DROP INDEX IF EXISTS idx_service_categories_active;
DROP INDEX IF EXISTS idx_properties_featured;
DROP INDEX IF EXISTS idx_services_featured;
DROP INDEX IF EXISTS idx_profiles_fcm_token;

-- Remove unused geolocation indexes (these would need PostGIS for real spatial queries)
DROP INDEX IF EXISTS idx_bookings_location;
DROP INDEX IF EXISTS idx_properties_location;
DROP INDEX IF EXISTS idx_services_location;
DROP INDEX IF EXISTS idx_professionals_location;

-- Keep these indexes as they will be used by actual queries:
-- - idx_bookings_client_id (used in "my bookings" queries)
-- - idx_bookings_professional_id (used in "professional's bookings" queries)
-- - idx_bookings_service_id (used in service booking lookups)
-- - idx_bookings_date (used for date-based queries)
-- - idx_bookings_status (used for filtering by status)
-- - idx_notifications_user_id (used in "my notifications" queries)
-- - idx_notifications_read (used for unread notifications)
-- - idx_notifications_created (used for chronological sorting)
-- - idx_property_viewings_property_id (used for property viewing queries)
-- - idx_property_viewings_viewer_id (used for user's viewing requests)
-- - idx_property_viewings_date (used for date-based queries)
-- - idx_services_category_id (used for category browsing)

-- =====================================================
-- 3. FIX MULTIPLE PERMISSIVE POLICIES - BOOKINGS
-- =====================================================

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their bookings as client" ON bookings;
DROP POLICY IF EXISTS "Professionals can view their bookings" ON bookings;
DROP POLICY IF EXISTS "Clients can update their bookings" ON bookings;
DROP POLICY IF EXISTS "Professionals can update their bookings" ON bookings;

-- Create combined SELECT policy
CREATE POLICY "Users can view their bookings"
  ON bookings
  FOR SELECT
  TO authenticated
  USING (
    (SELECT auth.uid()) = client_id
    OR
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  );

-- Create combined UPDATE policy
CREATE POLICY "Users can update their bookings"
  ON bookings
  FOR UPDATE
  TO authenticated
  USING (
    (SELECT auth.uid()) = client_id
    OR
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  )
  WITH CHECK (
    (SELECT auth.uid()) = client_id
    OR
    (SELECT auth.uid()) IN (
      SELECT user_id FROM professionals WHERE id = professional_id
    )
  );

-- =====================================================
-- 4. FIX MULTIPLE PERMISSIVE POLICIES - PROPERTY VIEWINGS
-- =====================================================

-- Drop existing policies
DROP POLICY IF EXISTS "Viewers can view their viewing requests" ON property_viewings;
DROP POLICY IF EXISTS "Property owners can view requests for their properties" ON property_viewings;
DROP POLICY IF EXISTS "Viewers can update their requests" ON property_viewings;
DROP POLICY IF EXISTS "Property owners can update viewing status" ON property_viewings;

-- Create combined SELECT policy
CREATE POLICY "Users can view their property viewings"
  ON property_viewings
  FOR SELECT
  TO authenticated
  USING (
    (SELECT auth.uid()) = viewer_id
    OR
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  );

-- Create combined UPDATE policy
CREATE POLICY "Users can update their property viewings"
  ON property_viewings
  FOR UPDATE
  TO authenticated
  USING (
    (SELECT auth.uid()) = viewer_id
    OR
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  )
  WITH CHECK (
    (SELECT auth.uid()) = viewer_id
    OR
    (SELECT auth.uid()) IN (
      SELECT owner_id FROM properties WHERE id = property_id
    )
  );

-- Keep the DELETE policy for viewers
-- (Already exists: "Viewers can delete their requests")

-- =====================================================
-- 5. FIX FUNCTION SECURITY - SEARCH PATH
-- =====================================================

-- Drop all triggers first
DROP TRIGGER IF EXISTS update_bookings_updated_at ON bookings;
DROP TRIGGER IF EXISTS update_properties_updated_at ON properties;
DROP TRIGGER IF EXISTS update_services_updated_at ON services;
DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;

-- Drop the function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Recreate the function with a secure, immutable search_path
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER 
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Re-add triggers
CREATE TRIGGER update_bookings_updated_at
  BEFORE UPDATE ON bookings
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_properties_updated_at
  BEFORE UPDATE ON properties
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at
  BEFORE UPDATE ON services
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 6. ANALYZE TABLES FOR QUERY PLANNER
-- =====================================================

ANALYZE bookings;
ANALYZE property_viewings;
ANALYZE chats;
ANALYZE messages;
ANALYZE reviews;

-- =====================================================
-- 7. ADD DOCUMENTATION COMMENTS
-- =====================================================

COMMENT ON INDEX idx_chats_user1_id_fk IS 'Foreign key index for chat participant 1 lookups';
COMMENT ON INDEX idx_messages_chat_id_fk IS 'Foreign key index for retrieving messages by chat';
COMMENT ON INDEX idx_reviews_professional_id_fk IS 'Foreign key index for professional review queries';

COMMENT ON FUNCTION update_updated_at_column() IS 'Secure trigger function to update updated_at timestamp with immutable search_path';

-- =====================================================
-- MANUAL CONFIGURATION REQUIRED
-- =====================================================

/*
  IMPORTANT: The following security improvements require manual configuration
  in the Supabase Dashboard and CANNOT be set via SQL:
  
  1. AUTH CONNECTION STRATEGY (Critical for Scalability)
     Location: Project Settings > Database > Connection Pooling
     Action: Change Auth connection strategy from "Fixed (10)" to "Percentage (10%)"
     Reason: Allows Auth connections to scale with instance size
  
  2. LEAKED PASSWORD PROTECTION (Critical for Security)
     Location: Authentication > Providers > Email
     Action: Enable "Leaked Password Protection"
     Reason: Prevents users from using passwords compromised in data breaches
             by checking against HaveIBeenPwned.org database
  
  Please configure these settings in the Supabase Dashboard to complete
  the security hardening process.
*/
