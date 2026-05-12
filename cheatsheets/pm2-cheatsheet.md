# ⚙️ PM2 Cheatsheet

> Production process manager for Node.js — cluster mode, zero-downtime deploys, log management, and monitoring.

---

## 📦 Installation & Setup

```bash
npm install -g pm2
pm2 startup                                           # Auto-start on reboot
pm2 startup systemd                                   # Specify init system
pm2 save                                              # Save current process list
pm2 unstartup systemd                                 # Remove startup hook
```

## 🚀 Process Management

```bash
pm2 start app.js                                      # Start a Node app
pm2 start app.js --name "api-server"                  # With custom name
pm2 start app.js -i max                               # Cluster mode (all CPUs)
pm2 start app.js -i 4                                 # 4 instances
pm2 start npm -- start                                # Start npm script
pm2 start app.js --watch                              # Auto-restart on change
pm2 start app.js --max-memory-restart 300M            # Restart if > 300MB

pm2 stop api-server                                   # Stop by name
pm2 stop all                                          # Stop everything
pm2 restart api-server                                # Hard restart
pm2 reload api-server                                 # Graceful reload (0-downtime)
pm2 delete api-server                                 # Remove from PM2

pm2 scale api-server +2                               # Add 2 instances
pm2 scale api-server 6                                # Scale to exactly 6
```

## 📊 Monitoring & Status

```bash
pm2 list                                              # List all processes
pm2 show api-server                                   # Detailed info
pm2 monit                                             # Terminal dashboard
pm2 plus                                              # PM2 Plus web dashboard
pm2 report                                            # Full diagnostic report
```

## 📝 Ecosystem File (Production Standard)

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api-server',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    max_memory_restart: '1G',
    env_production: {
      NODE_ENV: 'production',
      PORT: 8080,
    },
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    error_file: './logs/api-error.log',
    out_file: './logs/api-out.log',
    merge_logs: true,
    max_restarts: 10,
    min_uptime: '10s',
    restart_delay: 4000,
    kill_timeout: 5000,
    listen_timeout: 3000,
  }],
};
```

```bash
pm2 start ecosystem.config.js --env production         # Production mode
pm2 reload ecosystem.config.js --env production        # Graceful reload
```

## 📋 Log Management

```bash
pm2 logs                                              # All process logs
pm2 logs api-server --lines 200                       # Last 200 lines
pm2 logs --json                                       # JSON format
pm2 flush                                             # Empty all log files

# Log rotation module
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 50M
pm2 set pm2-logrotate:retain 30
pm2 set pm2-logrotate:compress true
```

## 🚢 Deployment

```javascript
// ecosystem.config.js deploy section
module.exports = {
  apps: [{ /* ... */ }],
  deploy: {
    production: {
      user: 'deploy',
      host: ['10.0.1.10', '10.0.1.11'],
      ref: 'origin/main',
      repo: 'git@github.com:org/myapp.git',
      path: '/var/www/myapp',
      'post-deploy': 'npm ci && npm run build && pm2 reload ecosystem.config.js --env production',
    },
  },
};
```

```bash
pm2 deploy production setup                           # First-time setup
pm2 deploy production                                 # Deploy latest
pm2 deploy production revert 1                        # Rollback 1 revision
```

## 🔍 Graceful Shutdown (In Your App)

```javascript
process.on('SIGINT', () => {
  server.close(() => {
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 5000);
});
```

## 🧹 Maintenance

```bash
pm2 update                                            # Update PM2 daemon
pm2 reset api-server                                  # Reset restart counters
pm2 resurrect                                         # Restore saved processes
pm2 kill                                              # Kill PM2 daemon
pm2 ping                                              # Check if daemon alive
```

---

> 💡 **Production Rules:** Always use `ecosystem.config.js`. Always use `pm2 reload` (not restart) for zero-downtime. Always run `pm2 save` after changes. Never use `--watch` in production.
