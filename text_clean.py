import json
import pandas as pd
import re
import jieba

#set stop words
with open('./dataset/stop_words.txt', 'r', encoding='utf-8') as f:
    stop_words = f.read().split('\n')
#set company name
with open('./dataset/company.txt', 'r', encoding='utf-8') as f:
    company_name = f.read().split('\n')
#set category
with open('./dataset/category.txt', 'r', encoding='utf-8') as f:
    category_list = f.read().split('\n')
#讀取csv檔
def extract_data(year):
    year = str(year)
    file = './textdata/PttCvs_'+year+'.json'
    raw_data = pd.read_json(file)
    raw_data['quarter'] = raw_data['date_and_time'].dt.to_period("Q")
    raw_data['total_score'] = raw_data['pushscore'] + 1
    raw_data['title'] = raw_data['title'].str.strip('\n')
    raw_data['title'] = raw_data.replace(r'[^\w\s]','',regex=True)
    return raw_data
#斷字，參數為的資料型態為string，輸出為list，同時移除常用字跟標題
def cut_word_title(string):
    words = [ ]
    seg_list = jieba.cut(string)
    for word in seg_list:
        if word not in stop_words + category_list:
            words.append(word)
    return words
#評論的預處理，參數為每個文章的評論，擷取所需要的，移除網址、特殊字元
def clean_comment(comment):
    try:
        comment = comment.split('※')[1]
        comment = comment.split('\n')[1:]
        comment = ''.join(comment)
        comment = re.sub(r'http\S+[jpg$]','',comment)
        comment = re.sub(r'[0-9]{2}\S+\:[0-9]{2}','',comment)
        comment = re.sub(r'[^\w\s]',' ',comment)
        comment = comment.replace('\n','')
    except:
        comment = comment.split('※')[0]
        comment = comment.replace(comment,'null')
    return comment
#把同義字宜並轉換，輸入的參數為list
def change_thesaurus(words):
    thesaurus = { }
    same_7 = ['7-11', '小七', '711', '統一超商', '7-ELEVEN', '7-Eleven']
    for item in same_7:
        a = {item: '7-11'}
        thesaurus.update(a)
    same_family = ['全家便利商店', 'family mart', 'Family Mart', 'FMC']
    for item in same_family:
        b = {item:'全家'}
        thesaurus.update(b)
    for i,word in enumerate(words):
        if word in thesaurus:
            words[i] = thesaurus[word]
    return words
#內容的預處理，擷取本文，移除特殊字元
def clean_content(content):
    content = content.split('時間')[1]
    content = re.sub(r'[A-Za-z]{3}\s[A-Za-z]{3}\s[0-9]{2}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2}\s[0-9]{4}','',content)
    content = re.sub(r'[^\w\s]', ' ',content)
    content = content.replace('\n', ' ')
    return content
#斷字，只移除停止詞
def cut_word(string):
    words = [ ]
    seg_list = jieba.cut(string)
    for word in seg_list:
        if word not in stop_words :
            words.append(word)
    return words
#把最後出來的結果轉為字串，方便存取csv再次使用時比較方便
def list_as_string(list_object):
    sentence = ' '.join(list_object)
    return sentence
def main():
    #設定jieba
    #set dictionary
    jieba.set_dictionary('./dataset/dict.txt.big')
    #set user dictionary
    jieba.load_userdict('./dataset/my_dict.txt')
    #設定特殊字的詞頻
    jieba.suggest_freq('福袋', True)
    jieba.suggest_freq('全家',True)
    jieba.suggest_freq(('全家','福'),True)


    #讀取2020的檔案
    data = extract_data(2016)
    #標題斷字
    data['title_clean'] = data['title'].apply(lambda x : cut_word_title(x))
    # 內容處理
    data['content_clean'] = data['content'].apply(lambda x: clean_content(x))
    #評論預處理
    data['comment_clean'] = data['comment'].apply(lambda x : clean_comment(x))

    #將以下都轉換同義詞，並將list轉字串
    data['title_clean'] = data['title_clean'].apply(lambda x :change_thesaurus(x))
    data['title_clean'] = data['title_clean'].apply(lambda x: list_as_string(x))
    data['content_clean'] = data['content_clean'].apply(lambda x:cut_word(x))
    data['content_clean'] = data['content_clean'].apply(lambda x: change_thesaurus(x))
    data['content_clean'] = data['content_clean'].apply(lambda x: list_as_string(x))
    data['comment_clean'] = data['comment_clean'].apply(lambda x:cut_word(x))
    data['comment_clean'] = data['comment_clean'].apply(lambda x: change_thesaurus(x))
    data['comment_clean'] = data['comment_clean'].apply(lambda x: list_as_string(x))
    #存為csv檔
    data.to_csv ('./export/export_dataframe_2016.csv', index = False, header=True)

if __name__ == '__main__':
    main()