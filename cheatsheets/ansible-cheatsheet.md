# 🤖 Ansible Cheatsheet

> Agentless automation — playbooks, roles, templates, vault, and production patterns.

---

## 📦 Installation & Setup

```bash
pip install ansible                                   # Python pip
sudo apt install -y ansible                           # Debian/Ubuntu
brew install ansible                                  # macOS
ansible --version                                     # Verify

# Test connectivity
ansible all -m ping -i inventory.yml
```

## 📋 Inventory

```yaml
# inventory.yml
all:
  children:
    web:
      hosts:
        web1.example.com:
        web2.example.com:
      vars:
        http_port: 80
    db:
      hosts:
        db1.example.com:
          ansible_port: 2222
        db2.example.com:
    staging:
      hosts:
        staging.example.com:
          ansible_user: deploy
          ansible_ssh_private_key_file: ~/.ssh/staging.pem

  vars:
    ansible_user: ubuntu
    ansible_python_interpreter: /usr/bin/python3
```

## 🚀 Ad-Hoc Commands

```bash
ansible all -m ping -i inventory.yml                  # Connectivity test
ansible web -m shell -a "uptime" -i inventory.yml    # Run command
ansible web -m copy -a "src=app.conf dest=/etc/app/" -i inventory.yml
ansible web -m apt -a "name=nginx state=present" -i inventory.yml --become
ansible web -m service -a "name=nginx state=restarted" -i inventory.yml --become
ansible all -m setup -i inventory.yml                 # Gather facts
ansible all -m setup -a "filter=ansible_memtotal_mb" -i inventory.yml
```

## 📝 Playbooks

```yaml
# deploy.yml
---
- name: Deploy web application
  hosts: web
  become: yes
  vars:
    app_version: "2.0.0"
    app_port: 3000

  pre_tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

  tasks:
    - name: Install dependencies
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - nodejs
        - npm

    - name: Create app directory
      file:
        path: /opt/myapp
        state: directory
        owner: appuser
        group: appgroup
        mode: '0755'

    - name: Deploy application
      copy:
        src: "dist/"
        dest: /opt/myapp/
        owner: appuser
      notify: restart app

    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/myapp
        mode: '0644'
      notify: reload nginx

    - name: Enable site
      file:
        src: /etc/nginx/sites-available/myapp
        dest: /etc/nginx/sites-enabled/myapp
        state: link
      notify: reload nginx

    - name: Ensure app is running
      systemd:
        name: myapp
        state: started
        enabled: yes

  handlers:
    - name: restart app
      systemd:
        name: myapp
        state: restarted

    - name: reload nginx
      systemd:
        name: nginx
        state: reloaded
```

## 🧩 Roles

```
# Role directory structure
roles/
└── webserver/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── nginx.conf.j2
    ├── files/
    │   └── app.conf
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml          # Default variables (lowest priority)
    └── meta/
        └── main.yml          # Dependencies
```

```yaml
# Using roles in playbook
- hosts: web
  become: yes
  roles:
    - common
    - { role: webserver, http_port: 8080 }
    - { role: monitoring, when: enable_monitoring | default(true) }
```

## 📐 Jinja2 Templates

```jinja2
{# templates/nginx.conf.j2 #}
server {
    listen {{ http_port | default(80) }};
    server_name {{ ansible_fqdn }};

    location / {
        proxy_pass http://127.0.0.1:{{ app_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

{% if ssl_enabled | default(false) %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
{% endif %}

{% for upstream in app_instances %}
    upstream backend_{{ loop.index }} {
        server {{ upstream.host }}:{{ upstream.port }};
    }
{% endfor %}
}
```

## 🔐 Ansible Vault (Secrets)

```bash
# Create encrypted file
ansible-vault create secrets.yml
ansible-vault edit secrets.yml                        # Edit encrypted file
ansible-vault view secrets.yml                        # View contents
ansible-vault encrypt vars.yml                        # Encrypt existing file
ansible-vault decrypt vars.yml                        # Decrypt file
ansible-vault rekey secrets.yml                       # Change password

# Use in playbook
ansible-playbook deploy.yml --ask-vault-pass
ansible-playbook deploy.yml --vault-password-file=.vault_pass

# Encrypt single string
ansible-vault encrypt_string 'mySecretPassword' --name 'db_password'
# Output: !vault | encrypted_string...
```

## 🔄 Loops, Conditionals & Error Handling

```yaml
# Loops
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop: [nginx, redis, postgresql]

# Conditionals
- name: Install on Debian only
  apt: name=nginx state=present
  when: ansible_os_family == "Debian"

# Error handling
- name: Try risky operation
  block:
    - name: Attempt deployment
      shell: /opt/deploy.sh
  rescue:
    - name: Rollback on failure
      shell: /opt/rollback.sh
  always:
    - name: Send notification
      slack: msg="Deploy {{ 'succeeded' if not ansible_failed_task else 'failed' }}"

# Ignore errors
- name: Check optional service
  command: systemctl status optional-service
  ignore_errors: yes
  register: service_check

# Retries
- name: Wait for service
  uri:
    url: http://localhost:8080/health
    status_code: 200
  register: result
  until: result.status == 200
  retries: 10
  delay: 5
```

## 🎯 FAANG Interview Q&A

```
Q: Ansible vs Terraform?
A: Ansible: configuration management (install packages, configure services).
   Terraform: infrastructure provisioning (create VMs, networks, DBs).
   They're complementary: Terraform creates infra, Ansible configures it.

Q: What makes Ansible idempotent?
A: Ansible modules check current state before making changes.
   Example: apt module checks if package is installed before installing.
   Running the same playbook twice produces no changes the second time.
   Key: use modules (declarative), avoid raw shell commands.

Q: How do you handle secrets in Ansible?
A: ansible-vault for file encryption, encrypt_string for inline secrets,
   or integrate with HashiCorp Vault / AWS Secrets Manager.
   Never store plaintext secrets in playbooks or inventory.

Q: Ansible vs Chef/Puppet?
A: Ansible: agentless (SSH), push-based, YAML (simple), Python.
   Chef: agent-based, pull-based, Ruby DSL, steep learning curve.
   Puppet: agent-based, pull-based, declarative DSL.
   Ansible wins on simplicity and zero-dependency setup.
```

---

> 💡 **Production Rule:** Always use roles for reusable code, vault for secrets, and `--check` (dry run) before applying changes. Test playbooks in staging before production.
