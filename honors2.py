import random

###########################################################
#  Honors Project #2
#
#  Algorithm
#    prompt for number of games to be played after the first demo-game
#    input an integer
#    prompt for valid x and y sizes of game board
#    input 2 integers
#    prompt for int seed for RNG
#    input an integer
#       
#    Create Game object containing different functions of play and player objects
#    
#    Call single_play function
#       Create empty Board object
#       Obtain list of valid moves
#       Obtain list of boxes
#       loop twice       
#           loop while board not full
#               Random player goes first game 1 and smart player goes first game 2.
#               Player objects swap turns
#                   Random Player will always pick a random, valid move
#                   Winning Player will always complete a box if a box is 3/4 moves to completion
#                       If no move presents itself, the Winning Player will pick a random, valid move
#               Update board accordingly
#               Display scores and board updates in text file
#               player repeats turn if box made
#           Display final score in text file
#    
#    Call multiple-Play function
#       loop until specified number of games completed
#           Create empty Board object
#           Obtain list of valid moves
#           Obtain list of boxes
#           loop while board not full
#               Player objects swap turns
#                   Random Player will always pick a random, valid move
#                   Winning Player will always complete a box if a box is 3/4 moves to completion
#                       If no move presents itself, the Winning Player will pick a random, valid move
#               Update board accordingly
#               Display scores and board updates in text file
#               player repeats turn if box made
#           record and reset scores
#       Display various data in text file
#    
#       Indicate functions have completed
###########################################################

"""
SampleBoard = [[0, =, 1, =, 2, =, 3],
              [+, X, +, X, +, X, +],
              [4, =, 5, =, 6, =, 7],
              [+, X, +, X, +, X, +],
              [8, =, 9, =, 10, =, 11],
              [+, X, +, X, +, X, +],
              [12, =, 13, =, 14, =, 15]]
"""
"""
"single_play.txt"
"multiple_play.txt"
"""

class Board:
    """
    Game Board object that holds a list version of the gameboard
    Can determine if a move between two given points is valid
    Capable of updating the gameboard to represent moves made.
    Can scan through the list to determine if the game has been won
    """
    #Default values to be used in creating/displaying board
    GameBoard = []
    filepath = open("single_play.txt", "w")
    
    def __init__(self, HSize = 3, VSize = 3, filepath = open("single_play.txt", "w")):
        """
        Creates the empty gameboard to be filled by the player classes

        Parameters
        ----------
        HSize : Int, optional
            Horizontal size of game board. The default is 3.
        VSize : int, optional
            Vertical size of game board. The default is 3.
        filepath : filepath, optional
            File to display gameboard information to. The default is open("single_play.txt", "w").

        Returns
        -------
        None.

        """
        self.GameBoard = []
        self.filepath = filepath
        
        count = 0
        #Creates Game Board
        for row in range(0, VSize):
            temp = []
            temp2 = []
            

            #Creates main rows consisting of nodes and empty horizontal lines
            for n in range(count, count + HSize):
                temp.append(str(n))
                if (n % HSize) != (HSize - 1):
                    temp.append("=")
                count += 1
            #Adds row to main gameboard        
            self.GameBoard.append(temp)
            
            #Creates the inbetween rows, consisting of vertical lines and centers of boxes
            if row != (VSize - 1):
                for n in range(0, HSize):
                    temp2.append("+")
                    if n != (HSize - 1):
                        temp2.append("X")
                #Adds row to main game board
                self.GameBoard.append(temp2)
                
    def __str__(self):
        """
        Returns the grid as a string representation

        Returns
        -------
        String representation of game board.

        """
        output = ""
        #For each row of the gameboar, creates a string that is added to the master output string
        for row in self.GameBoard:
            output = ""
            for space in row:
                if row.index(space) != (len(row) - 1):
                    output += ""
                else: 
                    output += space
            output += "\n"
        return(output)            
    
    def display_board(self):
        """
        Writes the board to the filepath provided in the __init__ function

        Returns
        -------
        None.

        """
        #Displays each space of the gameboard
        for row in self.GameBoard:
            for n in range(0,len(row)):
                #Determines if the space is "empty" and should not be displayed
                #Also determiens if space is last in row in order to add new line character
                if row[n] != "+" and row[n] != "=" and row[n] != "X":
                    if n != len(row)-1:
                        print("{thing:^3}".format(thing = row[n]), end = " ", file = self.filepath)
                    else:
                        print("{thing:^3}".format(thing = row[n]), file = self.filepath)
                else:
                    if n != len(row)-1:
                        print("{thing:^3}".format(thing = " "), end = " ", file = self.filepath)
                    else:
                        print("{thing:^3}".format(thing = " "), file = self.filepath)
            
    def check_for_box(self):
        """
        Searches the board for any posistions that have become boxes this turn

        Returns
        -------
        boxes : list
            List of coordinates where boxes have been created.

        """
        #Creates an empty list of boxes to add completed boxes to
        boxes = []
        for Line in range(0, len(self.GameBoard)):
            for space in range(0, len(self.GameBoard[Line])):
                #Checks to see if a potential box is unclaimed
                if self.GameBoard[Line][space] == "X":
                    #Checks to see if a potential box is surrounded by lines on all sides
                    check = self.GameBoard[Line-1][space] == "-"
                    check = check and self.GameBoard[Line][space+1] == "|"
                    check = check and self.GameBoard[Line+1][space] == "-"
                    check = check and self.GameBoard[Line][space-1] == "|"
                    if check:
                        #adds box to list if it meets all criteria
                        boxes.append([Line, space])
        return boxes
    
    def is_valid_move(self, start, end):
        """
        Checks if the move between the nodes provided is valid

        Parameters
        ----------
        start : int
            Starting node to draw a line from.
        end : int
            Ending node to draw a line to.

        Returns
        -------
        bool
            True if move is valid. False if invalid

        """
        #Creates empty variables
        cord1 = []
        cord2 = []
        #Finds the coordinates of the nodes provided
        for line in self.GameBoard:
            for space in line:
                if space.isdigit(): 
                    if int(space) == start:
                        cord1 = [self.GameBoard.index(line), line.index(space)]
                    if int(space) == end:
                        cord2 = [self.GameBoard.index(line), line.index(space)]
        
        
        #checks if cords occupy the same row and are close enough
        if cord1[0] == cord2[0] and abs(cord1[1] - cord2[1]) == 2:
            if self.GameBoard[cord1[0]][(cord1[1] + cord2[1])//2] == "=":
                return True
        #checks if the cords occupy the same column and are close enough
        elif  cord1[1] == cord2[1] and abs(cord1[0] - cord2[0]) == 2:
            if self.GameBoard[(cord1[0] + cord2[0])//2][cord1[1]] == "+":
                return True
        
        #If cords were not close enough or not in line with eachother, the moves invalid
        return False
                    
    def update_board(self,row, column, team = None):
        """
        Changes the board in the space provided

        Parameters
        ----------
        row : int
            Node to draw line from OR row to create box in.
        column : int
            Node to draw line to OR column to create box in.
        team : String, optional
            Player that filled in a box.  If provided, uses row&column to create a box. 
            The default is None, which tells the function to use row&column as nodes to draw a line between.

        Returns
        -------
        None.

        """
        #If team==None, the board is creating a line and treats parameters differently
        if team == None:
            #Creates empty coordinates
            cord1 = []
            cord2 = []
            for line in self.GameBoard:
                for space in line:
                    if space.isdigit():
                        #Finds coordinates of nodes provided
                        if int(space) == row:
                            cord1 = [self.GameBoard.index(line), line.index(space)]
                        if int(space) == column:
                            cord2 = [self.GameBoard.index(line), line.index(space)]
            
            #Checks if cords occupy same row to draw a horizontal line
            if cord1[0] == cord2[0] and abs(cord1[1] - cord2[1]) == 2:
                self.GameBoard[cord1[0]][(cord1[1] + cord2[1])//2] = "-"
            #checks if the cords occupy the same column to draw a vertical line 
            elif  cord1[1] == cord2[1] and abs(cord1[0] - cord2[0]) == 2:
                self.GameBoard[(cord1[0] + cord2[0])//2][cord1[1]] = "|"
            
        #If team is provided, then the board is creating a claimed box
        else:
            #Claims a box at the provided coordinate from list of boxes for current player
            self.GameBoard[row][column] = team
    
    def Win(self, default = "Random Player", display = False):
        """
        Determines there are no valid moves left.  If all moves have been taken,
        the program determines who won the game.

        Parameters
        ----------
        default : String, optional
            Tells the game which player should be declared the winner in the event of a tie.
            The default is the Random Player
        display : boolean, optional
            Tells the game if it should display the message declaring which player won. 
            The default is False.

        Returns
        -------
        bool
            Declares if all boxes are claimed(True) or if moves can be made(False).

        """
        #Creating variables
        Xcount = 0
        Acount = 0
        Bcount = 0
        
        #Determiens how many claimed and unclaimed boxes are present
        for line in self.GameBoard:
            for space in line:
                if space == "X":
                    Xcount += 1
                if space == "A":
                    Acount += 1
                if space == "B":
                    Bcount += 1
        
        #Displays results of individual game in single-play mode
        if display:            
            #Unclaimed Boxes stil exist and the game is not finished
            if Xcount != 0:
                return False
            #Player A has the most boxes and wins
            elif Acount > Bcount:
                print("A Wins", file = self.filepath)
                return True
            #Player B has the most boxes and wins
            elif Bcount > Acount:
                print("B Wins", file = self.filepath)
                return True
            #Players are tied for number of boxes
            elif Acount == Bcount:
                print(default,"Wins", file = self.filepath)
                return True
        else:
            #Unclaimed Boxes stil exist and the game is not finished
            if Xcount != 0:
                return False
            #Player A has the most boxes and wins
            elif Acount > Bcount:
                return True
            #Player B has the most boxes and wins
            elif Bcount > Acount:
                return True
            #Players are tied for number of boxes
            elif Acount == Bcount:
                return True
    
class RandomPlayer:
    """
    The player responsible for playing the game by picking moves
    Holds a score value representing how many points they've earnied in a game
    Score value can be returned to the main program
    Can be passed a list of valid moves to randomly select a move and remove it from the list
    """
    
    
    #Creating default values for Player Class
    m_score = 0
    filepath = open("single_play.txt", "w")
    
    def __init__(self,filepath, in_score = 0):
        """
        Creates the RandomPlayer class with necessary values

        Parameters
        ----------
        filepath : filepath
            file messages should be written to.  Passed to other functions
        in_score : int, optional
            Starting score of player. The default is 0.

        Returns
        -------
        None.

        """
        #Reassigns values for default variables
        self.m_score = in_score
        self.filepath = filepath
         
    def __str__(self):
        """
        Prints player and their scoree

        Returns
        -------
        String
            String representation of player and score.

        """
        return 'RandomPlayer(score=' + self.m_score + ')'
    
    def add_points(self, num):
        """
        Adds points to score

        Parameters
        ----------
        num : int
            amount of points added to score.

        Returns
        -------
        None.

        """
        #Adds points to existing Score
        self.m_score += num
            
    def play_move(self, board, moves, box_moves, display = False):
        """
        Player picks a line to draw from a list of valid moves.  Removes move from list.

        Parameters
        ----------
        board : Board Class
            Board to draw a line on.
        moves : list of list of ints
            List of valid nodes to draw lines between.
        box_moves : list of list of list of ints
            List of boxes, which are lists of all moves (list of ints) that make them up.
        display : Boolean, optional
            Tells the game if it should display the message declaring chosen move. 
            The default is False.

        Returns
        -------
        None.

        """
        #Obtains random value for move
        choice = random.randint(0, len(moves))

        #sends the physical numbers to the function, not the coordinates
        #If, for some reason, the random integer is greater than the length of the list, it reduces it to be within a valid range
        while choice >= len(moves):
            choice -= len(moves)
        
        #Displays move being made if in single-play mode
        move = moves[choice]
        
        if display:
            print("{A} {B}".format(A = move[0], B = move[1]), file = self.filepath)
        
        #sends the physical numbers to the function to update board, not the coordinates
        board.update_board(move[0], move[1]) 
        #Removes move from list 
        moves.pop(choice)
        for box in box_moves:
            for thing in box:
                if thing == move or [thing[1], thing[0]] == move:
                    box.remove(thing)
        for thing in moves:
            if thing == move or [thing[1], thing[0]] == move:
                box.remove(thing)
   
    def score(self):
        """
        Returns score of player.

        Returns
        -------
        int
            Score of player.

        """
        return self.m_score

class WinningPlayer:
    """
    The player responsible for playing the game by playing moves in a somewhat non-random strategy
    Holds a score value representing how many points they've earnied in a game
    Score value can be returned to the main program
    Passed two lists when making a move
    Will always pick moves that complete boxes when available
    """
    
    
    #Creating default values for Player Class
    m_score = 0
    filepath = open("single_play.txt", "w")
    
    def __init__(self,filepath, in_score = 0):
        """
        Creates the WinningPlayer class with necessary values

        Parameters
        ----------
        filepath : filepath
            file messages should be written to.  Passed to other functions
        in_score : int, optional
            Starting score of player. The default is 0.

        Returns
        -------
        None.

        """
        #Reassigns values for default variables
        self.m_score = in_score
        self.filepath = filepath
         
    def __str__(self):
        """
        Prints player and their scoree

        Returns
        -------
        String
            String representation of player and score.

        """
        return 'RandomPlayer(score=' + self.m_score + ')'
    
    def add_points(self, num):
        """
        Adds points to score

        Parameters
        ----------
        num : int
            amount of points added to score.

        Returns
        -------
        None.

        """
        #Adds points to existing Score
        self.m_score += num
            
    def play_move(self, board, moves, box_moves, display = False):
        """
        Player picks a line to draw from a list of valid moves.  Removes move from all lists.
        WinningPlayer will always prioritize boxes that are 3/4 moves towards completion, requiring only one move to be complete.

        Parameters
        ----------
        board : Board Class
            Board to draw a line on.
        moves : list of list of ints
            List of valid nodes to draw lines between.
        box_moves : list of list of list of ints
            List of boxes, which are lists of all moves (list of ints) that make them up.
        display : Boolean, optional
            Tells the game if it should display the message declaring chosen move. 
            The default is False.

        Returns
        -------
        None.

        """
        
        #Boolean stating if a box is one move away from completion
        smart = False
        
        #Checks if there is a potential box available
        move = []
        for box in box_moves:
            if len(box) == 1:
                move = box.pop()
                smart = True
                break
        
        #Fills in box if available
        if smart:
            if display:
                print("{A} {B}".format(A = move[0], B = move[1]), file = self.filepath)
                print("Potential box detected, moving accordingly.", file = self.filepath)
            board.update_board(move[0], move[1])
            for box in box_moves:
                for thing in box:
                    if thing == move or [thing[1], thing[0]] == move:
                        box.remove(thing)
            for thing in moves:
                if thing == move or [thing[1], thing[0]] == move:
                    moves.remove(thing)
        
        #If there is no box one move away from completion, it will instead move randomly
        else:
            #Obtains random value for move
            choice = random.randint(0, len(moves))
    
            #sends the physical numbers to the function, not the coordinates
            #If, for some reason, the random integer is greater than the length of the list, it reduces it to be within a valid range
            while choice >= len(moves):
                choice -= len(moves)
            
            #Displays move being made if in single-play mode
            move = moves.pop(choice)
            
            if display:
                print("{A} {B}".format(A = move[0], B = move[1]), file = self.filepath)
            for box in box_moves:
                for thing in box:
                    if thing == move or [thing[1], thing[0]] == move:
                        box.remove(thing)
            for thing in moves:
                if thing == move or [thing[1], thing[0]] == move:
                    moves.remove(thing)
            #sends the physical numbers to the function to update board, not the coordinates
            board.update_board(move[0], move[1]) 

    
    def score(self):
        """
        Returns score of player.

        Returns
        -------
        int
            Score of player.

        """
        return self.m_score


class Game:
    """
    Game Object responsible for running through the turns through a game.
    Holds function responsible for running a single game, displaying all moves and board updates
        between two different random player objects
    Holds function responsible for running multiple games in a series, displaying various data collected from all games
    Holds function responsible for determining which player goes first
    """
    
    
    #Creates default values
    HSize = 0
    VSize = 0
    filepath = open("single_play.txt", "w")
    rseed = 0
    
    def __init__(self, rseed, HSize, VSize):
        """
        Creates a game containing players and different ways to play the game

        Parameters
        ----------
        rseed : int
            seed to be used for random number generation regarding first turn and moves picked.
        HSize : int
            Horizontal Size of game board.
        VSize : int
            Vertical size of game board.

        Returns
        -------
        None.

        """
        #Replaces default values
        self.rseed = rseed
        random.seed(rseed)
        self.HSize = HSize
        self.VSize = VSize
        
    def single_play(self, filepath):
        """
        Plays a single game, writing all updates to game board and score to a txt file

        Parameters
        ----------
        filepath : filepath
            Text file to write information to.

        Returns
        -------
        None.

        """
        #Creates players
        player1 = RandomPlayer(filepath=filepath)
        player2 = WinningPlayer(filepath=filepath)
        
        """
        SampleBoard = [[0, =, 1, =, 2, =, 3],
                      [+, X, +, X, +, X, +],
                      [4, =, 5, =, 6, =, 7],
                      [+, X, +, X, +, X, +],
                      [8, =, 9, =, 10, =, 11],
                      [+, X, +, X, +, X, +],
                      [12, =, 13, =, 14, =, 15]]
        """
 
        
        first_turn = True
        
        for time in range(0,2):
            #Creates default values necessary for single-play mode
            pastscore1 = 0
            pastscore2 = 0
            gameboard = Board(self.HSize, self.VSize, filepath = filepath)
            end = False
            
            #Creates a list of valid moves to be depleted as the game continues
            #box moves organises moves into sets that create boxes
            valid_moves = []
            box_moves = []
            for a in range(0, self.VSize - 1):
                for b in range(0, self.HSize - 1):
                    box = []
                    #spot = a*Vsize + b
                    c1 = (a * self.VSize) + b
                    c2 = ((a) * self.VSize) + b + 1
                    c3 = ((a+1) * self.VSize) + b
                    c4 = ((a+1) * self.VSize) + b + 1
                    
                    box.append([c1, c2])
                    box.append([c1, c3])
                    box.append([c2, c4])
                    box.append([c3, c4])
                    box_moves.append(box)
            
            for a in range(0, self.HSize*self.VSize):
                for b in range(0, self.HSize*self.VSize):
                    if a != b:
                        valid = False
                        valid = gameboard.is_valid_move(a,b)
                        if valid:
                            if [a,b] not in valid_moves and [b,a] not in valid_moves:
                                valid_moves.append([a,b])
            
            print("==================GAME " + str(time + 1) + "==================", file = filepath)
            if time == 0:
                print("The Random Player will go first\n", file = filepath)
            elif time == 1:
                print("The Smart Player will go first\n", file = filepath)
            while True:
                
                #PlayerA's turn.  Loops until a box is not made during their turn
                while True:
                    if time == 1 and first_turn:
                        first_turn = False
                        break
                    #Displays board information at start of turn
                    gameboard.display_board()
                    print("Score is A:" + str(player1.score()) + " and B:" + str(player2.score()), file = filepath)
                    
                    #Gets past score as reference point
                    pastscore1 = player1.score()
                    
                    #Player A declares and makes move
                    print("A's turn:", end = " ", file=filepath)
                    player1.play_move(gameboard, valid_moves, box_moves, display=True)
                    
                    #Determines if boxes have been made and acts accordingly
                    boxes = gameboard.check_for_box()
                    if boxes:
                        print("Box made, going again", file = filepath)
                        #Updates score for each box made and claims box
                        for box in boxes:
                            gameboard.update_board(box[0], box[1], "A")
                            player1.add_points(1)
                    
                    #Determines if the player failed to make a box this turn
                    if player1.score() == pastscore1:
                        break
                    
                    #Determines if game is over
                    if gameboard.Win(default = "Random Player", display=True):
                        end = True
                        gameboard.display_board()
                        break
                    
                #Ends if game is over
                if end:
                    break
                    
                #Player2's turn.  Loops until a box is not made during their turn
                while True:
                    #Displays board information at start of turn
    
                    gameboard.display_board()
                    print("Score is A:" + str(player1.score()) + " and B:" + str(player2.score()), file = filepath)
        
                    #Gets past score as reference point
                    pastscore2 = player2.score()
                    
                    #Player B declares and makes move
                    print("B's turn:", end = " ", file=filepath)
                    player2.play_move(gameboard, valid_moves, box_moves, display = True)
                    boxes = gameboard.check_for_box()
                    
                    #Determines if boxes have been made and acts accordingly
                    if boxes:
                        print("Box made, going again", file = filepath)
                        for box in boxes:
                            #Updates score for each box made and claims box
                            gameboard.update_board(box[0], box[1], "B")
                            player2.add_points(1)
                    
                    #Determines if the player failed to make a box this turn
                    if player2.score() == pastscore2:
                        break
                    
                    #Determines if game is over
                    if gameboard.Win(default = "Smart Player", display=True):
                        end = True
                        gameboard.display_board()
                        break
                    
                #Ends if game is over 
                if end:
                    break
            
            #Displays final score
            print("Final score is A:" + str(player1.score()) + " and B:" + str(player2.score()) + "\n", file = filepath)
            player1.add_points(player1.score() * -1)
            player2.add_points(player2.score() * -1)
            
    def multiple_play(self, games, filepath):
        """
        PLayes multiple games, writing various statistics to the text file

        Parameters
        ----------
        games : int
            Amount of games to be played.
        filepath : filepath
            File to write data to.

        Returns
        -------
        None.

        """
        #Creates default values
        player1 = RandomPlayer(filepath=filepath)
        player2 = WinningPlayer(filepath=filepath)
        pastscore1 = 0
        pastscore2 = 0
        score_list_1 = []
        score_list_2 = []
        A_first = 0
        B_first = 0
        A_wins = 0
        B_wins = 0
        first_turn = 1
        end = False
  
        
        for n in range(0, games):
            #Resets game state, including game board and list of valid moves
            end = False
            default = False
            
            first_turn = self.coin_flip()
            gameboard = Board(self.HSize, self.VSize, filepath)
            
            valid_moves = []
            box_moves = []
            for a in range(0, self.VSize - 1):
                for b in range(0, self.HSize - 1):
                    box = []
                    #spot = a*Vsize + b
                    c1 = (a * self.VSize) + b
                    c2 = ((a) * self.VSize) + b + 1
                    c3 = ((a+1) * self.VSize) + b
                    c4 = ((a+1) * self.VSize) + b + 1
                    
                    box.append([c1, c2])
                    box.append([c1, c3])
                    box.append([c2, c4])
                    box.append([c3, c4])
                    box_moves.append(box)
            for a in range(0, self.HSize*self.VSize):
                for b in range(0, self.HSize*self.VSize):
                    if a != b:
                        valid = False
                        valid = gameboard.is_valid_move(a,b)
                        if valid:
                            if [a,b] not in valid_moves and [b,a] not in valid_moves:
                                valid_moves.append([a,b])

            
            while True:
                #PlayerA's turn.  Loops until a box is not made during their turn
                while True:
                    #Skips playerA's 1st turn if PlayerB should go first.  Keeps track of who went first.
                    if first_turn == 0:
                        first_turn = 99
                        B_first += 1
                        break
                    elif first_turn == 1:
                        first_turn = 99
                        A_first += 1
                    
                    #Gets past score as reference point
                    pastscore1 = player1.score()
                    
                    #PlayerA plays moves and acts accordingly
                    player1.play_move(gameboard, valid_moves, box_moves)
                    
                    #Obtains list of any boxes made during PlayerA's turn
                    boxes = gameboard.check_for_box()
                    #Updates board and player score if boxes made
                    if boxes:
                        for box in boxes:
                            gameboard.update_board(box[0], box[1], "A")
                            player1.add_points(1)
                    
                    #ends turn if no boxes made
                    if player1.score() == pastscore1:
                        break
                    
                    #Ends round if board full
                    if gameboard.Win(default = "Random Player"):
                        end = True   
                        default = True
                        break
                    
                #Ends round if board full
                if end:
                    break
                    
                #PlayerB's turn.  Loops until a box is not made during their turn
                while True:
                    #Gets past score as reference point
                    pastscore2 = player2.score()
                    
                    #PlayerB plays moves and acts accordingly
                    player2.play_move(gameboard, valid_moves, box_moves)
                    
                    #Obtains list of any boxes made during PlayerB's turn
                    boxes = gameboard.check_for_box()
                    
                    #Updates board and player score if boxes made
                    if boxes:
                        for box in boxes:
                            gameboard.update_board(box[0], box[1], "B")
                            player2.add_points(1)
                    
                    #Ends turn if no boxes made
                    if player2.score() == pastscore2:
                        break
                    
                    #Ends roudn if board is full
                    if gameboard.Win(default = "Smart Player"):
                        end = True
                        default = False
                        #gameboard.display_board()
                        break
                    
                #Ends round if board is full
                if end:
                    break
            
            #Adds each players score to a list once round ends
            score_list_1.append(player1.score())
            score_list_2.append(player2.score())
            if player1.score() > player2.score():
                A_wins += 1
            elif player2.score() > player1.score():
                B_wins += 1
            elif player2.score() == player1.score():
                if default:
                    A_wins += 1
                else:
                    B_wins += 1
            
            #Resets each players score at the end of each round
            player1.add_points((-1 * player1.score()))
            player2.add_points((-1 * player2.score()))
            del gameboard
        
        #Creates full list of scores at the end of all games
        score_list_1 = sorted(score_list_1, reverse = False)
        score_list_2 = sorted(score_list_2, reverse = False)
        
        #Calculates each player's average score
        average1 = sum(score_list_1)/len(score_list_1)
        average2 = sum(score_list_2)/len(score_list_2)
        
        #Calculates mean of each player's scores
        if len(score_list_1)%2 == 0:
            median1 = (score_list_1[len(score_list_1)//2] + score_list_1[len(score_list_1)//2 - 1]) / 2
            median2 = (score_list_2[len(score_list_2)//2 - 1] + score_list_2[len(score_list_2)//2]) / 2
        else:
            median1 = score_list_1[len(score_list_1)//2]
            median2 = score_list_2[len(score_list_2)//2]
        
        #Displays various data at the end of all games
        print("Number of Games: ", games, file = filepath)
        print("RNG Seed: ", self.rseed, file = filepath)
        print("Scores of Random Player:\n", score_list_1, file = filepath)
        print("\nScores of Smart Player:\n", score_list_2, file = filepath)
        print("\nAVG of Random Player: ", average1, file = filepath)
        print("AVG of Smart Player: ", average2, file = filepath)
        print("Median of Random Player: ", median1, file = filepath)
        print("Median of Smart Player: ", median2, file = filepath)
        print("Random Player First: ", A_first, file = filepath)
        print("Smart Player First: ", B_first, file = filepath)
        print("Random Player Wins: ", A_wins, file = filepath)
        print("Smart Player Wins: ", B_wins, file = filepath)
        print("Highest Random Score:", score_list_1[len(score_list_1)-1], "  lowest Random Score:", score_list_1[0], file = filepath)
        print("Highest Smart Score:", score_list_2[len(score_list_2)-1], "  lowest Smart Score:", score_list_2[0], file = filepath)
           
        print("---Data Calculation has finished---")
        
    def coin_flip(self):
        """
        Flips a coin to determine which player goes first

        Returns
        -------
        result : int
            int from 0-1 to determine which player goes first.

        """
        #Obtains random int between 0-1 to determine who plays first
        result = random.randint(0,1)
        return result

def main():
    number = 1
    #Prompts user for valid amount of games to play in Multiple-Play mode
    while True:
        try:
            number = int(input("How many games would you like to play in multiple-play mode: "))
            if number < 0:
                raise IndexError
            break
        except:
            print("Please provide a valid number. Please try again.")
    
    #Prompts user for valid size of game board
    userX = 0
    userY = 0
    while True:
        try:
            userX = int(input("Input X-Length of grid (AMOUNT OF CORNERS/DOTS NOT BOXES): "))
            if userX <= 1:
                raise IndexError
            break
        except IndexError:
            print("Please enter a value >=1")
        except:
            print("Invalid input. Please try again.")
    while True:
        try:
            userY = int(input("Input Y-Height of grid (AMOUNT OF CORNERS/DOTS NOT BOXES): "))
            if userX <= 1:
                raise IndexError
            break
        except IndexError:
            print("Please enter a value >=1")
        except:
            print("Invalid input. Please try again.")
    
    #Prompts user for an int seed to be used for random number generation
    user_seed = 0
    while True:
        try:
            user_seed = int(input("Input an RNG Seed: "))
            break
        except:
            print("Invalid input. Please try again.")
    
    #Creates game object
    main_game = Game(user_seed, userX, userY)
    #Running a Singular Game
    single_file = open("single_play.txt", "w")
    main_game.single_play(filepath=single_file)
    
    #Running Multiple Games
    multiple_file = open("multiple_play.txt", "w")
    main_game.multiple_play(number,filepath=multiple_file)
    
    single_file.close()
    multiple_file.close()
    
    
if __name__ == "__main__": 
    main()
    #   >:)