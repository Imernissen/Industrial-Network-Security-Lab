# Unauthorized Modbus Function Detection Scenario

## Objective

Demonstrate the detection of an unauthorized Modbus TCP function using a controlled laboratory scenario.

## Test Environment

- PLC simulation: OpenPLC Runtime
- Protocol: Modbus TCP
- Client: PyModbus
- Network capture: TShark
- Detection: Python
- Network interface: Loopback (127.0.0.1)

## Scenario

The detection configuration authorizes the following functions:

- FC1: Read Coils
- FC5: Write Single Coil

A separate Python script generates a request using FC3 (Read Holding Registers).

## Network Capture Results

The PCAP file contains:

- One FC3 request from the client to the PLC.
- One response from the PLC.
- Modbus exception code 2 (Illegal Data Address).

The exception indicates that the requested register address is unavailable or invalid.

## Detection Results

The detection script identifies FC3 as an unauthorized function.

Expected alert:

    ALERTE : fonction Modbus non autorisee : FC3
    Nombre de requetes : 1

The detection is based on the configured function allowlist, independently of the PLC response.

## Security Relevance

Monitoring Modbus function codes can help identify unexpected operations within an industrial network.

## Limitations

- The test uses a simulated PLC.
- Communication takes place locally through loopback.
- Only one unauthorized function is tested.
- Detection is performed offline using a PCAP file.
- The detection mechanism generates alerts but does not block communication.

## Conclusion

The scenario successfully demonstrates the detection of a Modbus function that is not included in the configured allowlist.
