
import subprocess
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) > 1:
    capture = Path(sys.argv[1])
else:
    capture = Path("traffic-analysis/modbus_capture.pcap")
# Vérifier que le fichier existe
if not capture.exists():
    print("ERREUR : fichier de capture introuvable.")
    raise SystemExit(1)

# Extraire uniquement les requêtes Modbus vers le port 502
commande = [
    "tshark",
    "-r", str(capture),
    "-Y", "modbus && tcp.dstport == 502",
    "-T", "fields",
    "-e", "modbus.func_code"
]

resultat = subprocess.run(
    commande,
    capture_output=True,
    text=True,
    check=True
)

# Compter les fonctions Modbus observées
fonctions = Counter(
    ligne.strip()
    for ligne in resultat.stdout.splitlines()
    if ligne.strip()
)

# Politique de sécurité du laboratoire
fonctions_autorisees = ["1", "5"]

print("\n===== DETECTION DES FONCTIONS MODBUS INHABITUELLES =====")

anomalie = False

for fonction, nombre in sorted(fonctions.items()):
    if fonction not in fonctions_autorisees:
        print(f"ALERTE : fonction Modbus non autorisee : FC{fonction}")
        print(f"Nombre de requetes : {nombre}")
        anomalie = True
    else:
        print(f"Fonction FC{fonction} autorisee : {nombre} requetes")

if not anomalie:
    print("\nAucune fonction Modbus inhabituelle detectee.")

print("\n===== FIN DE L'ANALYSE =====")
