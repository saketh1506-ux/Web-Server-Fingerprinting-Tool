import socket, ssl, time

TARGETS = [
    ("10.175.161.210", 4443, True),   # Your Local Server
    ("www.google.com", 443, True),     # HTTPS
    ("www.microsoft.com", 443, True),  # HTTPS
    ("ftp.sjtu.edu.cn", 21, False),    # FTP
]

def run_scanner():
    results_for_table = []
    
    for host, port, use_ssl in TARGETS:
        start_time = time.time()
        try:
            sock = socket.create_connection((host, port), timeout=5)
            if use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)

            if port == 21:
                raw_data = sock.recv(4096)
            else:
                # Identification Probe with Client Banner
                probe = (
                    f"HEAD / HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"Client-Identity: Jackfruit-Scanner-v1.0 (PES-University)\r\n"
                    f"Connection: close\r\n\r\n"
                )
                sock.sendall(probe.encode())
                raw_data = sock.recv(4096)

            duration = time.time() - start_time
            latency = duration * 1000
            throughput = (len(raw_data) * 8) / duration if duration > 0 else 0
            
            # --- CLEANED OUTPUT LOGIC ---
            decoded = raw_data.decode(errors='ignore').strip()
            print(f"\n[SCANNING] {host}...")
            
            banner_summary = "Not Found"
            server_line = ""
            
            # Filter headers to find only the 'Server' identification
            for line in decoded.split('\n'):
                if "Server:" in line or port == 21:
                    server_line = line.strip()
                    banner_summary = server_line.replace("Server:", "").strip()
                    break
            
            print("--- CLEAN DATA RECEIVED ---")
            print(f"Target Identity: {banner_summary}")
            if use_ssl:
                print("Security: SSL/TLS Encrypted")
            print("---------------------------")
            
            results_for_table.append((host, port, "YES" if use_ssl else "NO", banner_summary, latency, throughput))
            sock.close()

        except Exception as e:
            results_for_table.append((host, port, "N/A", "Failed", 0, 0))

    # FINAL PERFORMANCE TABLE
    print("\n" + "="*125)
    print(f"{'TARGET HOST':<25} | {'PORT':<6} | {'SSL':<5} | {'BANNER SUMMARY':<40} | {'LATENCY':<10} | {'THROUGHPUT'}")
    print("-" * 125)
    for h, p, s, b, l, t in results_for_table:
        tp_str = f"{t/1000:.2f} kbps" if t > 1000 else f"{t:.2f} bps"
        print(f"{h:<25} | {p:<6} | {s:<5} | {b[:38]:<40} | {l:<8.2f}ms | {tp_str}")
    print("="*125 + "\n")

if __name__ == "__main__":
    run_scanner()