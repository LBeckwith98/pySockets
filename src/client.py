import socket
import pickle

class Client:


  def __init__(self):
    self.maxSize = 1024
    self.client = None
    self.active = False
    self.address = None
    self.port = None


  def close():
    self.client.close()

  # Connect on address, returns true if successful
  def connect(self, address, port):
    ret_val = False

    self.client = socket.socket()
    self.client.settimeout(5)
    self.address = address
    self.port = port
    try:
      self.client.connect((self.address, int(self.port))) 
      if self.client.recv(0) == '':
        ret_val = False
        print("connection failed")
      else:
        # Check if connection was successful
        self.active = True
        ret_val = True
    except Exception as e:
      self.client=socket.socket()
      self.active = False
      ret_val = False
      print("Connection failed: {}".format(e))
    return ret_val


  # if connection is not active, try to connect again
  # returns true if socket is connected
  def refreshConnect(self):
    ret_val = True
    if self.active == False:
      try:
        self.client.connect((self.address,self.port))
        self.active = True
      except:
        self.client = socket.socket()
        self.active = False
        ret_val = False  
    else:
      ret_val = True # already connected

    return ret_val

  # send pickled
  # Failure: make as inactive, reset socket, return false
  # Success: return true
  def send(self, msg):
    ret_val = False
    try:
      if self.active:
        data = pickle.dumps(msg)
        self.client.send(data)
        ret_val = True
      else:
        ret_val = False

    except ConnectionResetError:
      # connect is bad
      self.client = socket.socket()
      self.active = False
      ret_val = False
    
    return ret_val

  # receive pickled
  # Failure: make as inactive, reset socket, return None
  # Success: return message
  def recv(self):
    ret_val = None
    if self.active is True:
      try:
        msg = self.client.recv(self.maxSize)
        if msg == '':  # indicates connection is closed
          self.client=socket.socket()
          self.active = False
          ret_val = None
        else:
          ret_val = pickle.loads(msg)

      except socket.error:
        # nothing to get
        ret_val = None
    else:
      ret_val = None

    return ret_val

  def close(self):
    if self.active:
      self.client.close()

