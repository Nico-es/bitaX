/*
  # Add support for user-uploaded services
  
  1. Changes
    - Make professional_id nullable in services table
    - Add user_id column to services table
    - Add price column to replace price_from/price_to for simple pricing
    - Update RLS policies to support both user and professional services
  
  2. Security
    - Users can insert their own services
    - Users can update their own services
    - Everyone can view active services
    - Users can delete their own services
*/

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'services' AND column_name = 'user_id'
  ) THEN
    ALTER TABLE services ADD COLUMN user_id uuid REFERENCES profiles(id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'services' AND column_name = 'price'
  ) THEN
    ALTER TABLE services ADD COLUMN price numeric;
  END IF;
END $$;

ALTER TABLE services ALTER COLUMN professional_id DROP NOT NULL;

DROP POLICY IF EXISTS "Users can view active services" ON services;
CREATE POLICY "Users can view active services"
  ON services FOR SELECT
  TO authenticated
  USING (active = true);

DROP POLICY IF EXISTS "Users can insert own services" ON services;
CREATE POLICY "Users can insert own services"
  ON services FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id OR auth.uid() IN (SELECT user_id FROM professionals WHERE id = professional_id));

DROP POLICY IF EXISTS "Users can update own services" ON services;
CREATE POLICY "Users can update own services"
  ON services FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id OR auth.uid() IN (SELECT user_id FROM professionals WHERE id = professional_id))
  WITH CHECK (auth.uid() = user_id OR auth.uid() IN (SELECT user_id FROM professionals WHERE id = professional_id));

DROP POLICY IF EXISTS "Users can delete own services" ON services;
CREATE POLICY "Users can delete own services"
  ON services FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id OR auth.uid() IN (SELECT user_id FROM professionals WHERE id = professional_id));
