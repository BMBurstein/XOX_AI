import itertools
import random

class Game:
    WON = 'WON'
    ERROR = 'ERROR'
    ONGOING = 'ONGOING'
    TIE = 'TIE'

    symbols = ('X', 'O')

    lines = (
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6)
    )

    def __init__(self):
        self.board = [' '] * 9
        self.player = 1
        self.state = self.ONGOING
        self.hist = []

    def play(self, pos):
        if self.state != self.ONGOING:
            return self.ERROR
        self.hist.append(pos)
        if pos is None:
            self.player = 3 - self.player
            self.state = self.WON
            return self.state
        if not 0 <= pos <= 8:
            self.state = self.ERROR
            return self.state
        if self.board[pos] != ' ':
            self.state = self.ERROR
            return self.state
        self.board[pos] = self.symbols[self.player - 1]
        
        for line in self.lines:
            if pos in line:
                for i in line:
                    if self.board[i] != self.board[pos]:
                        break
                else:
                    self.state = self.WON
                    return self.state
        for c in self.board:
            if c == ' ':
                break
        else:
            self.state = self.TIE
            return self.state
        self.player = 3 - self.player
        return self.state

    def __repr__(self):
        return ''.join(self.board)

    def __str__(self):
        if self.state == self.WON:
            s = f'Player {self.player} won:\n'
        elif self.state == self.ERROR:
            s = f'Got error from player {self.player}\n'
        elif self.state == self.TIE:
            s = 'Tie:\n'
        else:
            s = ''
        for i in range(0,9,3):
            s += ''.join(self.board[i:i+3]) + '\n'
        s += f'\nMoves so far: {self.hist}\n'
        return s


    def __bool__(self):
        return self.state == Game.ONGOING

class Player:
    def reset(self, game, player):
        self.game = game
        self.player = player

    def get_move(self):
        return None

class RandomPlayer(Player):
    def get_move(self):
        move = random.randrange(0,9)
        while self.game.board[move] != ' ':
            move = random.randrange(0,9)
        return move

class LearningPlayer(Player):
    def __init__(self):
        self.mem = {' '*9: list(range(9))*2}
        self.player = 0

    def reset(self, game, player):
        if self.player and self.game.state == Game.WON:
            replay = Game()
            for move in self.game.hist:
                if replay.player == self.player:
                    if self.game.player == self.player:
                        self.mem[repr(replay)] += [move] * 3
                    elif self.game.player != self.player and move is not None:
                        self.mem[repr(replay)].remove(move)
                replay.play(move)
        return super().reset(game, player)

    def get_move(self):
        board = repr(self.game)
        choices = self.mem.setdefault(board, [x for x in range(9) if self.game.board[x] == ' '])
        if choices:
            return random.choice(choices)
        return None



def play_game(p1, p2):
    game = Game()
    p1.reset(game, 1)
    p2.reset(game, 2)
    p = itertools.cycle((p1,p2)).__next__
    player = p()
    while game:
        move = player.get_move()
        game.play(move)
        player = p()
    if game.state == game.WON:
        return game.player
    elif game.state == game.ERROR:
        print(game)
        return -1
    return 0


if __name__ == "__main__":
    stats = [0, 0, 0]
    p1 = RandomPlayer()
    p2 = LearningPlayer()
    for i in range(10000):
        res = play_game(p1, p2)
        if res < 0:
            break
        stats[res] += 1
        print('\r' + str(i) + ': ' + str(stats), end='')
    print()