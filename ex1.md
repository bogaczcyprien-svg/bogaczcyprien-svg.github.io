
def lire_fichier_binaire(chemin):
    """Lit un fichier en mode binaire"""
    with open(chemin, 'rb') as f:  # Mode binaire (rb)
        contenu = f.read()
    return contenu

def obtenir_taille_fichier(chemin):
    """Retourne la taille en octets"""
    import os
    return os.path.getsize(chemin)

!<ex2
from cryptography.fernet import Fernet

def chiffrer_message(message, cle):
    """Chiffre un message avec la clé fournie"""
    chiffre = Fernet(cle)              # Créer objet Fernet
    message_bytes = message.encode('utf-8')  # string → bytes
    ciphertext = chiffre.encrypt(message_bytes)
    return ciphertext

def dechiffrer_message(ciphertext, cle):
    """Déchiffre un ciphertext"""
    chiffre = Fernet(cle)
    plaintext = chiffre.decrypt(ciphertext)
    return plaintext.decode('utf-8')

!<ex3
def chiffrer_fichier(chemin_entree, chemin_sortie, cle):
    """Lit un fichier, le chiffre et l'enregistre"""
    # 1. Lire le fichier en binaire
    contenu = lire_fichier_binaire(chemin_entree)
    
    # 2. Chiffrer (contenu est déjà en bytes !)
    chiffre = Fernet(cle)
    ciphertext = chiffre.encrypt(contenu)
    
    # 3. Écrire le fichier chiffré en binaire
    with open(chemin_sortie, 'wb') as f:  # Mode 'wb'
        f.write(ciphertext)

# Utilisation:
cle = Fernet.generate_key()
chiffrer_fichier('test.txt', 'test.txt.enc', cle)

!<ex4
from cryptography.fernet import Fernet
import os

# Générer clé
cle = Fernet.generate_key()
print(f"Clé générée: {cle}")

# Créer fichier de test
with open('test.txt', 'w') as f:
    f.write('Données sensibles pour sauvegarde\n' * 10)

# Chiffrer
def chiffrer_fichier_v2(chemin_entree, chemin_sortie, cle):
    with open(chemin_entree, 'rb') as f:
        contenu = f.read()
    chiffre = Fernet(cle)
    ciphertext = chiffre.encrypt(contenu)
    with open(chemin_sortie, 'wb') as f:
        f.write(ciphertext)

chiffrer_fichier_v2('test.txt', 'test.txt.enc', cle)

# Vérifier tailles
print(f"Taille original: {os.path.getsize('test.txt')} octets")
print(f"Taille chiffré: {os.path.getsize('test.txt.enc')} octets")

# Déchiffrer et vérifier
with open('test.txt.enc', 'rb') as f:
    ciphertext = f.read()
plaintext = Fernet(cle).decrypt(ciphertext)
print(f"Vérification: {plaintext[:30]}") 