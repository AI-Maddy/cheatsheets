================================================================================
SSH HARDENING
================================================================================

**Complete Guide to Secure Shell Hardening and Key-Based Authentication**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 6

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # SSH Server Hardening
   sudo nano /etc/ssh/sshd_config                              # Edit SSH config
   sudo systemctl restart sshd                                  # Restart SSH
   
   # Generate SSH Keys
   ssh-keygen -t ed25519 -C "user@email"                       # Generate Ed25519 key
   ssh-copy-id user@server                                      # Copy key to server
   
   # Disable Password Authentication
   PermitRootLogin no                                           # In sshd_config
   PasswordAuthentication no                                    # In sshd_config
   PubkeyAuthentication yes                                     # In sshd_config
   
   # fail2ban Setup
   sudo apt install fail2ban                                    # Install
   sudo systemctl enable --now fail2ban                         # Enable
   sudo fail2ban-client status sshd                            # Check status

================================================================================
PART 1: SSH FUNDAMENTALS
================================================================================

1. SSH Basics
=============

1.1 What is SSH?
----------------

**SSH (Secure Shell)** provides:
- Encrypted remote access
- Secure file transfers (SCP, SFTP)
- Port forwarding/tunneling
- Secure command execution
- Public key authentication

**Why Harden SSH?**
- Primary target for attacks
- Often exposed to internet
- Gateway to entire system
- Brute-force attempts common
- Misconfiguration = compromise

1.2 SSH Configuration Files
----------------------------

.. code-block:: text

   /etc/ssh/sshd_config          # Server configuration
   /etc/ssh/ssh_config           # Client configuration
   ~/.ssh/config                 # User client configuration
   ~/.ssh/authorized_keys        # Authorized public keys
   ~/.ssh/known_hosts            # Known server fingerprints
   ~/.ssh/id_rsa                 # Private key (RSA)
   ~/.ssh/id_ed25519             # Private key (Ed25519)
   ~/.ssh/id_rsa.pub             # Public key (RSA)
   ~/.ssh/id_ed25519.pub         # Public key (Ed25519)

================================================================================
2. SSH Key Generation
================================================================================

2.1 Generate SSH Keys
----------------------

.. code-block:: bash

   # Ed25519 (recommended - faster, more secure)
   ssh-keygen -t ed25519 -C "user@email.com"
   
   # RSA 4096-bit (widely compatible)
   ssh-keygen -t rsa -b 4096 -C "user@email.com"
   
   # ECDSA (elliptic curve)
   ssh-keygen -t ecdsa -b 521 -C "user@email.com"
   
   # Specify custom filename
   ssh-keygen -t ed25519 -f ~/.ssh/id_server1 -C "Server1 key"
   
   # Generate without passphrase (NOT recommended)
   ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_nopass

2.2 Key Types Comparison
-------------------------

.. code-block:: text

   Type       Key Size   Security   Speed    Compatibility
   --------   --------   --------   -----    -------------
   Ed25519    256-bit    Excellent  Fastest  Modern systems
   RSA        4096-bit   Excellent  Slower   Universal
   ECDSA      521-bit    Good       Fast     Modern systems
   RSA        2048-bit   Good       Slow     Universal (legacy)

   **Recommendation:** Ed25519 for new setups, RSA 4096 for legacy support

2.3 Change Key Passphrase
--------------------------

.. code-block:: bash

   # Change passphrase
   ssh-keygen -p -f ~/.ssh/id_ed25519
   
   # Remove passphrase (NOT recommended)
   ssh-keygen -p -N "" -f ~/.ssh/id_ed25519
   
   # Add passphrase to existing key
   ssh-keygen -p -f ~/.ssh/id_ed25519

================================================================================
3. SSH Key Deployment
================================================================================

3.1 Copy Public Key to Server
------------------------------

.. code-block:: bash

   # Automatic (preferred method)
   ssh-copy-id user@server
   
   # Specify key file
   ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
   
   # Specify custom port
   ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 user@server
   
   # Manual method
   cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
   
   # Or copy-paste method
   cat ~/.ssh/id_ed25519.pub
   # Copy output, then on server:
   mkdir -p ~/.ssh
   nano ~/.ssh/authorized_keys  # Paste key
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys

3.2 Test Key Authentication
----------------------------

.. code-block:: bash

   # Test connection
   ssh user@server
   
   # Test with specific key
   ssh -i ~/.ssh/id_ed25519 user@server
   
   # Verbose mode (debugging)
   ssh -v user@server           # Verbose
   ssh -vv user@server          # More verbose
   ssh -vvv user@server         # Maximum verbose

3.3 Multiple Keys Management
-----------------------------

.. code-block:: bash

   # Create SSH config file
   nano ~/.ssh/config
   
   # Add hosts:
   Host server1
       HostName 192.168.1.10
       User admin
       IdentityFile ~/.ssh/id_server1
       Port 2222
   
   Host server2
       HostName server2.example.com
       User root
       IdentityFile ~/.ssh/id_server2
   
   Host github
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_github
   
   # Now connect simply:
   ssh server1
   ssh server2
   ssh github

================================================================================
PART 2: SSH SERVER HARDENING
================================================================================

4. Basic SSH Hardening
======================

4.1 Edit SSH Configuration
---------------------------

.. code-block:: bash

   # Backup original config
   sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
   
   # Edit config
   sudo nano /etc/ssh/sshd_config
   
   # Test configuration
   sudo sshd -t
   
   # Restart SSH service
   sudo systemctl restart sshd           # Ubuntu/Debian
   sudo systemctl restart ssh            # Some systems
   sudo systemctl restart openssh-server # Older systems

4.2 Essential Hardening Settings
---------------------------------

.. code-block:: bash

   # Disable root login
   PermitRootLogin no
   
   # Disable password authentication (after setting up keys!)
   PasswordAuthentication no
   PubkeyAuthentication yes
   
   # Disable empty passwords
   PermitEmptyPasswords no
   
   # Change default port (reduces automated attacks)
   Port 2222
   
   # Limit authentication attempts
   MaxAuthTries 3
   
   # Set idle timeout (15 minutes)
   ClientAliveInterval 300
   ClientAliveCountMax 0
   
   # Disable X11 forwarding (if not needed)
   X11Forwarding no
   
   # Allow only specific users
   AllowUsers alice bob charlie
   # Or allow only specific groups
   AllowGroups sshusers
   
   # Disable host-based authentication
   HostbasedAuthentication no
   
   # Disable rhosts
   IgnoreRhosts yes

4.3 Complete Hardened Configuration
------------------------------------

.. code-block:: bash

   # /etc/ssh/sshd_config - Hardened Configuration
   
   # Network
   Port 2222
   AddressFamily inet                    # IPv4 only (or inet6 for IPv6)
   ListenAddress 0.0.0.0                # Or specific IP
   
   # Protocol
   Protocol 2                            # SSH version 2 only
   
   # Logging
   SyslogFacility AUTH
   LogLevel VERBOSE                      # Or INFO
   
   # Authentication
   LoginGraceTime 30
   PermitRootLogin no
   StrictModes yes
   MaxAuthTries 3
   MaxSessions 2
   PubkeyAuthentication yes
   PasswordAuthentication no
   PermitEmptyPasswords no
   ChallengeResponseAuthentication no
   UsePAM yes
   
   # Limit users/groups
   AllowGroups sshusers
   
   # Kerberos/GSSAPI (disable if not using)
   KerberosAuthentication no
   GSSAPIAuthentication no
   
   # Security options
   IgnoreRhosts yes
   HostbasedAuthentication no
   PermitUserEnvironment no
   
   # Idle timeout (15 minutes)
   ClientAliveInterval 300
   ClientAliveCountMax 0
   
   # Disable forwarding (enable if needed)
   AllowTcpForwarding no
   AllowStreamLocalForwarding no
   GatewayPorts no
   PermitTunnel no
   X11Forwarding no
   
   # Subsystems
   Subsystem sftp /usr/lib/openssh/sftp-server
   
   # Banner
   Banner /etc/ssh/banner.txt

4.4 Create SSH Banner
---------------------

.. code-block:: bash

   # Create banner file
   sudo nano /etc/ssh/banner.txt
   
   # Example content:
   ################################################################################
   #                         AUTHORIZED ACCESS ONLY                               #
   #                                                                              #
   # This system is for authorized use only. All activity is logged and          #
   # monitored. Unauthorized access is prohibited and will be prosecuted         #
   # to the fullest extent of the law.                                           #
   ################################################################################
   
   # Apply permissions
   sudo chmod 644 /etc/ssh/banner.txt

================================================================================
5. Advanced SSH Hardening
==========================

5.1 Strong Encryption Ciphers
------------------------------

.. code-block:: bash

   # Add to /etc/ssh/sshd_config
   
   # Key exchange algorithms (strong only)
   KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
   
   # Ciphers (strong only)
   Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
   
   # MACs (strong only)
   MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
   
   # Host keys (Ed25519 and RSA only)
   HostKey /etc/ssh/ssh_host_ed25519_key
   HostKey /etc/ssh/ssh_host_rsa_key

5.2 Two-Factor Authentication (2FA)
------------------------------------

.. code-block:: bash

   # Install Google Authenticator
   sudo apt install libpam-google-authenticator     # Debian/Ubuntu
   sudo dnf install google-authenticator            # RHEL/CentOS/Fedora
   
   # Configure for user
   google-authenticator
   # Answer:
   # - Time-based tokens: y
   # - Update .google_authenticator file: y
   # - Disallow multiple uses: y
   # - Rate limiting: y
   # - Rate limiting window: y
   
   # Scan QR code with authenticator app (Google Authenticator, Authy, etc.)
   
   # Edit PAM configuration
   sudo nano /etc/pam.d/sshd
   
   # Add at the top:
   auth required pam_google_authenticator.so nullok
   # nullok allows users without 2FA to still login
   
   # Edit SSH config
   sudo nano /etc/ssh/sshd_config
   
   # Enable challenge-response
   ChallengeResponseAuthentication yes
   # If using keys + 2FA:
   AuthenticationMethods publickey,keyboard-interactive
   
   # Restart SSH
   sudo systemctl restart sshd
   
   # Test (keep current session open!)
   ssh user@localhost

5.3 SSH Certificate Authentication
-----------------------------------

.. code-block:: bash

   # Generate CA key (on secure system)
   ssh-keygen -t ed25519 -f ~/.ssh/ca_key -C "SSH CA"
   
   # Sign user key
   ssh-keygen -s ~/.ssh/ca_key -I user_identifier -n username -V +52w ~/.ssh/id_ed25519.pub
   # Creates id_ed25519-cert.pub
   
   # On server, trust the CA
   echo "@cert-authority * $(cat ~/.ssh/ca_key.pub)" | sudo tee -a /etc/ssh/ca_keys
   
   # Edit sshd_config
   TrustedUserCAKeys /etc/ssh/ca_keys
   
   # User can now login with certificate
   ssh -i ~/.ssh/id_ed25519 user@server

================================================================================
PART 3: FAIL2BAN INTEGRATION
================================================================================

6. fail2ban Setup
=================

6.1 Install and Configure fail2ban
-----------------------------------

.. code-block:: bash

   # Install
   sudo apt install fail2ban                        # Debian/Ubuntu
   sudo dnf install fail2ban                        # RHEL/CentOS/Fedora
   
   # Enable and start
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   
   # Check status
   sudo systemctl status fail2ban
   
   # Copy default config
   sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   
   # Edit local config
   sudo nano /etc/fail2ban/jail.local

6.2 SSH Jail Configuration
---------------------------

.. code-block:: bash

   # Edit /etc/fail2ban/jail.local
   
   [DEFAULT]
   # Ban time (10 minutes)
   bantime = 10m
   
   # Find time window (10 minutes)
   findtime = 10m
   
   # Max retry attempts
   maxretry = 3
   
   # Destination email for notifications
   destemail = admin@example.com
   sendername = Fail2Ban
   
   # Email action
   action = %(action_mwl)s
   
   [sshd]
   enabled = true
   port = ssh,2222                              # Add custom port
   logpath = /var/log/auth.log                 # Debian/Ubuntu
   # logpath = /var/log/secure                 # RHEL/CentOS
   maxretry = 3
   bantime = 1h
   findtime = 10m

6.3 fail2ban Management
------------------------

.. code-block:: bash

   # Check status
   sudo fail2ban-client status
   
   # Check specific jail
   sudo fail2ban-client status sshd
   
   # Manually ban IP
   sudo fail2ban-client set sshd banip 192.168.1.100
   
   # Manually unban IP
   sudo fail2ban-client set sshd unbanip 192.168.1.100
   
   # Show banned IPs
   sudo fail2ban-client get sshd banned
   
   # Reload configuration
   sudo fail2ban-client reload
   
   # Restart fail2ban
   sudo systemctl restart fail2ban
   
   # View logs
   sudo tail -f /var/log/fail2ban.log

6.4 Advanced fail2ban Rules
----------------------------

.. code-block:: bash

   # Create custom filter
   sudo nano /etc/fail2ban/filter.d/sshd-aggressive.conf
   
   [Definition]
   failregex = ^%(__prefix_line)sFailed (?:password|publickey) for .* from <HOST>(?: port \d+)?(?: ssh\d*)?$
               ^%(__prefix_line)sConnection closed by <HOST> port \d+ \[preauth\]$
               ^%(__prefix_line)sDisconnected from <HOST> port \d+ \[preauth\]$
   ignoreregex =
   
   # Use in jail.local
   [sshd-aggressive]
   enabled = true
   filter = sshd-aggressive
   port = ssh,2222
   logpath = /var/log/auth.log
   maxretry = 2
   bantime = 24h
   findtime = 5m

================================================================================
7. SSH Port Forwarding and Tunneling
================================================================================

7.1 Local Port Forwarding
--------------------------

.. code-block:: bash

   # Forward local port to remote service
   ssh -L 8080:localhost:80 user@server
   # Access remote port 80 via local port 8080
   # Browse: http://localhost:8080
   
   # Forward to different remote host
   ssh -L 3306:database.internal:3306 user@jumphost
   # Access database.internal:3306 via localhost:3306
   
   # Background (-f) and no command (-N)
   ssh -f -N -L 8080:localhost:80 user@server

7.2 Remote Port Forwarding
---------------------------

.. code-block:: bash

   # Forward remote port to local service
   ssh -R 8080:localhost:80 user@server
   # Server port 8080 -> your localhost:80
   
   # Allow others on remote to connect
   # On server, set in sshd_config:
   GatewayPorts yes
   
   # Then:
   ssh -R 0.0.0.0:8080:localhost:80 user@server

7.3 Dynamic Port Forwarding (SOCKS Proxy)
------------------------------------------

.. code-block:: bash

   # Create SOCKS proxy
   ssh -D 1080 user@server
   
   # Configure browser:
   # SOCKS Host: localhost
   # Port: 1080
   # SOCKS v5
   
   # Test with curl
   curl --socks5 localhost:1080 http://example.com
   
   # Background
   ssh -f -N -D 1080 user@server

7.4 Jump Host / Bastion
------------------------

.. code-block:: bash

   # Connect through jump host
   ssh -J jumpuser@jumphost user@destination
   
   # Multiple jumps
   ssh -J jump1,jump2 user@destination
   
   # In ~/.ssh/config:
   Host destination
       HostName 10.0.0.100
       User admin
       ProxyJump jumphost
   
   Host jumphost
       HostName jumphost.example.com
       User jumpuser

================================================================================
8. SSH Monitoring and Logging
================================================================================

8.1 View SSH Logs
-----------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo tail -f /var/log/auth.log
   sudo grep sshd /var/log/auth.log
   
   # RHEL/CentOS/Fedora
   sudo tail -f /var/log/secure
   sudo grep sshd /var/log/secure
   
   # With journalctl (systemd)
   sudo journalctl -u sshd -f
   sudo journalctl -u ssh -f
   
   # Show failed login attempts
   sudo grep "Failed password" /var/log/auth.log
   
   # Show successful logins
   sudo grep "Accepted publickey" /var/log/auth.log
   sudo grep "Accepted password" /var/log/auth.log

8.2 Monitor Active SSH Sessions
--------------------------------

.. code-block:: bash

   # Show logged-in users
   who
   w
   
   # Show user logins
   last
   lastlog
   
   # Show failed login attempts
   lastb
   
   # Show current SSH connections
   ss -tnp | grep sshd
   netstat -tnp | grep sshd
   
   # Show detailed connection info
   sudo lsof -i :22
   sudo lsof -i :2222  # Custom port

8.3 Automated Monitoring Script
--------------------------------

.. code-block:: bash

   #!/bin/bash
   # ssh-monitor.sh
   
   LOG_FILE="/var/log/ssh-monitor.log"
   
   # Function to log with timestamp
   log() {
       echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
   }
   
   # Check for failed logins in last hour
   FAILED=$(sudo grep "Failed password" /var/log/auth.log | grep "$(date '+%b %d')" | tail -10)
   if [ -n "$FAILED" ]; then
       log "WARNING: Failed SSH login attempts detected"
       echo "$FAILED" >> "$LOG_FILE"
   fi
   
   # Check active sessions
   SESSIONS=$(who | grep -c pts)
   log "Active SSH sessions: $SESSIONS"
   
   # Check fail2ban status
   if systemctl is-active --quiet fail2ban; then
       BANNED=$(sudo fail2ban-client status sshd | grep "Currently banned" | awk '{print $NF}')
       log "fail2ban banned IPs: $BANNED"
   fi

================================================================================
9. SSH Best Practices
================================================================================

9.1 Security Checklist
-----------------------

.. code-block:: text

   ☐ Use Ed25519 or RSA 4096-bit keys
   ☐ Disable password authentication
   ☐ Disable root login
   ☐ Change default SSH port
   ☐ Use fail2ban
   ☐ Enable 2FA (if possible)
   ☐ Limit user access (AllowUsers/AllowGroups)
   ☐ Set idle timeout
   ☐ Use strong ciphers only
   ☐ Keep SSH updated
   ☐ Monitor SSH logs
   ☐ Use SSH keys with passphrases
   ☐ Regular security audits
   ☐ Firewall rules (limit SSH access)
   ☐ Use jump hosts for internal servers

9.2 Emergency Access Recovery
------------------------------

.. code-block:: bash

   # If locked out, use console access (VPS panel, physical access)
   
   # Reset sshd_config to defaults
   sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
   sudo systemctl restart sshd
   
   # Temporarily enable password auth
   # Edit /etc/ssh/sshd_config:
   PasswordAuthentication yes
   # Restart and fix keys, then disable again
   
   # Check fail2ban bans
   sudo fail2ban-client set sshd unbanip YOUR_IP
   
   # Disable fail2ban temporarily
   sudo systemctl stop fail2ban

9.3 SSH Client Hardening
-------------------------

.. code-block:: bash

   # Edit ~/.ssh/config or /etc/ssh/ssh_config
   
   # Use strong ciphers
   Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
   
   # Verify host keys
   StrictHostKeyChecking ask
   
   # Use SSH agent
   AddKeysToAgent yes
   
   # Connection timeout
   ServerAliveInterval 60
   ServerAliveCountMax 3
   
   # Disable roaming
   UseRoaming no
   
   # Hashing known_hosts
   HashKnownHosts yes

================================================================================
10. Troubleshooting
===================

10.1 Common Issues
------------------

.. code-block:: bash

   # Permission errors
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   chmod 600 ~/.ssh/authorized_keys
   
   # Wrong ownership
   chown $USER:$USER ~/.ssh
   chown $USER:$USER ~/.ssh/*
   
   # Server-side authorized_keys permissions
   sudo chmod 700 /home/username/.ssh
   sudo chmod 600 /home/username/.ssh/authorized_keys
   sudo chown username:username /home/username/.ssh -R
   
   # SELinux context (RHEL/CentOS)
   restorecon -Rv ~/.ssh

10.2 Debug Connection Issues
-----------------------------

.. code-block:: bash

   # Verbose client output
   ssh -vvv user@server
   
   # Test server configuration
   sudo sshd -t
   
   # Check server logs
   sudo tail -50 /var/log/auth.log
   sudo journalctl -u sshd -n 50
   
   # Test specific key
   ssh -i ~/.ssh/id_ed25519 -vv user@server
   
   # Check if server is listening
   sudo ss -tlnp | grep sshd
   
   # Test from different network
   ssh -p 2222 user@server.example.com

10.3 Performance Issues
-----------------------

.. code-block:: bash

   # Disable DNS lookup (speeds up connections)
   UseDNS no                    # In sshd_config
   
   # Use compression
   Compression yes              # In sshd_config
   
   # Client-side compression
   ssh -C user@server
   
   # Reduce verbosity
   LogLevel INFO                # In sshd_config

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- User_Account_Security.rst - User management and sudo configuration
- Firewall_iptables.rst - Firewall rules for SSH
- Encryption_Technologies.rst - GPG and encryption fundamentals
- Linux_Security_Basics.rst - Overall security principles

================================================================================
END OF SSH HARDENING
================================================================================
