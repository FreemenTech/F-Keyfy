import hashlib
import math
import re
import requests


# ==================== Common passwords & patterns ====================
# Top weak passwords — caught instantly by any dictionary attack
COMMON_PASSWORDS = frozenset({
    "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "1234567", "letmein", "trustno1", "dragon", "baseball", "iloveyou",
    "master", "sunshine", "ashley", "michael", "shadow", "123123",
    "654321", "superman", "qazwsx", "password1", "password123",
    "welcome", "hello", "charlie", "donald", "admin", "login",
    "princess", "football", "azerty", "000000", "111111",
})

# Keyboard walks — sequences a brute-forcer tries early
KEYBOARD_PATTERNS = (
    "qwerty", "qwertz", "azerty", "asdfgh", "zxcvbn",
    "qweasd", "1qaz2wsx", "1q2w3e", "zaq1xsw2",
)

# Leet-speak map used to normalize before checking patterns
LEET_MAP = str.maketrans("@4301!$5", "aaeoiiss")


class Password:
    def __init__(self, passwd_value):
        self.passwd_value = passwd_value
        self.length = len(passwd_value)
        self.has_uppercase = any(c.isupper() for c in passwd_value)
        self.has_lowercase = any(c.islower() for c in passwd_value)
        self.has_number = any(c.isdigit() for c in passwd_value)
        self.has_special_char = any(not c.isalnum() for c in passwd_value)

        # Pattern detection (new)
        self.has_common_password = self._is_common_password()
        self.has_keyboard_pattern = self._has_keyboard_pattern()
        self.has_repeats = self._has_repeating_chars()
        self.has_sequences = self._has_sequential_chars()

        # Core analysis
        self.unicity = self.check_unicity()  # API check
        self.entropy_bits = self._entropy_bits()
        self.entropy_label = self._entropy_label()
        self.strength_label, self.suggestions = self._strength_analysis()

    # ==================== Pattern detectors ====================

    def _is_common_password(self):
        """Check against common passwords, including leet-speak variants."""
        lower = self.passwd_value.lower()
        normalized = lower.translate(LEET_MAP)
        # Strip trailing digits/symbols to catch "password1!", "admin123"
        base = re.sub(r"[\d!@#$%^&*]+$", "", normalized)
        return lower in COMMON_PASSWORDS or base in COMMON_PASSWORDS

    def _has_keyboard_pattern(self):
        """Detect keyboard walk patterns (qwerty, asdfgh, etc.)."""
        lower = self.passwd_value.lower()
        return any(pattern in lower for pattern in KEYBOARD_PATTERNS)

    def _has_repeating_chars(self, threshold=3):
        """Detect 3+ consecutive identical characters (aaa, 111)."""
        return bool(re.search(r"(.)\1{" + str(threshold - 1) + r",}", self.passwd_value))

    def _has_sequential_chars(self, run_length=3):
        """Detect sequential runs (abc, 321, cba) of run_length or more."""
        pwd = self.passwd_value.lower()
        for i in range(len(pwd) - run_length + 1):
            ords = [ord(c) for c in pwd[i:i + run_length]]
            diffs = [ords[j + 1] - ords[j] for j in range(len(ords) - 1)]
            # All diffs == +1 (ascending) or all == -1 (descending)
            if all(d == 1 for d in diffs) or all(d == -1 for d in diffs):
                return True
        return False

    # ==================== Entropy ====================

    def _entropy_bits(self):
        """Calculate password entropy in bits."""
        pool = 0
        if self.has_uppercase: pool += 26
        if self.has_lowercase: pool += 26
        if self.has_number:    pool += 10
        if self.has_special_char: pool += 32

        if pool == 0:
            return 0
        return round(self.length * math.log2(pool), 2)

    def _entropy_label(self):
        """Classify password difficulty based on entropy."""
        e = self.entropy_bits
        if e < 28:
            return "Very easy to guess 😬"
        elif e < 36:
            return "Acceptable but weak ⚠️"
        elif e < 60:
            return "Good level 🔒"
        else:
            return "Very strong 💪"

    # ==================== Strength scoring ====================

    def _strength_analysis(self):
        """Score based on length, complexity, entropy, AND pattern penalties."""
        score = 0
        suggestions = []

        # --- Positive factors ---

        # Length
        if self.length >= 12:
            score += 2
        elif self.length >= 8:
            score += 1
        else:
            suggestions.append("Use at least 8 characters")

        # Character types
        if self.has_uppercase:
            score += 1
        else:
            suggestions.append("Add an uppercase letter")

        if self.has_lowercase:
            score += 1
        else:
            suggestions.append("Add a lowercase letter")

        if self.has_number:
            score += 1
        else:
            suggestions.append("Add a number")

        if self.has_special_char:
            score += 1
        else:
            suggestions.append("Add a special character (!, @, #, $, %)")

        # Entropy bonus
        if self.entropy_bits >= 50:
            score += 1

        # --- Negative factors (penalties) ---

        if self.has_common_password:
            score -= 3
            suggestions.insert(0, "⛔ This is a commonly used password — change it entirely")

        if self.has_keyboard_pattern:
            score -= 2
            suggestions.insert(0, "Avoid keyboard patterns (qwerty, asdfgh…)")

        if self.has_repeats:
            score -= 1
            suggestions.insert(0, "Avoid repeated characters (aaa, 111…)")

        if self.has_sequences:
            score -= 1
            suggestions.insert(0, "Avoid sequential characters (abc, 123…)")

        # Clamp score to 0 minimum
        score = max(score, 0)

        # Overall label
        if score <= 2:
            label = "Very weak 🔴"
        elif score <= 4:
            label = "Medium 🟠"
        elif score <= 6:
            label = "Good 🟢"
        else:
            label = "Excellent 🟣"

        return label, suggestions

    # ==================== Display ====================

    def get_info(self):
        """Return password strength info."""
        if self.suggestions:
            first_suggestion = self.suggestions[0]
        else:
            first_suggestion = "No suggestion"

        analysis_result = (
            f"📊 Entropy : {self.entropy_label}\n"
            f"💪 Overall strength : {self.strength_label}\n"
            f"🧩 Main suggestion : {first_suggestion}"
        )
        return analysis_result

    # ==================== HIBP API ====================

    def check_unicity(self):
        """
        Checks if the password appears in leaks via the Have I Been Pwned API.
        Method: k-anonymity SHA-1 prefix (only the first 5 hex digits are sent).
        Returns: int (occurrences found). 0 = not found. -1 = check failed.
        """
        HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"
        USER_AGENT = "F-Keyfy/1.0"
        REQUEST_TIMEOUT = 10
        try:
            sha1 = hashlib.sha1(self.passwd_value.encode("utf-8")).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]

            url = HIBP_RANGE_URL.format(prefix)
            headers = {"User-Agent": USER_AGENT}
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if resp.status_code != 200:
                return -1

            for line in resp.text.splitlines():
                if ":" not in line:
                    continue
                line_suffix, count = line.split(":")
                if line_suffix.strip().upper() == suffix:
                    try:
                        return int(count.strip())
                    except ValueError:
                        return -1
            return 0

        except requests.RequestException:
            return -1
        except Exception:
            return -1
