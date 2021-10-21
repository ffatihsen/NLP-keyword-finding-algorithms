#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 13:02:26 2021

@author: fatih
"""

#TF-IDF skoru hesaplanarak anahtar kelime bulma


from nltk import tokenize
from operator import itemgetter
import math

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english'))


import re
import string
from nltk.corpus import stopwords
from  DB_Baglantı import  DB

import time
import psycopg2




nok_isaretleri_kumesi = string.punctuation
etkisiz_kelimeler_kumesi = stopwords.words('turkish')

etkisiz_kelimeler_kumesi.extend(["bir","kadar","sonra","veyahut"])

def veri_temizleme(metin):
    #Metindeki tüm harfleri küçük duruma getirir
    metin = metin.lower()
    #Veri setimizdeki yeni satır karakterleri, boşluk karakteriyle değiştirdik
    metin = metin.replace("\\n"," ")
    #Kesme işareti ve sonrasındaki karakterlerin kaldırılması 
    metin = re.sub("’(\w+)", "", metin) 
    metin = re.sub("'(\w+)", "", metin)
    metin = re.sub("[“,‘,’,”]", "", metin)
    
     
    #Sayıların kaldırılması
    metin = re.sub("[0-9]+", "", metin)
    
    #Noktalama işaretlerinin kaldırılması
   # metin = "".join(list(map(lambda x:x if x not in nok_isaretleri_kumesi else " ", metin )))
    
    #Etkisiz kelimelerin bir kısmının kaldırılması 
    metin = " ".join([i for i in metin.split() if i not in etkisiz_kelimeler_kumesi])

    #Metinde tek kalan harfleri de çıkaralım 
    metin = " ".join([i for i in metin.split() if len(i) > 1])

    return metin 




db1 = DB() #nesne oluşturma

baglanti = db1.basla()
baglanti.autocommit = True
        
        
        
cursor = baglanti.cursor()

query_select = "SELECT id,journal_id,article_id,title_tr,abstract_tr  FROM article_metadata where issue_year = 2020 and article_id > 818871 ORDER BY article_id"
        
        
cursor.execute(query_select)

articles = cursor.fetchall()




#Databse Bağlantısı
database_name = "article_key"
user_name = "***"
password = "***"
host_ip = "localhost"
host_port = "5432"
    
baglanti = psycopg2.connect(database=database_name,
                                    user=user_name,
                                    password=password,
                                    host=host_ip,
                                    port=host_port)

baglanti.autocommit = True
cursor = baglanti.cursor()


def db_yazdir(id,journal_id,article_id,teknik,anahtar_kelime):
    
    
    anahtarlar=[
            (id,journal_id,article_id,teknik,anahtar_kelime)]
            
    anahtar_kayıt=", ".join(["%s"] * len(anahtarlar))
            
            
    query_insert = (
        f"INSERT INTO key (id,journal_id,article_id,teknik,anahtar_kelime) VALUES{anahtar_kayıt}"
            )
                
    cursor.execute(query_insert,anahtarlar)


for article in articles:
    doc=article[4] #abstract
    id=article[0]
    journal_id=article[1]
    article_id=article[2]
    
    print(article_id)
    time.sleep(1)
    
    


   
    doc = veri_temizleme(doc)
    
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)
    
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    
    
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in etkisiz_kelimeler_kumesi:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1
    
    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

    
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))
    
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1
    
    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}

    
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result

   
   
   
    #TF İDF den gelen top sonuçlar
    sözluk = get_top_n(tf_idf_score, 20)
    
    anahtar_sozluk = list(sözluk.keys())
   # print(anahtar_sozluk)
    
    
    uzunluk = len(anahtar_sozluk)

    for i in range(uzunluk):
        if len(anahtar_sozluk[i]) < 50 :
            db_yazdir(id,journal_id,article_id,"tf_idf",anahtar_sozluk[i])

    
    print("**************")
    #time.sleep(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

