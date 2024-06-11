import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f'{nickname} left the chat!'.encode('ascii'))
        nicknames.remove(nickname)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
                display_message_server(message.decode('ascii'))
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def receive():
    while True:
        client, address = server_socket.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def display_message_server(message):
    text_area_server.config(state=tk.NORMAL)
    text_area_server.insert(tk.END, message + '\n')
    text_area_server.yview(tk.END)
    text_area_server.config(state=tk.DISABLED)

def send_message_server():
    message = f'Server: {msg_entry_server.get()}'
    broadcast(message.encode('ascii'))
    display_message_server(message)
    msg_entry_server.delete(0, tk.END)

def start_server_gui():
    global text_area_server, msg_entry_server

    window = tk.Tk()
    window.title("Chat Server")

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)
    text_area_server = scrolledtext.ScrolledText(master=frm_messages, wrap=tk.WORD, state=tk.DISABLED)
    text_area_server.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    frm_messages.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

    frm_entry = tk.Frame(master=window)
    msg_entry_server = tk.Entry(master=frm_entry, width=80)
    msg_entry_server.pack(side=tk.LEFT, padx=10, pady=10)
    send_button = tk.Button(master=frm_entry, text="Send", command=send_message_server)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)
    frm_entry.pack(padx=20, pady=5)

    window.mainloop()

def start_server():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print('Server is listening...')

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    start_server_gui()

def start_client():
    nickname = simpledialog.askstring("Nickname", "Choose your nickname:")
    if not nickname:
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
        return

    def receive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    text_area_client.config(state=tk.NORMAL)
                    text_area_client.insert(tk.END, message + '\n')
                    text_area_client.yview(tk.END)
                    text_area_client.config(state=tk.DISABLED)
            except Exception as e:
                print(f"An error occurred: {e}")
                client.close()
                break

    def write():
        message = f'{nickname}: {msg_entry_client.get()}'
        try:
            client.send(message.encode('ascii'))
        except Exception as e:
            print(f"Failed to send message: {e}")
        msg_entry_client.delete(0, tk.END)

    window = tk.Tk()
    window.title("Chat Client")

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)
    global text_area_client
    text_area_client = scrolledtext.ScrolledText(master=frm_messages, wrap=tk.WORD, state=tk.DISABLED)
    text_area_client.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    frm_messages.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

    frm_entry = tk.Frame(master=window)
    global msg_entry_client
    msg_entry_client = tk.Entry(master=frm_entry, width=80)
    msg_entry_client.pack(side=tk.LEFT, padx=10, pady=10)
    send_button = tk.Button(master=frm_entry, text="Send", command=write)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)
    frm_entry.pack(padx=20, pady=5)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    mode = simpledialog.askstring("Mode", "Enter 'server' to start as server or 'client' to start as client:")
    if mode == 'server':
        start_server()
    elif mode == 'client':
        start_client()
    else:
        messagebox.showerror("Invalid Mode", "Please enter 'server' or 'client'")
        root.destroy()