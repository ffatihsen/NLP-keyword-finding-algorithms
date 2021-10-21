#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 10:14:27 2021

@author: fatih
"""




from position_rank import position_rank

from tokenizer import StanfordCoreNlpTokenizer
import time

from  DB_Baglantı import  DB
import psycopg2



db1 = DB()

baglanti = db1.basla()
baglanti.autocommit = True
        
        
        
cursor = baglanti.cursor()

query_select = "SELECT id,journal_id,article_id,title_tr,abstract_tr  FROM article_metadata where issue_year = 2020 and article_id > 832260 ORDER BY article_id"
        
        
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


try:
    

    def db_yazdir(id,journal_id,article_id,teknik,anahtar_kelime):
        
        
        anahtarlar=[
                (id,journal_id,article_id,teknik,anahtar_kelime)]
                
        anahtar_kayıt=", ".join(["%s"] * len(anahtarlar))
                
                
        query_insert = (
            f"INSERT INTO key (id,journal_id,article_id,teknik,anahtar_kelime) VALUES{anahtar_kayıt}"
                )
                    
        cursor.execute(query_insert,anahtarlar)
        
    

    for article in articles:
        title=article[3]
        abstract=article[4]
        id=article[0]
        journal_id=article[1]
        article_id=article[2]
        print(article_id)
        time.sleep(1)
    
        abstract = abstract.replace("_","")
        abstract = abstract.replace("-", "")
        abstract = abstract.replace("(", "")
        abstract = abstract.replace(")", "")
        abstract = abstract.replace("%", "")
    
    
        tokenizer = StanfordCoreNlpTokenizer("http://localhost", port=9000)
        #time.sleep(3)
    
    
        anahtar_liste = position_rank(title + abstract, tokenizer)
        anahtar_liste_temiz=[]
        
        
    
        for anahtar in anahtar_liste:
            anahtar_liste_temiz.append(anahtar.replace("_"," "))
            if len(anahtar.replace("_"," ")) < 50 :
                db_yazdir(id,journal_id,article_id,"position_rank",anahtar.replace("_"," "))
            #time.sleep(1)  
        
    
    
    
        print("-----------------------------------")
        #time.sleep(2)

except :
    print("hata verdi ->",journal_id)










































