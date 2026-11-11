# Detection of Unauthorized IP Addresses in Modbus TCP Traffic

## 1. Objective

The objective of this component is to identify unauthorized IP addresses communicating with an industrial PLC through the Modbus TCP protocol.

The detection process relies on an offline analysis of network traffic captured in a PCAP file.

## 2. Technical Environment

- Operating system: Ubuntu 24.04 under WSL2
- PLC runtime: OpenPLC Runtime v4.3.2
- Industrial protocol: Modbus TCP
- Server port: TCP 502
- Analysis tool: TShark
- Programming language: Python 3

## 3. Detection Principle

The Python script analyzes the captured network traffic and extracts the source IP addresses of Modbus TCP requests directed to destination port 502.

An allowlist defines which IP addresses are authorized to communicate with the PLC.

Any source IP address not present in this list generates a security alert.

Example of the allowlist configuration:

```python
ips_autorisees = ["127.0.0.1"]
```

## 4. Implementation

The script is located at:

`detection/detect_unauthorized_ip.py`

The main processing steps are:

1. Check whether the PCAP file exists.
2. Execute TShark to extract Modbus TCP request source addresses.
3. Count requests by source IP address.
4. Compare each address against the authorized IP list.
5. Generate an alert when an unauthorized address is detected.

The script uses Python's `subprocess` module to execute TShark and `Counter` to count requests by IP address.

## 5. Validation and Test Results

Two test scenarios were performed using the same network capture.

### Test 1 — Authorized IP address

Configuration:

```python
ips_autorisees = ["127.0.0.1"]
```

Observed result:

```text
===== DETECTION DES IP NON AUTORISEES =====
Aucune IP non autorisee detectee.
===== FIN DE L'ANALYSE =====
```

Interpretation:

The source address belongs to the authorized list. No alert is generated.

### Test 2 — Unauthorized IP address

For this controlled test, the allowlist was temporarily changed:

```python
ips_autorisees = ["192.168.1.100"]
```

Observed result:

```text
===== DETECTION DES IP NON AUTORISEES =====
ALERTE : IP non autorisee : 127.0.0.1
Nombre de requetes : 5
===== FIN DE L'ANALYSE =====
```

Interpretation:

The address `127.0.0.1` is not present in the temporary allowlist. The script correctly generates an alert and reports five requests.

The original configuration was subsequently restored.

## 6. Security Relevance

In an industrial environment, unauthorized communication with a PLC can represent a security risk.

An IP allowlist provides a basic mechanism for identifying unexpected communication sources.

Recommended security measures include:

- Restricting access to TCP port 502.
- Allowing only authorized engineering stations and supervisory systems.
- Segmenting IT and OT networks.
- Monitoring unexpected Modbus communications.
- Investigating unauthorized access attempts.

## 7. Limitations

This implementation has several limitations:

- Analysis is performed offline on a PCAP file.
- The allowlist is manually configured.
- The script does not block unauthorized connections.
- The request counter does not measure traffic rate over time.
- The current capture contains local loopback traffic only.

This component is a basic detection mechanism and does not replace a real-time industrial network monitoring solution.

## 8. Conclusion

The detection script successfully identifies source IP addresses that are not included in the configured allowlist.

Both authorized and unauthorized scenarios were tested successfully.

This component provides a foundation for further development of industrial network monitoring and security analysis.
