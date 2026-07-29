from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableView,
    QAbstractItemView,
    QFileDialog,
)
from PySide6.QtWidgets import QMessageBox
from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager
from ui.dialog.add_dialog import AddCredentialDialog
from ui.dialog.view_dialog import ViewCredentialDialog
from backup.backup_manager import BackupManager
from ui.login_window import LoginWindow



class Dashboard(QWidget):

    def __init__(self, key):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.resize(1100, 700)
        self.key = key

        db = DatabaseManager()
        encryption = EncryptionManager(key)

        self.vault = VaultManager(db, encryption)
        self.backup = BackupManager(db)
        self.build_ui()
        self.load_credentials()

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        # ===========================
        # Header
        # ===========================

        header = QHBoxLayout()

        title = QLabel("🔐 Password Manager")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        header.addWidget(title)
        header.addStretch()

        self.logout_btn = QPushButton("Logout")
        header.addWidget(self.logout_btn)

        main_layout.addLayout(header)

        # ===========================
        # Toolbar
        # ===========================

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")

        toolbar.addWidget(self.search)

        self.add_btn = QPushButton("+ Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.backup_btn = QPushButton("Backup")
        self.restore_btn = QPushButton("Restore")

        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addWidget(self.backup_btn)
        toolbar.addWidget(self.restore_btn)

        main_layout.addLayout(toolbar)

        # ===========================
        # Table
        # ===========================

        self.table = QTableView()

        self.model = QStandardItemModel()

        self.model.setHorizontalHeaderLabels([
            "Name",
            "Website",
            "Username",
            "Email",
            "Category",
            "Favourite"
        ])

        self.table.setModel(self.model)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)

        # ===========================
        # Signals
        # ===========================

        self.logout_btn.clicked.connect(self.logout)

        self.search.textChanged.connect(self.search_credentials)

        self.add_btn.clicked.connect(self.add_credential)

        self.delete_btn.clicked.connect(self.delete_credential)

        self.edit_btn.clicked.connect(self.edit_credential)

        self.backup_btn.clicked.connect(self.export_backup)

        self.restore_btn.clicked.connect(self.restore_backup)

        self.table.doubleClicked.connect(self.view_credential)

    def load_credentials(self):

        self.model.removeRows(
            0,
            self.model.rowCount()
        )

        credentials = self.vault.get_credentials()

        for credential in credentials:

            row = [

                QStandardItem(credential.name),

                QStandardItem(
                    credential.website or ""
                ),

                QStandardItem(
                    credential.username or ""
                ),

                QStandardItem(
                    credential.email or ""
                ),

                QStandardItem(
                    credential.category or ""
                ),

                QStandardItem(
                    "★" if credential.favorite else ""
                ),
            ]

            row[0].setData(credential.id,Qt.UserRole,)
            self.model.appendRow(row)

    def search_credentials(self):

        keyword = self.search.text()

        self.model.removeRows(
            0,
            self.model.rowCount()
        )

        credentials = self.vault.search_credentials(
            keyword
        )

        for credential in credentials:

            row = [

                QStandardItem(credential.name),

                QStandardItem(
                    credential.website or ""
                ),

                QStandardItem(
                    credential.username or ""
                ),

                QStandardItem(
                    credential.email or ""
                ),

                QStandardItem(
                    credential.category or ""
                ),

                QStandardItem(
                    "★" if credential.favorite else ""
                ),
            ]

            row[0].setData(credential.id,Qt.UserRole,)
            self.model.appendRow(row)

    def add_credential(self):

        dialog = AddCredentialDialog(
            self.key,
            self,
        )

        if dialog.exec():
            self.load_credentials()

    def edit_credential(self):

        indexes = self.table.selectionModel().selectedRows()

        if not indexes:
            return

        row = indexes[0].row()

        credential_id = self.model.item(
            row,
            0,
        ).data(Qt.UserRole)

        credential = self.vault.get_credential_by_id(
            credential_id
        )

        if credential is None:
            return

        dialog = AddCredentialDialog(
            self.key,
            self,
            credential,
        )

        if dialog.exec():
            self.load_credentials()

    def delete_credential(self):

        indexes = self.table.selectionModel().selectedRows()

        if not indexes:
            QMessageBox.information(
                self,
                "Delete Credential",
                "Please select a credential to delete."
            )
            return
    
        row = indexes[0].row()

        credential_id = self.model.item(
            row,
            0,
        ).data(Qt.UserRole)

        credential_name = self.model.item(
            row,
            0,
        ).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete '{credential_name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:

            self.vault.delete_credential(
                credential_id
            )

            self.load_credentials()

            QMessageBox.information(
                self,
                "Success",
                "Credential deleted successfully."
            )

    def export_backup(self):

        backup_path = self.backup.export_backup()

        QMessageBox.information(
            self,
            "Backup Successful",
            f"Backup saved to:\n\n{backup_path}"
        )

    def restore_backup(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup",
            "backups",
            "JSON Files (*.json)"
        )

        if not filename:
            return

        reply = QMessageBox.question(
            self,
            "Restore Backup",
            "Restoring will import credentials from the selected backup.\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        self.backup.import_backup(filename)

        self.load_credentials()

        QMessageBox.information(
            self,
            "Restore Complete",
            "Backup restored successfully."
        )

    def view_credential(self):

        indexes = self.table.selectionModel().selectedRows()

        if not indexes:
            return

        row = indexes[0].row()

        credential_id = self.model.item(
            row,
            0,
        ).data(Qt.UserRole)

        credential = self.vault.get_credential_by_id(
            credential_id
        )

        if credential is None:
            return

        dialog = ViewCredentialDialog(
            credential,
            self,
            self,
     )

        dialog.exec()

        self.load_credentials()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.view_credential()
            return

        super().keyPressEvent(event)

    def logout(self):

        self.close()

        self.login = LoginWindow()
        self.login.show()