import pandas as pd
import jieba
import jieba.posseg as pseg
import re
from collections import Counter
from text_clean import clean_content

#positive
with open('./dataset/pos_verb.txt','r',encoding='utf-8') as f:
    pos_verb = f.read().split('\n')
with open('./dataset/pos_adv.txt','r',encoding='utf-8') as f:
    pos_adv = f.read().split('\n')
#negative
with open('./dataset/neg_verb.txt','r',encoding='utf-8') as f:
    neg_verb = f.read().split('\n')
with open('./dataset/neg_adv.txt','r',encoding='utf-8') as f:
    neg_adv = f.read().split('\n')

def filter_topic(title):
    neutral = ['[情報]', '[公告]', '[新聞]','[問題]']
    for w in neutral:
        if w not in title:
            return True
        else:
            return False

def cut_word(string):
    new = string.replace('\n',' ')
    final = new.replace('(未滿60分為不推薦)','')
    words = jieba.lcut(final)
    return words

def categorize(row):
    if row['condition'] == True:
        word_list = row['word_list']
        score = []
        #positive
        for i,w in enumerate(word_list):
            # word is negative
            if word_list[i] in neg_verb:
                if word_list[i-1] in neg_adv or word_list[i-2] in neg_adv:
                    npn = 1
                    score.append(int(npn))
                elif word_list[i-1] in neg_adv and word_list[i-2] in neg_adv:
                    nnn = -1
                    score.append(int(nnn))
                elif word_list[i-1] in pos_adv:
                    p_n = -2
                    score.append(int(p_n))
            # word is positive
            elif word_list[i] in pos_verb:
                if word_list[i-1] in neg_adv or word_list[i-2] in neg_adv:
                    np = -1
                    score.append(int(np))
                elif word_list[i-1] in neg_adv and word_list[i-2] in neg_adv:
                    nn = 1
                    score.append(int(nn))
                elif word_list[i-1] in pos_adv or word_list[i-2] in pos_adv:
                    p = 2
                    score.append(int(p))
            else:
                neu = 0
                score.append(int(neu))
        result = sum(score)
        if result > 0:
            return 1
        elif result < 0:
            return -1
        else:
            return 0
    else:
        return 0

def write_data(row):
    if row['score'] == 1:
        with open('./mypos.txt','a',encoding='utf-8') as f:
            f.write(row['content'])
    elif row['score'] == -1:
        with open('./myneg.txt','a',encoding='utf-8') as f:
            f.write(row['content'])

def main():
    # set dictionary
    jieba.set_dictionary('./dataset/dict.txt.big')
    # set user dictionary
    jieba.load_userdict('./dataset/my_dict.txt')
    jieba.suggest_freq('福袋', True)
    jieba.suggest_freq('全家', True)
    jieba.suggest_freq(('全家', '福'), True)

    data = pd.read_csv('./export/export_dataframe_2016.csv')
    data['corpus'] = data['content'].apply(lambda x: clean_content(x))
    data['condition'] = data['content'].apply(lambda x: filter_topic(x))
    data['word_list'] = data['corpus'].apply(lambda x: cut_word(x))
    data['score'] = data.apply(lambda row: categorize(row), axis=1)
    data.apply(lambda row: write_data(row), axis=1)

if __name__ == '__main__':
    main()
