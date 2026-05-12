# 🖥️ Systemd Cheatsheet

> The init system that runs modern Linux — service management, journald logging, timers, and resource control.

---

## 🚀 Service Management (systemctl)

```bash
# Start / Stop / Restart
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx                          # Hard restart
sudo systemctl reload nginx                           # Graceful reload (SIGHUP)
sudo systemctl reload-or-restart nginx                # Reload if supported, else restart

# Enable / Disable (boot persistence)
sudo systemctl enable nginx                           # Start on boot
sudo systemctl disable nginx                          # Don't start on boot
sudo systemctl enable --now nginx                     # Enable + start immediately

# Status & Inspection
systemctl status nginx                                # Current status + recent logs
systemctl is-active nginx                             # "active" or "inactive"
systemctl is-enabled nginx                            # "enabled" or "disabled"
systemctl is-failed nginx                             # "failed" or "active"
systemctl show nginx                                  # All properties
systemctl show nginx -p MainPID                       # Specific property
systemctl cat nginx                                   # Show unit file contents

# List services
systemctl list-units --type=service                   # Running services
systemctl list-units --type=service --state=failed    # Failed services
systemctl list-unit-files --type=service              # All installed services
```

## 📝 Unit Files

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Server
Documentation=https://docs.example.com
After=network.target postgresql.service
Requires=postgresql.service                           # Hard dependency
Wants=redis.service                                   # Soft dependency

[Service]
Type=simple                                           # simple|forking|oneshot|notify
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp

# Environment
Environment=NODE_ENV=production
Environment=PORT=3000
EnvironmentFile=/opt/myapp/.env                       # Load from file

# Execution
ExecStartPre=/opt/myapp/pre-start.sh                 # Run before start
ExecStart=/usr/bin/node /opt/myapp/server.js
ExecStartPost=/opt/myapp/post-start.sh               # Run after start
ExecReload=/bin/kill -HUP $MAINPID                   # Graceful reload
ExecStop=/bin/kill -SIGTERM $MAINPID

# Restart policy
Restart=on-failure                                    # always|on-failure|on-abnormal|no
RestartSec=5                                          # Wait 5s between restarts
StartLimitIntervalSec=60                              # Restart limit window
StartLimitBurst=3                                     # Max restarts in window

# Security hardening
NoNewPrivileges=yes
ProtectSystem=strict                                  # Read-only /usr, /boot
ProtectHome=yes                                       # Hide /home, /root
PrivateTmp=yes                                        # Isolated /tmp
ReadWritePaths=/opt/myapp/data /var/log/myapp

# Resource limits
LimitNOFILE=65535
MemoryMax=1G
CPUQuota=200%                                         # 2 CPU cores max

[Install]
WantedBy=multi-user.target
```

```bash
# After creating/modifying unit files
sudo systemctl daemon-reload                          # ALWAYS run after changes
sudo systemctl restart myapp
```

## 📝 Override Files (Don't Edit Vendor Units)

```bash
# Create override without touching original unit file
sudo systemctl edit nginx
# Creates: /etc/systemd/system/nginx.service.d/override.conf

# Example override content:
[Service]
LimitNOFILE=65535
Environment=WORKER_CONNECTIONS=4096

# View effective configuration
systemctl cat nginx                                   # Shows base + overrides
```

## 📋 Journalctl (Log Management)

```bash
# View logs
journalctl -u nginx                                   # Service logs
journalctl -u nginx --since "1 hour ago"             # Time-filtered
journalctl -u nginx --since "2026-01-15 10:00" --until "2026-01-15 12:00"
journalctl -u nginx -f                                # Follow (like tail -f)
journalctl -u nginx -n 100                            # Last 100 lines
journalctl -u nginx -p err                            # Only errors
journalctl -u nginx -o json-pretty                    # JSON format
journalctl -u nginx --no-pager                        # Disable paging

# System-wide logs
journalctl -b                                         # Current boot
journalctl -b -1                                      # Previous boot
journalctl -k                                         # Kernel messages (dmesg)
journalctl --list-boots                               # List all boots

# Priority levels: emerg, alert, crit, err, warning, notice, info, debug
journalctl -p err..crit                               # Range of priorities

# Disk usage
journalctl --disk-usage
sudo journalctl --vacuum-size=500M                    # Trim to 500MB
sudo journalctl --vacuum-time=7d                      # Keep only 7 days
```

## ⏰ Timers (Replacement for Cron)

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=*-*-* 02:00:00                            # Daily at 2 AM
# OnCalendar=Mon *-*-* 09:00:00                      # Every Monday 9 AM
# OnCalendar=*-*-* *:00:00                            # Every hour
# OnBootSec=5min                                      # 5 min after boot
# OnUnitActiveSec=1h                                  # Every hour after last run
Persistent=true                                       # Run missed executions
RandomizedDelaySec=300                                # Jitter up to 5 min
AccuracySec=1s

[Install]
WantedBy=timers.target

# /etc/systemd/system/backup.service (paired service)
[Unit]
Description=Daily backup job

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
```

```bash
sudo systemctl enable --now backup.timer
systemctl list-timers --all                           # List all timers
systemctl status backup.timer                         # Timer status
```

## 🔍 Debugging Failed Services

```bash
# Step 1: Check status
systemctl status myapp

# Step 2: Read logs
journalctl -u myapp -n 50 --no-pager

# Step 3: Check dependencies
systemctl list-dependencies myapp

# Step 4: Verify unit file syntax
systemd-analyze verify /etc/systemd/system/myapp.service

# Step 5: Check if service is masked
systemctl is-enabled myapp                            # "masked" = blocked

# Step 6: Boot analysis
systemd-analyze                                       # Total boot time
systemd-analyze blame                                 # Per-service boot time
systemd-analyze critical-chain myapp.service          # Dependency chain
```

## 🎯 FAANG Interview Q&A

```
Q: systemd vs cron for scheduled tasks?
A: systemd timers: better logging (journald), dependency management,
   missed execution handling (Persistent=true), resource control.
   Cron: simpler syntax, universally available, sufficient for basics.

Q: What happens when Restart=on-failure and the service keeps crashing?
A: systemd respects StartLimitBurst and StartLimitIntervalSec.
   If the service crashes more than StartLimitBurst times within
   StartLimitIntervalSec, systemd stops trying and marks it failed.
   This prevents restart storms.

Q: How would you secure a systemd service?
A: NoNewPrivileges=yes, ProtectSystem=strict, ProtectHome=yes,
   PrivateTmp=yes, ReadWritePaths for specific dirs only,
   run as non-root User/Group, set resource limits,
   CapabilityBoundingSet to restrict capabilities.

Q: What's the difference between Requires and Wants?
A: Requires: hard dependency — if the dependency fails/stops,
   this unit also stops. Wants: soft dependency — try to start
   the dependency, but don't fail if it's unavailable.
```

---

> 💡 **Production Rule:** Never edit vendor-provided unit files directly. Always use `systemctl edit` to create override files. Run `daemon-reload` after every unit file change.
