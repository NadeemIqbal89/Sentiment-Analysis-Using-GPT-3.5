import openai
import streamlit as st
from pathlib import Path
import configparser
import time
import pandas as pd
import csv


openai.api_key = #'Enter your key here'
# Setting Key Programmatically
cfg_reader = configparser.ConfigParser()
fpath = Path.cwd() / Path('config.ini')
cfg_reader.read(str(fpath))
#openai.api_key = cfg_reader.get('API_KEYS','OPENAI_API_KEY')

def get_response_from_chatgpt(text):
    prompt= f"Classify a news is either a human killing evetn or not, return 1 if it is a human killing event or 0 if it is not a human killing event . text: {text}"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
                {"role": "system", "content": "You are a helpful Text Sentiment Analyzer That returns death count."},
                {"role": "user", "content":prompt }
        ],
        temperature = 0.1
        ) 
    sentiment = response['choices'][0]['message']['content']
    return sentiment
Kill_lable=[]
No_of_Rows_analyzed=0
Analyze_Falg=0
analyzed_List=[]
df1=pd.read_csv("News/Murder/Murder_Label_News.csv",encoding="ISO-8859-1" )
for line in df1.itertuples():
    analyzed_List.append(line[1])
df=pd.read_csv("News/Murder/Murder_News.csv", header=None, encoding="ISO-8859-1")
counter=1
while len(analyzed_List)<len(df.index):
    print(len(df.index))
    #print("loop completed")
    for row in df.itertuples():

        if row[1] not in analyzed_List:
            time.sleep(21) 
            try:
                print("Analyzing news..", counter)
                Input_Heading=row[5]    
                #print(Input_Heading)
                Return_label=get_response_from_chatgpt(Input_Heading)
                print(Return_label)
                Kill_lable.append(Return_label)
                counter+=1
                with open("News/Terror/Terror_Label_News.csv", "a", encoding="ISO-8859-1", newline='') as writer1:
                    Label_writer=csv.writer(writer1)
                    Label_writer.writerow([row[1], row[2], row[3],row[4],row[5], Return_label])
                    analyzed_List.append(row[1])
            except Exception as ex:
                continue
        else:
            print(row[1], ": Already Analyzed")
    #print(Kill_lable)   
    #df['Murder-Label']=Kill_lable
    #df.to_csv("Murder_Labeled.csv",index=False)
print("All News analzed and classified")


