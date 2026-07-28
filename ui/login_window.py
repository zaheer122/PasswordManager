from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
)

from auth.auth_manager import AuthenticationManager


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.auth = AuthenticationManager()

        self.setWindowTitle("Password Manager")
        self.setFixedSize(500, 350)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)

        title = QLabel("🔐 Password Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        subtitle = QLabel("Enter Master Password")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size:16px;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Master Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.login)

        self.show_btn = QPushButton("👁 Show")
        self.show_btn.setFixedWidth(90)
        self.show_btn.clicked.connect(self.toggle_password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_btn)

        login_button = QPushButton("Unlock Vault")
        login_button.setFixedHeight(45)
        login_button.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(password_layout)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_btn.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_btn.setText("👁 Show")

    def login(self):

        password = self.password.text().strip()

        if not self.auth.login(password):
            QMessageBox.warning(
                self,
                "Login Failed",
                "Incorrect master password."
            )
            return

        key = self.auth.get_encryption_key(password)

        self.close()

        from ui.dashboard_window import Dashboard

        self.dashboard = Dashboard(key)
        self.dashboard.show()