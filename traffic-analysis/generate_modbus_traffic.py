import time
from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 502
NOMBRE_REQUETES = 10
INTERVALLE = 0.1

client = ModbusTcpClient(HOST, port=PORT, timeout=2, retries=0)

print("\n===== GENERATION DE TRAFIC MODBUS =====")

try:
    if not client.connect():
        print("ERREUR : connexion au PLC impossible.")
        raise SystemExit(1)

    print(f"Connexion au PLC : {HOST}:{PORT}")

    for numero in range(1, NOMBRE_REQUETES + 1):
        reponse = client.read_coils(
            address=0,
            count=1,
            device_id=1
        )

        if reponse.isError():
            print(f"Requete {numero} : erreur")
        else:
            print(f"Requete {numero} : lecture reussie - valeur : {reponse.bits[0]}")

        time.sleep(INTERVALLE)

finally:
    client.close()
    print("\nConnexion fermee.")
    print("===== FIN DE LA GENERATION =====")
