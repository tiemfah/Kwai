from random import choice

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

def choice_n_time(n, hardness):
        possibility = random_with_weight([('.',12), ('D',11), ('#',7), ('G',2), ('T',hardness//15)])
        temp = []
        for num in range(n):
            temp.append(choice(possibility))
        if True in [('#' != x and 'T' != x) for x in temp]:
            return temp
        else:
            return choice_n_time(n)

def wild_random(level, hardness):
    if level == 1:
        return ''.join(['$$#'] + choice_n_time(3, hardness) + ['#$$'])
    elif level == 2:
        return ''.join(['$#'] + choice_n_time(5, hardness) + ['#$'])