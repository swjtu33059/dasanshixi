import random


all_item = []
sf_list = []
static_list = []


def initCount(line, op):
    line_list = line.strip('\n').split(',')
    if len(line_list) == 6:
        rd = random.randint(500, 500000)
        line_list[4] = str(rd)
        line_list[3] = str(random.randint(0, min(rd // 100, 1000)))
        if op == 0:
            sf_list.append(','.join(line_list))
        else:
            static_list.append(','.join(line_list))


def fileNormal(path, lmt):
    cnt = 0
    with open(path, 'r', encoding='utf-8') as raw:
        for line in raw:
            cnt += 1
            if cnt <= lmt:
                initCount(line, 0)
            else:
                initCount(line, 1)


def fileTypical(path):
    cnt = 0
    with open(path, 'r', encoding='utf-8') as raw:
        for line in raw:
            n = random.randint(100, 2000)
            cnt += n
            for i in range(n):
                initCount(line, 0)
    print('Random ' + str(cnt))


random.seed()
fileNormal(r'E:\大三实习\res1.txt', 20000)
print(str(len(sf_list)) + ' Normal')
fileTypical(r'E:\大三实习\typical.txt')
random.shuffle(sf_list)
all_item = sf_list + static_list
with open(r'E:\大三实习\res2.txt', 'w', encoding='utf-8') as out:
    for item in all_item:
        out.write(item + '\n')
