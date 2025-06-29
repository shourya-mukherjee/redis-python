import socket  # noqa: F401
import threading
from .serializer import Serializer

OK = b"+OK\r\n"
PONG = b"+PONG\r\n"
NULL = b"$-1\r\n"

serializer = Serializer()

def handle_client(connection):
    h = {}
    try:
        while True:
            print("Waiting for data")
            data = connection.recv(1024)
            print(f"Received data: {data}")
            if not data:  # Connection closed by client
                print("Connection closed by client")
                break
            d_arr = serializer.decode(data)
            if d_arr:
                command = d_arr[0].upper()
                if command == 'ECHO':
                    ret = serializer.encode(d_arr[1:])
                    connection.sendall(ret)
                    print('Sent echo response')
                elif command == 'PING':
                    connection.sendall(PONG)
                    print('Sent pong response')
                elif command == 'SET':
                    try:
                        key, value = d_arr[1], d_arr[2]
                    except IndexError:
                        print("SET command requires 2 arguments")
                        connection.sendall(NULL)
                        continue
                    h[key] = value
                    connection.sendall(OK)
                    print(f"SET {key} {value}")
                elif command == 'GET':
                    try:
                        key = d_arr[1]
                    except IndexError:
                        print("GET command requires 1 argument")
                        connection.sendall(NULL)
                        continue
                    value = h.get(key)
                    if value:
                        ret = serializer.encode([value])
                        connection.sendall(ret)
                    else:
                        connection.sendall(NULL)
                else:
                    connection.sendall(NULL)
            else:
                connection.sendall(NULL)
    finally:
        connection.close()
        print("Connection closed")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    active_threads = []
    
    try:
        while True:
            print("Waiting for new connection")
            connection, _ = server_socket.accept()
            print("New connection accepted")
            
            # Create daemon thread so it doesn't prevent program exit
            client_thread = threading.Thread(target=handle_client, args=(connection,), daemon=True)
            client_thread.start()
            active_threads.append(client_thread)
            print("Started new thread for client connection")
            
            # Clean up finished threads
            active_threads = [thread for thread in active_threads if thread.is_alive()]
            print(f"Active threads: {len(active_threads)}")
    except KeyboardInterrupt:
        print("Shutting down server...")
        server_socket.close()
        # Wait for all threads to finish (with timeout)
        for thread in active_threads:
            thread.join(timeout=1.0)
        print("Server shutdown complete")

if __name__ == "__main__":
    main()
