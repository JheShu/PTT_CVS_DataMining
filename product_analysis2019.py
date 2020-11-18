'''
將熱門字帶回原始資料，並運用文字雲查看大家對於這個產品都說了甚麼
'''

# import package
import json
import pandas as pd
import re
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from collections import Counter
from wordcloud import WordCloud

# set env
with open('./dataset/stop_words.txt', 'r', encoding='utf-8') as f:
    stop_words = f.read().split('\n')
# set company name
with open('./dataset/company.txt', 'r', encoding='utf-8') as f:
    company_name = f.read().split('\n')
# set category
with open('./dataset/category.txt', 'r', encoding='utf-8') as f:
    category_list = f.read().split('\n')
# set dictionary
jieba.set_dictionary('./dataset/dict.txt.big')
# set user dictionary
jieba.load_userdict('./dataset/my_dict.txt')
# set frequency for certain words
jieba.suggest_freq('福袋', True)
jieba.suggest_freq('全家', True)
jieba.suggest_freq(('全家', '福'), True)


# 讀取清理過資料
def read_csv_to_pandas(year):
    year = str(year)
    dataFrame = pd.read_csv('./export/export_dataframe_' + year + '.csv')
    return dataFrame


# 把欄位轉回list方便操作
def transform_list(x):
    x = str(x)
    return x.split(' ')

def main():
    # 讀取該年度熱銷商品關鍵字
    top_product = pd.read_csv('./product/top5_2019.csv')
    # 讀取清理過的資料
    raw_2019 = read_csv_to_pandas(2019)
    # 將標題轉換成list
    raw_2019['title_clean'] = raw_2019['title_clean'].apply(lambda x: transform_list(x))
    # 把熱銷關鍵字變成list
    top_product_list = list(set(top_product['name'].tolist()))
    print(top_product_list)
    # 練立空的dataframe，並且輸入關鍵字，藉由標題篩選該商品的文章
    product = pd.DataFrame()
    keyword = '啤酒'
    for i in range(len(raw_2019['title'])):
        for word in raw_2019['title_clean'][i]:
            if word == keyword:
                product = product.append(raw_2019.iloc[i, :], ignore_index=True)
                product['content_clean'] = product['content_clean'].apply(lambda x: x.replace(keyword, ' '))

    # 觀察該商品的
    print('內容:', dict(Counter(product['content_category'])))
    print('評論:', dict(Counter(product['comment_category'])))

    # 建立一個空字串，並把內容全部連一起
    result = ''
    for i in range(len(product['title'])):
        result = result + str(product['content_clean'][i])
    # 畫文字雲
    wc = WordCloud(font_path='./font/NotoSansCJKtc-Regular.otf',
                   background_color='white',
                   max_words=20,
                   stopwords=stop_words)

    wc.generate(result)
    plt.imshow(wc)
    plt.axis("off")
    plt.figure(figsize=(10, 6), dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
