import api
import copy
import datetime
from queue import PriorityQueue
import random

from quantum import update as quantum_update
from greem import update as greem_update
from test import update

dir_dict = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (-1, 0),
    'D': (1, 0)
}

class Game:
    def __init__(self):
        self.context = api.get_context()
        self.gems = self._get_gems()
        self.road_pos = self._get_road_pos()
        self.need_refresh_context = False

    def _get_road_pos(self):
        candidates = []
        for i in range(self.context.height):
            for j in range(self.context.width):
                if (i == self.context.players[0].exit.row) and (j == self.context.players[0].exit.col):
                    continue
                if (i, j) == (self.context.players[1].exit.row, self.context.players[1].exit.col):
                    continue
                if self.context.maze[i][j] == 'ROAD':
                    candidates.append((i, j))
        return candidates

    def _get_gems(self):
        all_gems = {}
        for gems in self.context.items.values():
            for gem in gems:
                all_gems[(gem.row, gem.col)] = gem.score
        return all_gems
    
    def _add_random_gem(self, score=1):
        while True:
            idx = random.randint(0, len(self.road_pos)-1)
            pos = self.road_pos[idx]
            if self.gems.get(pos) is not None:
                continue
            if (self.context.players[0].row == pos[0]) and (self.context.players[0].col == pos[1]):
                continue
            if (self.context.players[1].row == pos[0]) and (self.context.players[1].col == pos[1]):
                continue
            self.gems[pos] = score
            return
        
    def _refresh_context_gems(self):
        ret = {
            'pink_gem': [],
            'red_gem': [],
            'yellow_gem': [],
            'purple_gem': [], 'blue_gem': [], 'box': []
        }
        for pos, score in self.gems.items():
            if score == 1:
                ret['yellow_gem'].append(api.data_type.Item(pos[0], pos[1], score))
            else:
                ret['red_gem'].append(api.data_type.Item(pos[0], pos[1], score))
        self.context.items = ret

    def _move(self, player, d):
        #print('move: ', d)
        if d == 'S':
            return
        offset = dir_dict[d]
        r = player.row + offset[0]
        c = player.col + offset[1]
        if self.context.maze[r][c] != 'ROAD':
            return
        
        player.row = r
        player.col = c
        player.energy -= 1
        if player.energy <= 0:
            player.finished = True

        if (player.exit.row == r) and (player.exit.col == c):
            player.finished = True
            return

        if self.gems.get((r, c)) is not None:
            score = self.gems[(r, c)]
            player.score += score
            del self.gems[(r, c)]
            self._add_random_gem(score)
            self.need_refresh_context = True

    def step(self, player0, player1, update0, update1):
        if not player0.finished:
                self.context.players[0] = player0
                self.context.players[1] = player1
                api.check.context = self.context
                d1 = update0(self.context)
                self._move(player0, d1)
        if not player1.finished:
                self.context.players[0] = player1
                self.context.players[1] = player0
                api.check.context = self.context
                d1 = update1(self.context)
                self._move(player1, d1)

    def run(self, update0, update1):
        p0 = self.context.players[0]
        p1 = self.context.players[1]

        round = 0
        while not p0.finished or not p1.finished:
            # 每250步先手轮换，以示公平
            if round % 250 == 0:
                p0.order = 1 - p0.order
                p1.order = 1 - p1.order
                print(f"    {round}: ", p0.score, p1.score)

            self.need_refresh_context = False
            
            #print(p0, p1)
            #self.print_maze()
            if p0.order == 0:
                self.step(p0, p1, update0, update1)
            else:
                self.step(p1, p0, update1, update0)
            
            if self.need_refresh_context:
                self._refresh_context_gems()

            round += 1

        if p0.col == p0.exit.col and p0.row == p0.exit.row:
            p0.score += 100

        if p1.col == p1.exit.col and p1.row == p1.exit.row:
            p1.score += 100

        #print(p0, p1)
        return (p0.score, p1.score)
            
    def test(self):
        d = api.check.next(end=(6, 5))

    def print_maze(self):
        tmp = copy.deepcopy(self.context.maze)
        #for i in range(len(self.gems)):
        for pos, score in self.gems.items():
            tmp[pos[0]][pos[1]] = f" {score}  "
        player0 = self.context.players[0]
        tmp[player0.row][player0.col] = f" P0 "
        player1 = self.context.players[1]
        tmp[player1.row][player1.col] = f" P1 "
        for line in tmp:
            for block in line:
                if block == 'ROAD':
                    print('    ', end="")
                else:
                    print(block, end="")
            print()

game = Game()
game.print_maze()
#print(api.check.path((7, 1), (7, 13), dist_only=False))

p0_win = p1_win = 0
p0_total_score = p1_total_score = 0
total_round = 50
for i in range(total_round):
    print(datetime.datetime.now())
    game = Game()
    p0_score, p1_score = game.run(update, quantum_update)
    if p0_score > p1_score:
        p0_win += 1
        print("p0 win: ", end="")
    elif p0_score < p1_score:
        p1_win += 1
        print("p1 win: ", end="")
    print(p0_score, p1_score)
    p0_total_score += p0_score
    p1_total_score += p1_score

print(datetime.datetime.now())
print(f"总胜场 {p0_win}:{p1_win}")
print(f"总得分 {p0_total_score}:{p1_total_score}")
print(f"每局平均净胜分 {(p0_total_score-p1_total_score)/total_round}")
    #game.print_maze()
    #game.test()



#print(datetime.datetime.now())
#s = Solution(context)
#print(update1(context))
#print(datetime.datetime.now())

#print(s.maze)
