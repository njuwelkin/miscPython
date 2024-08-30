import random
#import copy
import queue

class Position:
    # row, col
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return f"Position(col={self.col}, row={self.row})"

class Exit(Position):
    # row, col
    def __init__(self, row, col):
        super(Exit, self).__init__(row, col)
    def __str__(self):
        return f"Exit(col={self.col}, row={self.row})"

class Item(Position):
    def __init__(self, row, col, score):
        super(Item, self).__init__(row, col)
        self.score = score
    def __str__(self):
        return f"Item(col={self.col}, row={self.row}, score={self.score})"

class Player(Position):
    def __init__(self, id, row, col, exit, order, energy=1000):
        super(Player, self).__init__(row, col)
        self.exit = exit
        self.order = order
        self.score = 0
        self.id = id
        self.energy = energy
        self.item_count = {'yellow_gem': 0, 'red_gem': 0}
        self.direction = 'D'
        self.finished = False
    def __str__(self):
        return f"Player(id={self.id}, row={self.row}, col={self.col}, energy={self.energy}, order={self.order}, score={self.score}, exit={self.exit})"

class Context:
    # exit
    # width, heigh
    # round
    # maze
    # items
    # players
    def __init__(self):
        self.maze = [
            ['WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL'], 
            ['WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'WALL', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'WALL', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'ROAD', 'WALL'], 
            ['WALL', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'ROAD', 'WALL'], 
            ['WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL', 'WALL']]
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.round = 0
        self.players = {
            0: Player(id=0, row=7, col=1,  order=0, exit=Exit(row=7, col=6)),
            1: Player(id=1, row=7, col=13, order=1, exit=Exit(row=7, col=8))
        }
        self.items = self._init_gems()
        #self.items = self._make_random_items()
        #self.items = self._make_items()

    def _init_gems(self):
        ret = {
            'pink_gem': [],
            'red_gem': [Item(7, 5, 3), Item(7, 9, 3)],
            'yellow_gem': [Item(3, 3, 1), Item(3, 11, 1), Item(11, 3, 1), Item(11, 11, 1)],
            'purple_gem': [], 'blue_gem': [], 'box': []
        }
        return ret
    
    def _make_random_items(self):
        candidates = []
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == 'ROAD':
                    candidates.append(Item(i, j, 1))

        random.shuffle(candidates)
        candidates[0].score = candidates[1].score = 3
        ret = {
            'pink_gem': [],
            'red_gem': candidates[:2],
            'yellow_gem': candidates[2:6],
            'purple_gem': [], 'blue_gem': [], 'box': []
        }
        
        return ret
    
    def _make_items(self):
        ret = {
            'pink_gem': [],
            'red_gem': [Item(9, 7, 3), Item(8, 13, 3)],
            'yellow_gem': [Item(9, 6, 1), Item(11, 5, 1), Item(9, 11, 1), Item(9, 3, 1)],
            'purple_gem': [], 'blue_gem': [], 'box': []
        }
        return ret
    
    def _make_items2(self):
        ret = {
            'pink_gem': [],
            'red_gem': [Item(9, 7, 3), Item(8, 13, 3)],
            'yellow_gem': [],
            'purple_gem': [], 'blue_gem': [], 'box': []
        }
        return ret

    def __str__(self):
        red_gem_str = ""
        for gem in self.items['red_gem']:
            red_gem_str += gem.__str__() + ","
        yellow_gem_str = ""
        for gem in self.items['yellow_gem']:
            yellow_gem_str += gem.__str__() + ","
        return f"""
            Items: {{
                'red_gem': [{red_gem_str}],
                'yellow_gem': [{yellow_gem_str}]
            }},
            Players: {{
                0: {self.players[0].__str__()},
                1: {self.players[1].__str__()}
            }}
        """
    

class FloodNode(Position):
    # row, col
    def __init__(self, row, col, prev=None, distance=0, d=''):
        super(FloodNode, self).__init__(row, col)
        self.prev = prev
        self.distance = distance
        self.d = d
    def neibors(self):
        r = self.row
        c = self.col
        return {
            'L': FloodNode(r, c-1, prev=self, distance=self.distance+1, d='L'),
            'R': FloodNode(r, c+1, prev=self, distance=self.distance+1, d='R'),
            'U': FloodNode(r-1, c, prev=self, distance=self.distance+1, d='U'),
            'D': FloodNode(r+1, c, prev=self, distance=self.distance+1, d='D')
        }
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    def __str__(self):
        return f"FloodNode(row={self.row}, col={self.col})"

    

class Check:
    def __init__(self):
        self.context = Context()

    def path_len(self, row, col, player):
        crt_layer = [(row, col, 0)]
        visited = {(row, col)}
        while len(crt_layer) > 0:
            next_layer = []
            for r, c, d in crt_layer:
                for neibor in [(r-1, c), (r, c-1), (r+1, c), (r, c+1)]:
                    if (neibor not in visited) and (self.context.maze[neibor[0]][neibor[1]] != 'WALL'):
                        if (neibor[0] == player.row) and (neibor[1] == player.col):
                            return d + 1
                        next_layer.append((neibor[0], neibor[1], d+1))
                        visited.add(neibor)
            crt_layer = next_layer
        return -1
    
    def next(self, end):
        player = self.context.players[0]
        start = FloodNode(player.row, player.col)
        q = queue.Queue()
        q.put(start)
        visited = {start.__str__()}
        found = None
        while not q.empty() and not found:
            node = q.get()
            for neibor in node.neibors().values():
                if (neibor.__str__() not in visited) and (self.context.maze[neibor.row][neibor.col] != 'WALL'):
                    if (neibor.row == end[0]) and (neibor.col == end[1]):
                        found = neibor
                        break
                    q.put(neibor)
                    visited.add(neibor.__str__())

        if not found:
            print(f"can't find {end}")
            return 'S'
        while found.prev != player:
            found = found.prev
        return found.d
    
    def path(self, from_pos, to_pos, dist_only=True):
        start = FloodNode(from_pos[0], from_pos[1])
        q = queue.Queue()
        q.put(start)
        visited = {start.__str__()}
        found = None
        while not q.empty() and not found:
            node = q.get()
            for neibor in node.neibors().values():
                if (neibor.__str__() not in visited) and (self.context.maze[neibor.row][neibor.col] != 'WALL'):
                    if (neibor.row == to_pos[0]) and (neibor.col == to_pos[1]):
                        found = neibor
                        break
                    q.put(neibor)
                    visited.add(neibor.__str__())
        if not found:
            print(f"can't find {to_pos}")
            return -1
        if dist_only:
            return found.distance, ""
        dist = found.distance
        while found.prev != start:
            found = found.prev
        return dist, found.d