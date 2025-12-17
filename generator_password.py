import random
import string
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource - compatible cx_Freeze"""
    if getattr(sys, 'frozen', False):
        # Mode application compilée
        base_path = sys._MEIPASS
    else:
        # Mode développement
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

class Generator_Pwd:
    def __init__(self, lenght):
        self.lenght = lenght  # longueur_password
        self.password_generer = self.pwd_generator()
        self.memonic_pwd = self.memonic_password()
       
    def pwd_generator(self):
        char = string.ascii_letters + string.digits + string.punctuation
        passwd = ''.join(random.choice(char) for _ in range(self.lenght))
        return passwd
    
    def memonic_password(self):
        # Utiliser resource_path pour trouver list.txt
        list_path = resource_path("list.txt")
        
        try:
            with open(list_path, "r", encoding="utf-8") as file:
                contenu = file.read()
                word_list = [word.strip() for word in contenu.split(",")]
            
            # S'assurer qu'on ne demande pas plus de mots que disponibles
            available_words = min(self.lenght, len(word_list))
            m_password = random.sample(word_list, available_words)
            return "-".join(m_password)
            
        except FileNotFoundError:
            # Fallback si list.txt n'existe pas
            fallback_words = ["chat", "maison", "soleil", "arbre", "fleur", 
                            "ciel", "mer", "montagne", "livre", "musique"]
            available_words = min(self.lenght, len(fallback_words))
            m_password = random.sample(fallback_words, available_words)
            return "-".join(m_password)