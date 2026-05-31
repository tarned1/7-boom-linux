#############################
# made by: Melody
# description: Simple 7-boom game for linux terminal
# date: 31 may 2026
############################

###########Imports#############
import sys
import termios
import tty
from dataclasses import dataclass

##########Class###############
@dataclass
class Player:
    boom: str
    num: str

############Functions############
def getch():
    """Gets a single character from sys.stdin.
    :return str: The key input character."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def is_boom_number(number: int) -> bool:
    """Checks if a number contains 7 or divides by 7.
    :arg number: The number to check.
    :type number: integer.
    :return bool: True if the number contains 7 or divided by 7, otherwise False."""
    return "7" in str(number) or number%7==0

def handle_turn(player: Player, player_input: str, number: int) -> tuple[bool, int]:
    """Handles a player's turn in the game.
    :arg player: The current player playing.
    :type player: Player
    :arg player_input: The input of the current player.
    :type player_input: str
    :arg number: The current number in the game.
    :type number: int
    :return: True if it's the correct input, otherwise False. Returns the next number too if correct."""
    if is_boom_number(number):
        if player.boom == player_input: #if the player pressed boom in time
            print("Boom!", end=" ", flush=True)
            return True, number + 1
        else:
            return False, number
    else:
        if player_input == player.num: #if the player pressed number in time
            print(number, end=" ", flush=True)
            return True, number + 1
        else:
            return False, number

def get_player_input(player: Player) -> str:
    """Gets and checks the input of the current player.
    :arg player: The current player playing.
    :type player: Player
    :return str: The input of the current player."""
    answer = getch().lower()
    chosen_one = player.boom + player.num
    while len(answer) != 1 or answer not in chosen_one: #checks if it's the key of the current player
        answer = getch().lower()

    return answer

def single_player_game():
    """7 boom Game with only 1 player"""
    number = 1 #the first number

    #gets the keys the players chooses for boom and number
    boom = get_unique_key([], "boom")
    num = get_unique_key([], "number", boom)

    player = Player(boom, num)

    print("andd.... START!!")

    while True: #while the input isn't incorrect
        player_input = get_player_input(player)

        correct, number = handle_turn(player, player_input, number)
        if not correct:
            break

    print("Amazing! you got to the number ", number, "! That's very impressive!", sep="")

def is_key_available(players: list[Player], key: str) -> bool:
    """Checks if a key wasn't used by any other player.
    :arg players: All players who already chosen their keys
    :type players: list[Player]
    :arg key: The key the current player chose.
    :type key: str
    :return bool: True if it wasn't used, otherwise False."""
    return all(player.boom != key and player.num != key for player in players)

def get_unique_key(players: list[Player], text: str, forbidden_key: str | None = None) -> str:
    """Gets a key from the current player and checks if it wasn't used before by the player or other users.
    :arg players: All players who already chosen their keys
    :type players: list[Player]
    :arg text: The key type the current player chose, boom or number.
    :type text: str
    :forbidden_key: If was chosen, the key player chosen for boom.
    :type forbidden_key: str | None
    :return str: The chosen key by the current player."""
    while True:
        print(f"enter a key for {text}: ", end="", flush=True)
        key = getch().lower()
        print(key)

        if key != forbidden_key and is_key_available(players, key):#checks if the key was used by the player or other players
            return key

def multi_player_game(player_count: int):
    """7 boom Game with multiple players.
    :arg player_count: The number of players."""
    players = []
    number = 1
    turn = 0

    for i in range(player_count): #all players choose their keys
        print(f"player {i + 1}:", flush=True)
        boom_key = get_unique_key(players, "boom")
        num_key = get_unique_key(players, "number", boom_key)
        players.append(Player(boom_key, num_key))
    print("----------------------------------")

    while True:
        current_player = players[turn]
        key = get_player_input(current_player)

        correct, number = handle_turn(current_player, key, number)
        if not correct:
            break

        turn = (turn + 1) % player_count

    print("Player number", turn + 1, "lost the game!")

def main():
    """The main for the 7-boom game."""
    player_num = input("With how many players do you want to play? ")
    while not player_num.isnumeric() or int(player_num) < 1:
        player_num = input("With how many players do you want to play? ")

    player_num = int(player_num)

    if player_num == 1:
        single_player_game()
    else:
        multi_player_game(player_num)

if __name__ == "__main__":
    main()