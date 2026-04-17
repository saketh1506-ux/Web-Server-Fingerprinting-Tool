# Jackfruit Secure Network Scanner & Webserver

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/Security-SSL%2FTLS-red.svg)

A high-performance, secure networking implementation built with low-level Python sockets. This project demonstrates a custom bidirectional fingerprinting protocol, multi-threaded concurrency, and real-time performance evaluation.

##  Key Features

###  Jackfruit-Secure-Webserver (`server.py`)
* **SSL/TLS Encryption:** Mandatory security layer using custom `.pem` certificates.
* **Concurrency:** Thread-safe handling of multiple concurrent scanner probes.
* **Persistent Monitoring:** * Tracks **Total Requests** across the server's lifetime.
  * Monitors **Active User Count** in real-time.
* **Full Visibility:** Intercepts and logs the full raw probe data from clients.
* **Internal Metrics:** Calculates server-side processing latency and outbound throughput.

###  Jackfruit-Scanner (`client.py`)
* **Multi-Protocol Support:** Scans HTTPS (Web) and FTP services.
* **Mutual Identification:** Sends a custom `Client-Identity` banner to the target.
* **Performance Dashboard:** Displays a real-time table of:
  * **Latency:** Measured in milliseconds (ms).
  * **Throughput:** Calculated in bits per second (bps) or kbps.
* **Cleaned Output:** Intelligently filters messy HTTP headers to show only relevant identity and security data.

##  Project Architecture

The system operates on a **Request-Response** model over an encrypted socket.



1. **Secure Handshake:** Client and Server establish an SSL/TLS encrypted tunnel.
2. **Identity Probe:** Client sends a `HEAD` request with a `Client-Identity` header.
3. **Internal Processing:** Server logs the client banner and increments global counters.
4. **Fingerprint Response:** Server returns the `Jackfruit-Secure-Webserver/2.0` banner.
5. **Metric Calculation:** Both endpoints calculate the transmission speed and delay.

##  File Structure

```text
D:\CN_PROJECT\
├── server.py      # The multi-threaded secure server
├── client.py      # The performance-monitoring scanner
├── cert.pem       # SSL Certificate
└── key.pem        # SSL Private Key
