import socket
import select
import time
import threading
import File
from Functions import *
from Protocol import *

SERVER_IP = "10.10.10.226"
addr = SERVER_IP
ADDRESSES = []
OUR_FILES = []
PEERS_FILES = []
UDP_PORT = 50000
DOWNLOAD_PORT = 50001
BUFFER_SIZE = 4096
TIMEOUT = 2
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_msg_to_all(msg, sending_socket):
    for addr in ADDRESSES:
        sending_socket.send(msg, (addr, UDP_PORT))


def initialize():
    """
    Initalize our files list
    OUR_FILES will be list of object of type FILE_INFO
    """
    global OUR_FILES
    OUR_FILES = get_all_files()
    print_our_files()


def print_our_files():
    debug_print("Our files:")
    for file_object in OUR_FILES:
        file_object.print_file_info()


def print_peers_files():
    debug_print("Peers files:")
    for file_object in PEERS_FILES:
        file_object.print_file_info()


def UDP_listener():
    """
    This function starts a new thread that listens
    to incoming UDP packets
    """
    listen_thread = threading.Thread(target=UDP_listen)
    listen_thread.start()


def handle_data(data):
    """
    Receives the incoming data
    and does the appropriate action (send file, send list of connected peers etc...)
    """
    try:
        command_num, file_name, file_hash, file_parts_num, file_size, file_description, answer_type = convert_message(data)
    except NameError:
        debug_print("Data doesn't fit the protocol")


def new_connection(addr):
    """
    We received new connection from addr
    We will send him the addresses we have or None
    Then we will add him to our peers list
    """
    debug_print(addr + "Connected")
    if ADDRESSES:
        client_socket.sendto(';'.join(ADDRESSES), (addr, UDP_PORT))
    else:
        client_socket.sendto("None", (addr, UDP_PORT))
    ask_for_files()  # This client has connected to us, ask him about his files list


def send_files_list(addr):
    check_our = True
    check_peers = True
    debug_print("{0} asked us for our files list!".format(addr))
    if addr not in ADDRESSES:
        ADDRESSES.append(addr)
        client_socket.sendto("show-files",(addr, UDP_PORT))
    content = "FILES:"
    if OUR_FILES:
        for file_object in OUR_FILES:
            content += file_object.to_string() + ';'
        content = content[:-1]  # Remove the last ;
        check_our = False
    if PEERS_FILES:
        for file_object in PEERS_FILES:
            content += file_object.to_string() + ';'
        content = content[:-1]
        check_peers = False
    elif check_peers and check_our:
        content += "None"
    client_socket.sendto(content, (addr, UDP_PORT))



def get_files_list(data):
    """
    Gets response of show-files, and creates the File Info objects

    """
    list_of_files = data[6:]
    if list_of_files != "None":
        list_of_files = list_of_files.split(';')
        for file_object in list_of_files:
            file_info_after_base64 = file_object.decode("base64")
            file_info_object = decrypt_file(file_info_after_base64)
            file_info_object.print_file_info()
            PEERS_FILES.append(file_info_object)



def UDP_listen():
    """
    This function listens for incoming UDP packets
    It will be run a new thread
    """
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_socket.bind(("0.0.0.0", UDP_PORT))
    content = ''
    while True:
        rlist, wlist, xlist = select.select([new_socket], [new_socket], [])
        for read_socket in rlist:
            data, addr = new_socket.recvfrom(BUFFER_SIZE)
            addr = addr[0]
            debug_print("Received this data " + data + " from " + addr)

            if data == "Hello":
                new_connection(addr)

            elif data == "show-files":
                send_files_list(addr)

            elif data.startswith("FILES:"):
                get_files_list(data)

            elif data.startswith("PARTCHECK;"):


        if msvcrt.kbhit():
            key = msvcrt.getch()
            # if user hit enter key
            if key == chr(13):
                sys.stdout.write('\n')
                msg = request_part(content)
                send_msg_to_all(msg, new_socket)
                content = ''
            elif key == chr(127) or key == chr(8):
                content = content[:-1]
                sys.stdout.write("\b")
            else:
                content += key
                sys.stdout.write(key)


def print_addresses():
    print("Addresses:\n\t" + "\n\t".join(ADDRESSES))


def ask_for_files():
    for addr in ADDRESSES:
        client_socket.sendto("show-files", (addr, UDP_PORT))


def debug_print(data):
    print data


def is_ip(ip):
    """
    Returns True if the provided ip is an IP
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def add_addresses(data):
    if data != 'None':
        for address in data.split(';'):
            if address != socket.gethostbyname(socket.gethostname()) and address not in ADDRESSES and is_ip(address):
                ADDRESSES.append(address)
        if ADDRESSES:
            print_addresses()
    else:
        debug_print("We didn't receive any addresses")


def connect_to_server():
    global ADDRESSES, addr
    connected = False  # While we aren't connected to any server
    new_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_listen_socket.bind(("0.0.0.0", UDP_PORT))
    while not connected:
        try:
            new_listen_socket.sendto("Hello", (addr, UDP_PORT))
        except:
            pass
        rlist = select.select([new_listen_socket], [], [], TIMEOUT)
        if rlist[0]:
            # The server responded
            data, address = new_listen_socket.recvfrom(BUFFER_SIZE)
            address = address[0]  # address was a tuple of address and port
            if address == addr:
                debug_print("Connected to " + ("Main Server" if addr == SERVER_IP else addr))
                debug_print("We received " + data + " from " + ("Main server" if addr == SERVER_IP else addr))
                add_addresses(data)
                if addr not in ADDRESSES and addr != SERVER_IP:
                    ADDRESSES.append(addr)
                connected = True
        else:
            addr = raw_input("Could not connect to the IP " + addr + "\nPlease write another IP\n")
    new_listen_socket.close()


def receive_name():
    content = ''
    future_send = False
    while not future_send:
        # if user hit a key
        if msvcrt.kbhit():
            key = msvcrt.getch()
            content += key
            # if user hit enter key
            if key == chr(13):
                future_send = True
                sys.stdout.write('\n')
            if key == chr(127) or key == chr(8):
                content = content[:-1]
                sys.stdout.write("\b")
            else:
                sys.stdout.write(key)
    return content


def downloader():
    downloader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    downloader_socket.bind(('0.0.0.0', DOWNLOAD_PORT))


def request_part(name):
    file_requested = find_file_list_name(name, OUR_FILES)
    final_msg = None
    if file_requested:
        final_msg = "PARTCHECK;" + name + ";" + file_requested.get_hash()

    return final_msg



def find_file_list_name(name, list_search):
    for my_file in list_search:
        if my_file.get_name() == name:
            return my_file
    return None


def find_file_list_hash(hash, list_search):
    for my_file in list_search:
        if my_file.get_hash() == hash:
            return my_file
    return None


def handle_part_request(name, hash):
    requested_file = find_file_list(hash, OUR_FILES)
    if requested_file:
        # Send which parts we have
    else:
        # Send we have no parts



if __name__ == '__main__':
    initialize()
    connect_to_server()
    UDP_listener()
    ask_for_files()
