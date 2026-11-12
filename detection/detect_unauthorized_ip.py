
import subprocess
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) > 1:
    capture = Path(sys.argv[1])
else:
    capture = Path("traffic-analysis/modbus_capture.pcap")
# Vérifier que la capture existe
if not capture.exists():
    print("ERREUR : fichier de capture introuvable.")
    raise SystemExit(1)

# Extraire les requêtes Modbus envoyées vers le port 502
commande = [
    "tshark",
    "-r", str(capture),
    "-Y", "modbus && tcp.dstport == 502",
    "-T", "fields",
    "-e", "ip.src"
]

resultat = subprocess.run(
    commande,
    capture_output=True,
    text=True,
    check=True
)

# Compter les requêtes par adresse IP
adresses = Counter(
    ligne.strip()
    for ligne in resultat.stdout.splitlines()
    if ligne.strip()
)

# Liste des adresses IP autorisées dans notre laboratoire
ips_autorisees = ["127.0.0.1"]

print("\n===== DETECTION DES IP NON AUTORISEES =====")

anomalie = False

for adresse, nombre in adresses.items():
    if adresse not in ips_autorisees:
        print(f"ALERTE : IP non autorisee : {adresse}")
        print(f"Nombre de requetes : {nombre}")
        anomalie = True

if not anomalie:
    print("Aucune IP non autorisee detectee.")

print("\n===== FIN DE L'ANALYSE =====")
