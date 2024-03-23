#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)

    coreSwitch = self.addSwitch('s1')
   
    #Faculty LAN
    facultySwitch = self.addSwitch('s2')
    facultyPC = self.addHost('facultyPC', ip='10.0.1.4/24',defaultRoute="facultyPC-eth1")
    self.addLink(facultyPC, facultySwitch, port1=1, port2=3)

    printer = self.addHost('printer', ip='10.0.1.3/24',defaultRoute="printer-eth1")
    self.addLink(printer, facultySwitch, port1=1, port2=2)

    facultyWS = self.addHost('facultyWS', ip='10.0.1.2/24',defaultRoute="facultyWS-eth1")
    self.addLink(facultyWS, facultySwitch, port1=1, port2=5)

    self.addLink(facultySwitch, coreSwitch, port1=4, port2=2)

    #Student Housing LAN
    studentSwitch = self.addSwitch('s5')
    studentPC = self.addHost('studentPC', ip='10.0.2.2/24',defaultRoute="studentPC-eth1")
    self.addLink(studentPC, studentSwitch, port1=1, port2=2)

    labWS = self.addHost('labWS', ip='10.0.2.3/24',defaultRoute="labWS-eth1")
    self.addLink(labWS, studentSwitch, port1=1, port2=3)

    self.addLink(studentSwitch, coreSwitch, port1=4, port2=5)

    #IT Department LAN
    itSwitch = self.addSwitch('s4')
    itWS = self.addHost('itWS', ip='10.0.3.2/24',defaultRoute="itWS-eth1")
    self.addLink(itWS, itSwitch, port1=1, port2=2)

    itPC = self.addHost('itPC', ip='10.0.3.3/24',defaultRoute="itPC-eth1")
    self.addLink(itPC, itSwitch, port1=1, port2=3)

    self.addLink(itSwitch, coreSwitch, port1=4, port2=4)

    #University Data Center
    dataCenterSwitch = self.addSwitch('s3')
    examServer = self.addHost('examServer', ip='10.0.100.2/24',defaultRoute="examServer-eth1")
    self.addLink(examServer, dataCenterSwitch, port1=1, port2=5)

    webServer = self.addHost('webServer', ip='10.0.100.3/24',defaultRoute="webServer-eth1")
    self.addLink(webServer, dataCenterSwitch, port1=1, port2=2)

    dnsServer = self.addHost('dnsServer', ip='10.0.100.4/24',defaultRoute="dnsServer-eth1")
    self.addLink(dnsServer, dataCenterSwitch, port1=1, port2=3)

    self.addLink(dataCenterSwitch, coreSwitch, port1=4, port2=3)

    #Internet
    trustedPC = self.addHost('trustedPC', ip='200.20.203.2/32', defaultRoute="trustedPC-eth1")
    self.addLink(trustedPC, coreSwitch, port1=1, port2=7)

    guestPC = self.addHost('guestPC', ip='200.20.198.2/32', defaultRoute="guestPC-eth1")
    self.addLink(guestPC, coreSwitch, port1=1, port2=6)

    discord = self.addHost('discord', ip='200.20.193.2/32', defaultRoute="discord-eth1")
    self.addLink(discord, coreSwitch, port1=1, port2=8)




if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet