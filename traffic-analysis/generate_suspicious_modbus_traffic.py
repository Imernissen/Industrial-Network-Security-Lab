from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 502

client = ModbusTcpClient(HOST, port=PORT, timeout=2)

print("\n===== GENERATION DE TRAFIC MODBUS =====")

try:
    if not client.connect():
        print("ERREUR : connexion au PLC impossible.")
        raise SystemExit(1)

    print(f"Connexion au PLC : {HOST}:{PORT}")

    reponse = client.read_holding_registers(
        address=0,
        count=1,
        device_id=1
    )

    if reponse.isError():
        print("Reponse Modbus : exception ou erreur")
    else:
        print("Lecture FC3 reussie :", reponse.registers)

finally:
    client.close()
    print("Connexion fermee.")
    print("===== FIN DE LA GENERATION =====")
