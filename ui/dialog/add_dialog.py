from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)

from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager
from utils.password_generator import PasswordGenerator


class AddCredentialDialog(QDialog):

    def __init__(self, key, parent=None,credential=None,):
        super().__init__(parent)

        self.setWindowTitle("Add Credential")
        self.resize(500, 600)

        db = DatabaseManager()
        encryption = EncryptionManager(key)

        self.vault = VaultManager(
            db,
            encryption,
        )

        self.build_ui()

        self.credential = credential

        if self.credential:
            self.load_credential()

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()
        self.website = QLineEdit()
        self.username = QLineEdit()
        self.email = QLineEdit()

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.notes = QTextEdit()

        self.category = QComboBox()
        self.category.addItems([
            "General",
            "Social",
            "Development",
            "Email",
            "Cloud",
            "Banking",
            "Shopping",
            "Work",
        ])

        self.favorite = QCheckBox("Favourite")

        form.addRow("Name", self.name)
        form.addRow("Website", self.website)
        form.addRow("Username", self.username)
        form.addRow("Email", self.email)
        form.addRow("Password", self.password)
        form.addRow("Category", self.category)
        form.addRow("Notes", self.notes)
        form.addRow("", self.favorite)

        layout.addLayout(form)

        password_buttons = QHBoxLayout()

        self.show_btn = QPushButton("Show")
        self.generate_btn = QPushButton("Generate")

        password_buttons.addWidget(self.show_btn)
        password_buttons.addWidget(self.generate_btn)

        layout.addLayout(password_buttons)

        buttons = QHBoxLayout()

        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        buttons.addStretch()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addLayout(buttons)

        self.show_btn.clicked.connect(self.toggle_password)
        self.generate_btn.clicked.connect(self.generate_password)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_btn.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_btn.setText("Show")

    def generate_password(self):

        generator = PasswordGenerator()
        password = generator.generate()

        self.password.setText(password)

    def save(self):

        if not self.name.text().strip():
            QMessageBox.warning(
                self,
                "Validation",
                "Name is required.",
            )
            return

        if not self.password.text():
            QMessageBox.warning(
                self,
                "Validation",
                "Password is required.",
            )
            return

        if self.credential is None:

            self.vault.add_credential(
                name=self.name.text(),
                website=self.website.text(),
                username=self.username.text(),
                email=self.email.text(),
                password=self.password.text(),
                notes=self.notes.toPlainText(),
                category=self.category.currentText(),
                favorite=self.favorite.isChecked(),
            )

        else:

            self.vault.update_credential(
                credential_id=self.credential.id,
                name=self.name.text(),
                website=self.website.text(),
                username=self.username.text(),
                email=self.email.text(),
                password=self.password.text(),
                notes=self.notes.toPlainText(),
                category=self.category.currentText(),
                favorite=self.favorite.isChecked(),
            )

        self.accept()

    def load_credential(self):

        self.name.setText(self.credential.name)
        self.website.setText(self.credential.website or "")
        self.username.setText(self.credential.username or "")
        self.email.setText(self.credential.email or "")
        self.password.setText(self.credential.password)
        self.notes.setPlainText(self.credential.notes or "")

        index = self.category.findText(
            self.credential.category or "General"
        )

        if index >= 0:
            self.category.setCurrentIndex(index)

        self.favorite.setChecked(
            self.credential.favorite
        )

        self.save_btn.setText("Update")