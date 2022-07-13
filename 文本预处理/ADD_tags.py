tag_dict = {
    0: '政治', 1: '财经', 2: '体育', 3: '娱乐',
    4: '军事', 5: '科技',  6: '文化',
    7: '教育', 8: '社会',  9: '其他'
}

total_arr = [0]*10

filename = "D:\\before.txt"
filename1 = "D:\\after.txt"
with open(filename1,'r',encoding='utf-8') as fnum:
    for lines in fnum:
        for k,v in tag_dict.items():
            if v in lines:
                total_arr[k]+=1
    fnum.close()


with open(filename, 'r', encoding='utf-8') as f:
    for lines in f:
        str1 = ''
        str1 = lines.strip('\n')  # 获取before文档里面的title
        print(str1)
        str1 += ' '
        pos = int(input('请输入分类：'))
        total_arr[pos] += 1
        str1 += tag_dict[pos]
        print(total_arr)

        with open(filename1, 'a', encoding='utf-8') as f1:
            f1.write(str1)
            f1.write('\n')
        f1.close()
    f1.close()



