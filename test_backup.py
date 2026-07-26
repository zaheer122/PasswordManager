from database.db_manager import DatabaseManager
from backup.backup_manager import BackupManager

db = DatabaseManager()

backup = BackupManager(db)

path = backup.export_backup()

print(path)