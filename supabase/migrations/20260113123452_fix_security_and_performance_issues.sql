/*
  # Fix Security and Performance Issues

  ## Changes
  
  ### 1. Add Missing Foreign Key Indexes
  - Add index on `chats.user2_id`
  - Add index on `messages.sender_id`
  - Add index on `reviews.reviewer_id`
  - Add index on `reviews.service_id`

  ### 2. Optimize RLS Policies
  - Replace `auth.uid()` with `(select auth.uid())` in all policies
  - This prevents re-evaluation for each row, improving performance at scale

  ### 3. Fix Function Search Paths
  - Make function search paths immutable for security

  ### 4. Consolidate Duplicate Policies
  - Remove redundant SELECT policies that overlap
*/

-- Add missing foreign key indexes
CREATE INDEX IF NOT EXISTS idx_chats_user2_id ON chats(user2_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_reviews_reviewer_id ON reviews(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_service_id ON reviews(service_id);

-- Drop existing policies to recreate them with optimizations
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
DROP POLICY IF EXISTS "Professionals can update own profile" ON professionals;
DROP POLICY IF EXISTS "Users can create professional profile" ON professionals;
DROP POLICY IF EXISTS "Professionals can manage own services" ON services;
DROP POLICY IF EXISTS "Owners can manage own properties" ON properties;
DROP POLICY IF EXISTS "Users can create reviews" ON reviews;
DROP POLICY IF EXISTS "Users can update own reviews" ON reviews;
DROP POLICY IF EXISTS "Users can view own chats" ON chats;
DROP POLICY IF EXISTS "Users can create chats" ON chats;
DROP POLICY IF EXISTS "Users can update own chats" ON chats;
DROP POLICY IF EXISTS "Users can view messages from own chats" ON messages;
DROP POLICY IF EXISTS "Users can send messages to own chats" ON messages;
DROP POLICY IF EXISTS "Users can update own messages" ON messages;
DROP POLICY IF EXISTS "Users can view own favorites" ON favorites;
DROP POLICY IF EXISTS "Users can manage own favorites" ON favorites;

-- Recreate optimized policies for profiles
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = id)
  WITH CHECK ((select auth.uid()) = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = id);

-- Recreate optimized policies for professionals
CREATE POLICY "Professionals can update own profile"
  ON professionals FOR UPDATE
  TO authenticated
  USING (user_id = (select auth.uid()))
  WITH CHECK (user_id = (select auth.uid()));

CREATE POLICY "Users can create professional profile"
  ON professionals FOR INSERT
  TO authenticated
  WITH CHECK (user_id = (select auth.uid()));

-- Recreate optimized policies for services
CREATE POLICY "Professionals can manage own services"
  ON services FOR ALL
  TO authenticated
  USING (
    professional_id IN (
      SELECT id FROM professionals WHERE user_id = (select auth.uid())
    )
  )
  WITH CHECK (
    professional_id IN (
      SELECT id FROM professionals WHERE user_id = (select auth.uid())
    )
  );

-- Recreate optimized policies for properties
CREATE POLICY "Owners can manage own properties"
  ON properties FOR ALL
  TO authenticated
  USING (owner_id = (select auth.uid()))
  WITH CHECK (owner_id = (select auth.uid()));

-- Recreate optimized policies for reviews
CREATE POLICY "Users can create reviews"
  ON reviews FOR INSERT
  TO authenticated
  WITH CHECK (reviewer_id = (select auth.uid()));

CREATE POLICY "Users can update own reviews"
  ON reviews FOR UPDATE
  TO authenticated
  USING (reviewer_id = (select auth.uid()))
  WITH CHECK (reviewer_id = (select auth.uid()));

-- Recreate optimized policies for chats
CREATE POLICY "Users can view own chats"
  ON chats FOR SELECT
  TO authenticated
  USING (user1_id = (select auth.uid()) OR user2_id = (select auth.uid()));

CREATE POLICY "Users can create chats"
  ON chats FOR INSERT
  TO authenticated
  WITH CHECK (user1_id = (select auth.uid()) OR user2_id = (select auth.uid()));

CREATE POLICY "Users can update own chats"
  ON chats FOR UPDATE
  TO authenticated
  USING (user1_id = (select auth.uid()) OR user2_id = (select auth.uid()))
  WITH CHECK (user1_id = (select auth.uid()) OR user2_id = (select auth.uid()));

-- Recreate optimized policies for messages
CREATE POLICY "Users can view messages from own chats"
  ON messages FOR SELECT
  TO authenticated
  USING (
    chat_id IN (
      SELECT id FROM chats WHERE user1_id = (select auth.uid()) OR user2_id = (select auth.uid())
    )
  );

CREATE POLICY "Users can send messages to own chats"
  ON messages FOR INSERT
  TO authenticated
  WITH CHECK (
    sender_id = (select auth.uid()) AND
    chat_id IN (
      SELECT id FROM chats WHERE user1_id = (select auth.uid()) OR user2_id = (select auth.uid())
    )
  );

CREATE POLICY "Users can update own messages"
  ON messages FOR UPDATE
  TO authenticated
  USING (
    chat_id IN (
      SELECT id FROM chats WHERE user1_id = (select auth.uid()) OR user2_id = (select auth.uid())
    )
  )
  WITH CHECK (
    chat_id IN (
      SELECT id FROM chats WHERE user1_id = (select auth.uid()) OR user2_id = (select auth.uid())
    )
  );

-- Consolidate favorites policies (remove duplicate SELECT policy)
DROP POLICY IF EXISTS "Users can view own favorites" ON favorites;

CREATE POLICY "Users can manage own favorites"
  ON favorites FOR ALL
  TO authenticated
  USING (user_id = (select auth.uid()))
  WITH CHECK (user_id = (select auth.uid()));

-- Drop triggers first before dropping functions
DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;
DROP TRIGGER IF EXISTS update_services_updated_at ON services;
DROP TRIGGER IF EXISTS update_properties_updated_at ON properties;
DROP TRIGGER IF EXISTS update_rating_after_review ON reviews;

-- Drop and recreate functions with immutable search paths
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP FUNCTION IF EXISTS update_professional_rating();

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION update_professional_rating()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  UPDATE professionals
  SET 
    rating = (SELECT AVG(rating)::numeric(3,2) FROM reviews WHERE professional_id = NEW.professional_id),
    total_reviews = (SELECT COUNT(*) FROM reviews WHERE professional_id = NEW.professional_id)
  WHERE id = NEW.professional_id;
  RETURN NEW;
END;
$$;

-- Recreate triggers
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_properties_updated_at BEFORE UPDATE ON properties
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rating_after_review AFTER INSERT OR UPDATE ON reviews
  FOR EACH ROW EXECUTE FUNCTION update_professional_rating();
