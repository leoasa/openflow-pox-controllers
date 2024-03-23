# openflow-pox-controllers
Python3 Openflow POX controller with Mininet topologies. POX documentation from https://github.com/noxrepo/pox. Custom topology and firewall files can be found in pox/pox/sdn0 and pox/pox/sdn1. Description found in pox/SDN1-Description.pdf

## SDN1 Goal

The primary goal of this SDN is to control and manage network traffic between various devices in the network topology without using flooding techniques (specifically forbidding the use of `of.OFPP_FLOOD`). Traffic is directed based on subnet specifications, ensuring specific ports are used for all communications. This approach necessitates a method to validate whether an IP address belongs to a given subnet, based on predefined network topology rules.

### Naming Conventions

For consistency, the following naming conventions are used:

- **Workstations:** `facultyWS`, `labWS`, `itWS`
- **Laptops:** `facultyPC`, `studentPC`, `itPC`, `trustedPC`, `guestPC`
- **Servers:** `examServer`, `webServer`, `dnsServer`
- **Other Devices:** `printer`
- **Switches:** `s1`, `s2`, `s3`, `s4`, `s5`

## SDN1 Topology Rules

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

