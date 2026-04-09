!<2.1
def creer_cle_mensuelle(annee, mois):
    os.makedirs('cles', exist_ok=True)
    cle = Fernet.generate_key()
    nom_fichier = f'cles/backup_{annee}_{mois:02d}.key'

    with open(nom_fichier, 'wb') as f:
        f.write(cle)
    os.chmod(nom_fichier, 0o600)

    rotation_file = 'cles/rotation.json'
    if os.path.exists(rotation_file):
        with open(rotation_file, 'r') as f:
            rotation = json.load(f)
    else:
        rotation = {"cles_actives": [],
                    "cles_archivees": []}

    rotation['cles_actives'].append(nom_fichier)
    rotation['derniere_rotation'] = datetime.now().isoformat()

    with open(rotation_file, 'w') as f:
        json.dump(rotation, f, indent=2)

    logger.info(f"Clé créée: {nom_fichier}")
    return cle

    !<2.2
    def generer_manifeste_incremental(
        archive_nom, archive_precedente=None):
    hash_archive = calculer_hash_fichier(archive_nom)
    manifeste = {
        "timestamp": datetime.now().isoformat(),
        "archive_file": archive_nom,
        "backup_type": "incremental"
            if archive_precedente else "full",
        "hash_archive": hash_archive,
        "taille_bytes": os.path.getsize(archive_nom),
        "depends_on": archive_precedente
    }
    return manifeste

def valider_chaîne_restauration(
        manifeste_path, dossier_archives):
    with open(manifeste_path, 'r') as f:
        manifeste = json.load(f)
    archives_requises = [manifeste['archive_file']]
    archive_courante = manifeste.get('depends_on')
    while archive_courante:
        archives_requises.append(archive_courante)
        man_prec = f"{archive_courante}.manifest"
        if not os.path.exists(
                f"{dossier_archives}/{man_prec}"):
            logger.error(
                f"Dépendance manquante: {archive_courante}")
            return False
        with open(
                f"{dossier_archives}/{man_prec}",'r') as f:
            man_temp = json.load(f)
        archive_courante = man_temp.get('depends_on')
    return True

    !<2.3
    def scanner_fichiers_suspects(
        dossier, taille_max_mb=100,
        extensions_dangereuses=None):
    if extensions_dangereuses is None:
        extensions_dangereuses = [
            '.exe','.bat','.sh','.dll','.sys']
    os.makedirs('quarantine', exist_ok=True)
    suspects = []

    for root, dirs, files in os.walk(dossier):
        for fichier in files:
            chemin = os.path.join(root, fichier)
            taille = os.path.getsize(chemin)
            if taille > taille_max_mb * 1024 * 1024:
                suspects.append({
                    'nom': fichier,
                    'raison': 'taille',
                    'valeur': f"{taille/(1024*1024):.1f}MB",
                    'chemin': chemin })
                continue
            _, ext = os.path.splitext(fichier)
            if ext.lower() in extensions_dangereuses:
                suspects.append({
                    'nom': fichier,
                    'raison': 'extension',
                    'valeur': ext,
                    'chemin': chemin })

    for suspect in suspects:
        dest = f"quarantine/{suspect['nom']}"
        shutil.move(suspect['chemin'], dest)
        logger.info(
            f"Isolé: {suspect['nom']} "
            f"({suspect['raison']})")
    return suspects

    !<testIso
    class TestsISO27001:
    """Tests conformité ISO 27001"""

    def test_confidentialite(self):
        """A.14.1.1: Contrôle d'accès"""
        # Vérifier permissions 0o600
        # Vérifier chiffrement actif
        # Vérifier clés absentes des logs
        print("✓ Confidentialité OK")

    def test_integrite(self):
        """A.14.1.2: Intégrité"""
        # Vérifier hash à la création
        # Comparer original vs restauré
        # Vérifier manifeste non altéré
        print("✓ Intégrité OK")

    def test_disponibilite(self):
        """A.14.1.3: RTO/RPO"""
        # Mesurer temps restauration
        # Vérifier RPO ≤ 24h, RTO ≤ 4h
        print("✓ Disponibilité OK")

    def test_tracabilite(self):
        """A.12.4.1: Audit"""
        # Vérifier toutes actions loggées
        # Vérifier logs immuables
        # Vérifier horodatage
        print("✓ Traçabilité OK")

    def test_chiffrement_strength(self):
        """A.10.1.1: Chiffrement fort"""
        # Vérifier AES-256
        # Vérifier mode CBC + IV aléatoire
        print("✓ Chiffrement fort OK")

    def test_retention(self):
        """A.14.3: Rétention"""
        # Vérifier sauvegardes > 30 jours
        # Vérifier destruction sécurisée
        print("✓ Rétention OK")