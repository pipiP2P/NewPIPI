import socket

def debug_print(data):
    print data

UDP_PORT = 50000
ADDRESSES = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if __name__ == '__main__':
    udp_socket.bind(('0.0.0.0', UDP_PORT))
    debug_print("Succeed binding on port " + str(UDP_PORT) )
    while True:
        data, addr = udp_socket.recvfrom(4096)
        addr = addr[0]
        print 'DATA RECEIVED: ', data
        if data == "Hello":
            if ADDRESSES:
                print 'Sending %s To: %s' %('\n'.join(ADDRESSES), addr)
                udp_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
            else:
                print 'Sending None To: ', addr
                udp_socket.sendto("None", (addr, UDP_PORT))
            if addr not in ADDRESSES:
                # Todo: Check how much people send to the client
                ADDRESSES.append(addr)
