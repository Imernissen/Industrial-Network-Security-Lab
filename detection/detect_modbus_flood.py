
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

if len(sys.argv) > 1:
    capture = Path(sys.argv[1])
else:
    capture = Path("traffic-analysis/modbus_capture.pcap")

if not capture.exists():
    print("ERREUR : fichier de capture introuvable.")
    raise SystemExit(1)

commande = [
    "tshark",
    "-r", str(capture),
    "-Y", "modbus && tcp.dstport == 502",
    "-T", "fields",
    "-E", "separator=|",
    "-e", "frame.time_relative",
    "-e", "ip.src"
]

resultat = subprocess.run(
    commande,
    capture_output=True,
    text=True,
    check=True
)

requetes_par_ip = defaultdict(list)

for ligne in resultat.stdout.splitlines():
    champs = ligne.split("|")

    if len(champs) != 2:
        continue

    temps, adresse = champs

    try:
        requetes_par_ip[adresse].append(float(temps))
    except ValueError:
        continue

# Parametres de detection
fenetre = 0.010
seuil_requetes = 3

print("\n===== DETECTION DU TRAFIC MODBUS EXCESSIF =====")

anomalie = False
total_requetes = sum(len(temps) for temps in requetes_par_ip.values())

for adresse, temps in requetes_par_ip.items():
    temps.sort()

    gauche = 0
    maximum = 0

    # Analyse avec une fenetre glissante
    for droite in range(len(temps)):
        while temps[droite] - temps[gauche] > fenetre:
            gauche += 1

        nombre = droite - gauche + 1
        maximum = max(maximum, nombre)

    if maximum > seuil_requetes:
        print(f"ALERTE : trafic Modbus excessif depuis {adresse}")
        print(f"Maximum de requetes dans une fenetre de 10 ms : {maximum}")
        anomalie = True
    else:
        print(f"{adresse} : trafic normal ({maximum} requetes maximum)")

if not anomalie and not requetes_par_ip:
    print("Aucune requete Modbus trouvee.")

elif not anomalie:
    print("Aucun trafic Modbus excessif detecte.")

print(f"\nNombre total de requetes analysees : {total_requetes}")
print("\n===== FIN DE L'ANALYSE =====")
