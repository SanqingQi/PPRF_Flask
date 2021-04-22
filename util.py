#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import datetime
import time
import random
import socket
import sqlite3
from threading import Thread
import queue
import pickle

backIPaddress="127.0.0.1"
backport=9090
middleIPaddress1="127.0.0.1"
middleport1=9090
middleIPaddress2="127.0.0.1"
middleport2=9090

img_path="Your Path"
Q = 23740629843760239486723
BASE = 2
PRECISION_INTEGRAL = 16
PRECISION_FRACTIONAL = 32

def get_count(db_name="PPRF_Info",table_name="userInfo"):
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute("SELECT Count(*) from userInfo")
    for i in cursor:
        ans=i
    print("Table inserted successfully")
    conn.commit()
    conn.close()
    return ans

def select_by_index(start_index=0,num=8,db_name="PPRF_Info",table_name="userInfo"):
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    ans=[]
    cursor = c.execute("SELECT * from userInfo limit ?,?",(start_index,num))
    for i in cursor:
        ans.append(i)
    print("Table inserted successfully")
    conn.commit()
    conn.close()
    return ans

def insert(ID=0,userName='未知',Age=0,Department="未知", db_name="PPRF_Info",table_name="userInfo"):
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute("INSERT INTO userInfo (ID,Age,userName,Department) \
      VALUES (?, ?, ?, ?)",(int(ID),Age,userName,Department))
    print("Table inserted successfully")
    conn.commit()
    conn.close()

def create_table(db_name="PPRF_Info"):
    """
    :param db_name: str name of db
    :return: void
    test_info: Success
    """
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE userInfo
       (ID INT PRIMARY KEY     NOT NULL,
       Age INT NOT NULL,
       userName            CHAR(150)     NOT NULL,
       Department       CHAR(100)   NOT NULL
       );''')
    print("Table created successfully")
    conn.commit()
    conn.close()

def select_by_id(id=1,db_name="PPRF_Info", table_name="userInfo"):
    """
    :param db_name: str
    :param attr: str name of selected attribute
    :return:
    test_info: Success
    """
    id=int(id)
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    ans="无"
    cursor=''
    cursor = c.execute("SELECT ID, Age, userName, Department from userInfo WHERE ID=?", (id,))
    for i in cursor:
        ans=i
    conn.commit()
    conn.close()
    return ans

def delete_by_id(id=1,db_name="PPRF_Info", table_name="userInfo"):
    """
    :param db_name: str name of database
    :param id: int
    :return: Null
    test_info: Success
    """
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")
    c = conn.cursor()
    if table_name=="PrivacyVector":
        c.execute('''Delete From userInfo Where ID = ?''', (id,))
    print("Delete successfully")
    conn.commit()
    conn.close()

def insert_by_id(db_name,table_name,ID='',U_NAME='',Embedding='',ImagePath='',Password=''):
    """
    :param db_name: str name of database
    :param id: int
    :return: Null
    test_info: Success
    """
    conn = sqlite3.connect(db_name)
    print("Opened database successfully")

    c = conn.cursor()
    cursor=''
    if table_name=="PrivacyVector":
     cursor = c.execute('''SELECT ? From PrivacyVector Where ID = ?''', ("*",ID))
    elif table_name=="PrivacyID":
     cursor = c.execute('''SELECT ? From PrivacyID Where ID = ?''', ("*",ID))
    if  not cursor:
     insert(db_name,table_name,ID=ID,U_NAME=U_NAME,Embedding=Embedding,ImagePath=ImagePath,Password=Password)
     print("Insert successfully")
    else:
     print("Insert fail")
    conn.commit()
    conn.close()


def share(secret):
    secret=secret * BASE ** PRECISION_FRACTIONAL #把小数转换为整数
    a1=Q*random.random()
    share_1=(secret+a1*1)%Q
    share_2=(secret+a1*2)%Q
    share_1=share_1.astype('float64')
    share_2=share_2.astype('float64')
    return share_1,share_2

def decode(share_1,share_2):
    result=share_1*2-share_2
    map_negative_range = np.vectorize(lambda element: element if element <= Q / 2 else element - Q)
    return map_negative_range(result) / BASE ** PRECISION_FRACTIONAL

def write_record(index):
    ans=select_by_index(index,1)[0]
    ID=ans[0]
    name=ans[2]
    age=ans[1]
    Department=ans[3]
    now_time = str(datetime.datetime.now())
    now_time = now_time.split(' ')[0].split('-')
    year = now_time[0]
    month = str(int(now_time[1]))
    day = now_time[2]
    hour=time.localtime().tm_hour
    min=time.localtime().tm_min
    info=name+'-'+str(ID)+'-'+str(age)+'-'+Department+'-'+str(hour)+':'+str(min)+'\n'
    fileName = 'record/' + year + '_' + month + '_' + day + '.txt'
    with open(fileName, 'w+', encoding='utf-8') as f:
        f.write(info)

def np2img(array):
    """
    把矩阵转换为图片
    test_info: Success
    """
    array = np.array(array, dtype='uint8')
    image = Image.fromarray(array)
    image.show()


def file2np(fileName, d_type='float64', shape=None):
    """
    字符串转换为numpy数组
    array_str: str
    array_size: numpy array
    test_info: Success
    """
    if shape is None:
        array = np.fromfile(fileName, dtype=d_type)
    else:
        array = np.fromfile(fileName, dtype=d_type).reshape(shape)
    return array

#send encoded data
def send_data(client_socket,data):
  client_socket.sendall(pickle.dumps(data))

#listen to and receive decoded data
def receive_data(client_socket):
  while True:
   recv_data=client_socket.recv(1024)
   if recv_data:
     return recv_data
