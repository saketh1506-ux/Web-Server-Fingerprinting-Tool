import socket, ssl, threading, time

# Global variables
active_clients = 0
total_requests_received = 0
counter_lock = threading.Lock()

def handle_client(conn, addr):
    global active_clients, total_requests_received
    try:
        start_process_time = time.time()
        with counter_lock:
            total_requests_received += 1
            active_clients += 1
            req_num, current_active = total_requests_received, active_clients

        # 1. Receive Full Message from Client
        data = conn.recv(1024).decode(errors='ignore')
        
        if data:
            # LOOK FOR CLIENT BANNER (Identifying the scanner)
            client_banner = "No Client Banner Detected"
            for line in data.split('\n'):
                if "Client-Identity:" in line:
                    client_banner = line.replace("Client-Identity:", "").strip()
                    break
            
            print(f"\n" + "="*75)
            print(f"[NEW CONNECTION] Source: {addr}")
            print(f"[*] IDENTIFIED CLIENT: {client_banner}") # Server gets the banner here
            print(f"[*] Request Count: {req_num} | Active Now: {current_active}")
            print(f"--- MESSAGE RECEIVED FROM CLIENT ---\n{data.strip()}\n--------------------------------------")
            
            # 2. Prepare response (REMOVED Server-Side Request ID as requested)
            server_identity = "Jackfruit-Secure-Webserver/2.0 (PES-University)"
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Server: {server_identity}\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                f"Target Identity Verified: {server_identity}\n"
                "Security: SSL/TLS Active\n"
            )
            
            # 3. Send and calculate Server Metrics
            conn.sendall(response.encode())
            
            duration = time.time() - start_process_time
            throughput = (len(response.encode()) * 8) / duration if duration > 0 else 0
            
            print(f"[SERVER METRICS] Latency: {duration*1000:.4f}ms | Throughput: {throughput:.2f} bps")
            
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        with counter_lock:
            active_clients -= 1
        conn.close()

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', 4443))
    server_sock.listen(15)
    print(f"[*] JACKFRUIT MASTER MONITOR SYSTEM ONLINE")

    while True:
        newsock, addr = server_sock.accept()
        try:
            secure_conn = context.wrap_socket(newsock, server_side=True)
            threading.Thread(target=handle_client, args=(secure_conn, addr)).start()
        except:
            newsock.close()

if __name__ == "__main__":
    start_server()