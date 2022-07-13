import math

import jieba

type_dict = {}
sum_dict = {}
total_dict = {}
hot_dict = {}
trash_type = {'体育', '教育', '文化', '娱乐', '其他'}


def readType(influence):
    with open(r'E:\大三实习\hot_word.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line_list = line.strip('\n').split(' ')
            if len(line_list) != 2:
                continue
            hot_dict[line_list[0]] = 1 + math.log10(int(line_list[1]))
    with open(r'E:\大三实习\after.txt', 'r', encoding='utf-8') as file_t:
        for line in file_t:
            kv = line.strip('\n').split(' ')
            if len(kv) != 2 or kv[1] == '其他':
                continue
            if kv[1] not in type_dict:
                type_dict[kv[1]] = {}
                type_dict[kv[1]][kv[1]] = influence
                sum_dict[kv[1]] = math.pow(1 + math.log10(influence), 2)
            word_list = jieba.cut(kv[0], cut_all=False)
            for word in word_list:
                if word not in type_dict[kv[1]]:
                    type_dict[kv[1]][word] = 1
                    sum_dict[kv[1]] += 1
                else:
                    sum_dict[kv[1]] -= math.pow(1 + math.log10(type_dict[kv[1]][word]), 2)
                    type_dict[kv[1]][word] += 1
                    sum_dict[kv[1]] += math.pow(1 + math.log10(type_dict[kv[1]][word]), 2)


def similarity(title, ty):
    word_list = list(jieba.cut(title, cut_all=False))
    word_set = set(word_list)
    sum = 0.0
    vec = 0.0
    for word in word_set:
        vec += 1
        if word in type_dict[ty]:
            if word in hot_dict:
                sum += type_dict[ty][word] * hot_dict[word]
                vec += math.pow(hot_dict[word], 2) - 1
            else:
                sum += type_dict[ty][word]
    # print(sum_dict[ty])
    # print(ty)
    return sum / (math.sqrt(vec) * math.sqrt(sum_dict[ty]))


def updateType(title, ty):
    word_list = jieba.cut(title, cut_all=False)
    for word in word_list:
        if word not in type_dict[ty]:
            type_dict[ty][word] = 1
            sum_dict[ty] += 1
        else:
            sum_dict[ty] -= math.pow(1 + math.log10(type_dict[ty][word]), 2)
            type_dict[ty][word] += 1
            sum_dict[ty] += math.pow(1 + math.log10(type_dict[ty][word]), 2)


def lineToList(line):
    res = line.strip('\n').split(',')
    if len(res) != 6:
        return list()
    return res


def gotoType(path, lmt):
    idx = 0
    with open(path, 'r', encoding='utf-8') as raw:
        with open(r'E:\大三实习\res1.txt', 'w', encoding='utf-8') as out:
            for line in raw:
                line = lineToList(line)
                if len(line) ==6 and len(line[2]) >= 10:
                    item = line[2][1:-1]
                    max_sim = 0.0
                    t_id = '其他'
                    for ty in sum_dict:
                        if ty in trash_type:
                            continue
                        sim = similarity(item, ty)
                        if sim > max_sim:
                            max_sim = sim
                            t_id = ty
                    if max_sim <= lmt:
                        t_id = '其他'
                    line[0] = t_id
                    line[2] = '[' + item + ']'
                    out.write(','.join(line) + '\n')
                    if t_id not in total_dict:
                        total_dict[t_id] = 0
                    else:
                        total_dict[t_id] += 1
                    idx += 1
                    if idx % 100 == 0:
                        print(str(idx) + ' items is ok')


def cleanData(path, lmt):
    idx = 0
    with open(path, 'r', encoding='utf-8') as raw:
        for line in raw:
            line = lineToList(line)
            if len(line) ==6 and len(line[2]) >= 10:
                item = line[2][1:-1]
                max_sim = 0.0
                t_id = '其他'
                for ty in sum_dict:
                    if ty in trash_type:
                        continue
                    sim = similarity(item, ty)
                    if sim > max_sim:
                        max_sim = sim
                        t_id = ty
                if max_sim <= lmt:
                    t_id = '其他'
                if t_id != '其他':
                    updateType(item, ty)
                idx += 1
                if idx % 100 == 0:
                    print(str(idx) + ' items is clean')


readType(100000)
print('Initial')
cleanData(r'E:\大三实习\items.txt', 0.065)
gotoType(r'E:\大三实习\items.txt', 0.065)
print(total_dict)
