
# Live Modbus TCP Traffic Generation and Capture

## Objective

This experiment demonstrates how to generate Modbus TCP traffic by communicating with a simulated industrial PLC running OpenPLC Runtime.

The generated traffic is captured and analyzed using TShark.

## Environment

- OpenPLC Runtime v4.3.2
- Modbus TCP (port 502)
- Python 3.12
- PyModbus 3.16.2
- Wireshark / TShark 4.2.2
- Ubuntu 24.04 (WSL2)

## Traffic Generation

The Python script `generate_modbus_traffic.py` establishes a connection to the simulated PLC and sends 10 Read Coils requests (Function Code 1).

The requests are sent at intervals of 100 milliseconds.

## Network Capture

Traffic is captured on the loopback interface using TShark:

```bash
tshark -i lo -f "tcp port 502" -w traffic-analysis/modbus_live_capture.pcap
```

The capture contains both client requests and PLC responses.

## Analysis Results

The captured traffic contains:

- 10 Modbus TCP requests.
- 10 corresponding PLC responses.
- Modbus Function Code 1 (Read Coils).
- Source and destination IP address: 127.0.0.1.
- No Modbus exception code observed.

The general analysis script successfully processes this capture and reports 10 requests.

## Security Relevance

This experiment demonstrates practical network traffic generation, packet capture and Modbus TCP protocol analysis in an isolated industrial environment.

It also provides a reusable PCAP file for testing the traffic analysis and detection scripts.

## Limitations

- Communication takes place locally on the loopback interface.
- Only Read Coils requests are generated.
- The experiment does not reproduce a complete industrial production network.
- The generated traffic is benign and does not represent an attack.

## Conclusion

The experiment validates the communication between the Python Modbus client and the simulated PLC, as well as the capture and analysis of live Modbus TCP exchanges.
