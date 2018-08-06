import socket
import select
import pickle

class Server:


    def __init__(self, connDict):
        self.maxSize = 1024
        self.connDict = connDict

        for connection in self.connDict:
            self.connDict[connection]["socket"] = socket.socket()
            self.connDict[connection]["socket"].settimeout(0)
            self.connDict[connection]["socket"].bind((self.connDict[connection]["selfAddr"], 
                                                      self.connDict[connection]["port"]))
        self.numConns = 0

    def close(self):
      for conn in self.connDict:
        try:
          self.connDict[conn]["socket"].close()
        except:
          pass


    # For any connections no active, connect if connection is available
    # Return nothing
    def refreshConnection(self):
      for connection in self.connDict:
        if self.connDict[connection]["active"] is False:
          # Listen for incomming connection
          self.connDict[connection]["socket"].listen(1)
            
          # check to see if anyone is trying to connect
          ready = select.select([self.connDict[connection]["socket"]], [], [], .25)
          if ready[0]:
            (self.connDict[connection]["conn"], \
              self.connDict[connection]["address"]) = \
                   self.connDict[connection]["socket"].accept()

            self.connDict[connection]["active"] = True
            self.numConns += 1
          else:
            print("No client trying to connect")
        else:
          print("Connection alread active")


    # send pickled object (can take anything as input)
    # Failure: make as inactive, reset socket, return false
    # Success: return true
    def send(self, connName, cmd):
        self.refreshConnection()
        ret_val = False
        try:
            if self.connDict[connName]["active"] is False:
                ret_val = False
            else:
                data = pickle.dumps(cmd)
                ret_val = (self.connDict[connName]["conn"].send(data) > 0)
        except ConnectionResetError:
            # nothing to get
            self.connDict[connName]["active"] = False
            ret_val = False

        return ret_val


    # receive pickled object
    # Failure: make as inactive, reset socket, return None
    # Success: return message
    def recv(self, connName):
        ret_val = None
        if self.connDict[connName]["active"] is not False:
            try:
                msg = self.connDict[connName]["conn"].recv(self.maxSize)
                if msg == '':  # indicates connection is closed
                    self.connDict[connName]["active"] = False
                else:
                    ret_val = pickle.loads(msg)
            except socket.error:
                # nothing to get
                ret_val = None

        return ret_val





