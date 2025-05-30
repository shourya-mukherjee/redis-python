import socket  # noqa: F401
import threading

def handle_client(connection):
    try:
        while True:
            print("Waiting for data")
            data = connection.recv(1024)
            print(f"Received data: {data}")
            if not data:  # Connection closed by client
                print("Connection closed by client")
                break
            connection.sendall(b"+PONG\r\n")
            print("Sent PONG response")
    finally:
        connection.close()
        print("Connection closed")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        print("Waiting for new connection")
        connection, _ = server_socket.accept()
        print("New connection accepted")
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()
        print("Started new thread for client connection")

if __name__ == "__main__":
    main()
