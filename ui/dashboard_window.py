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
)

from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager
from ui.dialog.add_dialog import AddCredentialDialog


class Dashboard(QWidget):

    def __init__(self, key):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.resize(1100, 700)
        self.key = key

        db = DatabaseManager()
        encryption = EncryptionManager(key)

        self.vault = VaultManager(db, encryption)

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

        self.search.textChanged.connect(
            self.search_credentials
        )

        self.add_btn.clicked.connect(
            self.add_credential
        )

        self.edit_btn.clicked.connect(self.edit_credential)

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