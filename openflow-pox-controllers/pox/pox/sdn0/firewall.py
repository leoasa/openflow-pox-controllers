# Openflow POX controller -- rule-based firewall
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet

    arp = packet.find('arp')
    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    udp = packet.find('udp')
    facultyWS_ip = '10.0.1.2'
    facultyPC_ip = '10.0.1.4'
    itWS_ip = '10.0.3.2'
    itPC_ip = '10.0.3.3'
    studentPC_ip = '10.0.2.2'
    labWS_ip = '10.0.2.3'
    examServer_ip = '10.0.100.2'
    webServer_ip = '10.0.100.3'
    dnsServer_ip = '10.0.100.4'
    printer_ip = '10.0.1.3'
    guestPC_ip = '10.0.198.2'
    trustedPC_ip = '10.0.203.2'
    access_ip_list = [facultyPC_ip, facultyWS_ip, itWS_ip, itPC_ip, studentPC_ip, labWS_ip]


    def accept():
      # Write code for an accept function
      rule = of.ofp_flow_mod()
      rule.match = of.ofp_match.from_packet(packet)
      rule.idle_timeout = 45
      rule.hard_timeout = 400
      rule.buffer_id = packet_in.buffer_id
      rule.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      rule.data = packet_in
      self.connection.send(rule)

      print("Packet Accepted - Flow Table Installed on Switches")

    def drop():
      # Write code for a drop function
      rule = of.ofp_flow_mod()
      rule.match = of.ofp_match.from_packet(packet)
      rule.idle_timeout = 45
      rule.hard_timeout = 45
      rule.buffer_id = packet_in.buffer_id
      self.connection.send(rule)
      print("Packet Dropped - Flow Table Installed on Switches")

    # Write firewall code 
    
    # Rule 1  
    if arp:
      accept()

    # Rule 2
    elif icmp:
      #Rule for question 10a simple DoS prevention
      ip = packet.find('ipv4')
      if ip.dstip == dnsServer_ip:
        drop()
      else:
        accept()

    #Rules 3-10
    elif tcp or udp:
      ip = packet.find('ipv4')

      if tcp:
        #3 and 4
        if (ip.srcip in access_ip_list and ip.dstip == webServer_ip) or (ip.srcip == webServer_ip and ip.dstip in access_ip_list):
          accept()

        #5 and 6
        elif (ip.srcip in [facultyWS_ip, facultyPC_ip] and ip.dstip == examServer_ip) or (ip.srcip == examServer_ip and ip.dstip in [facultyWS_ip, facultyPC_ip]):
          accept()

        #Rule for question 10b
        elif (ip.srcip in [facultyWS_ip, labWS_ip, itWS_ip] and ip.dstip == printer_ip) or (ip.dstip in [facultyWS_ip, labWS_ip, itWS_ip] and ip.srcip == printer_ip):
          accept()

        #Rules for question 10c webServer access
        elif (ip.srcip in [guestPC_ip, trustedPC_ip] and ip.dstip == webServer_ip) or (ip.dstip in [guestPC_ip, trustedPC_ip] and ip.srcip == webServer_ip):
          accept()

      #UDP rules
      else:
        #9 and 10
        if (ip.srcip in access_ip_list and ip.dstip == dnsServer_ip) or (ip.dstip in access_ip_list and ip.srcip == dnsServer_ip):
          accept()


        #Rule for question 10c dnsServer access
        elif (ip.srcip in [guestPC_ip, trustedPC_ip] and ip.dstip == dnsServer_ip) or (ip.dstip in [guestPC_ip, trustedPC_ip] and ip.srcip == dnsServer_ip):
          accept()


      #7 and 8
      if (ip.srcip in access_ip_list and ip.dstip in [itWS_ip, itPC_ip]) or (ip.dstip in access_ip_list and ip.srcip in [itWS_ip, itPC_ip]):
        accept()

      #Broader access for trustedPC rule for question 10c
      elif (ip.srcip == trustedPC_ip and ip.dstip in [studentPC_ip, labWS_ip]) or (ip.dstip == trustedPC_ip and ip.srcip in [studentPC_ip, labWS_ip]):
        accept()

    else:
      drop()

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the components
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)