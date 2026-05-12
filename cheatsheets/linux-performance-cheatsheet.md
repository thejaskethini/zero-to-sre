# 🔥 Linux Performance Cheatsheet

> Brendan Gregg's USE Method + the complete performance toolkit — CPU, memory, disk, network analysis for production SREs.

---

## 📐 USE Method (Utilization, Saturation, Errors)

```
For EVERY resource, check these three:

CPU:
  Utilization → mpstat, top, vmstat (us+sy columns)
  Saturation  → vmstat (r column > CPU count), runqlat
  Errors      → perf stat (machine check exceptions)

MEMORY:
  Utilization → free -h, vmstat (si/so columns)
  Saturation  → vmstat si/so > 0, sar -B (pgscand)
  Errors      → dmesg | grep -i "oom\|memory"

DISK I/O:
  Utilization → iostat -xz (%util column)
  Saturation  → iostat (avgqu-sz > 1), await > 10ms
  Errors      → dmesg | grep -i "error\|fault\|bad"

NETWORK:
  Utilization → sar -n DEV (rxkB/s, txkB/s vs link speed)
  Saturation  → netstat -s (overflows, drops), ifconfig (overruns)
  Errors      → ip -s link (errors, drops), ethtool -S
```

## 🧠 CPU Analysis

```bash
# Quick overview
uptime                                                # Load averages (1, 5, 15 min)
# Load > number of CPUs = saturation

# Per-CPU breakdown
mpstat -P ALL 1 5                                     # All CPUs, 1s interval, 5 samples
# Key: %usr (user), %sys (kernel), %iowait (disk), %idle

# Top CPU consumers
top -bn1 -o %CPU | head -20                          # Snapshot
pidstat -u 1 5                                        # Per-process CPU (5 samples)
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -10

# CPU profiling
perf top                                              # Live kernel profiling
perf record -g -p <PID> -- sleep 30                  # Record 30s profile
perf report                                           # Analyze
perf stat -p <PID> sleep 5                           # Hardware counters

# Generate flamegraph
perf record -F 99 -g -p <PID> -- sleep 30
perf script | stackcollapse-perf.pl | flamegraph.pl > cpu.svg

# Context switches
vmstat 1 5                                            # cs column
pidstat -w 1 5                                        # Per-process switches
```

## 💾 Memory Analysis

```bash
# Overview
free -h                                               # System memory
cat /proc/meminfo | head -15                         # Detailed breakdown

# Per-process memory
ps aux --sort=-%mem | head -10                        # Top memory consumers
pmap -x <PID> | tail -5                              # Process memory map
smem -tk                                              # Proportional memory (USS/PSS/RSS)

# Watch for memory growth (leak detection)
watch -n 5 'ps -p <PID> -o pid,rss,vsz,comm'

# OOM Killer
dmesg -T | grep -i "oom\|killed\|out of memory"
cat /proc/<PID>/oom_score                            # 0-1000 (higher = killed first)
echo -17 > /proc/<PID>/oom_adj                       # Protect from OOM (not recommended)

# Swap analysis
swapon --show                                         # Swap devices
vmstat 1 5                                            # si/so columns (swap in/out)
# si/so > 0 means system is swapping — investigate immediately

# Page cache / buffer analysis
cat /proc/meminfo | grep -E "^(Buffers|Cached|Active|Inactive|Dirty)"
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches    # Drop page cache (emergency)
```

## 💽 Disk I/O Analysis

```bash
# Disk usage
df -h                                                 # Filesystem usage
df -i                                                 # Inode usage
du -sh /var/log/* | sort -rh | head -10              # Largest directories
find / -xdev -type f -size +100M 2>/dev/null | head  # Large files

# I/O performance
iostat -xz 1 5                                        # Extended disk stats
# Key columns:
#   r/s, w/s    → IOPS (reads/writes per second)
#   rkB/s, wkB/s → Throughput
#   await       → Average latency (ms) — > 10ms is concerning
#   %util       → Disk utilization — > 80% is concerning

# Per-process I/O
iotop -oPa                                            # Cumulative I/O per process
pidstat -d 1 5                                        # I/O stats per process

# Disk latency testing
ioping -c 10 /var/lib/data                           # Latency test
dd if=/dev/zero of=/tmp/test bs=1M count=1024 oflag=direct  # Write speed
fio --name=test --rw=randread --bs=4k --numjobs=4 --time_based --runtime=30  # FIO benchmark

# Filesystem analysis
lsof +D /var/log                                      # Open files in directory
lsof -p <PID> | wc -l                                # File descriptors used
cat /proc/sys/fs/file-nr                             # System-wide FD usage
```

## 🌐 Network Analysis

```bash
# Connection overview
ss -s                                                 # Socket statistics summary
ss -tlnp                                              # Listening ports
ss -tnp | wc -l                                      # Total connections
ss -tnp state time-wait | wc -l                      # TIME_WAIT count
ss -tnp state close-wait | wc -l                     # CLOSE_WAIT (leak!)

# Network throughput
sar -n DEV 1 5                                        # Interface stats
iftop -i eth0                                         # Real-time bandwidth
nethogs                                               # Per-process bandwidth

# Packet drops & errors
ip -s link show eth0                                  # Interface errors/drops
netstat -s | grep -i "error\|drop\|overflow"         # Protocol-level stats
ethtool -S eth0 | grep -i "err\|drop"               # Driver-level stats

# TCP tuning parameters
sysctl net.core.somaxconn                            # Listen backlog
sysctl net.ipv4.tcp_max_syn_backlog                  # SYN queue
sysctl net.ipv4.tcp_tw_reuse                         # TIME_WAIT reuse
sysctl net.core.netdev_max_backlog                   # Receive queue
```

## 🔧 Essential Tuning Parameters

```bash
# /etc/sysctl.conf — Production tuning
# Network
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.ip_local_port_range = 1024 65535

# Memory
vm.swappiness = 10                                    # Minimize swap usage
vm.overcommit_memory = 0                              # Heuristic overcommit
vm.dirty_ratio = 15                                   # % memory for dirty pages
vm.dirty_background_ratio = 5

# File descriptors
fs.file-max = 2097152
fs.nr_open = 2097152

# Apply: sudo sysctl -p
```

## ⚡ Quick Triage Checklist (60 Seconds)

```bash
# Brendan Gregg's "60-second checklist"
uptime                                                # 1. Load averages
dmesg -T | tail                                       # 2. Kernel errors
vmstat 1 5                                            # 3. System-wide stats
mpstat -P ALL 1 1                                     # 4. Per-CPU balance
pidstat 1 5                                           # 5. Per-process CPU
iostat -xz 1 1                                        # 6. Disk I/O
free -h                                               # 7. Memory
sar -n DEV 1 1                                        # 8. Network
sar -n TCP 1 1                                        # 9. TCP stats
top -bn1 | head -20                                   # 10. Overall check
```

## 🎯 FAANG Interview Q&A

```
Q: A server has high load average but low CPU usage. What's happening?
A: Load average includes processes waiting for I/O (D state).
   Check iostat for disk I/O saturation, and vmstat for
   processes in uninterruptible sleep (b column).

Q: How do you find a memory leak in production?
A: 1. Watch RSS growth: watch 'ps -p PID -o rss,vsz'
   2. Check /proc/PID/smaps for heap growth
   3. Use smem for proportional memory (USS)
   4. For JVM: jmap -heap PID, jstat -gc PID
   5. For Node.js: --inspect flag + Chrome DevTools heap snapshot

Q: What's the difference between RSS, VSZ, USS, PSS?
A: VSZ = virtual memory allocated (may not be used)
   RSS = physical memory used (includes shared libs)
   PSS = proportional share of shared memory
   USS = unique private memory (best for per-process tracking)

Q: How do you diagnose network packet drops?
A: Check: ip -s link (interface), netstat -s (protocol),
   ethtool -S (driver), /proc/net/softnet_stat (softirq),
   nstat -s (TCP overflows). Common causes: ring buffer full,
   backlog queue full, iptables drops, application too slow.
```

---

> 💡 **Brendan Gregg Rule:** "USE Method for resources, RED Method for services. Start with the 60-second checklist. Don't skip steps — the problem is usually in the first thing you didn't check."
