#!/usr/bin/env python3
"""
Migration script from MIGRU V1 (JSON) to V2 (SQL Database)

Usage:
    python migrate_v1_to_v2.py

This will:
1. Read data from migru_data.json
2. Create a demo user in the new database
3. Migrate all logs to the new schema
4. Calculate initial analytics
"""
import json
from pathlib import Path
from datetime import datetime
from app.database import (
    SessionLocal, init_db,
    User, MigraineLog, UserAnalytics,
    get_or_create_user, calculate_user_analytics,
    HealthStatus, RiskLevel, OnboardingStatus
)


def migrate():
    """Run the migration"""
    print("🚀 MIGRU V1 → V2 Migration")
    print("-" * 50)

    # Initialize database
    print("📊 Initializing database...")
    init_db()

    # Check for old data file
    data_file = Path("migru_data.json")
    if not data_file.exists():
        print("⚠️  No migru_data.json found - creating fresh database")
        print("✅ Database initialized successfully")
        return

    # Load old data
    print("📖 Reading migru_data.json...")
    with open(data_file) as f:
        old_data = json.load(f)

    print(f"   Found {len(old_data.get('logs', []))} logs to migrate")

    # Create database session
    db = SessionLocal()

    try:
        # Create demo user for migrated data
        print("👤 Creating demo user...")
        user = get_or_create_user(db, "migrated_v1_user", "demo@migru.app")

        # Set status from old data
        status_map = {
            "Balanced": HealthStatus.BALANCED,
            "Prodromal": HealthStatus.PRODROMAL,
            "Attack": HealthStatus.ATTACK,
            "Postdromal": HealthStatus.POSTDROMAL,
            "Recovery": HealthStatus.RECOVERY
        }
        user.current_status = status_map.get(old_data.get('status', 'Balanced'), HealthStatus.BALANCED)

        # Set HRV
        user.current_hrv = old_data.get('hrv', 65)

        # Set risk level
        risk_map = {
            "Low": RiskLevel.LOW,
            "Moderate": RiskLevel.MODERATE,
            "High": RiskLevel.HIGH
        }
        user.current_risk_level = risk_map.get(old_data.get('risk_level', 'Moderate'), RiskLevel.MODERATE)

        # Mark onboarding as complete
        user.onboarding_status = OnboardingStatus.COMPLETED
        user.onboarding_completed_at = datetime.utcnow()

        db.commit()
        print(f"   ✅ User created: {user.email}")

        # Migrate logs
        print("📝 Migrating logs...")
        migrated_count = 0
        for log in old_data.get('logs', []):
            try:
                # Parse date
                log_date = datetime.fromisoformat(log['date'].replace('Z', '+00:00'))

                # Create new log entry
                migraine_log = MigraineLog(
                    user_id=user.id,
                    created_at=log_date,
                    severity=log.get('severity', 5),
                    primary_symptoms=log.get('symptoms', []),
                    notes=log.get('notes', ''),
                    status_before=user.current_status
                )

                db.add(migraine_log)
                migrated_count += 1

            except Exception as e:
                print(f"   ⚠️  Failed to migrate log: {e}")
                continue

        db.commit()
        print(f"   ✅ Migrated {migrated_count} logs")

        # Calculate analytics
        print("📊 Calculating analytics...")
        analytics = calculate_user_analytics(db, user)
        print(f"   ✅ Analytics generated")
        print(f"      - Total logs: {migrated_count}")
        print(f"      - Current attack frequency: {analytics.current_attack_frequency}")
        print(f"      - Baseline attack frequency: {analytics.baseline_attack_frequency}")

        # Backup old file
        backup_path = data_file.with_suffix('.json.backup')
        print(f"💾 Backing up old data to {backup_path}...")
        data_file.rename(backup_path)

        print("-" * 50)
        print("✅ Migration complete!")
        print()
        print("Next steps:")
        print("1. Start V2 backend: uvicorn app.main_v2:app --reload")
        print("2. Login as: demo@migru.app")
        print("3. Check /analytics to see migrated data")
        print()
        print("Note: Voice baseline and intervention history not migrated (new features)")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    migrate()
