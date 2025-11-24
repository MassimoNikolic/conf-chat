from p2pnetwork.node import Node
from p2pnetwork.nodeconnection import NodeConnection

import json
import os

global RUNNING
RUNNING = True

class MyOwnNodeConnection (NodeConnection):
    
    def __init__(self, main_node, sock, id, host, port):
        super(MyOwnNodeConnection, self).__init__(main_node, sock, id, host, port)

class MyOwnPeer2PeerNode (Node):

    def __init__(self, host, port, id=None, username=None):
        self.username = username

        super(MyOwnPeer2PeerNode, self).__init__(host, port, id)

    # def all_nodes():
    #     return self.nodes_outbound + self.nodes_inbound

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, node, data):
        print(f"<{node.username.upper()}> " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def create_new_connection(self, connection, id, host, port):
        return MyOwnNodeConnection(self, connection, id, host, port)

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.friends_list = {}

    def add_friend(self, friend_username):
        if friend_username in self.friends_list:
            print("Friend already in friends list.")
        else:
            self.friends_list[friend_username] = {}
            print("Friend added successfully.")
            self.save_friends_data()

    def print_friends_list(self):
        print("Friends List:")
        for friend in self.friends_list:
            print(f"- {friend}")

class AccountManager:
    def __init__(self):
        self.accounts = []
        self.data_loaded = False
    
    def get_account_data(self):
        try:
            with open('account_data.json', 'r') as f:
                account_data = json.load(f)
                for username, password in account_data.items():
                    self.accounts.append(Account(username, password))
            self.data_loaded = True
        except FileNotFoundError:
            pass

    def save_account_data(self):
        # Save Account Data #

        with open('account_data.json', 'w') as f:
            account_data = {account.username: account.password for account in self.accounts}
            json.dump(account_data, f)

    def add_account(self, username, password):
        if username in self.accounts:
            print("Account already exists.")
        elif username == "" or password == "":
            print("Username and password cannot be empty.")
        else:
            self.accounts.append(Account(username, password))
            print("Account created successfully.")

    def account_exists(self, username):
        for account in self.accounts:
            if account.username == username:
                return True
        return False
    
    def login_is_valid(self, input_username, input_password):
        for account in self.accounts:
            if account.username == input_username and account.password == input_password:
                print("Login successful.")
                return True
        print("Invalid username or password.")
        return False
    
    def save_friends_data(self):
        with open('friend_data.json', 'w') as f:
            friend_data = {account.username: account.friends_list for account in self.accounts}
            json.dump(friend_data, f)

    def load_friends_data(self, username):
        try:
            with open((f'{self.accounts[username]}_friend_data.json'), 'r') as f:
                self.friends_list = json.load(f)
        except FileNotFoundError:
            pass
    
# Account Registration and Login Functions #

def register_account(account_manager):
    print("Registering user account...")
    username = ""
    while username == "":
        username = input("Enter your username: ")
        if account_manager.account_exists(username):
            print("Username already exists. Please try again.")
            username = ""
    
    password = ""
    while password == "":    
        password = input("Enter your password: ")
        if len(password) < 8:
            print("Password must be at least 8 characters long. Please try again.")
            password = ""
    
    account_manager.add_account(username, password)
    account_manager.save_account_data()

    os.system('clear || cls') 

def login_account(account_manager):
    print("Logging in user account...")
    username = ""
    while username == "":
        username = input("Enter your username: ")
        if not account_manager.account_exists(username):
            print("Username does not exist. Please register first or enter a correct username.")
            username = ""

    password = ""
    while password == "":
        password = input("Enter your password: ")
        if not account_manager.login_is_valid(username, password):
            print("Incorrect password. Please try again.")
            password = ""
        else:
            print("Login successful.")
            return (username, password)

# Load Peer Data #        

def load_peer_data():
    peer_data = {}
    try:
        with open('peer_data.json', 'r') as f:
            peer_data = json.load(f)
    except FileNotFoundError:
        pass
    return peer_data

peer_data = load_peer_data()
        
# Chatting Functions #
        
def connect_to_friend(node, friend_host, friend_port):
    node.connect_with_node(friend_host, friend_port)

def chat_with_friend(node, friend_name, friend_host, friend_port):
    # os.system('clear || cls')
    # message = ""
    # friend_node = node.
    # print(f"Talking with {friend_name}. Type '/exit' to end the chat.")
    # while message.lower() != "/exit":
    #     message = input("You: ")
    #     if message.lower() != "/exit":
    #         node.send_to_node(friend_node, message)
    #         print("<YOU> " + message)

    # os.system('clear || cls') 
    os.system('clear || cls')
    message = ""
    print(f"Chatting with {friend_name}. Type '/exit' to end the chat.")

    # Build the expected peer id
    target_id = f"{friend_host}:{friend_port}"

    while message.lower() != "/exit":
        message = input("You: ")

        if message.lower() != "/exit":
            # Find the connected peer with that ID
            for peer in node.all_nodes:
                if peer.id == target_id:
                    node.send_to_node(peer, message)
                    break
            else:
                print("Friend did not receive message.")

            print("<YOU> " + message)

    os.system('clear || cls')

os.system('clear || cls')

account_manager = AccountManager()
account_manager.get_account_data()

prompt_answer = input("Are you a new user? (Y/N): ")

# Registration and Login #

while prompt_answer.lower() != 'y' and prompt_answer.lower() != 'n':
    print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
    prompt_answer = input("Are you a new user? (Y/N): ")

if prompt_answer.lower() == 'y':
    register_account(account_manager)
    username, password = login_account(account_manager)
    
elif prompt_answer.lower() == 'n':
    username, password = login_account(account_manager)

# Main Code #

user_node = MyOwnPeer2PeerNode(peer_data[username][0], peer_data[username][1], username=username)
user_node.start()

# account_manager.accounts[username].load_friends_data()

while RUNNING:
    try:
        command = input("Enter command (type '/help' for options): ")
        
        if command == "/help":
            print("Available commands:")
            print("  /help - Show this help message")
            print("  /connect - Connect with a friend")
            print("  /friends - Show friends list")
            print("  /exit - Exit the program")
        
        elif command == "/exit":
            print("Exiting program...")
            RUNNING = False

        elif command == "/connect":
            friend_name = ""
            friend_port = -1

            while friend_name == "":
                friend_name = input("Enter friend's username: ")
                if friend_name not in peer_data:
                    print("Invalid host username. Try again.")
                    friend_name = ""

            friend_host = peer_data[friend_name][0]
            friend_port = peer_data[friend_name][1]

            connect_to_friend(user_node, friend_host, friend_port)
            print(f"Connecting to {friend_name} at {friend_host}:{friend_port}...")

            chat_with_friend(user_node, friend_name, friend_host, friend_port)

        # elif command == "/friends":
        #     account_manager.accounts[username].print_friends_list()
        
        else:
            print("Unknown command. Type 'help' for a list of commands.")
    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting program...")
        RUNNING = False

user_node.stop()