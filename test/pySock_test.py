import sys
sys.path.append("../src")

import unittest
from threading import Thread
from server import Server
from client import Client

single_conn = { 
"CLIENT": 
    {
    "active": False,
    "conn": None,
    "selfAddr": "127.0.0.1",
    "address": "127.0.0.1",
    "port": 1500,
    "socket": None 
    }
}

multi_conn = { 
"CLIENT_1": 
    {
    "active": False,
    "conn": None,
    "selfAddr": "127.0.0.1",
    "address": "127.0.0.1",
    "port": 1601,
    "socket": None 
    },
"CLIENT_2": 
    {
    "active": False,
    "conn": None,
    "selfAddr": "127.0.0.1",
    "address": "127.0.0.1",
    "port": 1602,
    "socket": None 
    }

}


class test_client_no_server(unittest.TestCase):
 
  def test_init(self):
    c = Client()
    assert c.active == False
    c.close()

  def test_connect_fail(self):
    c = Client()
    assert c.connect("127.0.0.1",1555) == False
    assert c.refreshConnect() == False
    c.close()
    

  def test_send_fail(self):
    c = Client()
    msg = "hello"
    assert c.send(msg) == False
    c.close()
  
  def test_recv_faile(self):
    c = Client()
    ret = c.recv()
    assert ret == None 
    c.close()
 

class test_server_no_client(unittest.TestCase):
 
  def test_init(self):
    s = Server(single_conn)
    assert s.numConns == 0
    s.close()

  def test_send_fail(self):
    s = Server(single_conn)
    msg = "hello"
    assert s.send("CLIENT", msg) == False
    s.close()
  
  def test_recv_faile(self):
    s = Server(single_conn)
    ret = s.recv("CLIENT")
    assert ret == None 
    s.close()

  def test_run_refresh(self):
    s = Server(single_conn)
    s.refreshConnection()
    s.close()
    
     
class test_client_and_server(unittest.TestCase):

 def test_comms(self):
    s = Server(single_conn)
    c = Client()
    
    # Connect client and server
    thr = Thread(target= s.refreshConnection)
    thr.start()
    assert c.connect("127.0.0.1", 1500) == True
    thr.join()

    # Client to server  
    wbuf = "hello"
    rbuf = ''
    assert wbuf != rbuf
    c.send(wbuf)
    rbuf = s.recv("CLIENT")
    assert wbuf == rbuf
   
    # Server to client
    wbuf = "hello again"
    assert wbuf != rbuf
    s.send("CLIENT", wbuf)
    rbuf = c.recv()
    assert wbuf == rbuf

    # Close connections
    s.close()
    c.close()  


class test_multiclient_and_server(unittest.TestCase):

 def test_comms(self):
    s = Server(multi_conn)
    c_1 = Client()
    c_2 = Client()
    
    # Connect clients and server
    thr_1 = Thread(target= s.refreshConnection)
    thr_1.start()
    assert c_1.connect("127.0.0.1", 1601) == True
    thr_1.join()

    thr_2 = Thread(target= s.refreshConnection)
    thr_2.start()
    assert c_2.connect("127.0.0.1", 1602) == True
    thr_2.join()

    # Client 1 to server  
    wbuf = "hello"
    rbuf = ''
    assert wbuf != rbuf
    c_1.send(wbuf)
    rbuf = s.recv("CLIENT_1")
    assert wbuf == rbuf
   
    # Server to client 2
    wbuf = "hello again"
    assert wbuf != rbuf
    s.send("CLIENT_1", wbuf)
    rbuf = c_1.recv()
    assert wbuf == rbuf

    
    # Client 2 to server  
    wbuf = "hello"
    rbuf = ''
    assert wbuf != rbuf
    c_2.send(wbuf)
    rbuf = s.recv("CLIENT_2")
    assert wbuf == rbuf
   
    # Server to client 2
    wbuf = "hello again"
    assert wbuf != rbuf
    s.send("CLIENT_2", wbuf)
    rbuf = c_2.recv()
    assert wbuf == rbuf


    # Close connections
    s.close()
    c_1.close()  
    c_2.close()  


