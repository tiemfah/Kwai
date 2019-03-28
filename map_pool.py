LEV_1_CAP = 20
LEV_2_CAP = 40

level_1_map = ['$$#...#$$',
               '$$#DD.#$$',
               '$$#D.D#$$',
               '$$#.DD#$$']
level_2_map = ['$#.....#$',
               '$#DDDD.#$',
               '$#DDD..#$',
               '$#.DDDD#$',
               '$#DD.DD#$',
               '$#D.DDD#$',]

def random_with_weight(lst):
    temp = []
    for ele in lst:
        for n in range(ele[1]):
            temp += ele[0]
    return temp
