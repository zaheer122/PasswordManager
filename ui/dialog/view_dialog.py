from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QTextEdit
from ui.dialog.add_dialog import AddCredentialDialog

class ViewCredentialDialog(QDialog):

    def __init__(
        self,
        credential,
        dashboard,
        parent=None,
    ):
        super().__init__(parent)

        self.credential = credential
        self.dashboard = dashboard

        self.setWindowTitle("Credential Details")
        self.resize(500, 420)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        form.addRow(
            "Name",
            QLabel(self.credential.name),
        )

        form.addRow(
            "Website",
            QLabel(self.credential.website or ""),
        )

        form.addRow(
            "Username",
            QLabel(self.credential.username or ""),
        )

        form.addRow(
            "Email",
            QLabel(self.credential.email or ""),
        )

        self.password = QLineEdit(
            self.credential.password
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.password.setReadOnly(True)

        form.addRow(
            "Password",
            self.password,
        )

        form.addRow(
            "Category",
            QLabel(self.credential.category or ""),
        )

        self.notes = QTextEdit()
        self.notes.setPlainText(self.credential.notes or "")
        self.notes.setReadOnly(True)
        self.notes.setMaximumHeight(100)

        form.addRow("Notes", self.notes)

        layout.addLayout(form)

        # Buttons
        buttons = QHBoxLayout()

        self.show_btn = QPushButton("Show")
        
        copy_btn = QPushButton("Copy Password")

        edit_btn = QPushButton("Edit")

        close_btn = QPushButton("Close")

        buttons.addWidget(copy_btn)
        buttons.addStretch()
        buttons.addWidget(edit_btn)
        buttons.addWidget(close_btn)
        buttons.addWidget(self.show_btn)

        layout.addLayout(buttons)

        # Connect buttons

        self.show_btn.clicked.connect(self.toggle_password)

        copy_btn.clicked.connect(self.copy_password)

        edit_btn.clicked.connect(self.edit)

        close_btn.clicked.connect(self.accept)

    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(
                QLineEdit.Normal
            )

            self.show_btn.setText("Hide")

        else:

            self.password.setEchoMode(
                QLineEdit.Password
            )

            self.show_btn.setText("Show")

    def copy_password(self):

        QGuiApplication.clipboard().setText(
            self.credential.password
        )

    def edit(self):
        dialog = AddCredentialDialog(
            self.dashboard.key,
            self,
            self.credential,)
        if dialog.exec():
            self.dashboard.load_credentials()
            self.accept()