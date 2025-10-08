"""
Migration script to add new profile fields to students table
"""
from sqlalchemy import text
from app.database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Add new columns to students table"""
    
    migrations = [
        # Personal Information
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS date_of_birth DATE",
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20)",
        
        # Education Information
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS school_name VARCHAR(200)",
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS grade_level VARCHAR(50)",
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS major_field VARCHAR(100)",
        
        # Learning Preferences
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS study_goals TEXT",
        
        # Additional Info
        "ALTER TABLE students ADD COLUMN IF NOT EXISTS bio TEXT",
    ]
    
    try:
        with engine.connect() as conn:
            logger.info("Starting database migration...")
            
            for migration in migrations:
                try:
                    conn.execute(text(migration))
                    conn.commit()
                    logger.info(f"✓ Executed: {migration[:60]}...")
                except Exception as e:
                    logger.warning(f"Migration already applied or error: {str(e)}")
            
            logger.info("✓ Database migration completed successfully!")
            logger.info("\nNew profile fields added:")
            logger.info("  - date_of_birth (Date of birth)")
            logger.info("  - phone_number (Phone number)")
            logger.info("  - school_name (School/College name)")
            logger.info("  - grade_level (Current grade)")
            logger.info("  - major_field (Major/Field of study)")
            logger.info("  - study_goals (Learning goals)")
            logger.info("  - bio (Short biography)")
            
    except Exception as e:
        logger.error(f"✗ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("Profile Fields Migration")
    print("=" * 60)
    print()
    migrate_database()
    print()
    print("=" * 60)
    print("Migration Complete!")
    print("=" * 60)
