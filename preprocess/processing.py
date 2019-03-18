# coding:utf-8
'''
环境：python + jupyter notebook
安装 pip install nltk （http://www.nltk.org/install.html）
'''

import nltk
import nltk.text
import re 
import string
# 第一次运行(NTLK自带语料库默认路径下载) : 
# nltk.download()


'''测试是否成功下载'''
# from nltk.corpus import brown
# print(brown.words())
# print(len(brown.sents())) # 句子数
# print(len(brown.words())) # 单词数

# from nltk.book import *



'''英文文本处理'''
'''词性标注'''
text = open(u'./data/text_en.txt',encoding='utf-8',errors='ignore').read()
# raw=open('a.txt').read()
# text=nltk.text.Text(jieba.lcut(raw))


# 分句1
from nltk.tokenize import sent_tokenize 
# print(sent_tokenize(text))

# 分词1
words=nltk.word_tokenize(text)
text_en = nltk.text.Text(words)
# print(words)

# 提取词干
from nltk.stem import PorterStemmer
stemmerporter = PorterStemmer()
for i in range(len(words)):
    words[i] = stemmerporter.stem(words[i])
# print(words)

# 处理停用词
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
words = [word for word in words if word.lower() not in stops]
# print(len(words))

# 标点符号过滤
def filter_punctuation(words):
    new_words = []
    illegal_char = string.punctuation+'【·！…（）——：“”?《》、；】'
    pattern = re.compile('[%s]'%re.escape(illegal_char))
    for word in words:
        new_word = pattern.sub(u'',word)
        if not new_word == u'':
            new_words.append(new_word)
    return new_words

words_no_punc = filter_punctuation(words)
# print(len(words_no_punc))

# 低频词过滤
fdist = nltk.FreqDist(words_no_punc)
threshold = fdist.freq(fdist.max())/2.0
i = 0
while(i < len(words_no_punc)):
    if fdist.freq(words_no_punc[i]) <= threshold:
        words_no_punc.remove(words_no_punc[i])
    else:
        i += 1
# print(filter_word)

# 绘制分布位置离散图
print(text_en.dispersion_plot(["Elizabeth","Darey","Wickham","Bingley", "Jane"]))


#绘制前20频率词汇分布图
# print(threshold*len(words_no_punc))
# fdist = nltk.FreqDist(words_no_punc)
fdist.plot(20)