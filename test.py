import socket
import concurrent.futures
import sys
import getopt
import time

argvs = sys.argv[1:]
global host
global start_port 
global end_port 


try:
    opts, args = getopt.getopt(argvs, "t:s:e:", ["target=", "start="])
    for opt, arg in opts:
        if opt in ("-t", "--target"):
            host = str(arg)
        elif opt in ("-s", "--start"):
            start_port = int(arg)
        elif opt in ("-e", "--end"):
            end_port = int(arg)
except getopt.error as err:
    print("\n[*] "+str(err)+"\n\n[*] example:\n\t    python [filename] -t [target_ip] -r [starting port range] -n [ending port range]")
    sys.exit()
    
def check_port(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to avoid hanging indefinitely
        sock.settimeout(.6)
       
        # Attempt to connect to the host and port
        result = sock.connect_ex((host, port))
        # Check if the connection was successful
        if result == 0:
            print(f"[*] TCP/Port {port} is open")
        # Close the socket
        sock.close()
    except socket.error as err:
        print("[*] Socket error \n"+str(err))
        sys.exit()
        

def scan_ports(host, start_port, end_port):
    start_time = time.perf_counter() #clock start
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Map port scanning to the executor
        futures = {executor.submit(check_port, host, port): port for port in range(start_port, end_port + 1)}
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
        stop_time = time.perf_counter()#clock stop
        print("*****************************************************************\n""_____________________scanning_Complete!__in_%f_Seconds_________"
          "\n*****************************************************************\n" % (stop_time-start_time))

def main():
    print("_____________________scanning_by_deeta_hantaa___________________"
          "\n*****************************************************************")
    try:
        scan_ports(host, start_port, end_port)
    except:
        print("\n! empty credential\n")
        print("\n\n[*] example:\n\t    python [filename] -t [target_ip] -s [starting port range] -e [ending port range]")

if __name__ == "__main__":
    main()
