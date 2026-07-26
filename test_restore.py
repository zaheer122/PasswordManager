from pathlib import Path

from database.db_manager import DatabaseManager
from backup.backup_manager import BackupManager

db = DatabaseManager()
backup = BackupManager(db)

latest_backup = max(
    Path("backups").glob("*.json"),
    key=lambda f: f.stat().st_mtime,
)

backup.import_backup(latest_backup)

print("Restore Complete")