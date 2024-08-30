class Blocker:
    def __init__(self, context):
        self.context = context
    
    def can_block(self, p0, p1, extra_p0_step=0):
        if p0.score <= p1.score:
            return None
        
    def _scores_in_area(self, area_id):
        areas = ((1, 1, 5, 13), (9, 1, 13, 13), (1, 1, 13, 1), (1, 13, 13, 13))
        top = areas[area_id][0]
        left = areas[area_id][1]
        bottom = areas[area_id][2]
        right = areas[area_id][3]
    
        score = 0
        for gems in self.context.items.values():
            for gem in gems:
                if top <= gem.row <= bottom and left <= gem.col <= right:
                    if gem.name == 'box':
                        score += 10
                    elif self.context.players[1].item_count[gem.name] % 10 == 9:
                        score += 10
                    else:
                        score += 1
        print(self.context.round, area_id, score)
        return score

