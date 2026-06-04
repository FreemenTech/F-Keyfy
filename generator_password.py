import secrets
import string
import os
import sys


def resource_path(relative_path):
    """
    Resolve file path for both development and PyInstaller builds.
    In a PyInstaller bundle, files are extracted to a temp folder (_MEIPASS).
    In development, use the directory of this script.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


class Generator_Pwd:
    def __init__(self, length):
        self.length = length  # password length
        self.generated_password = self._pwd_generator()
        self.memonic_password = self._memonic_password()

    def _pwd_generator(self):
        """Generate a cryptographically secure random password."""
        chars = string.ascii_letters + string.digits + string.punctuation
        passwd = ''.join(secrets.choice(chars) for _ in range(self.length))
        return passwd

    def _memonic_password(self):
        """Generate a mnemonic passphrase from random dictionary words."""
        list_path = resource_path("list.txt")
        secure_rng = secrets.SystemRandom()

        try:
            with open(list_path, "r", encoding="utf-8") as file:
                content = file.read()
                word_list = [word.strip() for word in content.split(",") if word.strip()]

            available_words = min(self.length, len(word_list))
            m_password = secure_rng.sample(word_list, available_words)
            return "-".join(m_password)

        except FileNotFoundError:
            fallback_words = ["cat", "house", "sun", "tree", "flower",
                              "sky", "sea", "mountain", "book", "music"]
            available_words = min(self.length, len(fallback_words))
            m_password = secure_rng.sample(fallback_words, available_words)
            return "-".join(m_password)
