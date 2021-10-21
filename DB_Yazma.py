#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 10:04:39 2021

@author: fatih
"""

import psycopg2
import time

class DBYaz():
    
    database_name = "***"
    #database_name = "article_key"
    
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
    

    def olustur(self):
        database_name = "***"
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
        
       # query = "CREATE DATABASE article_subject_id"
       # cursor.execute(query)
        #time.sleep(4)
        
        
        
        database_name = "article_subject_id"
        baglanti = psycopg2.connect(database=database_name,
                                    user=user_name,
                                    password=password,
                                    host=host_ip,
                                    port=host_port)
        
        time.sleep(4)
        
        
        query_create_table="""
        CREATE TABLE IF NOT EXISTS subject_id(
        id bigint,   
        journal_id bigint,
        article_yıl bigint,
        sub_id bigint
        )
        """
        
        baglanti.autocommit = True
        cursor = baglanti.cursor()
        cursor.execute(query_create_table)
        
        time.sleep(4)
        
        print("bitti")
    
    
    def yazdir(self):
        dosya=open("dosya.txt","r")
        
        oku = dosya.read()
        print(type(oku))
        print(oku)
        
        liste = oku.split("\n")
        print("---")
        print(len(liste))
        liste_uzunluk = len(liste)
        
        
        for i in range(liste_uzunluk):
            liste2 = liste[i].split(" ")
            print(liste2)
            id = liste2[0]
            journal_id = liste2[1]
            article_id=liste2[2]
            teknik=liste2[3]
            anahtar_kelime=liste2[4]
        
            print(anahtar_kelime)
        
        
         
        anahtarlar=[
            (id,journal_id,article_id,teknik,anahtar_kelime)]
            
        anahtar_kayıt=", ".join(["%s"] * len(anahtarlar))
            
            
        query_insert = (
            f"INSERT INTO key (id,journal_id,article_id,teknik,anahtar_kelime) VALUES{anahtar_kayıt}"
            )
                
        self.cursor.execute(query_insert,anahtarlar)
        
        print("bitti")
            

            

    def db_sil(self):
        #query_delete ="DELETE FROM key" #tablodaki tüm kayıtları siler
        query_delete ="DELETE FROM key WHERE teknik='position_rank'" #şartlı silme
        self.cursor.execute(query_delete)
        
        
        
        
        
db = DBYaz()
#db.db_sil()
db.olustur()
#db.yazdir()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        