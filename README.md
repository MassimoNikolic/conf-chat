# Conf-Chat
Developed by Massimo Nikolic

# Installations

This chat application is primarily made with the p2pnetwork python library, so install it with "pip install p2pnetwork". It also uses the json python library to use and retain user and peer data.

# How to Run

To start, open a terminal and run the conf_chat.py file. You will be asked if you are a new user. Input "Y" to register a new account with a username and password before logging in, and input "N" to skip to the login prompt.  Do note that registration currently does not account for if your new username already exists in the system. The password also requires a minimum of 8 characters

After a successful login, the program makes a new p2pnetwork Node object for you to use for network communication. You will be sent to the command prompt section where you can enter commands like /help, /connect, and /exit. 

Note: there is a /friends command to bring up your friends list, but it is not fully implemented yet. For now, look into the peer_data json to find usernames.

# Command: /help

Use this command to print the possible commands you can use.

# Command: /connect

Entering this command to start a 1-to-1 conversation with a friend. You will be prompted to enter your friend's username. Entering a valid username will initiate the chat.

Here, you can send messages like you are in a terminal-based chatroom with your friend.
Note: Currently, messages do not print on both ends of the conversation; to be implemented.

Typing /exit will exit the conversation

# Command: /exit

Entering this command will close the application.

# TODO:

- Implement /friends command
- Implement commmand for adding friends
- Include more robust exiting and prompt validation.

