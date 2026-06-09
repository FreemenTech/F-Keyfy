# F-Keyfy

**F-Keyfy** is a desktop application designed to **evaluate password strength**, **detect compromised passwords**, and **generate secure passwords**.  
Built with **Python** and **PySide6**, with a strong focus on **security, privacy, and usability**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![Tests](https://img.shields.io/badge/tests-41%20passed-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Features

- **Strength analysis** — entropy calculation, character type detection, and composite scoring
- **Pattern detection** — catches common passwords (incl. leet-speak variants like `P@ssw0rd`), keyboard walks (`qwerty`, `asdfgh`), repeated characters, and sequential runs
- **Breach detection** — checks passwords against the Have I Been Pwned database using k-anonymity (only a 5-character SHA-1 prefix leaves your machine)
- **Password generation** — cryptographically secure random passwords (`secrets` module) and mnemonic passphrases
- **Clipboard auto-clear** — copied passwords are wiped from clipboard after 30 seconds
- **Non-blocking UI** — all network calls and heavy analysis run in background threads
- **Cross-platform builds** — build scripts for Windows, Linux, and macOS

---

## Security & Privacy

- Passwords are **never stored** and **never logged**
- Breach checks use the **k-anonymity model** — only a partial hash is transmitted
- Password generation uses Python's `secrets` module (cryptographically secure PRNG)
- No tracking, no data collection, no telemetry

---

## Installation

### From source

```bash
git clone https://github.com/FreemenTech/F-Keyfy.git
cd F-Keyfy
pip install -r requirements.txt
python main.py
```

### Build standalone executable

**Linux / macOS:**

```bash
chmod +x build.sh
./build.sh
```

The executable is in `dist/F-Keyfy/`. On macOS, a `.app` bundle is also generated.

**Windows:**

```
build.bat
```

The executable is in `dist\F-Keyfy\F-Keyfy.exe`. Zip the entire `dist\F-Keyfy\` folder to distribute.

---

## Tests

```bash
pip install pytest
pytest test_fkeyfy.py -v
```

41 tests covering character detection, entropy calculation, pattern detection (common passwords, leet-speak, keyboard walks, sequences, repeats), strength scoring, HIBP API (mocked), password generation, and mnemonic generation.

---

## Project Structure

```
F-Keyfy/
├── main.py                  # Application entry point
├── ui_check_passwd.py       # PySide6 user interface
├── check_password.py        # Password analysis + pattern detection
├── generator_password.py    # Secure password generation (secrets)
├── threads.py               # Background threads (analysis + HIBP)
├── test_fkeyfy.py           # Test suite (41 tests)
├── list.txt                 # Word list for mnemonic generation
├── style.qss                # GUI styling (QSS)
├── requirements.txt         # Python dependencies
├── F-Keyfy.spec             # PyInstaller build config
├── build.sh                 # Build script (Linux/macOS)
├── build.bat                # Build script (Windows)
├── LICENSE                  # MIT License
└── assets/
    └── icons/
        ├── logo.png         # App icon (512x512)
        └── logo.ico         # App icon (Windows)
```

---

## Technologies

- **Python 3.10+**
- **PySide6** — Qt-based GUI framework
- **QSS** — Qt Style Sheets for theming
- **Have I Been Pwned API** — breach detection via k-anonymity
- **PyInstaller** — cross-platform packaging

---

## Author

**Freemen Houngbedji**  
GitHub: [@FreemenTech](https://github.com/FreemenTech)

---

## License

This project is licensed under the [MIT License](LICENSE).
