from time import sleep
from sys import exit
from subprocess import run
import pkg_resources

def check_packages_installed():
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    return "wonderwords" in installed_packages

if not check_packages_installed():
    choice = input("This program requires the wonderwords module, Would you like to install it? [Y/n] ").lower()
    if choice == "y":
        run(["pip", "install", "wonderwords"])
        print("\n")
    else:
        exit()

from wonderwords import RandomSentence as rs

hangman_string = """
_________
I       I
I       I
I       O
I      /|\\
I      /2 \\2
I
I
"""

class Game:
    misses = 0
    sentence = rs().bare_bone_sentence().lower().replace(".", "")
    displayed_characters = []
    tries_dict = {1: "O", 2: "|", 3: "/", 4: "\\", 5: "/2", 6: " \\2"}
    letter_bank = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    game_won = False

    def __init__(self):
        self.guess_str = self.sentence
        for i in range(len(self.sentence)):
            if self.sentence[i] in self.alphabet:
                self.guess_str = self.guess_str[:i] + "_" + self.guess_str[i+1:]


    def display_hangman(self):
        for line in hangman_string.split("\n"):
            for char in self.tries_dict.values():
                if char in line and char not in self.displayed_characters:
                    line = line.replace(char, " ")
            if "2" in line:
                line = line.replace("2", "")
            if line.startswith("_"):
                line = f"{line}\t\t\tLetters Used: {', '.join(self.letter_bank)}"
            print(line)

    def is_valid_guess(self, guess):
        for char in guess.lower():
            if char not in self.alphabet and not char == " ":
                print("Please use phrases uses only letters and spaces")
                sleep(1)
                return False
        if len(guess) == 1 and guess in self.letter_bank:
            print(f"Already Guessed {guess}")
            sleep(1)
            return False
        
        return True
    
    def check_guess(self, guess):
        if len(guess) == 1:
            self.letter_bank.append(guess)
            return guess in self.sentence
        return guess == self.sentence

    def guess_correct(self, guess):
        if len(guess) == 1:
            for i in range(len(self.sentence)):
                if self.sentence[i] == guess:
                    self.guess_str = self.guess_str[:i] + guess + self.guess_str[i+1:]
                    if self.guess_str == self.sentence:
                        self.win_game()
            return
        self.guess_str = self.sentence
        self.win_game()


    def win_game(self):
        self.game_won = True
        self.display_hangman()
        print(self.guess_str, end="\n\n")
        print("You Won!")

    def start_game(self):
        while self.misses < 6 and not self.game_won:
            self.display_hangman()
            print(self.guess_str, end="\n\n")
            user_guess = input("Your Guess: ").lower()
            if not self.is_valid_guess(user_guess):
                continue
            if not self.check_guess(user_guess):
                self.misses += 1
                self.displayed_characters.append(self.tries_dict[self.misses])
                if self.misses == 6:
                    self.display_hangman()
                    print(f"Game Over, the phrase was {self.sentence}")
                    sleep(1)
            else:
                self.guess_correct(user_guess)
    

    

Game().start_game()
