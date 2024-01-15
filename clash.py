import clash_install # must be first to install dependencies
from clash_api import ClashAPI
from clash_encryption import decrypt
import configparser
from getpass import getpass
import os
import pretty_errors
import webbrowser

def main():
    # Clear the terminal
    _ = os.system('cls')

    config = configparser.ConfigParser()
    config.read("clash.ini")
    player_tag = config["Clash"]["player_tag"]
    encrypted_key = config["Clash"]["encrypted_key"]
    song_url = config["Clash"]["song_url"]

    print_header()

    play_song = input("Do you want to play the Clash Royale theme song? (y/n): ")
    if play_song.lower() == "y":
        webbrowser.open(song_url)
    print()

    api_key = get_api_key(encrypted_key)
    api = ClashAPI(api_key)

    print(f"Getting player #{player_tag}...")
    player = api.get_player(player_tag)
    win_rate = round(player.wins / (player.wins + player.losses) * 100)
    print(f"{player.name} has a {win_rate}% win rate.")
    print()

def print_header():
    print(r"  ____ _           _     _      _    _          _               _     _ _ _ ")
    print(r" / ___| | __ _ ___| |__ | |    / \  | |__      / \   __ _  __ _| |__ | | | |")
    print(r"| |   | |/ _` / __| '_ \| |   / _ \ | '_ \    / _ \ / _` |/ _` | '_ \| | | |")
    print(r"| |___| | (_| \__ \ | | |_|  / ___ \| | | |  / ___ \ (_| | (_| | | | |_|_|_|")
    print(r" \____|_|\__,_|___/_| |_(_) /_/   \_\_| |_| /_/   \_\__,_|\__,_|_| |_(_|_|_)")
    print()

def get_api_key(encrypted_key):
    print("Enter the password to decrypt your Clash Royale API key: ")
    try:
        while True:
            password = getpass()
            try:
                return decrypt(encrypted_key, password)
            except Exception as e:
                print("Incorrect password, please try again.")
    finally:
        print()

if __name__=="__main__":
    main()