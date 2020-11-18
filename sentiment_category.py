from snownlp import SnowNLP
from snownlp import sentiment
import pandas as pd
from text_clean import clean_content, clean_comment


def emotion_comment(comment):
    new = clean_comment(str(comment))
    try:
        s = SnowNLP(new)
        return round(s.sentiments,3)
    except ZeroDivisionError:
        pass
def emotion_content(content):
    new = clean_content(str(content))
    try:
        s = SnowNLP(new)
        return round(s.sentiments,3)
    except ZeroDivisionError:
        pass

def category(score):
    if score > 0.6:
        return 'positive'
    elif score < 0.4:
        return 'negative'
    elif score < 0.6 and score > 0.4:
        return 'neutral'
    else:
        return 'No'

def main():


    data = pd.read_csv('./export/export_dataframe_2017.csv')
    data['comment_emotion_score'] = data['comment'].apply(lambda x: emotion_comment(x))
    data['content_emotion_score'] = data['content'].apply(lambda x: emotion_content(x))
    data['comment_category'] = data['comment_emotion_score'].apply(lambda x: category(x))
    data['content_category'] = data['content_emotion_score'].apply(lambda x: category(x))
    data.to_csv('./export/export_dataframe_2017.csv')


if __name__ == '__main__':
    main()

