#!/bin/bash
# =============================================================================
# 🐧 Linux System Health Check Script
# =============================================================================
# Description:
#   Quick system health assessment for SRE on-call situations.
#   Checks: CPU, memory, disk, network, processes, and recent errors.
#
# Usage:
#   chmod +x system-healthcheck.sh
#   sudo ./system-healthcheck.sh
#
# Author: Zero to SRE
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🐧 System Health Check"
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo "========================================"

# --- CPU ---
echo ""
echo "⚡ CPU"
echo "--------"
CPU_CORES=$(nproc 2>/dev/null || echo "?")
LOAD=$(cat /proc/loadavg 2>/dev/null | awk '{print $1, $2, $3}')
echo "  Cores: $CPU_CORES"
echo "  Load Average (1m, 5m, 15m): $LOAD"

LOAD_1M=$(echo "$LOAD" | awk '{print $1}')
if (( $(echo "$LOAD_1M > $CPU_CORES" | bc -l 2>/dev/null || echo 0) )); then
    echo -e "  ${RED}⚠️  Load exceeds CPU count!${NC}"
else
    echo -e "  ${GREEN}✅ Load is healthy${NC}"
fi

# Top CPU consumers
echo ""
echo "  Top 5 CPU consumers:"
ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "    %-8s %-6s %s\n", $1, $3"%", $11}'

# --- Memory ---
echo ""
echo "💾 Memory"
echo "--------"
free -h 2>/dev/null | head -2
MEM_PCT=$(free | awk '/Mem:/ {printf "%.0f", $3/$2*100}')
if [ "$MEM_PCT" -gt 90 ]; then
    echo -e "  ${RED}⚠️  Memory usage: ${MEM_PCT}% — CRITICAL${NC}"
elif [ "$MEM_PCT" -gt 80 ]; then
    echo -e "  ${YELLOW}⚠️  Memory usage: ${MEM_PCT}% — WARNING${NC}"
else
    echo -e "  ${GREEN}✅ Memory usage: ${MEM_PCT}%${NC}"
fi

# --- Disk ---
echo ""
echo "💽 Disk"
echo "--------"
df -h --output=source,size,used,avail,pcent,target 2>/dev/null | grep -vE "tmpfs|devtmpfs|overlay" | head -10

# Check for disks > 80%
DISK_WARNING=$(df -h 2>/dev/null | awk 'NR>1 {gsub(/%/,""); if ($5+0 > 80) print "  ⚠️  " $6 " is at " $5 "%"}')
if [ -n "$DISK_WARNING" ]; then
    echo -e "${YELLOW}$DISK_WARNING${NC}"
else
    echo -e "  ${GREEN}✅ All disks below 80%${NC}"
fi

# --- Network ---
echo ""
echo "🌐 Network"
echo "--------"
echo "  Listening TCP ports:"
ss -tlnp 2>/dev/null | head -10 || netstat -tlnp 2>/dev/null | head -10

echo ""
echo "  Established connections:"
ss -s 2>/dev/null | head -5

# --- Services ---
echo ""
echo "⚙️ Failed Services"
echo "--------"
FAILED=$(systemctl list-units --state=failed --no-pager --no-legend 2>/dev/null)
if [ -n "$FAILED" ]; then
    echo -e "${RED}$FAILED${NC}"
else
    echo -e "  ${GREEN}✅ No failed services${NC}"
fi

# --- Recent Errors ---
echo ""
echo "🔴 Recent Errors (last 30 min)"
echo "--------"
journalctl -p err --since "30 min ago" --no-pager 2>/dev/null | tail -10 || echo "  Cannot access journal"

# --- Docker (if installed) ---
if command -v docker &> /dev/null; then
    echo ""
    echo "🐳 Docker"
    echo "--------"
    echo "  Running containers: $(docker ps -q 2>/dev/null | wc -l)"
    echo "  Stopped containers: $(docker ps -aq --filter 'status=exited' 2>/dev/null | wc -l)"
    echo "  Disk usage:"
    docker system df 2>/dev/null | head -5
fi

echo ""
echo "========================================"
echo "✅ Health check complete!"
