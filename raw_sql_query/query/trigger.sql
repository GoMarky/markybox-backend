
CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS '
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
' LANGUAGE 'plpgsql';
 
CREATE TRIGGER update_updated_at_modtime BEFORE UPDATE
  ON notes FOR EACH ROW EXECUTE PROCEDURE
  update_updated_at_column();
  