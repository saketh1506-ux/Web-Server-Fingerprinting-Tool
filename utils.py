import socket
import ssl

def grab_http_banner(host, port=80):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, port))

        request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
        s.send(request.encode())

        data = s.recv(1024).decode(errors="ignore")
        s.close()

        return data
    except:
        return None


def grab_https_banner(host, port=443):
    try:
        context = ssl.create_default_context()

        s = socket.create_connection((host, port), timeout=3)
        secure_sock = context.wrap_socket(s, server_hostname=host)

        request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
        secure_sock.send(request.encode())

        data = secure_sock.recv(1024).decode(errors="ignore")
        secure_sock.close()

        return data
    except:
        return None


def grab_ftp_banner(host, port=21):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, port))

        data = s.recv(1024).decode(errors="ignore")
        s.close()

        return data
    except:
        return None
