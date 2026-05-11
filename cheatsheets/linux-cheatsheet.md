# 🐧 Linux Cheatsheet

> Essential Linux commands for DevOps/SRE engineers.

---

## 📁 File Operations

```bash
ls -lah                                  # List with details + hidden
find / -name "*.log" -mtime +7           # Files modified 7+ days ago
find / -size +100M                       # Files larger than 100MB
du -sh /var/log/*                        # Directory sizes
df -h                                    # Disk usage by filesystem
ln -s /path/to/target link_name          # Symbolic link
tar -czf archive.tar.gz /path/           # Create gzip archive
tar -xzf archive.tar.gz                  # Extract gzip archive
```

## 📊 Process & System

```bash
top / htop                               # Real-time process viewer
ps aux --sort=-%mem | head               # Top memory consumers
ps aux --sort=-%cpu | head               # Top CPU consumers
kill -15 <PID>                           # Graceful shutdown
kill -9 <PID>                            # Force kill
pgrep -f "node app"                      # Find PID by name
lsof -i :8080                           # Who's using port 8080?
free -h                                  # Memory usage
uptime                                   # Uptime + load averages
nproc                                    # Number of CPU cores
cat /proc/cpuinfo | grep "model name"   # CPU info
```

## 🌐 Networking

```bash
ip addr show                             # Network interfaces
ss -tlnp                                 # Listening TCP ports
ss -s                                    # Socket statistics
curl -I https://example.com              # HTTP headers
wget -qO- https://example.com            # Download to stdout
dig example.com +short                   # DNS lookup
ping -c 4 google.com                     # ICMP ping
traceroute google.com                    # Network path
netstat -rn                              # Routing table
iptables -L -n                           # Firewall rules
```

## 📝 Text Processing

```bash
grep -r "ERROR" /var/log/                # Recursive search
grep -c "500" access.log                 # Count matches
grep -v "DEBUG" app.log                  # Exclude pattern
awk '{print $1}' access.log              # First column
awk '$9 >= 500' access.log               # Filter by column value
sed -i 's/old/new/g' file.txt            # Find & replace
sort | uniq -c | sort -rn                # Count unique, sorted
wc -l file.txt                           # Line count
head -n 50 file.txt                      # First 50 lines
tail -f /var/log/app.log                 # Follow log in real-time
jq '.' response.json                     # Pretty-print JSON
jq '.items[] | .name' response.json      # Extract JSON fields
```

## 🔐 Permissions & Users

```bash
chmod 755 script.sh                      # rwxr-xr-x
chmod 600 secret.key                     # rw-------
chown user:group file                    # Change ownership
whoami                                   # Current user
id                                       # User ID and groups
sudo -u postgres psql                    # Run as another user
```

## ⚙️ Systemd

```bash
systemctl status nginx                   # Service status
systemctl start/stop/restart nginx       # Control service
systemctl enable/disable nginx           # Boot behavior
systemctl list-units --failed            # Failed services
journalctl -u nginx -f                   # Follow service logs
journalctl -u nginx --since "1h ago"     # Recent logs
journalctl -p err                        # Error-level logs
```

## 💡 One-Liners

```bash
# Top 10 IPs hitting your server
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Disk usage alert
df -h | awk '$5+0 > 80 {print "WARNING:", $0}'

# Find large files
find / -xdev -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Watch a command every 2 seconds
watch -n 2 'kubectl get pods'

# Generate a random password
openssl rand -base64 24
```

---

> 💡 **Tip:** Install `bat` (better `cat`), `fd` (better `find`), `ripgrep` (better `grep`), and `exa` (better `ls`) for modern alternatives.
