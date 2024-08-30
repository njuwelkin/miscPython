import api
import copy

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
        
        self.G = self.get_dist_martrix(self.dest)
        self.order = (self.dest[-2].order/2, self.dest[-1].order/2)

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
        for i in range(l):
            tmpPlayer.row = items[i].row
            tmpPlayer.col = items[i].col
            for j in range(i+1, l):
                target_item = items[j]
                G[i][j] = api.check.path_len(target_item.row, target_item.col, tmpPlayer)
                G[j][i] = G[i][j]
        #print(G)
        return G
    
    def dfs(self, next_dest, visited, remain_score=10, depth=0):
        score = [0, 0]
        path = ["", ""]

        l0 = len(next_dest[0])
        l1 = len(next_dest[1])
        
        if l0 == 0 and l1 == 0:
            return score, [f"{len(self.dest)-1}", f"{len(self.dest)-2}"]
        close_one = 0
        if l0 != 0 and l1 != 0:
            close_one = 0 if next_dest[0][0][1] + self.order[0]/2 < next_dest[1][0][1] + self.order[1]/2 else 1
        elif l1 != 0:
            close_one = 1

        steps = next_dest[close_one][0][1]
        dest_idx = next_dest[close_one][0][0]

        ## 1st choice，选择吃最近的宝石
        new_visited = copy.copy(visited) # 该宝石被吃掉，加入visited中
        new_visited[dest_idx] = True
        new_next = [[], []]

        # to be improve: 如果所有距离都不变，那肯定选1
        for item in next_dest[1-close_one]: # 没吃宝石的一方，前进steps格
            if item[0] != dest_idx:
                new_next[1-close_one].append((item[0], item[1]-steps))

        for i in range(len(self.dest)): # 吃宝石的一方，从该宝石位置重新计算下一个目标及距离
            if not new_visited[i]:
                new_next[close_one].append((i, self.G[dest_idx][i]))
        new_next[close_one].sort(key=lambda item: item[1])


        res1, path1 = self.dfs(new_next, new_visited, remain_score-self.dest[dest_idx].score, depth=depth+1) # 递归
        res1[close_one] += self.dest[dest_idx].score * (remain_score+5) / 15 # 剩下的分数越少，参考价值越小，因为会随机产生新的gem
        path1[close_one] = f"{dest_idx}" + path1[close_one]

        ## 2nd choice，不吃最近的宝石
        new_visited = visited
        new_next = [None, None]

        new_next[1-close_one] = next_dest[1-close_one] # 没吃宝石的一方不变
        new_next[close_one] = [next_dest[close_one][i] for i in range(1, len(next_dest[close_one]))]

        res2, path2 = self.dfs(new_next, new_visited, remain_score, depth=depth+1)

        if res1[close_one] >= res2[close_one]:
            return res1, path1
        return res2, path2

    def solve(self):
        visited = [False for i in range(len(self.dest))]
        visited[-1] = visited[-2] = True

        p0_next = []
        p1_next = []
        for i in range(len(self.dest)-2):
            p0_next.append((i, self.G[-2][i]))
            p1_next.append((i, self.G[-1][i]))
        p0_next.sort(key=lambda item: item[1])
        p1_next.sort(key=lambda item: item[1])

        #print(p0_next)
        #print(p1_next)
        res, path = self.dfs([p0_next, p1_next], visited)
        target_idx = int(path[0][0])
        target = self.dest[target_idx]
        direction = api.check.next(end=(target.row, target.col))
        return direction

    def print_maze(self):
        tmp = copy.deepcopy(self.context.maze)
        for i in range(len(self.dest)-2):
            gem = self.dest[i]
            tmp[gem.row][gem.col] = f"{i}:{gem.score} "
        player0 = self.dest[-2]
        tmp[player0.row][player0.col] = f" P0 "
        player1 = self.dest[-1]
        tmp[player1.row][player1.col] = f" P1 "
        for line in tmp:
            for block in line:
                if block == 'ROAD':
                    print('    ', end="")
                else:
                    print(block, end="")
            print()

def update(context):
    p1 = context.players[0]
    dist_to_exit = api.check.path_len(p1.exit.row, p1.exit.col, p1) 
    if context.players[0].energy <= dist_to_exit+1:
        return api.check.next(end=(p1.exit.row, p1.exit.col))

    s = Solution(context)
    #s.print_maze()
    d = s.solve()
    if (context.round+1) % 100 == 0 or ((context.round+2) % 100 == 0):
        if context.players[0].score * 4 < context.round:
            print(f'round{context.round}: find deadlock')
            if context.players[0].score < context.players[1].score:
                print('hold')  
                d = 'S'
    return d
