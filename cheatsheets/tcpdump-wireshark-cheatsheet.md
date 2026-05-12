# 🦈 tcpdump & Wireshark Cheatsheet

> Packet-level debugging — capture, filter, and analyze network traffic like a FAANG network engineer.

---

## 📡 tcpdump Essentials

```bash
# Basic captures
sudo tcpdump -i any                                   # All interfaces
sudo tcpdump -i eth0                                  # Specific interface
sudo tcpdump -i any -c 50                             # Capture 50 packets
sudo tcpdump -i any -n                                # Don't resolve hostnames
sudo tcpdump -i any -nn                               # Don't resolve hostnames or ports

# Save to file / read from file
sudo tcpdump -i any -w /tmp/capture.pcap              # Write to file
sudo tcpdump -r /tmp/capture.pcap                     # Read from file
sudo tcpdump -r capture.pcap -nn | head -20           # Quick analysis

# Verbosity
sudo tcpdump -i any -v                                # Verbose
sudo tcpdump -i any -vv                               # More verbose
sudo tcpdump -i any -vvv                              # Maximum detail
sudo tcpdump -i any -A                                # ASCII payload (HTTP)
sudo tcpdump -i any -X                                # Hex + ASCII payload
```

## 🎯 tcpdump Filters

```bash
# Host filters
sudo tcpdump host 10.0.1.50                           # To or from host
sudo tcpdump src host 10.0.1.50                       # From host
sudo tcpdump dst host 10.0.1.50                       # To host

# Port filters
sudo tcpdump port 80                                  # HTTP
sudo tcpdump port 443                                 # HTTPS
sudo tcpdump port 5432                                # PostgreSQL
sudo tcpdump portrange 8000-9000                      # Port range
sudo tcpdump src port 3000                            # From specific port

# Protocol filters
sudo tcpdump tcp                                      # TCP only
sudo tcpdump udp                                      # UDP only
sudo tcpdump icmp                                     # ICMP (ping)
sudo tcpdump arp                                      # ARP

# Combination filters
sudo tcpdump 'host 10.0.1.50 and port 5432'          # DB traffic to host
sudo tcpdump 'src 10.0.1.50 and dst port 443'        # HTTPS from host
sudo tcpdump 'port 80 or port 443'                    # HTTP + HTTPS
sudo tcpdump 'not port 22'                            # Exclude SSH
sudo tcpdump 'tcp and not port 22 and host 10.0.1.50'

# TCP flags
sudo tcpdump 'tcp[tcpflags] & (tcp-syn) != 0'        # SYN packets
sudo tcpdump 'tcp[tcpflags] & (tcp-rst) != 0'        # RST packets (connection reset)
sudo tcpdump 'tcp[tcpflags] & (tcp-fin) != 0'        # FIN packets
sudo tcpdump 'tcp[tcpflags] == tcp-syn'               # SYN only (new connections)

# Size filters
sudo tcpdump 'greater 1000'                           # Packets > 1000 bytes
sudo tcpdump 'less 100'                               # Packets < 100 bytes

# Subnet
sudo tcpdump net 10.0.1.0/24                          # Entire subnet
```

## 🔍 Common Capture Scenarios

```bash
# 1. Debug API connectivity issues
sudo tcpdump -i any -nn 'host api.internal and port 8080' -c 100 -w /tmp/api.pcap

# 2. Find who's connecting to database
sudo tcpdump -i any -nn 'dst port 5432' -c 50

# 3. Capture DNS queries
sudo tcpdump -i any -nn 'port 53' -vv

# 4. Debug TCP connection failures (look for RST/timeout)
sudo tcpdump -i any -nn 'tcp[tcpflags] & (tcp-rst|tcp-syn) != 0 and host 10.0.1.50'

# 5. Capture HTTP requests (unencrypted)
sudo tcpdump -i any -nn -A 'port 80 and tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
# Above captures GET requests only

# 6. Monitor for SYN floods (DDoS indicator)
sudo tcpdump -i any -nn 'tcp[tcpflags] == tcp-syn' -c 1000 | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head

# 7. Capture with rotation (long-running)
sudo tcpdump -i any -w /tmp/capture_%Y%m%d_%H%M.pcap -G 3600 -W 24
# New file every hour (-G 3600), keep 24 files (-W 24)
```

## 🦈 Wireshark Display Filters

```
# Protocol filters
http                                                  # HTTP traffic
tls                                                   # TLS/SSL traffic
dns                                                   # DNS queries/responses
tcp                                                   # TCP traffic
icmp                                                  # ICMP

# IP filters
ip.addr == 10.0.1.50                                  # Source or destination
ip.src == 10.0.1.50                                   # Source only
ip.dst == 10.0.1.50                                   # Destination only

# Port filters
tcp.port == 8080                                      # Source or destination port
tcp.dstport == 443                                    # Destination port
tcp.srcport == 3000                                   # Source port

# HTTP filters
http.request.method == "GET"                          # GET requests
http.request.method == "POST"                         # POST requests
http.response.code == 500                             # 500 errors
http.response.code >= 400                             # All errors
http.host == "api.example.com"                        # Specific host
http.request.uri contains "/api/v1"                   # URI pattern

# TLS filters
tls.handshake.type == 1                               # Client Hello
tls.handshake.type == 2                               # Server Hello
tls.handshake.extensions.server_name == "example.com"

# TCP analysis
tcp.analysis.retransmission                           # Retransmissions
tcp.analysis.duplicate_ack                            # Duplicate ACKs
tcp.analysis.zero_window                              # Zero window
tcp.analysis.reset                                    # Connection resets
tcp.flags.syn == 1 && tcp.flags.ack == 0              # SYN only

# DNS
dns.qry.name == "api.example.com"                     # Query for domain
dns.flags.rcode != 0                                  # DNS errors

# Combination
http.response.code >= 500 && ip.src == 10.0.1.50
tcp.analysis.retransmission && ip.addr == 10.0.1.50
```

## 🛠️ Wireshark Analysis Techniques

```
FOLLOW TCP STREAM:
  Right-click packet → Follow → TCP Stream
  Shows complete conversation between client/server

EXPERT INFO:
  Analyze → Expert Information
  Shows warnings, errors, retransmissions, resets

IO GRAPH:
  Statistics → I/O Graphs
  Plot packets/bytes over time (find spikes)

CONVERSATIONS:
  Statistics → Conversations
  Shows all connections with bytes transferred

ENDPOINTS:
  Statistics → Endpoints
  Shows all IPs/ports with traffic volume

HTTP ANALYSIS:
  Statistics → HTTP → Requests
  Shows request distribution by URI

PROTOCOL HIERARCHY:
  Statistics → Protocol Hierarchy
  Shows bandwidth breakdown by protocol
```

## 🔧 tshark (Wireshark CLI)

```bash
# CLI version of Wireshark (for server-side analysis)
tshark -i eth0 -c 50                                  # Capture 50 packets
tshark -r capture.pcap                                # Read pcap file
tshark -r capture.pcap -Y "http.response.code >= 500" # Filter
tshark -r capture.pcap -T fields -e ip.src -e http.request.uri
tshark -r capture.pcap -qz "http,tree"                # HTTP statistics
tshark -r capture.pcap -qz "conv,tcp"                 # TCP conversations
tshark -r capture.pcap -qz "io,stat,1,tcp.analysis.retransmission"  # Retransmits/sec
```

## 🎯 FAANG Interview Q&A

```
Q: How would you debug intermittent packet loss?
A: 1. tcpdump to capture traffic
   2. Wireshark → tcp.analysis.retransmission filter
   3. Statistics → I/O Graph to find when loss occurs
   4. Check: interface errors (ip -s link), ring buffer drops
      (ethtool -S), TCP retransmits (nstat)
   5. Correlate with server load, network topology changes

Q: How do you capture HTTPS traffic?
A: You can't see encrypted payloads in tcpdump.
   Options: 1) Capture at the app (before encryption)
   2) Use SSLKEYLOGFILE with Wireshark for decryption
   3) Use a TLS-terminating proxy to capture plaintext
   4) Analyze TLS handshake metadata (SNI, cert info)

Q: What does a TCP RST indicate?
A: Connection forcibly closed. Causes:
   - Port not listening (connection refused)
   - Firewall sending RST
   - Application crashed
   - Half-open connection cleanup
   - Load balancer idle timeout
```

---

> 💡 **Production Rule:** Always capture with `-w` to a file for later analysis. Never run tcpdump without `-c` (count limit) or time limit on production servers — disk can fill up fast.
