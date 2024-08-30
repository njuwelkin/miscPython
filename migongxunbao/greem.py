import api
import copy

class Item:
    def __init__(self, player):
        self.row = player.row
        self.col = player.col
        self.score = 0
        self.order = player.order

def get_all_gems(context):
    all_gems = []        
    for gems in context.items.values():
        for gem in gems:
            all_gems.append(gem)
    return all_gems

def get_dist_martrix(context, items):
    l = len(items)
    G = []
    for i in range(l):
        G.append([0] * l)

    tmpPlayer = copy.copy(context.players[1])
    for i in range(l-2):
        tmpPlayer.row = items[i].row
        tmpPlayer.col = items[i].col
        for j in range(i+1, l):
            target_item = items[j]
            G[i][j] = api.check.path_len(target_item.row, target_item.col, tmpPlayer)
            G[j][i] = G[i][j]
    return G
        
def solve(G, p1_idx, p2_idx, p1_order, items, visited, p1_steps, depth):
    if depth > 4:
        return -1, 0

    next_candidates = []
    max_score = 0
    ret_next = -1
    latest_dist = 1000
    for i in range(len(G[p1_idx])-2):
        if (not visited[i]) and (G[p1_idx][i] + p1_order < G[p2_idx][i] - p1_steps):
            visited[i] = True
            next_idx, score = solve(G, i, p2_idx, p1_order, items, visited, p1_steps+G[p1_idx][i], depth+1)
            visited[i] = False
            if (score  > max_score) or ((score == max_score) and (G[p1_idx][i] < latest_dist)):
                max_score = score
                ret_next = i
                latest_dist = G[p1_idx][i]
    weight = 1
    #weight = 1 - depth / 10
    #weight = 50/ (50+p1_steps+latest_dist)
    return ret_next, (max_score + items[i].score)*weight

#主程序每回合自动调用玩家定义的update(context)函数，函数返回值（U, D, L, R, S ）使企鹅向某方向（上 ，下 ，左 ，右 ，停）移动
def update(context):
    p1 = context.players[0]
    dist_to_exit = api.check.path_len(p1.exit.row, p1.exit.col, p1) 
    if context.players[0].energy <= dist_to_exit+1:
        return api.check.next(end=(p1.exit.row, p1.exit.col))

    # all items, including gems and players
    items = get_all_gems(context)
    items.append(Item(context.players[0]))
    items.append(Item(context.players[1]))

    # get the dist matrix
    G = get_dist_martrix(context, items)
    
    #
    l = len(items)
    visited = [False]*l
    
    n, s = solve(G, l-2, l-1, context.players[0].order - 0.5, items, visited, 0, 0)
    target = items[n]
    if s == 0 or n == -1:
        #print(context.players[0].order - 0.5)
        target = items[0]
        #print("don't know where to go", s, n)
 
    direction = api.check.next(end=(target.row, target.col))
    if direction == 'S':
        print(direction, n, l)
    return direction