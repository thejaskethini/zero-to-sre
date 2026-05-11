#!/bin/bash
# =============================================================================
# 🌐 Network Debugging Toolkit
# =============================================================================
# Description:
#   Collection of commands for debugging common networking issues.
#   Run each section as needed for troubleshooting.
#
# Usage:
#   chmod +x network-debug.sh
#   ./network-debug.sh <target-host>
#
# Author: Zero to SRE
# =============================================================================

set -euo pipefail

TARGET=${1:-"google.com"}
echo "🌐 Network Debugging Toolkit"
echo "Target: $TARGET"
echo "================================="

# --- DNS Resolution ---
echo ""
echo "📡 1. DNS Resolution"
echo "-------------------"
echo "→ dig (detailed DNS lookup):"
dig "$TARGET" +short 2>/dev/null || echo "  dig not available, using nslookup"
echo ""
echo "→ nslookup:"
nslookup "$TARGET" 2>/dev/null || echo "  nslookup not available"
echo ""
echo "→ DNS servers being used:"
cat /etc/resolv.conf 2>/dev/null | grep nameserver || echo "  Cannot read resolv.conf"

# --- Connectivity ---
echo ""
echo "🔌 2. Connectivity"
echo "-------------------"
echo "→ ping (ICMP):"
ping -c 4 "$TARGET" 2>/dev/null || echo "  Ping failed or blocked"
echo ""
echo "→ TCP connectivity test (port 443):"
timeout 5 bash -c "echo >/dev/tcp/$TARGET/443" 2>/dev/null && echo "  ✅ Port 443 is OPEN" || echo "  ❌ Port 443 is CLOSED or filtered"
echo ""
echo "→ TCP connectivity test (port 80):"
timeout 5 bash -c "echo >/dev/tcp/$TARGET/80" 2>/dev/null && echo "  ✅ Port 80 is OPEN" || echo "  ❌ Port 80 is CLOSED or filtered"

# --- Traceroute ---
echo ""
echo "🗺️ 3. Route Path"
echo "-------------------"
echo "→ traceroute (network path):"
traceroute -m 15 "$TARGET" 2>/dev/null || echo "  traceroute not available"

# --- HTTP Check ---
echo ""
echo "🌐 4. HTTP Check"
echo "-------------------"
echo "→ HTTP response headers:"
curl -sI "https://$TARGET" 2>/dev/null | head -10 || echo "  curl failed"
echo ""
echo "→ TLS certificate info:"
echo | openssl s_client -servername "$TARGET" -connect "$TARGET:443" 2>/dev/null | openssl x509 -noout -subject -dates 2>/dev/null || echo "  TLS check failed"

# --- Local Network ---
echo ""
echo "💻 5. Local Network Info"
echo "-------------------"
echo "→ Network interfaces:"
ip addr show 2>/dev/null || ifconfig 2>/dev/null || echo "  Cannot get interface info"
echo ""
echo "→ Routing table:"
ip route show 2>/dev/null || netstat -rn 2>/dev/null || echo "  Cannot get routing info"
echo ""
echo "→ Listening ports:"
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || echo "  Cannot get port info"

# --- Summary ---
echo ""
echo "================================="
echo "✅ Network debug complete for: $TARGET"
echo ""
echo "Common issues to check:"
echo "  🔹 DNS: Can you resolve the hostname?"
echo "  🔹 Connectivity: Can you reach the port?"
echo "  🔹 Route: Is traffic going through the right path?"
echo "  🔹 TLS: Is the certificate valid?"
echo "  🔹 Firewall: Are the right ports open?"
