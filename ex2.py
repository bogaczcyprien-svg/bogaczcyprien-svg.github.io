import hashlib

def calculer_hash_fichier(chemin):
    """Calcule le SHA-256 d'un fichier"""
    hasher = hashlib.sha256()

    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(4096), b''):
            hasher.update(bloc)

    return hasher.hexdigest()
     !<B2
     def fichiers_identiques_v2(c1, c2):
    return (
        calculer_hash_fichier(c1)
        == calculer_hash_fichier(c2)
    )
   
    !<C1
    import json, os
from datetime import datetime

def creer_manifeste(dossier_source, fichiers_liste):
    manifeste = {
        "timestamp": datetime.now().isoformat(),
        "total_fichiers": len(fichiers_liste),
        "fichiers": []
    }
    total_octets = 0
    for fichier in fichiers_liste:
        chemin = f"{dossier_source}/{fichier}"
        manifeste["fichiers"].append({
            "chemin": fichier,
            "hash": calculer_hash_fichier(chemin),
            "taille": os.path.getsize(chemin)
        })
        total_octets += os.path.getsize(chemin)
    manifeste["total_octets"] = total_octets
    with open("backup.manifest", "w") as f:
        json.dump(manifeste, f, indent=2)
    
    !<C2
    def verifier_manifeste(dossier, manifeste_path):
    with open(manifeste_path, 'r') as f:
        manifeste = json.load(f)

    resultats = []
    for fichier_info in manifeste["fichiers"]:
        chemin = f"{dossier}/{fichier_info['chemin']}"
        hash_calcule = calculer_hash_fichier(chemin)
        hash_attendu = fichier_info['hash']
        resultats.append({
            "fichier": fichier_info['chemin'],
            "valide": hash_calcule == hash_attendu,
            "hash_calcule": hash_calcule,
            "hash_attendu": hash_attendu
        })
    return resultats

    !<C3
    def rapport_verif_complet(dossier, manifeste_path):
    resultats = verifier_manifeste(dossier, manifeste_path)
    total = len(resultats)
    valides = sum(1 for r in resultats if r['valide'])
    corrompus = total - valides

    print(f"\n{'='*60}")
    print(f"RAPPORT DE VÉRIFICATION D'INTÉGRITÉ")
    print(f"{'='*60}")
    print(f"Fichiers vérifiés: {total}")
    print(f"  ✓ Intègres:  {valides}")
    print(f"  ✗ Corrompus: {corrompus}")

    if corrompus > 0:
        print(f"\nFichiers problématiques:")
        for r in resultats:
            if not r['valide']:
                print(f"  - {r['fichier']}")

    statut = "✓ OK" if corrompus == 0 else "✗ ERREURS"
    print(f"\nStatut global: {statut}")
    return corrompus == 0
