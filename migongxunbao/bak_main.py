import api
import copy
import datetime
from queue import PriorityQueue


class State:
    def __init__(self, p0_pos=None, p0_score=0, p0_visited = {}, p1_pos=None, p1_score=0, p1_visited=None, gems=None, depth=0):
        self.p0_pos = p0_pos
        self.p0_score = p0_score
        self.p0_visited = p0_visited
        self.p1_pos = p1_pos
        self.p1_score = p1_score
        self.p1_visited = p1_visited
        self.gems = gems
        #self.weight = weight
        self.depth = depth

class Player:
    def __init__(self, player):
        self.row = player.row
        self.col = player.col
        self.score = 0
        self.order = player.order

class Solution:
    def __init__(self, context):
        self.context = context
        
        self.dest = self._get_gems()
        self.dest.append(Player(context.players[0]))
        self.dest.append(Player(context.players[1]))
        
        self.G = self.get_dist_martrix

        #self.visited = [False for i in range(len(self.dest))]
        #self.visited[-1] = self.visited[-2] = True
        #self.weight = self._make_weight()

    def _get_gems(self):
        all_gems = []
        for gems in self.context.items.values():
            for gem in gems:
                all_gems.append(gem)
        return all_gems
    
    def get_dist_martrix(self, items):
        l = len(items)
        G = [[0] * l for i in range(l)]

        tmpPlayer = copy.copy(self.context.players[1])
        for i in range(l-2):
            tmpPlayer.row = items[i].row
            tmpPlayer.col = items[i].col
            for j in range(i+1, l):
                target_item = items[j]
                G[i][j] = api.check.path_len(target_item.row, target_item.col, tmpPlayer)
                G[j][i] = G[i][j]
        return G

    def solve(self):
        visited = [False for i in range(len(self.dest))]
        visited[-1] = self.visited[-2] = True

        p0_next = []
        p1_next = []
        p0 = self.dest[-2]
        p1 = self.dest[-1]
        for i in range(len(self.dest)-2):
            if self.G[-2] + p0.order <= self.G[-1]:
                p0_next.append(i)
            else:
                p1_next.append(i)
        p0_next.sort(key=lambda idx: self.G[-2][idx])
        p1_next.sort(key=lambda idx: self.G[-1][idx])
        print(p0_next)
        print(p1_next)


    



context = api.get_context()
#print(context)
#print(context.__dict__)
print(datetime.datetime.now())
s = Solution(context)
print(s.solve())
print(datetime.datetime.now())

#print(s.maze)
