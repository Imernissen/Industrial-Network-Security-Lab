import subprocess
import sys
from collections import Counter
from pathlib import Path

# Choix de la capture réseau
if len(sys.argv) > 1:
    capture = Path(sys.argv[1])
else:
    capture = Path("traffic-analysis/modbus_capture.pcap")
# Vérifier que le fichier existe
if not capture.exists():
    print("Erreur : fichier de capture introuvable.")
    exit(1)

# Demander à TShark d'extraire les requêtes Modbus
commande = [
    "tshark",
    "-r", str(capture),
    "-Y", "modbus && tcp.dstport == 502",
    "-T", "fields",
    "-E", "separator=|",
    "-e", "frame.number",
    "-e", "ip.src",
    "-e", "ip.dst",
    "-e", "modbus.func_code",
    "-e", "modbus.reference_num"
]

resultat = subprocess.run(
    commande,
    capture_output=True,
    text=True,
    check=True
)

# Préparer les statistiques
requetes = []
fonctions = Counter()
adresses = Counter()

# Analyser chaque ligne récupérée
for ligne in resultat.stdout.splitlines():
    champs = ligne.split("|")

    if len(champs) < 5:
        continue

    numero, source, destination, fonction, reference = champs

    requetes.append(ligne)
    fonctions[fonction] += 1
    adresses[source] += 1

# Afficher le rapport
print("\n===== ANALYSE DU TRAFIC MODBUS =====")
print(f"Nombre total de requêtes : {len(requetes)}")

print("\nNombre de requêtes par fonction :")
for fonction, nombre in sorted(fonctions.items()):
    print(f"Fonction {fonction} : {nombre}")

print("\nNombre de requêtes par adresse IP source :")
for adresse, nombre in adresses.items():
    print(f"{adresse} : {nombre}")
# Liste des adresses IP autorisées
ips_autorisees = ["127.0.0.1"]

# Détection des adresses IP inconnues
print("\n===== DETECTION DES IP INCONNUES =====")

anomalie_detectee = False

for adresse in adresses:
    if adresse not in ips_autorisees:
        print(f"ALERTE : adresse IP inconnue détectée : {adresse}")
        anomalie_detectee = True

if not anomalie_detectee:
    print("Aucune adresse IP inconnue détectée.")
# Fonctions Modbus autorisées dans notre laboratoire
fonctions_autorisees = ["1","5"]

# Détection des fonctions inhabituelles
print("\n===== DETECTION DES FONCTIONS INHABITUELLES =====")

anomalie_fonction = False

for fonction in fonctions:
    if fonction not in fonctions_autorisees:
        print(f"ALERTE : fonction Modbus inhabituelle : {fonction}")
        anomalie_fonction = True

if not anomalie_fonction:
    print("Aucune fonction Modbus inhabituelle détectée.")
# Seuil maximum de requêtes par adresse IP
seuil_requetes = 10

# Détection d'un volume excessif
print("\n===== DETECTION DU TRAFIC EXCESSIF =====")

anomalie_trafic = False

for adresse, nombre in adresses.items():
    if nombre > seuil_requetes:
        print(f"ALERTE : trafic excessif depuis {adresse} : {nombre} requêtes")
        anomalie_trafic = True

if not anomalie_trafic:
    print("Aucun volume excessif détecté.")
print("\n===== FIN DE L'ANALYSE =====")
