# encoding=utf-8
import string
import re
import json
import nltk
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
# 加载字典
def load_word_list():
    max_length = 0
    word_dict = set()
    for line in open('./data/corpus.dict.txt',encoding='utf-8',errors='ignore').readlines():
        tmp = len(line)
        if(max_length < tmp):
            max_length = tmp
        word_dict.add(line.strip())
    return max_length, word_dict


# 最大正向匹配
# 到了只有一个字还没有匹配上的时候
# 第一种情况是直接把这个字取出来
# 第二种情况是把上一个得到的串向前找一个
# 这里采用第一种情况
def max_left_match(line):
    lines = []
    max_length, word_dict = load_word_list()
    test_line = ''
    i = 0
    while len(line) > 0:
        i += 1
        if len(line) < max_length:
            max_length = len(line)
        test_line = line[0:max_length]
        while test_line not in word_dict:
            if len(test_line) == 1:
                break
            else:
                test_line = test_line[0:len(test_line)-1]
        lines.append(line[0:len(test_line)])
        # 如果已经全部检查完毕       
        if len(test_line) == len(line):
            break
        else:
            line = line[len(test_line): ]
    return lines

# 最大反向匹配
# 到了只有一个字还没有匹配上的时候
# 第一种情况是直接把这个字取出来
# 第二种情况是把上一个得到的串向前找一个
# 这里采用第一种情况
def max_right_match(line):
    lines = []
    max_length, word_dict = load_word_list()
    test_line = ''
    i = 0
    while len(line) > 0:
        i += 1
        if len(line) < max_length:
            max_length = len(line)
        test_line = line[len(line)-max_length:]
        while test_line not in word_dict:
            if len(test_line) == 1:
                break
            else:
                test_line = test_line[1:]
        lines.append(line[len(line)-len(test_line):len(line)])  
        # 如果已经全部检查完毕    
        if len(test_line) == len(line):
            break
        else:
            line = line[0:len(line)-len(test_line)]
    return lines

# 使用最短编辑距离同理的动态规划算法，计算正确识别的词汇的个数
def max_match(words1, words2):
    x = len(words1) + 1
    y = len(words2) + 1
    same = [[0 for i in range(x)] for j in range(y)]
    for i in range(1, y):
        for j in range(1, x):
            if words1[j-1] == words2[i-1]:
                same[i][j] = same[i-1][j-1] + 1
            else:
                same[i][j] = max(same[i-1][j], same[i][j-1], same[i-1][j-1])
    return same[y-1][x-1]
    

# 测试
def main():
    output=open('./data/corpus.cut.txt','w+')
    output1=open('./data/corpus.output1.txt','w+')
    output2=open('./data/corpus.output2.output.txt','w+')
    output3=open('./data/corpus.output3.output.txt','w+')
    left = []
    right = []
    bidir = []
    standard_list = []
    right_num1, right_num2, right_num3 = 0, 0, 0
    standard = open('./data/corpus.standard.txt',encoding='utf-8',errors='ignore').readlines()
    sentence = open('./data/corpus.sentence.txt',encoding='utf-8',errors='ignore').readlines()
    for i in range(len(standard)):
        # 去标点
        illegal_char = string.punctuation+'【·！…（）——：“”?《》，,.。、；\n】'
        pattern = re.compile('[%s]'%re.escape(illegal_char))
        sentence_words = pattern.sub(u'',sentence[i])
        
        # 得到标准list以及三种匹配的list
        standard_words = pattern.sub(u'',standard[i]).split(' ')
        result1 = max_left_match(sentence_words)
        result2 = max_right_match(sentence_words)
        result2.reverse()
        result3 = (result2 if len(result1) > len(result2) else result1)
        # 存储list结构
        standard_list.extend(standard_words)
        left.extend(result1)
        right.extend(result2)
        bidir.extend(result3)
        # 计算匹配正确的数量
        right_num1 += max_match(result1, standard_words)
        right_num2 += max_match(result2, standard_words)
        right_num3 += max_match(result3, standard_words)
        # 结果
        print(result1,file=output1)
        print(result2,file=output2)
        print(result3,file=output3)

        # 词性分析
        seg = jieba.posseg.cut(sentence_words)
        l = []
        for j in seg:
            l.append(j.word)
            l.append(j.flag)
        print(l, file=output)
        
    P, R, F = [], [], []
    P.append(right_num1/len(left))
    P.append(right_num2/len(right))
    P.append(right_num3/len(bidir))
    R.append(right_num1/len(standard_list))
    R.append(right_num2/len(standard_list))
    R.append(right_num3/len(standard_list))
    for i in range(3):
        F.append(P[i] * R[i] * 2 / (P[i] + R[i]))
    print(P, '\n', R, '\n', F)
    output1.close()
    output2.close()
    output3.close()

main()