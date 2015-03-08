import socket


UDP_PORT = 50000
ADDRESSES = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', UDP_PORT))
while True:
    addr, data = udp_socket.recvfrom(4096)
    if data == "Hello":
        if addr not in ADDRESSES:
            # Todo: Check how much people send to the client
            udp_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
            ADDRESSES.append(addr)
