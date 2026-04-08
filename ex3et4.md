!<A1
import zipfile

def creer_archive_simple(nom_archive, fichiers_liste):
    with zipfile.ZipFile(nom_archive, 'w',
                         zipfile.ZIP_DEFLATED) as zf:
        for fichier in fichiers_liste:
            zf.write(fichier)

                def lister_archive(nom_archive):
    with zipfile.ZipFile(nom_archive, 'r') as zf:  # Mode lecture
        zf.printdir()  # Affiche contenu formaté

        !<B1
import os
import zipfile

def archiver_dossier(dossier_source, nom_archive, exclusions=None):
    """Archive un dossier complet"""
    if exclusions is None:
        exclusions = ['.pyc', '__pycache__']

    with zipfile.ZipFile(nom_archive, 'w', zipfile.ZIP_DEFLATED) as zf:
        for racine, dossiers, fichiers in os.walk(dossier_source):
            for fichier in fichiers:
                if any(excl in fichier for excl in exclusions):
                    continue

                chemin_complet = os.path.join(racine, fichier)

                arcname = os.path.relpath(chemin_complet, dossier_source)

                zf.write(chemin_complet, arcname=arcname)

!<C1
if extraire_archive_sécurisée(
    'app_backup.zip', '/restore/app'):
    print("✓ Restauration réussie")

!<ex4 A
class BackupManager:
    def __init__(self, dossier_source, nom_backup, cle=None):
        self.cle = cle if cle else Fernet.generate_key()
        self.archive_name  = f"{nom_backup}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        self.manifeste_name = f"{self.archive_name}.manifest"
        self.chiffre_name   = f"{self.archive_name}.enc"

    def executer_sauvegarde(self):
        etapes = [("Archivage", self.archiver),
                  ("Manifeste", self.generer_manifeste),
                  ("Vérification", self.verifier_integrite),
                  ("Chiffrement", self.chiffrer)]
        for nom, fn in etapes:
            if not fn():
                logger.error(f"✗ Échec à l'étape: {nom}")
                return False
        return True

!<B
restore = RestoreManager(
    manifeste_path='app_backup_20240101.zip.manifest',
    cle=b'votre-cle-fernet...'
)
# Charge automatiquement le manifeste JSON
# et normalise la clé en bytes

self.cle = cle if isinstance(cle, bytes) else cle.encode()

!<C
def main():
    # === TEST 1: SAUVEGARDE ===
    backup = BackupManager('/var/www/app', 'app_backup')
    if backup.executer_sauvegarde():
        cle = backup.cle
        print(f"✓ Clé: {cle.decode()}")
    else:
        return False

    # === TEST 2: RESTAURATION ===
    restore = RestoreManager(backup.manifeste_name, cle)
    if restore.executer_restauration('/restore/app'):
        print("✓ Restauration validée")
    else:
        return False

    return True

if __name__ == "__main__":
    exit(0 if main() else 1)
