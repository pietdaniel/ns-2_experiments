#!/usr/bin/python2
import sys, math, os, pickle, hashlib, subprocess
import matplotlib.pyplot as plt
from Queue import PriorityQueue
from time import time

"""
 woah, look at this pile of dirty python code
 written with time constraints in a late night
 daze, whomever may be stumbling upon this for
 whatever reason I pray for strength in three.
 Surmount this code in order to gain the ability
 to graph parsed ns-2 trace files with python's
 very own matplotlib.
"""

"""
 features to implement
   run tcl script from parse args
   change tcl script to vary init times

   parse run2.tcl files

   graph bi-directional tcp traffic with annotations

"""

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
        # packets come in out of order, order them
        init_packets = []
        for line in the_file:
            p = packet()
            p.parse(line)
            init_packets.append((p.time,p))

        init_packets.sort(lambda x,y: int(10000 * (x[0] - y[0])))

        self.packets = init_packets

    def get_tcp(self):
        """
            Returns a list of just tcp packets
        """
        return filter(lambda x: x[1].name == 'tcp', self.packets)

    def get_total_droprate(self, src_adr=None):
        """
         Packet loss / time
        """
        start_time = None
        end_time = None
        last_packet = None
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


        if last_packet is None:
            return 0.0

        end_time = last_packet[1].time
        total_time = end_time - start_time

        return float(total_dropped_packets / total_time)

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

        return float(total_recieved / total_time)

    def get_throughput(self, delta, dest_adr=None):
        """
          returns array of throughput values for given delta window
        """
        start_time = None
        end_time = None
        total_recieved = 0.0
        output = []
        for packet in self.packets:

            if dest_adr is not None and packet[1].dest_adr == dest_adr and packet[1].dest_node == dest_adr:
                if start_time is None:
                    start_time = packet[1].time

                total_recieved  += packet[1].size

                last_packet = packet

                if last_packet[1].time  - start_time >= delta:
                    output.append((total_recieved,start_time))
                    start_time = None
                    total_recieved = 0.0

        return output


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


    def get_latency(self, delta, src_adr=None):
        """
          returns the average latency within delta
        """
        pairs = []
        p1 = None
        p2 = None
        sqnc_num = None
        start_time = None

        output = []

        for packet in self.packets:

            if p1 is None and packet[1].name == "tcp" and packet[1].src_node == src_adr:
                if start_time is None:
                    start_time = packet[1].time
                p1 = packet
                sqnc_num = p1[1].sqnc_num

            if p1 is not None and packet[1].name == "ack" and packet[1].dest_node == 0 and packet[1].sqnc_num == sqnc_num:
                p2 = packet

            if p1 is not None and p2 is not None:
                pair = (p1,p2)
                pairs.append(pair)
                p1 = None
                p2 = None
                sqnc_num = None

            if start_time is not None and packet[1].time - start_time >= delta:
                p1 = None
                p2 = None
                sqnc_num = None

                latencies = []
                for pair in pairs:
                    diff = pair[1][0] - pair[0][0]
                    latencies.append(diff)

                if len(latencies) != 0:
                    output.append((sum(latencies) / len(latencies), start_time))

                start_time = None

        return output


    def get_droprate(self, delta, src_adr=None):
        """
            Returns the drop rate over all packet types
        """
        # count number of drop packets in each time / delta
        start_time = None
        output = []
        drop_ctr = 0
        for packet in self.packets:
            if src_adr is not None and packet[1].src_adr == src_adr:
                if packet[1].abr == 'd':
                    if start_time is None:
                        start_time = packet[1].time
                    drop_ctr += 1

                if start_time is not None and packet[1].time - start_time >= delta:
                    output.append((drop_ctr, start_time))
                    start_time = None
                    drop_ctr = 0

        return output

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


def graph_exp1(folder):
    t1 = time()
    agent_name = None
    # grab each of the files,
    data = {}

    for filename in os.listdir(folder):
        log_file = open(folder + "/" + filename, 'r')
        q = filename.split("-")
        cbr = q[1]
        agent_name = q[2].replace(".tr","")
        s = simulation()
        print "About to parse file " + folder + "/" + filename
        s.parse_file(log_file)
        data[cbr] = s

    t2 = time()
    print "Parsing done composing graphs " + str(t2 - t1) + " seconds"

    # set up the subplots
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    axes = [ax1, ax2, ax3]
    ax1.set_title("Droprate (lost / sent)")
    ax2.set_title("Latency (seconds)")
    ax3.set_title("Throughput (b/s)")
    
    # displace the boxes so the legends arent cut
    for ax in axes:
        box = ax.get_position()
        ax.set_position([box.x0 - box.width * 0.05 ,box.y0, box.width * 0.9, box.height]) 

    
    for cbr in data.keys():
        print "Constructing graph for " + cbr
        s = data[cbr]

        # get total drop rate, total latency, total through put
        drt = s.get_total_droprate(src_adr=0)
        lat = s.get_total_latency(src_adr=0)
        tpt = s.get_total_throughput(dest_adr=3)

        # get the array of value, time for the given simulation
        dr = s.get_droprate(1.0, src_adr=0)
        la = s.get_latency(0.1, src_adr=0)
        tp = s.get_throughput(0.1, dest_adr=3)

        # turn the array of tuples into a tuple of arrays
        dba, dbb = wobba_fobba(dr)
        laa, lab = wobba_fobba(la)
        tpa, tpb = wobba_fobba(tp)

        # plot the data against time
        ax1.plot(dbb, dba, linewidth=1.0, label=cbr + " CBR\nTotal:" + str(round(drt,4)))
        ax2.plot(lab, laa, linewidth=1.0, label=cbr + " CBR\nTotal:" + str(round(lat,4)))
        ax3.plot(tpb, tpa, linewidth=1.0, label=cbr + " CBR\nTotal:" + str(round(tpt,2)))

    # add the legend
    for ax in [ax1, ax2, ax3]:
        ax.legend(loc="upper left", fontsize='xx-small', bbox_to_anchor=(1.005, 1))

    # create the figure, title, resize, set dpi
    fig = plt.gcf()
    fig.suptitle(agent_name)
    fig.set_size_inches(fig.get_size_inches()[0] + 4, fig.get_size_inches()[1] + 3)
    fig.set_dpi(90)

    # save
    save_file = "./graphs/exp1-"+agent_name+".png"
    print "Saving figure to " + save_file
    fig.savefig(save_file)

    print "Done " + str(time() - t1) + " elapsed seconds"


def graph_exp3(folder):
    t1 = time()

    data = {}
    for filename in os.listdir(folder):
        if ".tr" in filename:
            log_file = open(folder + "/" + filename, 'r')
            filename = filename.replace(".tr","")
            q = filename.split("-")
            queue = q[1]
            agent_name = q[0]
            s = simulation()
            print "About to parse file " + folder + "/" + filename
            s.parse_file(log_file)
            data[queue] = s

    t2 = time()

    print "Parsing done composing graphs " + str(t2 - t1) + " seconds"

    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    axes = [ax1, ax2, ax3]
    ax1.set_title("Droprate (lost / sent)")
    ax2.set_title("Latency (seconds)")
    ax3.set_title("Throughput (b/s)")
    
    for ax in axes:
        box = ax.get_position()
        ax.set_position([box.x0 - box.width * 0.05 ,box.y0, box.width * 0.9, box.height]) 

    for key in data.keys():
        print "Constructing graph for " + key
        s = data[key]
        queue = key

        drt = s.get_total_droprate(src_adr=0)
        lat = s.get_total_latency(src_adr=0)
        tpt = s.get_total_throughput(dest_adr=3)

        dr = s.get_droprate(0.2, src_adr=0)
        la = s.get_latency(0.2, src_adr=0)
        tp = s.get_throughput(0.1, dest_adr=3)

        dba, dbb = wobba_fobba(dr)
        laa, lab = wobba_fobba(la)
        tpa, tpb = wobba_fobba(tp)

        ax1.plot(dbb, dba, linewidth=1.0, label=queue + " Total:\n" + str(round(drt,4)))
        ax2.plot(lab, laa, linewidth=1.0, label=queue + " Total:\n" + str(round(lat,4)))
        ax3.plot(tpb, tpa, linewidth=1.0, label=queue + " Total:\n" + str(round(tpt,2)))

        ax1.get_yaxis().set_view_interval(0, 5)
        
    for ax in [ax1, ax2, ax3]:
        ax.legend(loc="upper left", fontsize='xx-small', bbox_to_anchor=(1.005, 1))

    fig = plt.gcf()
    fig.suptitle(agent_name)
    fig.set_size_inches(fig.get_size_inches()[0] + 4, fig.get_size_inches()[1] + 3)
    fig.set_dpi(90)

    t3 = time()

    print "Saving figure " + str(t3 - t2) + " seconds"

    fig.savefig("./graphs/exp3/"+agent_name+".png")

    t4 = time()

    print "Done " + str(t4 - t1) + " elapsed seconds"


########################################################################

def wobba_fobba(output):
    """
      wobba fobba:
        sort an array of pairs by the second value
        then return a pair of arrays where a[0] is composed
        of pair[0] and a[1] is pair[1]
    """
    # sort array
    output.sort(lambda x,y: int(1000 * (x[1] - y[1])))
    # transformation for matplotlib
    # array[(x,y)] => (array[x],array[y])
    a = map(lambda x:x[0], output)
    b = map(lambda x:x[1], output)
    return (a,b)

def do_single_exp1(arg):
    if arg == "reno":
      graph_exp1("./logs/exp1/reno")
    elif arg == "newreno":
      graph_exp1("./logs/exp1/newreno")
    elif arg == "vegas":
      graph_exp1("./logs/exp1/vegas")
    elif arg == "tahoe":
      graph_exp1("./logs/exp1/tahoe")

def do_exp1():
    run_all_exp1()
    graph_exp1("./logs/exp1/reno")
    graph_exp1("./logs/exp1/newreno")
    graph_exp1("./logs/exp1/vegas")
    graph_exp1("./logs/exp1/tahoe")

def do_single_exp2(arg):
    if arg == "renoreno":
        graph_exp2("./logs/exp2/renoreno", 'reno','reno')
    elif arg == "newrenoreno":
        graph_exp2("./logs/exp2/newrenoreno", 'newreno','reno')
    elif arg == "vegasvegas":
        graph_exp2("./logs/exp2/vegasvegas", 'vegas','vegas')
    elif arg == "newrenovegas":
        graph_exp2("./logs/exp2/newrenovegas", 'newreno','vegas')
    else:
        print "error not valid pairwise combo"

def do_exp2():
    run_all_exp2()
    graph_exp2("./logs/exp2/renoreno", 'reno','reno')
    graph_exp2("./logs/exp2/newrenoreno", 'newreno','reno')
    graph_exp2("./logs/exp2/vegasvegas", 'vegas','vegas')
    graph_exp2("./logs/exp2/newrenovegas", 'newreno','vegas')


def graph_exp2(folder, agent1, agent2):
    t1 = time()
    # parse simulation by cbr refactor this and similar functionality in exp1 graph
    data={}
    for filename in os.listdir(folder):
        log_file = open(folder + "/" + filename, 'r')
        q = filename.split("-")
        cbr = q[1]
        agent_names = q[2].replace(".tr","")
        s = simulation()
        print "About to parse file " + folder + "/" + filename
        s.parse_file(log_file)
        data[cbr] = s

    # create the figure with 3 subplots, sharing time axis
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    axes = [ax1, ax2, ax3]
    ax1.set_title("Droprate (lost / sent)")
    ax2.set_title("Latency (seconds)")
    ax3.set_title("Throughput (b/s)")

    for ax in axes:
        box = ax.get_position()
        ax.set_position([box.x0 - box.width * 0.05 ,box.y0, box.width * 0.9, box.height]) 

    # for each cbr plot the two tcp agents
    #  agents are defined by src_adr 
    #  where the network topology is defined as follows
    #  4        5
    #   \      / 
    #    1----2
    #   /      \
    #  0        3
    #  cbr 1 -> 2
    #  tcp 0 -> 3 , first arg
    #  tcp 4 -> 5 , second arg

    t2 = time()

    color_ctr = 0.17
    for cbr in data.keys():
        s = data[cbr]

        # get the first tcp agents droprate and throughput
        drt0 = s.get_total_droprate(src_adr=0)
        lat0 = s.get_total_latency(src_adr=0)
        tpt0 = s.get_total_throughput(dest_adr=3)

        dr0 = s.get_droprate(0.5, src_adr=0)
        la0 = s.get_latency(0.2, src_adr=0)
        tp0 = s.get_throughput(0.1, dest_adr=3)

        # get the second tcp agents droprate and throughput
        drt4 = s.get_total_droprate(src_adr=4)
        lat4 = s.get_total_latency(src_adr=4)
        tpt4 = s.get_total_throughput(dest_adr=5)

        dr4 = s.get_droprate(0.5, src_adr=4)
        la4 = s.get_latency(0.2, src_adr=4)
        tp4 = s.get_throughput(0.1, dest_adr=5)

        # do the wobba fobba against both data sets
        dba0, dbb0 = wobba_fobba(dr0)
        laa0, lab0 = wobba_fobba(la0)
        tpa0, tpb0 = wobba_fobba(tp0)

        dba4, dbb4 = wobba_fobba(dr4)
        laa4, lab4 = wobba_fobba(la4)
        tpa4, tpb4 = wobba_fobba(tp4)

        # plot both data sets against the same graph
        color1 = (1-color_ctr, color_ctr/4.0, 1-color_ctr)
        color2 = (1-color_ctr, color_ctr, color_ctr)

        label1 = "1 " + agent1 + " " + cbr + " CBR Total:" 
        label2 = "2 " + agent2 + " " + cbr + " CBR Total:" 

        ax1.plot(dbb0, dba0, linewidth=0.80, color=color1,\
            label=label1 + str(round(drt0,4)))

        ax2.plot(lab0, laa0, linewidth=0.80, color=color1,\
            label=label1 + str(round(lat0,4)))

        ax3.plot(tpb0, tpa0, linewidth=0.80, color=color1,\
            label=label1 + str(round(tpt0,2)))


        ax1.plot(dbb4, dba4, linewidth=0.90, color=color2,\
            label=label2 + str(round(drt0,4)))

        ax2.plot(lab4, laa4, linewidth=0.90, color=color2,\
            label=label2 + str(round(lat0,4)))

        ax3.plot(tpb4, tpa4, linewidth=0.90, color=color2,\
            label=label2 + str(round(tpt0,2)))

        color_ctr += 0.17


    for ax in [ax1, ax2, ax3]:
        ax.legend(loc="upper left", fontsize='xx-small', bbox_to_anchor=(1.005, 1))

    fig = plt.gcf()
    fig.suptitle(agent1 + "vs" + agent2)
    fig.set_size_inches(fig.get_size_inches()[0] + 4, fig.get_size_inches()[1] + 3)
    fig.set_dpi(90)

    t3 = time()

    print "Saving figure " + str(t3 - t2) + " seconds"

    fig.savefig("./graphs/exp2-"+ agent1 + "-" + agent2 +".png")

    t4 = time()
    print "Done " + str(t4 - t1) + " elapsed seconds"



def run_all_exp2():
    cbrs = ['1mb','3mb','5mb','7mb','8mb']
    pairs = [('reno','reno') \
            ,('newreno','reno')\
            ,('vegas','vegas')\
            ,('newreno','vegas')]
    for cbr in cbrs:
        for pair in pairs:
            run_exp2_tcl(pair[0],pair[1],cbr)

def run_exp2_tcl(agent1, agent2, cbr):
    subprocess.call(["ns",'exp2.tcl', agent1, agent2, cbr])

def run_all_exp1():
    cbrs = ['1mb', '2mb', '3mb', '4mb', '5mb', '6mb', '7mb', '8mb', '9mb']
    agents = ['reno', 'newreno', 'tahoe', 'vegas']
    for cbr in cbrs:
      for agent in agents:
        run_exp1_tcl(agent, cbr)

def run_exp1_tcl(agent1, cbr):
    subprocess.call(["ns",'exp1.tcl', agent1, cbr])

if __name__ == "__main__":
    args = sys.argv

    if args[1] == "-exp3":
        graph_exp3("./logs/exp3/reno")
        graph_exp3("./logs/exp3/sack")

    if args[1] == "-exp2":
        if len(args) >= 3:
            do_single_exp2(args[2])
        else:
            do_exp2()

    elif args[1] == '-exp1':
        if len(args) >= 3:
            do_single_exp1(args[2])
        else:
            do_exp1()
