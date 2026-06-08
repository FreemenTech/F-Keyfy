"""
F-Keyfy test suite.
Run:  pytest test_fkeyfy.py -v
"""

import math
import string
from unittest.mock import patch, MagicMock

import pytest

from check_password import Password, COMMON_PASSWORDS, LEET_MAP
from generator_password import Generator_Pwd, resource_path


# ═══════════════════════════════════════════════════════════════
#  Helpers — mock HIBP so tests never hit the network
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def mock_hibp():
    """Block all outgoing HIBP requests. Default: password not found (0)."""
    with patch("check_password.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = ""  # no matching suffix → unicity = 0
        mock_get.return_value = mock_resp
        yield mock_get


def make_pwd(value):
    """Shortcut to build a Password object."""
    return Password(value)


# ═══════════════════════════════════════════════════════════════
#  1. Character detection
# ═══════════════════════════════════════════════════════════════

class TestCharacterDetection:
    def test_uppercase_detected(self):
        pwd = make_pwd("Hello1!")
        assert pwd.has_uppercase is True

    def test_no_uppercase(self):
        pwd = make_pwd("hello1!")
        assert pwd.has_uppercase is False

    def test_all_char_types(self):
        pwd = make_pwd("Abc123!@")
        assert pwd.has_uppercase is True
        assert pwd.has_lowercase is True
        assert pwd.has_number is True
        assert pwd.has_special_char is True

    def test_digits_only(self):
        pwd = make_pwd("12345678")
        assert pwd.has_number is True
        assert pwd.has_uppercase is False
        assert pwd.has_lowercase is False
        assert pwd.has_special_char is False


# ═══════════════════════════════════════════════════════════════
#  2. Entropy
# ═══════════════════════════════════════════════════════════════

class TestEntropy:
    def test_entropy_lowercase_only(self):
        pwd = make_pwd("abcdefgh")  # 8 chars, pool = 26
        expected = round(8 * math.log2(26), 2)
        assert pwd.entropy_bits == expected

    def test_entropy_all_types(self):
        pwd = make_pwd("Aa1!")  # 4 chars, pool = 94
        expected = round(4 * math.log2(94), 2)
        assert pwd.entropy_bits == expected

    def test_entropy_empty_pool(self):
        pwd = make_pwd("    ")  # spaces are not alnum → special char
        # has_special_char = True, pool = 32
        assert pwd.entropy_bits > 0

    def test_entropy_label_very_easy(self):
        pwd = make_pwd("ab")  # very low entropy
        assert "Very easy" in pwd.entropy_label

    def test_entropy_label_very_strong(self):
        pwd = make_pwd("X8#mK2!vZ6$rW9&q")  # 16 chars all types
        assert "Very strong" in pwd.entropy_label


# ═══════════════════════════════════════════════════════════════
#  3. Pattern detection
# ═══════════════════════════════════════════════════════════════

class TestPatternDetection:
    def test_common_password_direct(self):
        pwd = make_pwd("password")
        assert pwd.has_common_password is True

    def test_common_password_leet_speak(self):
        pwd = make_pwd("P@ssw0rd")
        assert pwd.has_common_password is True

    def test_common_password_with_trailing_digits(self):
        pwd = make_pwd("admin123!")
        assert pwd.has_common_password is True

    def test_not_common_password(self):
        pwd = make_pwd("xK9$mW2!vL")
        assert pwd.has_common_password is False

    def test_keyboard_pattern_qwerty(self):
        pwd = make_pwd("qwerty2024")
        assert pwd.has_keyboard_pattern is True

    def test_keyboard_pattern_asdfgh(self):
        pwd = make_pwd("myasdfgh99")
        assert pwd.has_keyboard_pattern is True

    def test_no_keyboard_pattern(self):
        pwd = make_pwd("xK9$mW2!vL")
        assert pwd.has_keyboard_pattern is False

    def test_repeating_chars(self):
        pwd = make_pwd("paAAAsword1!")
        assert pwd.has_repeats is True

    def test_no_repeating_chars(self):
        pwd = make_pwd("AbCdEf12!@")
        assert pwd.has_repeats is False

    def test_sequential_ascending(self):
        pwd = make_pwd("xyzabc99!A")
        assert pwd.has_sequences is True

    def test_sequential_descending(self):
        pwd = make_pwd("fe!dcba00X")
        assert pwd.has_sequences is True

    def test_no_sequences(self):
        pwd = make_pwd("xK9$mW2!vL")
        assert pwd.has_sequences is False


# ═══════════════════════════════════════════════════════════════
#  4. Strength scoring
# ═══════════════════════════════════════════════════════════════

class TestStrengthScoring:
    def test_weak_short_password(self):
        pwd = make_pwd("abc")
        assert "Very weak" in pwd.strength_label

    def test_common_password_penalized(self):
        """'Password1!' has all char types but should be penalized for being common."""
        pwd = make_pwd("Password1!")
        assert "Very weak" in pwd.strength_label or "Medium" in pwd.strength_label

    def test_strong_password(self):
        pwd = make_pwd("X8#mK2!vZ6$rW9&q")
        assert "Good" in pwd.strength_label or "Excellent" in pwd.strength_label

    def test_suggestions_for_missing_types(self):
        pwd = make_pwd("abcdefghijkl")  # no uppercase, no digit, no special
        suggestions_text = " ".join(pwd.suggestions)
        assert "uppercase" in suggestions_text
        assert "number" in suggestions_text
        assert "special" in suggestions_text

    def test_no_suggestions_for_excellent(self):
        pwd = make_pwd("X8#mK2!vZ6$rW9&q")
        # Excellent password — no pattern, all types, long
        pattern_suggestions = [s for s in pwd.suggestions if "common" in s.lower() 
                               or "keyboard" in s.lower() or "repeated" in s.lower()
                               or "sequential" in s.lower()]
        assert len(pattern_suggestions) == 0


# ═══════════════════════════════════════════════════════════════
#  5. get_info output
# ═══════════════════════════════════════════════════════════════

class TestGetInfo:
    def test_get_info_contains_entropy(self):
        pwd = make_pwd("Test1234!")
        info = pwd.get_info()
        assert "Entropy" in info

    def test_get_info_contains_strength(self):
        pwd = make_pwd("Test1234!")
        info = pwd.get_info()
        assert "strength" in info.lower()

    def test_get_info_contains_suggestion(self):
        pwd = make_pwd("Test1234!")
        info = pwd.get_info()
        assert "suggestion" in info.lower()


# ═══════════════════════════════════════════════════════════════
#  6. HIBP API (mocked)
# ═══════════════════════════════════════════════════════════════

class TestHibpApi:
    def test_password_not_found(self, mock_hibp):
        """Empty response → unicity = 0."""
        pwd = make_pwd("UniqueP@ss99!")
        assert pwd.unicity == 0

    def test_password_found_in_leaks(self, mock_hibp):
        """Simulate HIBP returning a matching suffix."""
        import hashlib
        test_pwd = "LeakedPass1!"
        sha1 = hashlib.sha1(test_pwd.encode("utf-8")).hexdigest().upper()
        suffix = sha1[5:]

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = f"{suffix}:42\nABCDE12345:10\n"
        mock_hibp.return_value = mock_resp

        pwd = make_pwd(test_pwd)
        assert pwd.unicity == 42

    def test_network_error_returns_minus_one(self, mock_hibp):
        """Network failure → unicity = -1."""
        from requests.exceptions import ConnectionError
        mock_hibp.side_effect = ConnectionError("No network")

        pwd = make_pwd("AnyPass1!")
        assert pwd.unicity == -1

    def test_bad_status_code(self, mock_hibp):
        """Non-200 response → unicity = -1."""
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        mock_hibp.return_value = mock_resp

        pwd = make_pwd("AnyPass1!")
        assert pwd.unicity == -1


# ═══════════════════════════════════════════════════════════════
#  7. Password generator
# ═══════════════════════════════════════════════════════════════

class TestGenerator:
    def test_generated_length(self):
        gen = Generator_Pwd(16)
        assert len(gen.generated_password) == 16

    def test_generated_length_minimum(self):
        gen = Generator_Pwd(6)
        assert len(gen.generated_password) == 6

    def test_generated_uses_expected_chars(self):
        gen = Generator_Pwd(100)  # large sample to reduce randomness
        allowed = set(string.ascii_letters + string.digits + string.punctuation)
        assert all(c in allowed for c in gen.generated_password)

    def test_mnemonic_word_count(self):
        gen = Generator_Pwd(5)
        words = gen.memonic_password.split("-")
        assert len(words) == 5

    def test_mnemonic_format(self):
        gen = Generator_Pwd(3)
        # Should be word-word-word
        assert "-" in gen.memonic_password
        for word in gen.memonic_password.split("-"):
            assert word.isalpha()

    def test_two_generations_differ(self):
        """Two consecutive generations should produce different passwords."""
        gen1 = Generator_Pwd(16)
        gen2 = Generator_Pwd(16)
        # Technically could collide, but probability is negligible at length 16
        assert gen1.generated_password != gen2.generated_password


# ═══════════════════════════════════════════════════════════════
#  8. resource_path
# ═══════════════════════════════════════════════════════════════

class TestResourcePath:
    def test_returns_absolute_path(self):
        import os
        result = resource_path("list.txt")
        assert os.path.isabs(result)

    def test_contains_filename(self):
        result = resource_path("style.qss")
        assert result.endswith("style.qss")
