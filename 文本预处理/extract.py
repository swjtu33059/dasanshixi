import random
import re
import jieba


word_dict = {}
hot_word = []
trash_word = ['为什么', '为何', '当然', '所以']


# 获取标题
def getHeader(item):
    pattern = re.compile(r'\[(.*)]')
    result = pattern.findall(item)
    if len(result) > 0:
        return result[0]
    else:
        return ''


# 把标题变成话题
def replaceHeader(item, rpl):
    pattern = re.compile(r'\[(.*)]')
    result = pattern.sub('[' + rpl + ']', item)
    return result


def getPoint(item):
    if len(item) == 0:
        return list()
    # 去除数字、符号和字母
    # 无法去除中文的'|'
    pattern = re.compile(r'[^\u4e00-\u9fa5 a-zA-Z\d]')
    sentence = pattern.sub('', item)
    cut_list = jieba.cut(sentence, cut_all=False)
    return list(cut_list)


def countWord(word_list):
    for word in word_list:
        if len(word) > 1:
            if word in word_dict:
                word_dict[word] = word_dict[word] + 1
            else:
                word_dict[word] = 1


def dealFile(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            countWord(getPoint(getHeader(line)))


class Pair(object):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __lt__(self, other):
        return self.val > other.val


def hotWord():
    with open(r'E:\大三实习\hot_word.txt', 'r', encoding='utf-8') as f:
        for i in range(10000):
            hot_word.append(f.readline().split(' ')[0])


def limitLength(ls, lmt):
    if len(ls) == 0:
        return ''
    res_list = []
    length = 0
    for item in ls:
        length = length + len(item)
        if length <= lmt:
            res_list.append(item)
        else:
            break
    return ''.join(res_list)


def mergeWord(res_list):
    cnt = 0
    for word in res_list:
        if word in hot_word and word not in trash_word:
            cnt = cnt + 1
    if cnt <= 2:
        return limitLength(res_list, 15)
    else:
        new_list = []
        for word in res_list:
            if word in hot_word:
                new_list.append(word)
        return limitLength(new_list, 15)


def fileProcess(path):
    with open(path, 'r', encoding='utf-8') as f:
        with open(r'E:\大三实习\items.txt', 'a', encoding='utf-8') as out1:
            with open(r'E:\大三实习\to_yyq.txt', 'a', encoding='utf-8') as out2:
                for line in f:
                    res = mergeWord(getPoint(getHeader(line)))
                    out2.write(res + '\n')
                    out1.write(replaceHeader(line, res))


dealFile(r'E:\大三实习\News\t1.txt')
dealFile(r'E:\大三实习\News\t2.txt')
dealFile(r'E:\大三实习\News\t3.txt')
dealFile(r'E:\大三实习\News\t4.txt')
dealFile(r'E:\大三实习\News\t5.txt')
total_list = []
for it in word_dict:
    total_list.append(Pair(it, word_dict[it]))
total_list.sort()
with open(r'E:\大三实习\hot_word.txt', 'w', encoding='utf-8') as file:
    for pair in total_list:
        file.write(pair.id + ' ' + str(pair.val) + '\n')
hotWord()
fileProcess(r'E:\大三实习\News\t1.txt')
fileProcess(r'E:\大三实习\News\t2.txt')
fileProcess(r'E:\大三实习\News\t3.txt')
fileProcess(r'E:\大三实习\News\t4.txt')
fileProcess(r'E:\大三实习\News\t5.txt')

random.seed()
r_list = []
with open(r'E:\大三实习\to_yyq.txt', 'r', encoding='utf-8') as f:
    for item in f:
        r_list.append(item)
    random.shuffle(r_list)
with open(r'E:\大三实习\to_yyq_1.txt', 'w', encoding='utf-8') as f:
    for item in r_list:
        f.write(item)
