import re
import pandas as pd

ASIN_list = []
with open('asin_test.txt','r') as fi:
    ASIN_list = fi.read().splitlines()

for asin in ASIN_list:
    words_per_review_list = []
    paragraphs_per_review = []
    break_tags_per_review = []
    fr = open(asin+".txt",'r',encoding='utf-8')
    for line in fr.readlines():
        break_counter = 0
        words = len(line.split())
        words_per_review_list.append(words)
        break_pattern = re.compile(r'<br/>')
        pattern = re.compile(r"(<br/>)+")
        matches = pattern.finditer(line)
        break_matches = break_pattern.findall(line)
        for match in break_matches:
            break_counter += 1
        break_tags_per_review.append(break_counter)
        new_line = pattern.sub(r'<br/>', line)
        if len(new_line)==2 and new_line[0:1]==" ":
            paragraphs = 0
        else:
            paragraphs = len(new_line.split('<br/>'))
        paragraphs_per_review.append(paragraphs)
    print(len(words_per_review_list))
    print(words_per_review_list)
    print(len(paragraphs_per_review))
    print(f"the number of paragraphs is {paragraphs_per_review}")



    # csv_input = pd.read_csv(asin+'metadata.csv')
    # csv_input['no_words'] = csv_input[words_per_review_list]
    # csv_input.to_csv('latest.csv', index = False)


    fr_1 = open(asin+'metadata.csv','r',encoding='utf-8')
    # metadata =  fr_1.readlines()
    metadata=pd.read_csv(asin+"metadata.csv", header= None, names=["Date","Stars","Helpful Votes"])
    df = pd.DataFrame(metadata)
    df['Words']= words_per_review_list
    df['Paragraphs'] = paragraphs_per_review
    df['No.break tags'] = break_tags_per_review
    print(df)
    df.to_csv(asin+'metadata.csv',index=False, header=False)
