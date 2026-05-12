# 🌐 Networking Cheatsheet (SRE/DevOps)

> TCP/IP, DNS, HTTP, load balancing, and troubleshooting — the networking fundamentals every SRE must know cold.

---

## 🏗️ OSI Model (Quick Reference)

```
Layer 7 — Application   HTTP, HTTPS, gRPC, WebSocket, DNS
Layer 4 — Transport      TCP (reliable), UDP (fast)
Layer 3 — Network        IP, ICMP, routing
Layer 2 — Data Link      Ethernet, MAC addresses, ARP
Layer 1 — Physical       Cables, radio, fiber

WHAT SREs CARE ABOUT:
  L7 → API calls, status codes, headers, TLS
  L4 → Port numbers, connection states, firewalls
  L3 → IP routing, subnets, VPCs, NAT
```

## 🔌 TCP Connection Lifecycle

```
THREE-WAY HANDSHAKE:
  Client → SYN → Server
  Client ← SYN-ACK ← Server
  Client → ACK → Server

CONNECTION STATES TO WATCH:
  ESTABLISHED  → Normal active connection
  TIME_WAIT    → Closed, waiting (2×MSL, ~60s) — too many = port exhaustion
  CLOSE_WAIT   → Remote closed, app hasn't closed yet — LEAK indicator
  FIN_WAIT_2   → Waiting for remote close acknowledgment
```

```bash
# Check connection states
ss -s                                                 # Summary of all states
ss -tnp state time-wait | wc -l                      # Count TIME_WAIT
ss -tnp state close-wait                              # Find CLOSE_WAIT leaks
ss -tnp state established | wc -l                    # Active connections
netstat -an | awk '{print $6}' | sort | uniq -c      # State distribution
```

## 🌍 DNS Deep Dive

```
RECORD TYPES:
  A       → Domain → IPv4 address
  AAAA    → Domain → IPv6 address
  CNAME   → Domain → Another domain (alias)
  MX      → Mail server routing
  TXT     → SPF, DKIM, domain verification
  NS      → Nameserver delegation
  SRV     → Service discovery (port + host)
  SOA     → Zone authority info

TTL STRATEGY:
  Long TTL (3600s)  → Static content, stable services
  Short TTL (60s)   → During migrations, before failovers
  0 TTL             → Real-time DNS failover (not cached)
```

```bash
# DNS debugging
dig example.com A +short                              # Quick A record lookup
dig example.com ANY +noall +answer                    # All records
dig @8.8.8.8 example.com A                            # Query specific DNS server
dig example.com +trace                                # Full resolution path
dig example.com SOA                                   # Check zone authority
nslookup -type=MX example.com                         # Mail records
host -t CNAME www.example.com                         # CNAME lookup

# DNS propagation check
for ns in 8.8.8.8 1.1.1.1 208.67.222.222; do
  echo "=== $ns ===" && dig @$ns example.com A +short
done
```

## 🌐 HTTP/HTTPS Essentials

```
STATUS CODE FAMILIES:
  1xx → Informational (100 Continue, 101 Switching Protocols)
  2xx → Success (200 OK, 201 Created, 204 No Content)
  3xx → Redirect (301 Permanent, 302 Temporary, 304 Not Modified)
  4xx → Client Error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many)
  5xx → Server Error (500 Internal, 502 Bad Gateway, 503 Unavailable, 504 Timeout)

CRITICAL ONES FOR SREs:
  502 Bad Gateway     → Upstream is down (check backend health)
  503 Service Unavail → Server overloaded (scale up / check health)
  504 Gateway Timeout → Upstream too slow (check DB, increase timeout)
  429 Too Many Req    → Rate limited (check rate limiter config)

HTTP METHODS:
  GET     → Read (idempotent, cacheable)
  POST    → Create (not idempotent)
  PUT     → Replace (idempotent)
  PATCH   → Partial update
  DELETE  → Remove (idempotent)
```

```bash
# HTTP debugging
curl -I https://api.example.com                        # Headers only
curl -vvv https://api.example.com 2>&1                 # Verbose with TLS
curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} Total:%{time_total}\n" -o /dev/null -s https://api.example.com
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com/data
```

## 🏠 Subnetting Quick Reference

```
CIDR NOTATION:
  /32 → 1 IP        (single host)
  /28 → 16 IPs      (14 usable)
  /24 → 256 IPs     (254 usable) ← "Class C"
  /20 → 4,096 IPs
  /16 → 65,536 IPs  ← "Class B"
  /8  → 16M IPs     ← "Class A"

PRIVATE IP RANGES (RFC 1918):
  10.0.0.0/8        → 16M addresses (cloud VPCs)
  172.16.0.0/12     → 1M addresses (Docker default)
  192.168.0.0/16    → 65K addresses (home networks)

TYPICAL VPC DESIGN:
  VPC: 10.0.0.0/16
  ├── Public Subnet 1:  10.0.1.0/24  (AZ-a, NAT/LB)
  ├── Public Subnet 2:  10.0.2.0/24  (AZ-b, NAT/LB)
  ├── Private Subnet 1: 10.0.10.0/24 (AZ-a, App servers)
  ├── Private Subnet 2: 10.0.11.0/24 (AZ-b, App servers)
  ├── DB Subnet 1:      10.0.20.0/24 (AZ-a, Databases)
  └── DB Subnet 2:      10.0.21.0/24 (AZ-b, Databases)
```

## 🔒 TLS/SSL Quick Reference

```bash
# Check certificate
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate

# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Generate self-signed cert (testing only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes

# Test TLS versions
nmap --script ssl-enum-ciphers -p 443 example.com
```

## 🔧 Essential Network Tools

```bash
# Connectivity
ping -c 5 10.0.1.10                                  # ICMP connectivity
traceroute 10.0.1.10                                  # Route path
mtr 10.0.1.10                                         # Continuous traceroute

# Port checking
nc -zv 10.0.1.10 5432                                # Check if port is open
telnet 10.0.1.10 5432                                 # Interactive port test
nmap -sT -p 80,443,8080 10.0.1.10                    # Port scan

# Traffic capture
tcpdump -i any port 80 -c 20                         # Capture HTTP traffic
tcpdump -i eth0 host 10.0.1.10 -w capture.pcap       # Save to file
tshark -r capture.pcap -Y "http.response.code == 500" # Analyze with Wireshark CLI

# Bandwidth
iperf3 -s                                             # Server mode
iperf3 -c 10.0.1.10                                  # Client mode (bandwidth test)
```

---

> 💡 **SRE Rule:** Most production incidents trace back to DNS, TLS certificates, or network configuration. Master networking = faster incident response.
