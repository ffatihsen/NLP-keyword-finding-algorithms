#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 09:29:26 2021

@author: fatih
"""

#Gensim kütüphanesini kullanarak anahtar kelime çıkartma

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords


from  DB_Baglantı import  DB
from DB_Yazma import DBYaz


import time
import psycopg2


nok_isaretleri_kumesi = string.punctuation
etkisiz_kelimeler_kumesi = stopwords.words('turkish')
etkisiz_kelimeler_kumesi.extend(["bir","kadar","sonra"])




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
    metin = "".join(list(map(lambda x:x if x not in nok_isaretleri_kumesi else " ", metin )))
    
    #Etkisiz kelimelerin bir kısmının kaldırılması 
    metin = " ".join([i for i in metin.split() if i not in etkisiz_kelimeler_kumesi])

    #Metinde tek kalan harfleri de çıkaralım 
    metin = " ".join([i for i in metin.split() if len(i) > 1])

    return metin 



#Databse Bağlantısı
database_name = "article_key"
user_name = "***"
password = "******"
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
    

def cikar():
    db1 = DB() #nesne oluşturma

    baglanti = db1.basla()
    baglanti.autocommit = True
    cursor = baglanti.cursor()
    query_select = "SELECT id,journal_id,article_id,title_tr,abstract_tr  FROM article_metadata where issue_year = 2020 and article_id > 669100 ORDER BY article_id"     
    cursor.execute(query_select)
    articles = cursor.fetchall()
    
    
    for article in articles:
        text1=article[4]
        id=article[0]
        journal_id=article[1]
        article_id=article[2]
        print(article_id)
        time.sleep(4)
        
        text1 = veri_temizleme(text1)
          
        keys = keywords(text1, words=20, lemmatize=True)
        keys = keys.split("\n")
        
        
        for i in keys:
            if len(i) < 50 :
                db_yazdir(id,journal_id,article_id,"gensim",i)
 
           
        print("**************************************")
        #time.sleep(3)
        
    
cikar()
    
    

    