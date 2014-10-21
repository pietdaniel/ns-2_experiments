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

    def get_total_droprate(self, src_adr=None):
        """
         Packet loss / packets sent
        """
        start_time = None
        end_time = None
        total_dropped_packets = 0.0
        total_packets = 0.0

        for packet in self.packets:
            if src_adr is not None and packet[1].src_adr == src_adr:

                if start_time is None:
                    start_time = packet[1].time
                last_packet = packet
                
                total_packets += 1

                if packet[1].abr == 'd':
                    total_dropped_packets += 1


        end_time = last_packet[1].time
        total_time = end_time - start_time

        return float(total_dropped_packets / total_packets)

    def get_total_throughput(self, dest_adr=None):
        """
         Returns bytes/s
        """
        start_time = None
        end_time = None

        total_recieved = 0.0
        for packet in self.packets:
            if dest_adr is not None and packet[1].dest_adr == dest_adr and packet[1].dest_node == dest_adr:

                if start_time is None:
                    start_time = packet[1].time
                last_packet = packet

                total_recieved += packet[1].size

        end_time = last_packet[1].time
        total_time = end_time - start_time

        print total_recieved

        return float(total_recieved / total_time)


    def get_total_latency(self, src_adr=None):
        """
          match times of tcp packets from 0 -> 1 with sqnc_num n
          with ack packets from 1 -> 0 with sqnc_num n

          returns average of all latencies
        """
        pairs = []
        p1 = None
        p2 = None
        sqnc_num = None
        for packet in self.packets:
            if packet[1].name == "tcp" or packet[1].name == "ack":

                if p1 is None and packet[1].src_node == 0:
                    p1 = packet
                    sqnc_num = p1[1].sqnc_num

                if p1 is not None and packet[1].dest_node == 0 and packet[1].sqnc_num == sqnc_num:
                    p2 = packet

            if p1 is not None and p2 is not None:
                pair = (p1,p2)
                pairs.append(pair)
                p1 = None
                p2 = None
                sqnc_num = None

        
        latencies = []
        for pair in pairs:
            delta = pair[1][0] - pair[0][0]
            #print delta
            latencies.append(delta)

        return sum(latencies) / len(latencies)

    def get_throuput(self, delta, src_adr=None):
        pass

    def get_latency(self):
        pass

    def get_drop_rate(self, delta, src_adr=None):
        """
            Returns the drop rate over all packet types
        """
        # count number of drop packets in each time / delta
        bucket={}
        for packet in self.packets:
            if src_adr is not None and packet[1].src_adr == src_adr:
                if packet[1].abr == 'd':
                    t = int(math.floor(packet[1].time / delta))
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
    args = sys.argv
    if args[1] == '-t':
        log_file = open(args[2], 'r')
        s = simulation()
        s.parse_file(log_file)

        dr = s.get_total_droprate(src_adr=0)
        la = s.get_total_latency(src_adr=0)
        tp = s.get_total_throughput(dest_adr=0)

        print "dropped per second"
        print dr
        print "latency seconds"
        print la
        print "throughput b/s"
        print tp

    else:
        for log_file in os.listdir("./logs"):
          f = open("./logs/" + log_file,'r')
    
          s = simulation()
          s.parse_file(f)
          packets = s.get_tcp()
    
          a,b = s.get_drop_rate(.1)
    
          plt.plot(a,b, linewidth=0.5)
    
        plt.savefig('./graphs/foo.png')

