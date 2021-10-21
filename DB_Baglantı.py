#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 09:56:48 2021

@author: fatih



"""


import time
import psycopg2

class DB():
    #Burada iki türlü DB işlemi de olabilir yani şu anda geriye baglantiyi dönderiyoruz ve bu sayede diğer .py uzantılı doysalardan da buna erişip işlemler yapabiliyoruz.
    #Bir diğeri ise geriye üzerinde işlem yapmak üzere gönderdiğimiz articles dir.

    def basla(self):
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
        
        return baglanti

    
"""
        baglanti.autocommit = True
        
        
        
        cursor = baglanti.cursor()

        query_select = "SELECT id,journal_id,article_id,title_tr,abstract_tr  FROM article_metadata where issue_year = 2020 and article_id > 588211 ORDER BY article_id"
        #query_select = "SELECT id,journal_id,article_id,title_tr,abstract_tr  FROM article_metadata where issue_year = 2020 ORDER BY article_id"
        #512190   548319
        
        cursor.execute(query_select)

        articles = cursor.fetchall()

        return articles
    
    """
