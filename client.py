import socket
import select
import time
import threading
import File
#import Functions

SERVER_IP = "10.20.90.57"
addr = SERVER_IP
ADDRESSES = []
FILES = []
UDP_PORT = 50000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("Hello",(SERVER_IP, UDP_PORT))
rlist = select.select([client_socket],[],[],5)
if rlist[0]:
    # The server responded
    data, addr= client_socket.recvfrom(4096)
    debug_print("We received" + data + "from server")
    ADDRESSES = data.split(';')
    debug_print("Connected to the main server")
    debug_print("We have the following addresses:\n" + ADDRESSES)

else:
    while not ADDRESSES:
        # TODO: Check if the IP is correct
        addr = raw_input("Could not connect to the IP " + addr + "\nplease input other IP\n")
        client_socket.sendto("Hello",(addr, UDP_PORT))
        rlist = select.select([client_socket],[],[], 5)
        if rlist[0]:
            ADDRESSES.append(addr)  # That user is online
            data, addr = client_socket.recvfrom(4096)
            debug_print("Connected to this address: " + addr)
            ADDRESSES += data.split(';')
            debug_print("We have the following addresses:\n" + ADDRESSES)

for addr in ADDRESSES:
    client_socket.sendto("show-files",(addr, UDP_PORT))

listen_thread = threading.Thread(target=UDP_listen())
listen_thread.start()


def handle_data():
    return




def UDP_listen():
    while True:
        data, addr = client_socket.recvfrom(4096)
        print "Received this data" + data
        command_num, file_name, answer_type, file_hash, file_parts_num, file_size, file_description = convert_message(data)
        if data == "Hello":
            debug_print(addr + "Connected")
            client_socket.sendto(';'.join(ADDRESSES), (addr,UDP_PORT))
            ADDRESSES.append(addr)

        if data == "show-files":
            if addr not in ADDRESSES:
                ADDRESSES.append(addr)
            my_files = Functions.get_all_files()
            content = "FILES:"
            for file_object in my_files:
                content += file_object.to_string() + ';'
            client_socket.sendto(content,(addr, UDP_PORT))


        if data.startswith("FILES:"):
            list_of_files = data[6:].split(';')
            for file_object in list_of_files:
                #  This response is list of all files that the peer has
                file_name, file_hash, file_size, file_description = decrypt_file(file_object)
                FILES.append([file_name, file_hash, file_size, file_description])
        if int(command_num) == 1:
            None


def debug_print(data):
    print data
