import pandas as pd
import sqlite3
import csv
import mysql.connector

def flood_items_t1(file_name):
    # con = sqlite3.connect("db.sqlite3")
    con = mysql.connector.connect(
    user="root",
    password = "",
    host = "localhost",
    database="enquiry_db")
    cur = con.cursor()
    a_file = open(file_name,"r")
    rows = csv.reader(a_file)
    header = next(rows)
    print(next(rows))
    # query1 = cur.execute("Select * from enquiry_enquiry")
    # print(cur.fetchall())
    # query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MRP,BP,MOQ) VALUES (?,?,?,?,?)",rows) for db.sqlite3
    query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MRP,BP,MOQ) VALUES (%s, %s, %s, %s, %s)",rows) # for mysql
    print("insertion complete")
    con.commit()
    con.close()

def flood_items_t2(file_name):
    # con = sqlite3.connect("db.sqlite3")
    con = mysql.connector.connect(
    user="root",
    password = "",
    host = "localhost",
    database="enquiry_db")
    cur = con.cursor()
    a_file = open(file_name,"r")
    rows = csv.reader(a_file)
    header = next(rows)
    print(next(rows))
    # query1 = cur.execute("Select * from enquiry_enquiry")
    # print(cur.fetchall())
    # query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MRP,BP,MOQ) VALUES (?,?,?,?,?)",rows)
    query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MRP,BP,MOQ) VALUES (%s, %s, %s, %s, %s)",rows)
    print("insertion complete")
    con.commit()
    con.close()

if __name__ == '__main__':
    # clean_data('chunk.csv')
    # flood("chunk.csv")
    # merge("Enquiry_data.csv","chunk.csv")
    # clean_data2("chunk.csv")
    # flood_items_t1("itemst1.csv")
    flood_items_t2("T2_PriceList.csv")