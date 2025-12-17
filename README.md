# F-Keyfy

**F-Keyfy** is a desktop application designed to **evaluate password strength**, **detect compromised passwords**, and **generate secure passwords**.  
It is built with **Python** and **PySide6**, with a strong focus on **security, privacy, and usability**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Features

- Advanced password strength analysis
- Secure password generation
- Compromised password detection using **Have I Been Pwned**
- Detailed security feedback and recommendations
- Modern desktop GUI (PySide6 + QSS)
- Asynchronous threading for smooth performance

---

## Why F-Keyfy?

Weak, reused, or leaked passwords remain one of the main causes of security breaches.  
F-Keyfy aims to:

- Help users evaluate the real strength of their passwords
- Detect whether a password has already appeared in known data breaches
- Encourage the use of strong and unique passwords
- Provide a fast, local, and user-friendly desktop solution

---

## Security & Privacy

Security and privacy are core principles of F-Keyfy:

- Passwords are **never stored**
- Passwords are **never logged**
- No plaintext password is saved locally
- Compromised password checks use the **Have I Been Pwned API**
- The password is processed in a **hashed form** before being checked
- Only partial hashes are transmitted (k-anonymity model)
- No sensitive data is sent or retained

F-Keyfy does **not** track users and does **not** collect personal data.

---

## Installation & Usage

### From source

```bash
# Clone the repository
git clone https://github.com/freemen812/F-Keyfy.git
cd F-Keyfy

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

Project Structure

F-Keyfy/
├── main.py                  # Application entry point
├── ui_check_password.py     # PySide6 user interface
├── check_password.py        # Password analysis logic
├── generator_password.py    # Secure password generation
├── threads.py               # Asynchronous task handling
├── style.qss                # GUI styling
├── requirements.txt         # Project dependencies
└── assets/                  # Icons and resources

Usage

    Launch the application with python main.py

    Enter a password to analyze its strength

    Check whether the password has been compromised

    Generate a strong and secure password

    Review security recommendations

Technologies Used

    Python 3.8+

    PySide6 (GUI framework)

    QSS (Qt Style Sheets)

    Threading for non-blocking operations

    Have I Been Pwned API for breach detection

Author

Freemen Houngbedji

    GitHub: @FreemenTech

    Project: F-Keyfy

License

This project is licensed under the MIT License.
See the LICENSE file for more information.

If you find this project useful, feel free to star the repository.

