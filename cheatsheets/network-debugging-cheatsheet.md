# 🔬 Network Debugging Cheatsheet

> Every network debugging tool an SRE needs — connection analysis, packet capture, DNS, TLS, and traffic inspection.

---

## 🔌 Connection Analysis (ss/netstat)

```bash
# ss (modern, faster than netstat)
ss -tlnp                                              # Listening TCP ports
ss -ulnp                                              # Listening UDP ports
ss -tnp                                               # Active TCP connections
ss -s                                                 # Socket summary
ss -tnp state established                            # Only established
ss -tnp dst 10.0.1.50                                # Connections to specific host
ss -tnp sport = :443                                 # From port 443
ss -tnp dport = :5432                                # To PostgreSQL

# Connection state distribution
ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn

# Find connection leaks
ss -tnp state close-wait                              # App didn't close connection
ss -tnp state time-wait | wc -l                      # Too many = port exhaustion

# Who's connected to my service?
ss -tnp sport = :8080 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn
```

## 🌍 DNS Debugging

```bash
# Basic lookups
dig example.com A +short                              # A record
dig example.com AAAA +short                           # IPv6
dig example.com MX +short                             # Mail servers
dig example.com NS +short                             # Nameservers
dig example.com TXT +short                            # TXT records
dig example.com ANY +noall +answer                    # All records

# Detailed trace
dig example.com +trace                                # Full resolution path
dig @8.8.8.8 example.com A                            # Query specific DNS
dig @ns1.example.com example.com A +norec             # Non-recursive (authoritative)

# Reverse DNS
dig -x 1.2.3.4                                        # PTR lookup

# DNS propagation check
for ns in 8.8.8.8 1.1.1.1 208.67.222.222 9.9.9.9; do
    echo "=== $ns ===" && dig @$ns example.com A +short
done

# DNS cache debugging
resolvectl statistics                                  # systemd-resolved stats
resolvectl flush-caches                               # Flush local DNS cache
cat /etc/resolv.conf                                  # Check DNS config

# DNS response time
dig example.com | grep "Query time"
time dig @8.8.8.8 example.com A +short                # Time the lookup

# Common DNS issues
# NXDOMAIN   → Domain doesn't exist
# SERVFAIL   → DNS server error (check zone config)
# REFUSED    → DNS server refused query (check ACLs)
# Timeout    → DNS server unreachable (check firewall)
```

## 🔒 TLS/SSL Debugging

```bash
# Check certificate details
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer

# Certificate expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -enddate

# Full certificate chain
openssl s_client -connect example.com:443 -showcerts </dev/null 2>/dev/null

# TLS version and cipher
openssl s_client -connect example.com:443 </dev/null 2>/dev/null | \
  grep -E "Protocol|Cipher"

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Certificate verification
openssl verify -CAfile ca-bundle.crt certificate.pem

# Check if cert matches key
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa -noout -modulus -in key.pem | md5sum
# Both should match

# Scan TLS ciphers
nmap --script ssl-enum-ciphers -p 443 example.com
```

## 🌐 HTTP Debugging (curl)

```bash
# Timing breakdown
curl -w "\nDNS:       %{time_namelookup}s\nConnect:   %{time_connect}s\nTLS:       %{time_appconnect}s\nPreTx:     %{time_pretransfer}s\nStartTx:   %{time_starttransfer}s\nTotal:     %{time_total}s\nHTTP Code: %{http_code}\nSize:      %{size_download} bytes\n" \
  -o /dev/null -s https://api.example.com

# Verbose with headers
curl -vvv https://api.example.com 2>&1

# Follow redirects
curl -L -v https://example.com 2>&1 | grep "< HTTP\|< Location"

# POST with data
curl -X POST -H "Content-Type: application/json" \
  -d '{"key":"value"}' https://api.example.com/data

# Download with retry
curl --retry 3 --retry-delay 5 --max-time 30 -o file.tar.gz https://example.com/file

# Test from specific source IP
curl --interface 10.0.1.50 https://api.example.com

# HTTP/2 test
curl --http2 -I https://api.example.com
```

## 🛤️ Route & Connectivity

```bash
# Traceroute
traceroute example.com                                # ICMP
traceroute -T -p 443 example.com                     # TCP (bypasses ICMP blocks)
mtr example.com                                       # Continuous traceroute
mtr --report --report-cycles=10 example.com          # Report mode

# Ping
ping -c 5 example.com                                # Basic connectivity
ping -c 5 -s 1472 example.com                        # MTU test (1472+28=1500)

# Port connectivity
nc -zv 10.0.1.50 5432                                # TCP port check
nc -zv -w 3 10.0.1.50 5432                           # With 3s timeout
echo "PING" | nc -w 2 10.0.1.50 6379                # Redis connectivity
nmap -sT -p 80,443,8080,5432 10.0.1.50              # Multiple port scan

# Routing table
ip route show                                         # Routing table
ip route get 10.0.1.50                               # Route to specific host
```

## 🔥 Firewall Inspection

```bash
# iptables
sudo iptables -L -n -v --line-numbers                # List all rules
sudo iptables -L INPUT -n -v                         # Input chain
sudo iptables -t nat -L -n -v                        # NAT rules

# nftables
sudo nft list ruleset                                 # All rules

# UFW
sudo ufw status verbose                               # Status
sudo ufw show raw                                     # Raw iptables rules

# Security groups check (AWS)
aws ec2 describe-security-groups --group-ids sg-xxx \
  --query "SecurityGroups[].IpPermissions[]" --output json
```

## 📊 Traffic Analysis

```bash
# Bandwidth monitoring
iftop -i eth0                                         # Real-time bandwidth by connection
nethogs                                               # Per-process bandwidth
bmon                                                  # Interface bandwidth monitor
sar -n DEV 1 5                                        # Interface stats over time
vnstat -i eth0                                        # Long-term traffic stats

# TCP retransmissions (indicator of packet loss)
nstat -s | grep -i retrans
ss -ti | grep -E "retrans|rto"

# Network latency
hping3 -c 5 -S -p 443 example.com                   # TCP-level ping
```

## 🎯 FAANG Interview Scenarios

```
Scenario: "Users report intermittent timeouts to your API."

Debugging Steps:
1. ss -s → Check connection states (TIME_WAIT/CLOSE_WAIT spike?)
2. ss -tnp state established | wc -l → Connection count
3. curl timing breakdown → Where is latency? DNS? TLS? Server?
4. tcpdump -i any port 8080 -c 100 → Packet-level analysis
5. dig api.example.com → DNS resolution issues?
6. mtr api.example.com → Network path issues?
7. Check for TCP retransmissions: nstat -s | grep retrans

Common Causes:
- DNS resolution slow → Use /etc/hosts or local DNS cache
- TLS handshake slow → Enable TLS session resumption
- TCP connection queueing → Increase somaxconn
- Upstream timeout → Check backend service latency
- Port exhaustion → Check TIME_WAIT count, enable tcp_tw_reuse

Scenario: "502 Bad Gateway errors from Nginx"

Debugging Steps:
1. curl -vvv https://api.example.com → What's the response?
2. Check Nginx error log → "upstream timed out" or "connection refused"?
3. ss -tnp dport = :3000 → Can Nginx connect to backend?
4. nc -zv 127.0.0.1 3000 → Is backend listening?
5. curl http://127.0.0.1:3000/health → Backend healthy?
```

---

> 💡 **SRE Rule:** When debugging network issues, follow the packet path: DNS → TCP connect → TLS → HTTP. The problem is usually at the first step that fails. Use curl timing breakdown as your starting point.
