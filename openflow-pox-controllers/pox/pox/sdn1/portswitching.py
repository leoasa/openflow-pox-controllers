# Openflow POX controller with port switching

from pox.core import core

import pox.openflow.libopenflow_01 as of

from netaddr import IPNetwork

log = core.getLogger()

class Routing (object):
    
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # def inSameSubnet(ip1, ip2):
    #   return ip1 in IPNetwork(str(ip2))

    def get_subnet_port(destination_ip):
      ip_to_port = {
        '10.0.1.2': 5,
        '10.0.1.3': 2,
        '10.0.1.4': 3,
        '10.0.100.2': 5,
        '10.0.100.3': 2,
        '10.0.100.4': 3,
        '10.0.3.2': 2,
        '10.0.3.3': 3,
        '10.0.2.2': 2,
        '10.0.2.3': 3
      }
      return ip_to_port[destination_ip]

    def forward(end_port):
      # Write code for a forward function
      rule = of.ofp_flow_mod()
      rule.match = of.ofp_match.from_packet(packet)
      rule.idle_timeout = 45
      rule.hard_timeout = 45
      rule.buffer_id = packet_in.buffer_id
      rule.actions.append(of.ofp_action_output(port=end_port))
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

      # Your code here
    ip = packet.find('ipv4')
    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    udp = packet.find('udp')
    arp = packet.find('arp')
    student_subnet = IPNetwork("10.0.2.0/24")
    faculty_subnet = IPNetwork("10.0.1.0/24")
    it_subnet = IPNetwork("10.0.3.0/24")
    dataCenter_subnet = IPNetwork("10.0.100.0/24")
    trustedPC_ip = '200.20.203.2'
    examServer_ip = '10.0.100.2'
    discord_ip = '200.20.193.2'
    end_port = None

    if arp:
      forward(of.OFPP_NORMAL)
      return

    if ip:

      src_ip = str(ip.srcip)
      dst_ip = str(ip.dstip)


    # Core Switch Routes
      if switch_id == 1:

        if icmp or tcp or udp:

          if src_ip in student_subnet and dst_ip == discord_ip:
            forward(8)
            return

          if port_on_switch == 8 and dst_ip in student_subnet:
            forward(5)
            return

          if icmp:
            if dst_ip in faculty_subnet:
              end_port = 2
            elif dst_ip in student_subnet:
              end_port = 5
            elif dst_ip in it_subnet:
              end_port = 4

          elif tcp:
            if dst_ip in faculty_subnet:
              end_port = 2
            elif dst_ip in dataCenter_subnet:
              if dst_ip == examServer_ip and src_ip not in faculty_subnet:
                drop()
                return
              else:
                end_port = 3
            elif dst_ip in it_subnet:
              end_port = 4
            elif dst_ip in student_subnet:
              end_port = 5
            elif dst_ip == trustedPC_ip:
              end_port = 7

          else:
            if port_on_switch == 7 or port_on_switch == 6:
              drop()
              return
            elif dst_ip in faculty_subnet:
              end_port = 2
            elif dst_ip in dataCenter_subnet:
              end_port = 3
            elif dst_ip in it_subnet:
              end_port = 4
            elif dst_ip in student_subnet:
              end_port = 5
            else:
              drop() #Internet host UDP packets should be dropped
              return
 
    # Switch 2 (Faculty) Routes
      elif switch_id == 2:
        
        if icmp or tcp or udp:
          if dst_ip in faculty_subnet:
            end_port = get_subnet_port(dst_ip)

          else:
            end_port = 4


    # Switch 3 (Data Center) Routes
      elif switch_id == 3:
        if icmp or tcp or udp:
          if dst_ip in dataCenter_subnet:
            end_port = get_subnet_port(dst_ip)
          else:
            end_port = 4


    # Switch 4 (IT) Routes
      elif switch_id == 4:
        if icmp or tcp or udp:
          if dst_ip in it_subnet:
            end_port = get_subnet_port(dst_ip)
          else:
            end_port = 4


    # Switch 5 (Student) Routes
      elif switch_id == 5:
        if icmp or tcp or udp:
          if dst_ip in student_subnet:
            end_port = get_subnet_port(dst_ip)

          else:
            end_port = 4

    if end_port:
      forward(end_port)

    else:
      drop()

  def _handle_PacketIn(self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
