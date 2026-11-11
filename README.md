# Industrial Network Security Lab

## Project Overview

This project is an isolated laboratory designed to explore industrial network security through PLC simulation, Modbus TCP traffic analysis, and basic anomaly detection.

The laboratory uses OpenPLC Runtime to simulate an industrial controller. Network traffic is captured and analyzed to identify potentially suspicious communication patterns.

## Objectives

- Simulate an industrial environment using OpenPLC Runtime.
- Understand and analyze Modbus TCP communications.
- Capture and inspect network traffic.
- Implement basic detection mechanisms for suspicious Modbus activity.
- Validate detection logic using automated tests.

## Laboratory Architecture

The laboratory is based on the following components:

- **OpenPLC Runtime:** PLC simulation.
- **Modbus TCP:** Industrial communication protocol using TCP port 502.
- **TShark / Wireshark:** Network traffic capture and analysis.
- **Python:** Implementation of detection scripts.
- **Pytest:** Automated testing of detection logic.
- **Docker:** Deployment of the OpenPLC Runtime.

The network architecture is documented in [`architecture/network_architecture.md`](architecture/network_architecture.md).

## Detection Mechanisms

Three detection mechanisms have been implemented:

### 1. Unauthorized IP Detection

Identifies Modbus requests originating from IP addresses that are not included in the configured allowlist.

Script: [`detect_unauthorized_ip.py`](detection/detect_unauthorized_ip.py)

### 2. Unusual Modbus Function Detection

Checks Modbus function codes against a predefined list of authorized functions.

Script: [`detect_unusual_modbus_functions.py`](detection/detect_unusual_modbus_functions.py)

### 3. Excessive Modbus Traffic Detection

Uses a sliding time window to identify unusually frequent Modbus requests.

Script: [`detect_modbus_flood.py`](detection/detect_modbus_flood.py)
### Detection Example — Unauthorized Modbus Function

The following screenshot shows a controlled test in which Modbus function FC5 was temporarily removed from the authorized function list.

![Unauthorized Modbus function detection](screenshots/detection_fonction_modbus.png)
## Automated Testing

Automated tests are implemented with Pytest to validate the detection logic.

**Current test results:**
- 10 tests executed.
- 10 tests passed.
- 0 tests failed.

The tests cover normal traffic, suspicious activity, and boundary conditions.
### Test Execution Results

![Automated test results](screenshots/tests_validation.png)
## Reports and Documentation

Technical reports are available in the [`reports/`](reports/) directory.

They document:
- Unauthorized IP detection.
- Unusual Modbus function detection.
- Excessive Modbus traffic detection.
- Automated test validation.

## Limitations and Future Improvements

The current laboratory has several limitations:

- The PLC is simulated; no physical industrial equipment is used.
- Traffic analysis is performed offline using PCAP files.
- Detection thresholds and authorized values are manually configured.
- Detection scripts generate alerts but do not block network traffic.
- Automated tests validate detection logic with controlled inputs rather than performing full end-to-end integration tests.

Future improvements could include:
- Testing with more realistic industrial traffic.
- Improving detection thresholds.
- Expanding Modbus anomaly detection.
- Adding more comprehensive network monitoring.

## Project Scope

This project is an educational laboratory focused on understanding industrial network communication and implementing basic security monitoring mechanisms.
### Detection Example — Excessive Modbus Traffic

The following screenshot shows the detection of an unusually high number of Modbus requests within a 10 ms time window.

![Excessive Modbus traffic detection](screenshots/detection_trafic_modbus.png)
### Detection Example — Unauthorized IP

The following screenshot shows a controlled test in which the authorized IP address was temporarily changed to trigger an unauthorized IP alert.

![Unauthorized IP detection](screenshots/detection_ip_non_autorisee.png)
