#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from util import *
from socketserver import BaseRequestHandler,ThreadingTCPServer
from multiprocessing import Semaphore
#引入注册状态，已成功和未成功

database_path="accounting.db"
num_of_camera=8
sem=[Semaphore(0)]*num_of_camera
match_state=[False]*num_of_camera
activate_state=[False]*num_of_camera
difference_tmp=[None]*num_of_camera
difference_mutex=Semaphore(1)


def match(data):
    id=data[0]
    distance=data[1]
    person_id=None
    difference_mutex.acquire()
    if activate_state[id]==True:
      euclidean=np.sqrt(np.sum(np.square(difference_tmp[id]+distance),axis=1))
      index=np.argmin(euclidean.flatten())
      value=np.min(euclidean.flatten())
      activate_state[id]=False
      if value<0.6:
         match_state[id]=True
         person_id=index
      else:
         match_state[id]=False
      sem[id].release()
      difference_mutex.release()
    else:
      activate_state[id]=True
      difference_tmp[id]=distance
      difference_mutex.release()
    return person_id


def sign(id):
    sem[id].acquire()
    return match_state[id]


def register(data):
    flag=insert_by_id(data[0],data[1],data[2],data[3])
    return flag


class Handler(BaseRequestHandler):
  def handle(self):
    address,pid = self.client_address
    print('%s connected!'%address)
    while True:
     try:
      data = pickle.loads(self.request.recv(8192))
      if data[0]==0:     #人脸向量匹配
         index=match(data[1])
         if index!=None:
          write_record(index)
      elif data[0]==1:    #注册信息
         flag=register(data[1])
         self.request.sendall(flag)
      else:        #登陆请求信息
         flag=sign(data[1])
         self.request.sendall(flag)
     except:
         break


def run():
  create_table(database_path)
  server = ThreadingTCPServer((backIPaddress,backport),Handler)
  print('listening')
  server.serve_forever()
  print(server)

