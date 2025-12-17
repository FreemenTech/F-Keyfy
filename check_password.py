from datetime import datetime
import hashlib
from argon2 import PasswordHasher, exceptions
import math #pour calculer l'entropie du passwd
import requests

class Password:
    def __init__(self,passwd_value):

        self.passwd_value = passwd_value
        self.length = len(passwd_value)
        self.has_majuscule = any(c.isupper() for c in passwd_value)
        self.has_minuscule = any(c.islower() for c in passwd_value)
        self.has_number = any(c.isdigit()for c in passwd_value)
        self.has_special_caractere = any(not c.isalnum() for c in passwd_value)
        self.created_at = datetime.now()

#========== Fonctions importantes ============
        self.password_hash=self.do_hash() #hashage passwd
        self.unicite = self.check_unicity() #verification api
        self.entropy_bits = self._entropy_bits()
        self.entropy_label = self._entropy_label()
        self.strength_label, self.suggestions = self._strength_analysis()


    def _entropy_bits(self): 
        #calcule l'entropie du passwd en bits
        i = 0
        if self.has_majuscule:           i +=26
        if self.has_minuscule:           i +=26
        if self.has_number:              i +=10
        if self.has_special_caractere:   i +=32

        if i ==0:
            return 0

        return round(self.length * math.log2(i), 2) #formule de l'entropie en bits


    def _entropy_label(self):
        """Classe la difficulté du mot de passe selon son entropie"""
        e = self.entropy_bits
        if e < 28:
            return "Très facile à deviner 😬"
        elif e < 36:
            return "Acceptable mais faible ⚠️"
        elif e < 60:
            return "Bon niveau 🔒"
        else:
            return "Très fort 💪"
        
        

    def _strength_analysis(self):

        """Combine longueur, complexité et entropie pour produire un score et des conseils."""
        score = 0
        suggestions = []

        # Longueur
        if self.length >= 12:
            score += 2
        elif self.length >= 8:
            score += 1
        else:
            suggestions.append("Utilisez au moins 8 caractères")

        # Types de caractères
        if self.has_majuscule: score += 1
        else: suggestions.append("Ajoutez une majuscule")

        if self.has_minuscule: score += 1
        else: suggestions.append("Ajoutez une minuscule")

        if self.has_number: score += 1
        else: suggestions.append("Ajoutez un chiffre")

        if self.has_special_caractere: score += 1
        else: suggestions.append("Ajoutez un caractère spécial (!, @, #, $, %)")

        # Influence de l'entropie
        if self.entropy_bits >= 50:
            score += 1

        # Niveau global
        if score <= 2:
            label = "Très faible 🔴"
        elif score <= 4:
            label = "Moyen 🟠"
        elif score <= 6:
            label = "Bon 🟢"
        else:
            label = "Excellent 🟣"

        return label , suggestions

    def get_info(self): #retourner les infos relatif à la force du password.
         
             # Vérifier si la liste n'est pas vide avant de prendre le premier élément
            if self.suggestions:
                premiere_suggestion = self.suggestions[0]  
            else:
                premiere_suggestion = "Aucune suggestion"
            
            analyse_resultat = f"""
            📊 Entropie : {self.entropy_label}
            💪 Force globale : {self.strength_label}
            🧩 Suggestion principale : {premiere_suggestion}
            """
            return analyse_resultat

#je fus aider d'ici
    
    def check_unicity(self):
        """
        Vérifie si le mot de passe a été trouvé dans des fuites via l'API Have I Been Pwned.
        Méthode : k-anonymity SHA-1 prefix (on n'envoie que les 5 premiers hex du SHA-1).
        Retourne : int (nombre d'occurrences trouvées). 0 = pas trouvé.
        En cas d'erreur réseau, retourne -1 pour indiquer 'vérification impossible'.
        """
        HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"
        USER_AGENT = "AfrikPlum-PasswordChecker/1.0 (contact: linguapro83@gmail.com)"
        REQUEST_TIMEOUT = 10
        try:
            # 1) calculer SHA-1 en hex majuscule
            sha1 = hashlib.sha1(self.passwd_value.encode("utf-8")).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]

            # 2) requête à l'API HIBP avec timeout et User-Agent
            url = HIBP_RANGE_URL.format(prefix)
            headers = {"User-Agent": USER_AGENT}
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if resp.status_code != 200:
                # on pourrait logger l'erreur, mais ne jamais logger le mot de passe lui-même
                return -1

            # 3) parcourir la réponse et comparer localement les suffixes
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
            # erreur réseau (timeout, DNS, etc.)
            return -1
        except Exception:
            # erreur imprévue
            return -1

    def do_hash(self):
        """
        Hash Argon2 du mot de passe pour stockage.
        Retourne la chaîne complète renvoyée par argon2 (contient salt + params + digest).
        NB : ne pas envoyer ce hash à des services tiers.
        """
        try:
            ph = PasswordHasher()  # paramètres par défaut 
            return ph.hash(self.passwd_value)
        except Exception as e:
            # en cas d'erreur, retourner une valeur nulle ou lever l'exception selon le besoin
            # ici on retourne None pour indiquer l'échec du hash (à traiter côté appelant)
            return None

