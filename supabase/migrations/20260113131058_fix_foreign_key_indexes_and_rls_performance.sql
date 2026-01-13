/*
  # Fix Foreign Key Indexes and RLS Performance Issues

  ## Changes
  
  1. **Add Missing Foreign Key Indexes**
     - Add indexes for all unindexed foreign keys
     - Improves join performance and foreign key constraint checks
  
  2. **Optimize RLS Policies for Performance**
     - Replace `auth.uid()` with `(select auth.uid())`
     - Prevents re-evaluation of auth function for each row
     - Significantly improves query performance at scale
  
  3. **Remove Unused Indexes**
     - Drop indexes that aren't being used by actual queries
  
  ## Performance Notes
  - Foreign key indexes improve join operations and cascade operations
  - RLS optimization can provide 10x+ performance improvement on large tables
  - Using subquery pattern for auth.uid() evaluates once per query instead of per row
*/

-- =====================================================
-- 1. ADD MISSING FOREIGN KEY INDEXES
-- =====================================================

-- Index for chats.user2_id foreign key
CREATE INDEX IF NOT EXISTS idx_chats_user2_id_fk 
  ON chats(user2_id);

-- Index for messages.sender_id foreign key
CREATE INDEX IF NOT EXISTS idx_messages_sender_id_fk 
  ON messages(sender_id);

-- Index for properties.owner_id foreign key
CREATE INDEX IF NOT EXISTS idx_properties_owner_id_fk 
  ON properties(owner_id);

-- Index for reviews.reviewer_id foreign key
CREATE INDEX IF NOT EXISTS idx_reviews_reviewer_id_fk 
  ON reviews(reviewer_id);

-- Index for reviews.service_id foreign key
CREATE INDEX IF NOT EXISTS idx_reviews_service_id_fk 
  ON reviews(service_id);

-- Index for services.professional_id foreign key
CREATE INDEX IF NOT EXISTS idx_services_professional_id_fk 
  ON services(professional_id);

-- =====================================================
-- 2. OPTIMIZE RLS POLICIES - PROPERTIES TABLE
-- =====================================================

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view available properties and owners can view own" ON properties;
DROP POLICY IF EXISTS "Owners can insert own properties" ON properties;
DROP POLICY IF EXISTS "Owners can update own properties" ON properties;
DROP POLICY IF EXISTS "Owners can delete own properties" ON properties;

-- Recreate with optimized auth.uid() pattern
CREATE POLICY "Users can view available properties and owners can view own"
  ON properties
  FOR SELECT
  TO authenticated
  USING (
    available = true 
    OR (SELECT auth.uid()) = owner_id
  );

CREATE POLICY "Owners can insert own properties"
  ON properties
  FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT auth.uid()) = owner_id);

CREATE POLICY "Owners can update own properties"
  ON properties
  FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = owner_id)
  WITH CHECK ((SELECT auth.uid()) = owner_id);

CREATE POLICY "Owners can delete own properties"
  ON properties
  FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = owner_id);

-- =====================================================
-- 3. OPTIMIZE RLS POLICIES - SERVICES TABLE
-- =====================================================

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view active services and professionals can view own" ON services;
DROP POLICY IF EXISTS "Professionals can insert own services" ON services;
DROP POLICY IF EXISTS "Professionals can update own services" ON services;
DROP POLICY IF EXISTS "Professionals can delete own services" ON services;

-- Recreate with optimized auth.uid() pattern
CREATE POLICY "Users can view active services and professionals can view own"
  ON services
  FOR SELECT
  TO authenticated
  USING (
    active = true 
    OR (SELECT auth.uid()) = professional_id
  );

CREATE POLICY "Professionals can insert own services"
  ON services
  FOR INSERT
  TO authenticated
  WITH CHECK (
    (SELECT auth.uid()) = professional_id
    AND EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = (SELECT auth.uid())
      AND profiles.user_type = 'professional'
    )
  );

CREATE POLICY "Professionals can update own services"
  ON services
  FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = professional_id)
  WITH CHECK ((SELECT auth.uid()) = professional_id);

CREATE POLICY "Professionals can delete own services"
  ON services
  FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = professional_id);

-- =====================================================
-- 4. DROP UNUSED INDEXES
-- =====================================================

-- Drop indexes that aren't being used by actual queries
DROP INDEX IF EXISTS idx_chats_user_lookup;
DROP INDEX IF EXISTS idx_messages_chat_created;
DROP INDEX IF EXISTS idx_properties_search;
DROP INDEX IF EXISTS idx_services_search;
DROP INDEX IF EXISTS idx_professionals_verified;
DROP INDEX IF EXISTS idx_reviews_target_recent;

-- =====================================================
-- 5. ANALYZE TABLES
-- =====================================================

-- Update query planner statistics
ANALYZE chats;
ANALYZE messages;
ANALYZE properties;
ANALYZE reviews;
ANALYZE services;
ANALYZE profiles;

-- =====================================================
-- NOTES FOR MANUAL CONFIGURATION
-- =====================================================

/*
  IMPORTANT: Manual Configuration Required in Supabase Dashboard
  
  1. Auth Connection Strategy (Database Settings)
     - Go to: Project Settings > Database > Connection Pooling
     - Change Auth from "Fixed (10)" to "Percentage (10%)"
     - This allows Auth connections to scale with instance size
  
  2. Leaked Password Protection (Auth Settings)
     - Go to: Authentication > Providers > Email
     - Enable "Leaked Password Protection"
     - This checks passwords against HaveIBeenPwned.org database
     - Prevents users from using compromised passwords
  
  These settings cannot be configured via SQL and must be set through the Dashboard.
*/

-- Add database comment for documentation
COMMENT ON DATABASE postgres IS 'abitaX Database - Manual config needed: 1) Set Auth connection to percentage-based, 2) Enable leaked password protection';
