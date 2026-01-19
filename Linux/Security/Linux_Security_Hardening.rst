===================================
Linux Security Hardening Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: System hardening, secure configuration, defense-in-depth

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Hardening Checklist
==================================

Essential Security Commands
----------------------------

.. code-block:: bash

   # Update system immediately
   sudo apt update && sudo apt upgrade -y  # Debian/Ubuntu
   sudo dnf upgrade -y  # Fedora/RHEL
   
   # Disable root SSH login
   sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
   sudo systemctl restart sshd
   
   # Configure firewall
   sudo ufw enable  # Ubuntu
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp  # SSH only
   
   # Enable automatic security updates
   sudo apt install unattended-upgrades  # Debian/Ubuntu
   sudo dpkg-reconfigure -plow unattended-upgrades
   
   # Check for rootkits
   sudo rkhunter --check
   sudo chkrootkit
   
   # Audit open ports
   sudo ss -tuln
   sudo netstat -tuln
   
   # Check failed login attempts
   sudo lastb
   sudo journalctl _COMM=sshd | grep -i failed

Quick Hardening Script
-----------------------

.. code-block:: bash

   #!/bin/bash
   # Basic security hardening
   
   # Disable unused services
   systemctl disable bluetooth cups avahi-daemon
   
   # Set secure umask
   echo "umask 027" >> /etc/profile
   
   # Disable USB storage (optional)
   echo "install usb-storage /bin/true" > /etc/modprobe.d/disable-usb-storage.conf
   
   # Enable process accounting
   apt install acct
   systemctl enable acct
   
   # Set password policies
   apt install libpam-pwquality
   sed -i 's/# minlen = 8/minlen = 12/' /etc/security/pwquality.conf

User Account Security
=====================

Password Policies
-----------------

.. code-block:: bash

   # Install password quality checking
   sudo apt install libpam-pwquality
   
   # Configure password requirements
   # /etc/security/pwquality.conf
   sudo tee -a /etc/security/pwquality.conf <<EOF
   # Password must be at least 12 characters
   minlen = 12
   # Require at least one digit
   dcredit = -1
   # Require at least one uppercase
   ucredit = -1
   # Require at least one lowercase
   lcredit = -1
   # Require at least one special character
   ocredit = -1
   # Check against dictionary
   dictcheck = 1
   # Enforce password history (prevent reuse)
   remember = 5
   EOF
   
   # Set password aging
   # /etc/login.defs
   sudo sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
   sudo sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   7/' /etc/login.defs
   sudo sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   14/' /etc/login.defs
   
   # Apply to existing user
   sudo chage -M 90 -m 7 -W 14 username

Account Lockout
---------------

.. code-block:: bash

   # Install fail2ban
   sudo apt install fail2ban
   
   # Configure fail2ban
   # /etc/fail2ban/jail.local
   sudo tee /etc/fail2ban/jail.local <<EOF
   [DEFAULT]
   bantime = 3600
   findtime = 600
   maxretry = 3
   
   [sshd]
   enabled = true
   port = 22
   logpath = /var/log/auth.log
   maxretry = 3
   EOF
   
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   
   # Check banned IPs
   sudo fail2ban-client status sshd
   
   # Unban IP
   sudo fail2ban-client set sshd unbanip 192.168.1.100

sudo Configuration
------------------

.. code-block:: bash

   # Best practices for sudoers
   # Use visudo to edit /etc/sudoers
   sudo visudo
   
   # Examples:
   # Allow user to run specific command without password
   username ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
   
   # Allow group to run all commands
   %admin ALL=(ALL:ALL) ALL
   
   # Require password for sudo
   Defaults timestamp_timeout=0
   
   # Log sudo commands
   Defaults logfile="/var/log/sudo.log"
   Defaults log_input,log_output
   
   # Require tty
   Defaults requiretty
   
   # View sudo logs
   sudo cat /var/log/sudo.log
   sudo journalctl _COMM=sudo

SSH Hardening
=============

SSH Server Configuration
-------------------------

.. code-block:: bash

   # /etc/ssh/sshd_config
   sudo tee /etc/ssh/sshd_config <<EOF
   # Protocol and encryption
   Protocol 2
   
   # Authentication
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   PermitEmptyPasswords no
   ChallengeResponseAuthentication no
   UsePAM yes
   
   # Limit users
   AllowUsers user1 user2
   AllowGroups sshusers
   DenyUsers baduser
   
   # Timeout
   ClientAliveInterval 300
   ClientAliveCountMax 0
   LoginGraceTime 60
   
   # Limits
   MaxAuthTries 3
   MaxSessions 2
   MaxStartups 10:30:60
   
   # Logging
   SyslogFacility AUTH
   LogLevel VERBOSE
   
   # Network
   AddressFamily inet  # IPv4 only
   ListenAddress 0.0.0.0
   Port 22  # Consider non-standard port
   
   # X11 and forwarding
   X11Forwarding no
   AllowTcpForwarding no
   AllowStreamLocalForwarding no
   GatewayPorts no
   PermitTunnel no
   
   # Banner
   Banner /etc/ssh/banner
   
   # Strong ciphers only
   Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com
   MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
   KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256
   EOF
   
   sudo systemctl restart sshd
   
   # Test configuration
   sudo sshd -t

SSH Key Management
------------------

.. code-block:: bash

   # Generate strong SSH key
   ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519
   # Or RSA 4096
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
   
   # Copy key to server
   ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
   
   # Set proper permissions
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   chmod 600 ~/.ssh/authorized_keys
   
   # Disable password authentication after key setup
   sudo sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
   sudo systemctl restart sshd

Two-Factor Authentication
--------------------------

.. code-block:: bash

   # Install Google Authenticator
   sudo apt install libpam-google-authenticator
   
   # Setup for user
   google-authenticator
   # Answer: yes, yes, yes, no, yes
   
   # Configure PAM
   # /etc/pam.d/sshd
   # Add at top:
   auth required pam_google_authenticator.so
   
   # Configure SSH
   # /etc/ssh/sshd_config
   ChallengeResponseAuthentication yes
   AuthenticationMethods publickey,keyboard-interactive
   
   sudo systemctl restart sshd

Filesystem Security
===================

File Permissions
----------------

.. code-block:: bash

   # Find world-writable files
   sudo find / -xdev -type f -perm -0002 -ls 2>/dev/null
   
   # Find files with no owner
   sudo find / -xdev -nouser -o -nogroup 2>/dev/null
   
   # Find SUID files
   sudo find / -xdev -type f -perm -4000 -ls 2>/dev/null
   
   # Find SGID files
   sudo find / -xdev -type f -perm -2000 -ls 2>/dev/null
   
   # Secure sensitive files
   sudo chmod 600 /etc/ssh/*_key
   sudo chmod 644 /etc/ssh/*_key.pub
   sudo chmod 600 /boot/grub/grub.cfg
   sudo chmod 640 /etc/shadow
   sudo chmod 640 /etc/gshadow
   
   # Set immutable attribute (prevent deletion/modification)
   sudo chattr +i /etc/resolv.conf
   sudo chattr -i /etc/resolv.conf  # Remove

Mount Options
-------------

.. code-block:: bash

   # Secure mount options in /etc/fstab
   
   # /tmp with noexec, nosuid, nodev
   tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev,size=2G 0 0
   
   # /var/tmp
   tmpfs /var/tmp tmpfs defaults,noexec,nosuid,nodev,size=2G 0 0
   
   # /home with nosuid, nodev
   /dev/sda2 /home ext4 defaults,nosuid,nodev 0 2
   
   # /boot with ro (read-only) - remount rw for updates
   /dev/sda1 /boot ext4 defaults,ro 0 2
   
   # Apply changes
   sudo mount -a
   sudo mount -o remount /tmp

Disk Encryption
---------------

.. code-block:: bash

   # LUKS encryption for new partition
   sudo cryptsetup luksFormat /dev/sdb1
   
   # Open encrypted partition
   sudo cryptsetup luksOpen /dev/sdb1 encrypted_data
   
   # Create filesystem
   sudo mkfs.ext4 /dev/mapper/encrypted_data
   
   # Mount
   sudo mount /dev/mapper/encrypted_data /mnt/secure
   
   # Add to /etc/crypttab for auto-mount
   encrypted_data /dev/sdb1 none luks
   
   # Close encrypted partition
   sudo umount /mnt/secure
   sudo cryptsetup luksClose encrypted_data

Kernel Hardening
================

Sysctl Security Settings
-------------------------

.. code-block:: bash

   # /etc/sysctl.d/99-security.conf
   sudo tee /etc/sysctl.d/99-security.conf <<EOF
   # IP Forwarding (disable unless router)
   net.ipv4.ip_forward = 0
   net.ipv6.conf.all.forwarding = 0
   
   # Disable source routing
   net.ipv4.conf.all.send_redirects = 0
   net.ipv4.conf.default.send_redirects = 0
   net.ipv4.conf.all.accept_source_route = 0
   net.ipv4.conf.default.accept_source_route = 0
   net.ipv6.conf.all.accept_source_route = 0
   
   # Disable ICMP redirects
   net.ipv4.conf.all.accept_redirects = 0
   net.ipv4.conf.default.accept_redirects = 0
   net.ipv6.conf.all.accept_redirects = 0
   
   # Enable IP spoofing protection
   net.ipv4.conf.all.rp_filter = 1
   net.ipv4.conf.default.rp_filter = 1
   
   # Ignore ICMP ping requests
   net.ipv4.icmp_echo_ignore_all = 1
   
   # Ignore broadcast pings
   net.ipv4.icmp_echo_ignore_broadcasts = 1
   
   # Enable bad error message protection
   net.ipv4.icmp_ignore_bogus_error_responses = 1
   
   # Enable TCP SYN cookies (DDoS protection)
   net.ipv4.tcp_syncookies = 1
   net.ipv4.tcp_syn_retries = 2
   net.ipv4.tcp_synack_retries = 2
   net.ipv4.tcp_max_syn_backlog = 4096
   
   # Log suspicious packets
   net.ipv4.conf.all.log_martians = 1
   net.ipv4.conf.default.log_martians = 1
   
   # Disable IPv6 if not needed
   net.ipv6.conf.all.disable_ipv6 = 1
   net.ipv6.conf.default.disable_ipv6 = 1
   
   # Kernel hardening
   kernel.dmesg_restrict = 1
   kernel.kptr_restrict = 2
   kernel.yama.ptrace_scope = 1
   kernel.kexec_load_disabled = 1
   
   # Core dumps
   kernel.core_uses_pid = 1
   fs.suid_dumpable = 0
   
   # Address Space Layout Randomization
   kernel.randomize_va_space = 2
   EOF
   
   # Apply settings
   sudo sysctl -p /etc/sysctl.d/99-security.conf

Kernel Modules
--------------

.. code-block:: bash

   # Disable unused kernel modules
   # /etc/modprobe.d/blacklist-security.conf
   sudo tee /etc/modprobe.d/blacklist-security.conf <<EOF
   # Disable uncommon network protocols
   install dccp /bin/true
   install sctp /bin/true
   install rds /bin/true
   install tipc /bin/true
   
   # Disable uncommon filesystems
   install cramfs /bin/true
   install freevxfs /bin/true
   install jffs2 /bin/true
   install hfs /bin/true
   install hfsplus /bin/true
   install udf /bin/true
   
   # Disable USB storage (if not needed)
   install usb-storage /bin/true
   
   # Disable Bluetooth (if not needed)
   install bluetooth /bin/true
   EOF
   
   # Update initramfs
   sudo update-initramfs -u

Service Hardening
=================

Disable Unnecessary Services
-----------------------------

.. code-block:: bash

   # List running services
   systemctl list-units --type=service --state=running
   
   # Disable common unnecessary services
   sudo systemctl disable --now avahi-daemon
   sudo systemctl disable --now cups
   sudo systemctl disable --now bluetooth
   sudo systemctl disable --now ModemManager
   
   # Check listening ports
   sudo ss -tuln
   sudo netstat -tuln
   
   # Remove unnecessary packages
   sudo apt remove --purge telnet ftp rsh-client
   sudo apt autoremove

Systemd Service Hardening
--------------------------

.. code-block:: bash

   # Example: Harden nginx service
   sudo systemctl edit nginx
   
   # Add these directives:
   [Service]
   # Run as unprivileged user
   User=nginx
   Group=nginx
   
   # Filesystem isolation
   ProtectSystem=strict
   ProtectHome=true
   ReadWritePaths=/var/log/nginx /var/cache/nginx
   
   # Network isolation
   PrivateNetwork=false
   RestrictAddressFamilies=AF_INET AF_INET6
   
   # Process isolation
   NoNewPrivileges=true
   PrivateTmp=true
   PrivateDevices=true
   
   # Capabilities
   CapabilityBoundingSet=CAP_NET_BIND_SERVICE
   AmbientCapabilities=CAP_NET_BIND_SERVICE
   
   # System calls
   SystemCallFilter=@system-service
   SystemCallFilter=~@privileged @resources
   
   # Restart policy
   Restart=on-failure
   RestartSec=5s
   
   sudo systemctl daemon-reload
   sudo systemctl restart nginx

Logging and Auditing
====================

Centralized Logging
-------------------

.. code-block:: bash

   # Configure rsyslog for centralized logging
   # /etc/rsyslog.conf
   
   # Send logs to remote server
   *.* @192.168.1.100:514  # UDP
   *.* @@192.168.1.100:514  # TCP
   
   # On log server, enable reception
   $ModLoad imudp
   $UDPServerRun 514
   
   # Restart rsyslog
   sudo systemctl restart rsyslog

Audit System (auditd)
---------------------

.. code-block:: bash

   # Install auditd
   sudo apt install auditd audispd-plugins
   
   # Enable auditd
   sudo systemctl enable auditd
   sudo systemctl start auditd
   
   # Add audit rules
   # /etc/audit/rules.d/audit.rules
   sudo tee -a /etc/audit/rules.d/audit.rules <<EOF
   # Monitor authentication
   -w /etc/passwd -p wa -k passwd_changes
   -w /etc/shadow -p wa -k shadow_changes
   -w /etc/group -p wa -k group_changes
   -w /etc/sudoers -p wa -k sudoers_changes
   
   # Monitor login/logout
   -w /var/log/lastlog -p wa -k logins
   -w /var/log/faillog -p wa -k logins
   -w /var/run/utmp -p wa -k session
   
   # Monitor network configuration
   -w /etc/hosts -p wa -k network_changes
   -w /etc/network/ -p wa -k network_changes
   
   # Monitor sysctl changes
   -w /etc/sysctl.conf -p wa -k sysctl_changes
   
   # Monitor kernel module loading
   -w /sbin/insmod -p x -k modules
   -w /sbin/rmmod -p x -k modules
   -w /sbin/modprobe -p x -k modules
   
   # Monitor file deletions
   -a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -k delete
   
   # Make rules immutable (reboot required to change)
   -e 2
   EOF
   
   # Reload rules
   sudo augenrules --load
   
   # Search audit logs
   sudo ausearch -k passwd_changes
   sudo ausearch -ts today -k network_changes
   
   # Generate audit report
   sudo aureport
   sudo aureport --auth
   sudo aureport --file

Best Practices
==============

1. **Apply principle of least privilege** to all accounts
2. **Keep system updated** with automatic security patches
3. **Use strong authentication** (SSH keys + 2FA)
4. **Enable logging and auditing** comprehensively
5. **Regular security scans** (rkhunter, chkrootkit, lynis)
6. **Monitor system** continuously for anomalies
7. **Backup critical data** with encryption
8. **Document all changes** for audit trail
9. **Test security** before production deployment
10. **Regular security reviews** and updates

Common Pitfalls
===============

1. **Locking yourself out** during SSH hardening - test before closing session
2. **Disabling services** needed by applications
3. **Too restrictive firewall** blocking legitimate traffic
4. **Not testing after changes** - always validate
5. **Forgetting to backup** before major changes
6. **Weak sudo policies** allowing privilege escalation
7. **Not monitoring logs** after hardening

Security Checklist
===================

.. code-block:: bash

   # Quick security audit
   #!/bin/bash
   
   echo "=== Security Audit ==="
   
   # System updates
   echo "[+] Checking for updates..."
   apt list --upgradable 2>/dev/null | grep -v "Listing"
   
   # Open ports
   echo "[+] Open ports:"
   ss -tuln | grep LISTEN
   
   # Failed logins
   echo "[+] Recent failed logins:"
   lastb | head -10
   
   # SUID files
   echo "[+] SUID files:"
   find / -perm -4000 2>/dev/null | wc -l
   
   # World-writable files
   echo "[+] World-writable files:"
   find / -xdev -type f -perm -0002 2>/dev/null | wc -l
   
   # Firewall status
   echo "[+] Firewall:"
   ufw status
   
   # SELinux/AppArmor
   echo "[+] Mandatory Access Control:"
   getenforce 2>/dev/null || aa-status 2>/dev/null | head -3
   
   # Audit daemon
   echo "[+] Audit daemon:"
   systemctl is-active auditd

See Also
========

- Linux_SELinux.rst
- Linux_AppArmor.rst
- Linux_Firewall_iptables.rst
- Linux_Firewall_nftables.rst
- Linux_Security_Auditing.rst

References
==========

- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST Security Guidelines
- ANSSI Hardening Guide
- man 5 sshd_config
- man 8 auditctl
