# 📜 Bash Scripting Cheatsheet

> Production-grade bash patterns — error handling, functions, loops, text processing, and script templates used in FAANG ops.

---

## 🛡️ Script Template (Always Start With This)

```bash
#!/usr/bin/env bash
set -euo pipefail                                     # THE holy trinity
IFS=$'\n\t'                                           # Safer word splitting

# set -e   → Exit on any error
# set -u   → Error on undefined variables
# set -o pipefail → Pipe fails if ANY command fails

# Script metadata
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"

# Cleanup trap
cleanup() {
    local exit_code=$?
    echo "[$(date -Iseconds)] Script exiting with code: $exit_code"
    # Remove temp files, release locks, etc.
    rm -f "${TMPFILE:-}"
    exit "$exit_code"
}
trap cleanup EXIT
trap 'echo "Signal received, cleaning up..."; exit 1' INT TERM

# Logging
log() { echo "[$(date -Iseconds)] $*" | tee -a "$LOG_FILE"; }
error() { echo "[$(date -Iseconds)] ERROR: $*" >&2 | tee -a "$LOG_FILE"; }
die() { error "$@"; exit 1; }
```

## 📊 Variables & Arrays

```bash
# Variables
name="value"                                          # No spaces around =
readonly VERSION="1.0.0"                              # Immutable
local count=0                                         # Function-scoped

# Default values
DB_HOST="${DB_HOST:-localhost}"                        # Default if unset
DB_PORT="${DB_PORT:?Error: DB_PORT is required}"      # Error if unset

# String operations
echo "${name^^}"                                      # UPPERCASE
echo "${name,,}"                                      # lowercase
echo "${name:0:5}"                                    # Substring (first 5)
echo "${name#*.}"                                     # Remove shortest prefix
echo "${name##*.}"                                    # Remove longest prefix (extension)
echo "${name%.txt}"                                   # Remove suffix
echo "${name/old/new}"                                # Replace first
echo "${name//old/new}"                               # Replace all
echo "${#name}"                                       # Length

# Arrays
servers=("web1" "web2" "web3")
echo "${servers[0]}"                                  # First element
echo "${servers[@]}"                                  # All elements
echo "${#servers[@]}"                                 # Length
servers+=("web4")                                     # Append

# Associative arrays (bash 4+)
declare -A config
config[host]="localhost"
config[port]="5432"
echo "${config[host]}"
echo "${!config[@]}"                                  # All keys
```

## 🔄 Control Flow

```bash
# Conditionals
if [[ -f "/etc/config.yml" ]]; then
    echo "Config exists"
elif [[ -d "/etc/config.d" ]]; then
    echo "Config dir exists"
else
    echo "No config found"
fi

# Test operators
[[ -f file ]]       # File exists
[[ -d dir ]]        # Directory exists
[[ -z "$var" ]]     # String is empty
[[ -n "$var" ]]     # String is not empty
[[ "$a" == "$b" ]]  # String equality
[[ "$a" =~ ^[0-9]+$ ]]  # Regex match
[[ "$num" -gt 10 ]] # Numeric comparison: -eq -ne -lt -le -gt -ge

# Loops
for server in "${servers[@]}"; do
    echo "Deploying to $server"
done

for i in {1..10}; do echo "$i"; done
for file in /var/log/*.log; do wc -l "$file"; done

while IFS= read -r line; do
    echo "Processing: $line"
done < input.txt

# Until (opposite of while)
until curl -sf http://localhost:8080/health; do
    echo "Waiting for service..."
    sleep 2
done

# Case
case "$1" in
    start)   start_service ;;
    stop)    stop_service ;;
    restart) stop_service; start_service ;;
    *)       die "Usage: $0 {start|stop|restart}" ;;
esac
```

## 🏗️ Functions

```bash
deploy() {
    local server="$1"
    local version="${2:-latest}"
    local timeout="${3:-30}"

    log "Deploying v${version} to ${server}..."

    if ! ssh "$server" "docker pull myapp:${version}"; then
        error "Failed to pull image on ${server}"
        return 1
    fi

    ssh "$server" "docker-compose up -d"
    log "Deployed successfully to ${server}"
}

# Call with: deploy "web1" "2.0.0" 60

# Return values (use echo + command substitution)
get_pod_count() {
    local count
    count=$(kubectl get pods -l app=api --no-headers | wc -l)
    echo "$count"
}
pod_count=$(get_pod_count)
```

## 📝 Text Processing

```bash
# awk (column extraction, math)
awk '{print $1, $NF}' file.log                       # First and last column
awk -F: '{print $1}' /etc/passwd                     # Custom delimiter
awk '$9 >= 500 {print $7, $9}' access.log            # Filter by column value
awk '{sum+=$1} END {print sum/NR}' data.txt          # Average

# sed (stream editing)
sed -i 's/old/new/g' file.txt                        # Replace in-place
sed -n '10,20p' file.txt                             # Print lines 10-20
sed '/^#/d' config.txt                               # Delete comment lines
sed -i '/pattern/a\new line' file.txt                # Append after match

# grep
grep -r "ERROR" /var/log/                            # Recursive search
grep -c "pattern" file.txt                           # Count matches
grep -A3 -B1 "FATAL" app.log                         # Context lines
grep -E "error|warn|fatal" app.log                   # Regex OR

# sort + uniq (analysis patterns)
sort file | uniq -c | sort -rn | head -10            # Top 10 frequencies
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn # Top IPs

# xargs (parallel execution)
find . -name "*.log" -mtime +30 | xargs rm -f       # Delete old logs
cat servers.txt | xargs -P4 -I{} ssh {} "uptime"    # Parallel SSH
```

## 🔒 Error Handling Patterns

```bash
# Retry with exponential backoff
retry() {
    local max_attempts="${1}"; shift
    local delay=1
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi
        log "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
        sleep "$delay"
        delay=$((delay * 2))
        attempt=$((attempt + 1))
    done
    error "All $max_attempts attempts failed"
    return 1
}
# Usage: retry 5 curl -sf http://localhost:8080/health

# Lock file (prevent concurrent runs)
readonly LOCKFILE="/var/run/${SCRIPT_NAME}.lock"
acquire_lock() {
    if ! mkdir "$LOCKFILE" 2>/dev/null; then
        die "Another instance is running (lockfile: $LOCKFILE)"
    fi
}
release_lock() { rmdir "$LOCKFILE" 2>/dev/null || true; }
trap 'release_lock; cleanup' EXIT
```

## 📋 Common SRE Script Patterns

```bash
# Health check loop
wait_for_healthy() {
    local url="$1" timeout="${2:-60}" interval="${3:-5}"
    local elapsed=0
    while [[ $elapsed -lt $timeout ]]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            log "Service is healthy"
            return 0
        fi
        sleep "$interval"
        elapsed=$((elapsed + interval))
    done
    die "Service not healthy after ${timeout}s"
}

# Parallel deployment
deploy_fleet() {
    local version="$1"
    local pids=()
    for server in "${servers[@]}"; do
        deploy "$server" "$version" &
        pids+=($!)
    done
    for pid in "${pids[@]}"; do
        wait "$pid" || die "Deployment failed (PID: $pid)"
    done
    log "All deployments complete"
}
```

## 🎯 FAANG Interview Q&A

```
Q: What does set -euo pipefail do?
A: -e: exit on error, -u: error on undefined vars,
   -o pipefail: pipe returns rightmost non-zero exit code.
   Without pipefail, `bad_cmd | good_cmd` returns 0.

Q: How do you handle cleanup in bash?
A: Use trap: trap 'cleanup_function' EXIT
   EXIT trap runs on normal exit AND on signals.
   Also trap INT TERM for interrupt/terminate signals.

Q: Difference between $@ and $*?
A: "$@" preserves each argument as separate word (use this).
   "$*" joins all arguments into single string.
   Always use "$@" in quoted form for argument passing.

Q: How do you prevent race conditions in scripts?
A: Lock files (mkdir is atomic), flock command, or PID files.
   mkdir-based locks are most portable.
```

---

> 💡 **Production Rule:** Every production bash script MUST have `set -euo pipefail`, a cleanup trap, and logging. No exceptions. Scripts without error handling will silently fail and corrupt your systems.
