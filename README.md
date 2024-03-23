# openflow-pox-controllers
Python3 Openflow POX controller with Mininet topologies. POX documentation from https://github.com/noxrepo/pox. Custom topology and firewall files can be found in pox/pox/sdn0 and pox/pox/sdn1. Descriptions can found in pox/SDN0-Description.pdf and pox/SDN1-Description.pdf.

## Naming Conventions for both SDNs

For consistency, the following naming conventions are used:

- **Workstations:** `facultyWS`, `labWS`, `itWS`
- **Laptops:** `facultyPC`, `studentPC`, `itPC`, `trustedPC`, `guestPC`
- **Servers:** `examServer`, `webServer`, `dnsServer`
- **Other Devices:** `printer`
- **Switches:** `s1`, `s2`, `s3`, `s4`, `s5`

## Network Topology

Utilizing Mininet for network simulation and the POX controller for network programmability, both SDNs operate according to the OpenFlow 1.3 standard, facilitating efficient packet routing between switches and controllers.

## SDN0 Goal

This program is designed to manage traffic within a software-defined network (SDN) with a firewall, ensuring that data packets are routed according to predefined rules. Therefore, it establishes control over the flow of network traffic through software.

## SDN0 Rules - Firewall

The SDN enforces the following firewall rules to manage and secure network traffic:

- **Rule 1**: All ARP traffic is unrestricted across the network.
- **Rule 2**: ICMP packets are permitted unless they are directed to or from the `dnsServer`.
- **Rule 3**: TCP connections to and from the `webServer` are authorized for specific hosts including `facultyWS`, `facultyPC`, `labWS`, `studentPC`, `itWS`, `trustedPC`, and `guestPC`.
- **Rule 4**: TCP traffic to `examServer` is exclusively permitted from `facultyWS` and `facultyPC`, and vice versa.
- **Rule 5**: Inter-host TCP and UDP traffic among `facultyWS`, `facultyPC`, `labWS`, `studentPC`, `itWS`, and `itPC` is allowed.
- **Rule 6**: All UDP traffic to and from `dnsServer` is accepted.
- **Default Rule**: Any other traffic not explicitly mentioned above is to be dropped.

## Implementation of Firewall Rules

 - A function `do_firewall(src, dst, protocol)` is outlined in pseudocode to apply the aforementioned firewall rules effectively.
 - Network flow is managed via OpenFlow messages such as `Packet_In`, `Packet_Out`, and `Flow_Mod`, which adjust flow tables and guide packet traffic within the network.

## Firewall Testing Procedures

The functionality of the firewall is tested using `ping` for ICMP traffic verification, `iperf` for TCP traffic, `iperfudp` for UDP traffic. This ensures that the traffic adheres to the defined rules, particularly in relation to `webServer`, `examServer`, and `dnsServer`.


## SDN1 Goal

The primary goal of this SDN is to control and manage network traffic between various devices in the network topology without using flooding techniques (specifically forbidding the use of `of.OFPP_FLOOD`). Traffic is directed based on subnet specifications, ensuring specific ports are used for all communications. This approach necessitates a method to validate whether an IP address belongs to a given subnet, based on predefined network topology rules.


## SDN1 Rules

The implementation must adhere to the following rules, directing traffic based on subnet affiliations:

- **Rule 1:** Allow ICMP traffic only between the Student Housing LAN, Faculty LAN, and IT Department subnets, or within the same subnet.
- **Rule 2:** TCP traffic should be allowed only between the University Data Center, IT Department, Faculty LAN, Student Housing LAN, and trustedPC, or within the same subnet. Notably, only the Faculty LAN can access the exam server.
- **Rule 3:** UDP traffic is permitted only between the University Data Center, IT Department, Faculty LAN, Student Housing LAN, or within the same subnet.
- **Rule 4:** All other types of traffic must be dropped.


## SDN1 Description Items

1. Annotation of the provided topology diagram with port numbers for each link end. Implement this topology in `lab5_topo_skel.py`.
2. Discussion of packet forwarding in this program, specifically focusing on the use of the `accept()` function.
3. Validation of Rule 1 using `pingall`, highlighting the output that shows expected inter-departmental communication. Includes explanations and timestamped screenshots.
4. Testing of Rule 2 using `iperf` between specified node pairs, discussing whether the outcomes match expectations. Includes explanations and timestamped screenshots for each test.
5. Verification of Rule 3 with `iperfudp 10M` between specified node pairs, explaining the results and including timestamped screenshots.
6. Creation of a "discord" host accessible only from the Student LAN and demonstrate access (or lack thereof) from student and faculty PCs using `ping`, `iperfudp`, and `iperf`. Includes timestamped screenshots to validate access control.

---

