#!/usr/bin/python2
import sys, math, os
import matplotlib.pyplot as plt
from Queue import PriorityQueue

class simulation:
    """
      A class which represents a single simulation
    """
    def __init__(self):
        self.packets = list()

    def parse_file(self, the_file):
        """
          turns a fileinto a sorted list of packets by time
        """
        init_packets = PriorityQueue()

        # packets come in out of order, order them
        # via priority queue
        for line in the_file:
            p = packet()
            p.parse(line)
            init_packets.put((p.time,p))

        # PriorityQueue => ordered list
        while not init_packets.empty():
            self.packets.append(init_packets.get())

    def get_tcp(self):
        """
            Returns a list of just tcp packets
        """
        return filter(lambda x: x[1].name == 'tcp', self.packets)

    def get_drop_rate(self, delta):
        """
            Returns the drop rate over all packet types
        """
        # count number of drop packets in each time / delta
        bucket={}
        for packet in self.packets:
            t = int(math.floor(packet[1].time / delta))
            if packet[1].abr == 'd':
                if t in bucket:
                    bucket[t] = bucket[t] + 1
                else:
                    bucket[t] = 1

        # turn dict into array of (bucket,bucket_ctr)
        output = []
        for i in bucket.keys():
            output.append((i,bucket[i]))

        # sort array
        output.sort(lambda x,y: x[0] - y[0])

        # transformation for matplotlib
        # array[(x,y)] => (array[x],array[y])
        a = map(lambda x:x[0], output)
        b = map(lambda x:x[1], output)

        return (a,b)

class packet:
  """
    A class used to represent ns-2 packets

      Abbreviation
        r: Receive
        d: Drop
        e: Error
        +: Enqueue
        -: Dequeue  
    
      Type : Value 
        double  Time
        int   (Link-layer) Source Node
        int   (Link-layer) Destination Node
        string  Packet Name
        int   Packet Size
        string  Flags
        int   Flow ID
        int   (Network-layer) Source Address
        int   Source Port
        int   (Network-layer) Destination Address
        int   Destination Port
        int   Sequence Number
        int   Unique Packet ID 
    
      Format
        %g %d %d %s %d %s %d %d.%d %d.%d %d %d
    
      Example
        r 9.051952 2 1 ack 40 ------- 0 3.0 0.0 2444 10206
  """
  def __init__(self):
    self.abr = None
    self.time = None
    self.src_node = None
    self.dest_node = None
    self.name = None
    self.size = None
    self.flags = None
    self.flow_id = None
    self.src_adr = None
    self.src_port = None
    self.dest_adr = None
    self.dest_port = None
    self.sqnc_num = None
    self.upacket_id = None
    self.raw = None

  def parse(self, string):
    args = string.split()
    self.abr = str(args[0])
    self.time = float(args[1])
    self.src_node = int(args[2])
    self.dest_node = int(args[3])
    self.name = str(args[4])
    self.size = int(args[5])
    self.flags = str(args[6])
    self.flow_id = int(args[7])
    self.src_adr = int(args[8].split('.')[0])
    self.src_port = int(args[8].split('.')[1])
    self.dest_adr = int(args[9].split('.')[0])
    self.dest_port = int(args[9].split('.')[1])
    self.sqnc_num = int(args[10])
    self.upacket_id = int(args[11])
    self.raw = string

  def get_abr_as_int(self):
      """
        r: Receive 0
        d: Drop    1
        e: Error   2
        +: Enqueue 3
        -: Dequeue 4
      """
      return {
              'r':0,
              'd':1,
              'e':2,
              '+':3,
              '-':4,
             }[self.abr]

  def __str__(self):
    return self.raw


if __name__ == "__main__":

    for log_file in os.listdir("./logs"):
      f = open("./logs/" + log_file,'r')

      s = simulation()
      s.parse_file(f)
      packets = s.get_tcp()

      a,b = s.get_drop_rate(.1)

      plt.plot(a,b, linewidth=0.5)

    plt.savefig('./graphs/foo.png')

