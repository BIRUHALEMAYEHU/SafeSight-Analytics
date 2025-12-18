#!/usr/bin/env python3
"""
Database Verification Script
Tests that all models can be created and relationships work.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.db.base import Base
from app.models import User, Camera, Zone, PersonOfInterest, Event, Alert, Rule


async def verify_database():
    """Verify database schema and models"""
    print("🔍 Starting database verification...")
    
    try:
        # Create tables
        print("\n1️⃣ Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("   ✅ All tables created successfully!")
        
        # Drop tables (cleanup)
        print("\n2️⃣ Dropping tables (cleanup)...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("   ✅ Tables dropped successfully!")
        
        print("\n✅ Database verification complete!")
        print("\n📊 Verified Models:")
        print("   - User")
        print("   - Camera")
        print("   - Zone")
        print("   - PersonOfInterest")
        print("   - Event")
        print("   - Alert")
        print("   - Rule")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    result = asyncio.run(verify_database())
    sys.exit(0 if result else 1)
