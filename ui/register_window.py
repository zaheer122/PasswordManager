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


class RegisterWindow(QWidget):

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

        subtitle = QLabel("Create Master Password")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size:16px;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Master Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.register)

        self.show_btn = QPushButton("👁 Show")
        self.show_btn.setFixedWidth(90)
        self.show_btn.clicked.connect(self.toggle_password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_btn)

        create_button = QPushButton("Create Vault")
        create_button.setFixedHeight(45)
        create_button.clicked.connect(self.register)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(password_layout)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_btn.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_btn.setText("👁 Show")

    def register(self):

        password = self.password.text().strip()

        if len(password) < 6:
            QMessageBox.warning(
                self,
                "Invalid Password",
                "Master password must be at least 6 characters."
            )
            return

        success = self.auth.register(password)

        if success:

            QMessageBox.information(
                self,
                "Success",
                "Vault created successfully."
            )

            self.close()

            from ui.login_window import LoginWindow

            self.login = LoginWindow()
            self.login.show()

        else:

            QMessageBox.warning(
                self,
                "User Exists",
                "A vault already exists."
            )