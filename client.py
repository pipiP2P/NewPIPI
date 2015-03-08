import socket
import select
import time
import threading
import File
import Functions

SERVER_IP = "127.0.0.1"
addr = SERVER_IP
ADDRESSES = []
FILES = []
UDP_PORT = 50000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("Hello",(SERVER_IP, UDP_PORT))
rlist = select.select([client_socket],[],[],timeout=5)
if rlist[0]:
    addr, data = client_socket.recvfrom(4096)
    ADDRESSES = data.split(';')
    debug_print("Connected to the main server")
    debug_print("We have the following addresses:\n" + ADDRESSES)

else:
    while not ADDRESSES:
        # TODO: Check if the IP is correct
        addr = raw_input("Could not connect to the IP" + addr + "please input other IP")
        client_socket.sendto("Hello",(SERVER_IP, UDP_PORT))
        rlist = select.select([client_socket],[],[],timeout=5)
        if rlist[0]:
            ADDRESSES.append(addr)  # That user is online
            addr, data = client_socket.recvfrom(4096)
            debug_print("Connected to this address: " + addr)
            ADDRESSES += data.split(';')
            debug_print("We have the following addresses:\n" + ADDRESSES)

for addr in ADDRESSES:
    client_socket.sendto("show-files",(addr, UDP_PORT))

listen_thread = threading.Thread(target=udp_listen(),args=client_socket)
listen_thread.start()


def handle_data():
    return




def UDP_listen():
    while True:
        addr, data = client_socket.recvfrom(4096)
        command_num, file_name, answer_type, file_hash, file_parts_num, file_size, file_description = handle_data(data)
        if data == "Hello":
            debug_print(addr + "Connected")
            client_socket.sendto(';'.join(ADDRESSES), (addr,UDP_PORT))
            ADDRESSES.append(addr)

        if data == "show-files":
            my_files = Functions.get_all_files()
            content = ""
            for file_object in my_files:
                content += file_object.to_string()
            client_socket.sendto(content,(addr, UDP_PORT))


        if data.startswith("FILES:"):
            list_of_files = data[6:].split(;)
            #  This response is list of all files that the peer has
            FILES.append([file_name, file_hash, file_size, file_description])
        if int(command_num) == 1:
            None


def debug_print(data):
    print data
