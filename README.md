# 🔐 Password Manager

> A secure, modern desktop password manager built with Python and PySide6, designed to securely store, manage, generate, and back up credentials using encrypted local storage.

<p align="center">
  <img src="assets/screenshots/MDashboard.png" alt="Password Manager Dashboard" width="850">
</p>

<p align="center">
  <b>Secure your credentials. Generate stronger passwords. Stay in control.</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Security](https://img.shields.io/badge/Security-Encrypted-8A2BE2?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)

</p>

---

## 📌 Overview

Password Manager is a desktop application designed to provide a secure and convenient way to manage online credentials.

Instead of storing passwords in plain text, the application encrypts credential passwords before storing them in the local SQLite database.

The application provides a complete credential-management workflow:

- 🔐 Master password authentication
- 🔒 Encrypted credential storage
- ➕ Add credentials
- ✏️ Edit credentials
- 🗑️ Delete credentials
- 👁️ View and reveal passwords
- 📋 Copy passwords to clipboard
- 🔎 Search credentials
- ⭐ Favourite credentials
- 🎲 Secure password generation
- 💾 Backup vault
- ♻️ Restore vault
- 🚪 Logout
- 🖥️ Modern PySide6 desktop interface

The project is being developed with a strong focus on **security, clean architecture, usability, and real-world software engineering practices**.

---

# ✨ Features

## 🔐 Master Password Authentication

The application uses a master password to protect access to the vault.

The master password is **not stored directly**.

Instead, authentication uses a password hashing mechanism with a cryptographic salt.

```text
Master Password
       │
       ▼
Password Hashing
       │
       ▼
Salt + Password Hash
       │
       ▼
Authentication

🔒 Encrypted Password Storage

Credential passwords are encrypted before being stored in the SQLite database.

User Password
      │
      ▼
Encryption Manager
      │
      ▼
Encrypted Password
      │
      ▼
SQLite Database

When the credential is viewed, the application decrypts the password using the appropriate encryption key.