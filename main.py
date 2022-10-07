from random import randint
from pickle import *

class Game:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.walls = []
        self.nb_players = 0

    def add_wall(self, position):
        self.walls.append(position)

    def add_player(self, player):
        self.nb_players += 1
        if self.nb_players == 1:
            self.player1 = player
        elif self.nb_players == 2:
            self.player2 = player

    def is_in_map(self, position):
        if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size:
            return True
        else:
            return False

    def is_wall(self, position):
        if position in self.walls:
            return True
        else:
            return False

    def is_player(self, position):
        if position == self.player1.position or position == self.player2.position:
            return True
        else:
            return False

    def draw(self):
        board = []
        for i in range(0, self.board_size):
            board.append([])

        for sublist in board:
            for i in range(0, self.board_size):
                sublist.append("*")

        for wall in self.walls:
            board[wall[0]][wall[1]] = "#"

        board[self.player1.position[0]][self.player1.position[1]] = "1"
        board[self.player2.position[0]][self.player2.position[1]] = "2"

        for line in board:
            for case in line:
                print(case, end=" ")
            print()

    def randomchoice(self, number):
        if number == 0:
            r = randint(self.player2.position[0] - 1, self.player2.position[0] + 1)
            if r < 0:
                r = 0
            elif r > 9:
                r =9
            r1 = randint(self.player2.position[1] - 1, self.player2.position[1] + 1)
            if r1 < 0:
                r1 = 0
            elif r1 > 9:
                r1 = 9
            while r == self.player2.position[0]:
                r = randint(self.player2.position[0] - 1, self.player2.position[0] + 1)
                if r < 0:
                    r = 0
                elif r > 9:
                    r = 9
            return r, r1
        elif number == 1:
            randomwallx = randint(0, 9)
            randomwally = randint(0, 9)
            return randomwallx, randomwally

    def clear_wall(self):
        num_wall = randint(0, 10)
        if num_wall == 2:
            self.walls = []
            print("All wall(s) just disappeared !")


    def save(self):
        f = open("file save.txt", "wb")
        dump(self.player1.name, f)
        dump(self.player2.name, f)
        dump(self.player1.position, f)
        dump(self.player2.position, f)
        dump(self.walls, f)
        f.close()

    def play(self, typeplay):
        if typeplay == "1":
            while not self.player1.is_winner() and not self.player2.is_winner():
                self.draw()
                print("It is your turn", self.player1.name, "!")
                self.player1.play()
                if self.player1.is_winner():
                    print("you won", self.player1.name)
                    exit()
                self.clear_wall()
                print(30 * "\n")
                self.draw()
                print("It is your turn", self.player2.name, "!")
                self.player2.play()
                if self.player2.is_winner():
                    print("you won", self.player2.name)
                    exit()
                self.clear_wall()
                print(30 * "\n")
        elif typeplay == "2":
            while not self.player1.is_winner() and not self.player2.is_winner():
                self.draw()
                print("It is your turn", self.player1.name, "!")
                self.player1.play()
                if self.player1.is_winner():
                    print("you won", self.player1.name)
                    exit()
                self.clear_wall()
                print(30 * "\n")
                self.draw()
                print("It is your turn", self.player2.name, "!")
                randomrange = randint(0, 1)
                self.player2.playai(self.randomchoice(randomrange), randomrange)
                print(self.player2.position)
                self.clear_wall()
                if self.player2.is_winner():
                    print("you won", self.player2.name)
                    exit()
                print(30 * "\n")

class Player:
    def __init__(self, name, game, start):
        self.name = name
        self.game = game
        self.position = start
        self.start = start
        self.game.add_player(self)

    def move(self, position):
        if self.game.is_wall(position) or self.game.is_player(position) or not self.game.is_in_map(position):
            print("cannot go to that place")
            return False
        else:
            print("Moved successfully")
            self.position = position
            return True

    def place_wall(self, position):
        if self.game.is_wall(position) or self.game.is_player(position) or not self.game.is_in_map(position):
            print("cannot be placed")
            return False
        else:
            print("The wall has been placed !")
            self.game.add_wall(position)
            return True

    def is_winner(self):
        if self.start == (0, 5) and self.position[0] == 9:  # player1
            return True
        elif self.start == (9, 5) and self.position[0] == 0:  # player2
            return True
        else:
            return False

    def play(self):
        choice = input("Do you want to place a wall, move or save the game? (W/M/S) : ").lower()
        while choice != "w" and choice != "m" and choice != "s":
            choice = input("Do you want to place a wall or move (W/M) : ").lower()
        if choice == "w":
            tup1 = int(input("Enter a position (x) : "))
            tup2 = int(input("Enter a position (y) : "))
            position = (tup1, tup2)
            while not self.place_wall(position):
                tup1 = int(input("Enter a position (x) : "))
                tup2 = int(input("Enter a position (y) : "))
                position = (tup1, tup2)
        elif choice == "m":
            print("to go up on the board : a")
            print("to move on the right : b")
            print("to move on the left : c")
            print("to go down on the board : d")
            moveit = input("Enter the position that you want to go : ").lower()
            position1 = self.position[0]
            position2 = self.position[1]
            if moveit == "a":
                position1 -= 1
            elif moveit == "b":
                position2 += 1
            elif moveit == "c":
                position2 -= 1
            elif moveit == "d":
                position1 += 1
            position = (position1, position2)
            while not self.move(position):
                print("to move forward : a")
                print("to move on the right : b")
                print("to move on the left : c")
                print("to go down on the board : d")
                moveit = input("Enter the position that you want to go : ").lower()
                position1 = self.position[0]
                position2 = self.position[1]
                if moveit == "a":
                    position1 -= 1
                elif moveit == "b":
                    position2 += 1
                elif moveit == "c":
                    position2 -= 1
                elif moveit == "d":
                    position1 += 1
                position = (position1, position2)
        elif choice == "s":
            self.game.save()
            exit()



    def playai(self, x, randomrange):
        if randomrange == 0:
            val1 = x[0]
            val2 = x[1]
            if x in self.game.walls:
                val1 += 1
                x = (val1, val2)
            self.move(x)
        elif randomrange == 1:
            self.place_wall(x)


def main():
    print("projet created by Ugo Dasseleer")
    print("1 for a 2 player game")
    print("2 for an AI")
    print("3 for loading last saved game")
    starter = str(input("do you want to play against an AI or a player ? "))
    while starter != "1" or starter != "2" or starter != "3":
        if starter == "1":
            player1_name = input("Player 1, Enter your name : ")
            player2_name = input("Player 2, Enter your name : ")
            my_game = Game()
            Player(player1_name, my_game, (0, 5))
            Player(player2_name, my_game, (9, 5))
            my_game.play(starter)
        elif starter == "2":
            player1_name = input("Player 1, Enter your name : ")
            my_game = Game()
            Player(player1_name, my_game, (0, 5))
            Player("Robotus", my_game, (9, 5))
            my_game.play(starter)
        elif starter == "3":
            f = open("file save.txt", "rb")
            player1_name = load(f)
            player2_name = load(f)
            my_game = Game()
            Player(player1_name, my_game, load(f))
            Player(player2_name, my_game, load(f))
            my_game.walls = load(f)
            print("game loaded")
            if player2_name == "Robotus":
                my_game.play("2")
            else:
                my_game.play("1")
        else:
            starter = str(input("do you want to play against an AI or a player ? Maybe loading the last game? "))


if __name__ == "__main__":
    main()
