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
