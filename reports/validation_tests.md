
# Automated Tests and Validation

## Objective

This document describes the automated tests implemented to validate the detection logic developed in the Industrial Network Security Lab.

## Testing Environment

- Python 3.12
- Pytest 9.2.0
- Ubuntu 24.04 (WSL2)

## Test Coverage

Three detection mechanisms are covered.

### 1. Unauthorized IP Detection

File: `tests/test_unauthorized_ip.py`

Three test cases:
- Authorized IP address.
- Unauthorized IP address.
- Empty input list.

### 2. Unusual Modbus Function Detection

File: `tests/test_modbus_functions.py`

Three test cases:
- Authorized Modbus functions.
- Unauthorized Modbus function.
- Empty input list.

### 3. Excessive Modbus Traffic Detection

File: `tests/test_modbus_flood.py`

Four test cases:
- Normal traffic.
- Excessive traffic within a 10 ms window.
- Request count exactly equal to the configured threshold.
- Empty input list.

## Test Results

Command executed:

`pytest -v`

Result:

- Total tests: 10
- Passed: 10
- Failed: 0

All implemented automated tests passed successfully.

## Limitations

- Tests validate detection logic using controlled input data.
- They do not independently validate the complete integration with TShark or real network traffic.
- Thresholds and authorized values are experimental and manually configured.
- Passing tests does not guarantee detection of every possible attack scenario.

## Conclusion

Automated testing provides an initial validation of the three detection mechanisms. It helps verify expected behavior under normal, abnormal and empty-input conditions.
