================================================================================
LINUX SECURITY BASICS
================================================================================

**Quick Reference for Linux Security Fundamentals and Best Practices**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 1, 14

================================================================================
TL;DR - Essential Security Commands
================================================================================

.. code-block:: bash

   # Check system security status
   uname -a                          # Kernel version
   cat /etc/os-release               # Distribution info
   last                              # Login history
   who                               # Currently logged in users
   w                                 # Active users and load
   
   # Quick security checks
   sudo lynis audit system           # Comprehensive security audit
   sudo rkhunter --check             # Rootkit scan
   sudo chkrootkit                   # Alternative rootkit scan
   sudo clamav                       # Antivirus scan
   
   # View security logs
   sudo journalctl -xe               # System logs
   sudo tail -f /var/log/auth.log    # Authentication logs (Debian/Ubuntu)
   sudo tail -f /var/log/secure      # Authentication logs (RHEL/CentOS)
   
   # Check running services
   systemctl list-units --type=service --state=running
   sudo netstat -tulpn               # Open ports
   sudo ss -tulpn                    # Open ports (modern)
   
   # File integrity
   sudo aide --check                 # Check file integrity
   sudo tripwire --check             # Alternative integrity check

================================================================================
1. Linux Security Landscape
================================================================================

1.1 Threat Models
-----------------

**Common Threats:**

- **External Attacks:** Unauthorized access attempts, DDoS, port scanning
- **Insider Threats:** Malicious or negligent employees
- **Malware:** Viruses, trojans, rootkits, ransomware
- **Data Breaches:** Unauthorized data access or exfiltration
- **Privilege Escalation:** Gaining unauthorized elevated privileges
- **Social Engineering:** Phishing, pretexting, baiting

**Linux-Specific Considerations:**

- Most servers run Linux → High-value targets
- Open source code → Vulnerabilities can be found and exploited
- Misconfigurations are common attack vectors
- Outdated software/kernels create vulnerabilities

1.2 Security Principles
------------------------

**CIA Triad:**

1. **Confidentiality:** Ensure data is only accessible to authorized users
   - Encryption (at rest and in transit)
   - Access controls (DAC, MAC)
   - Authentication mechanisms

2. **Integrity:** Ensure data hasn't been tampered with
   - File integrity monitoring
   - Digital signatures
   - Checksums and hashes

3. **Availability:** Ensure systems and data are accessible when needed
   - Redundancy
   - Backup and disaster recovery
   - DDoS protection

**Defense in Depth:**

Multiple layers of security controls:

.. code-block:: text

   ┌─────────────────────────────────────┐
   │   Physical Security                 │
   ├─────────────────────────────────────┤
   │   Network Security (Firewall)       │
   ├─────────────────────────────────────┤
   │   Host Security (SELinux/AppArmor)  │
   ├─────────────────────────────────────┤
   │   Application Security              │
   ├─────────────────────────────────────┤
   │   Data Security (Encryption)        │
   └─────────────────────────────────────┘

**Least Privilege Principle:**

- Users should have minimum permissions needed
- Don't use root unless absolutely necessary
- Use sudo with specific command restrictions
- Regular users for daily operations

**Security by Default:**

- Disable unnecessary services
- Close unused ports
- Remove unnecessary packages
- Use secure defaults for configurations

================================================================================
2. Virtual Environment Security
================================================================================

2.1 Why Use Virtual Environments?
----------------------------------

**Benefits for Security Testing:**

1. **Isolation:** Malware can't affect host system
2. **Snapshots:** Easy rollback to clean state
3. **Safe Testing:** Test security configurations without risk
4. **Multiple Scenarios:** Test different distributions/configurations
5. **Network Isolation:** Test network attacks safely

**Popular Virtualization Platforms:**

.. code-block:: bash

   # VirtualBox (Free, cross-platform)
   VBoxManage list vms
   VBoxManage startvm "Ubuntu-Security-Test" --type headless
   
   # KVM/QEMU (Linux native, high performance)
   virsh list --all
   virsh start security-test
   
   # VMware Workstation (Commercial, feature-rich)
   vmrun list
   vmrun start "/path/to/vm.vmx"

2.2 Virtual Machine Security Best Practices
--------------------------------------------

**VM Isolation:**

.. code-block:: bash

   # VirtualBox network modes
   # NAT: VM can access external network, host can't access VM
   VBoxManage modifyvm "MyVM" --nic1 nat
   
   # Host-only: VM and host can communicate, no external access
   VBoxManage modifyvm "MyVM" --nic1 hostonly
   
   # Bridged: VM appears as separate machine on network
   VBoxManage modifyvm "MyVM" --nic1 bridged
   
   # Internal: VMs can communicate with each other only
   VBoxManage modifyvm "MyVM" --nic1 intnet

**Snapshot Management:**

.. code-block:: bash

   # VirtualBox snapshots
   VBoxManage snapshot "MyVM" take "Clean Install" --description "Fresh OS install"
   VBoxManage snapshot "MyVM" list
   VBoxManage snapshot "MyVM" restore "Clean Install"
   
   # KVM snapshots
   virsh snapshot-create-as security-test snapshot1 "Clean state"
   virsh snapshot-list security-test
   virsh snapshot-revert security-test snapshot1

**Resource Limitations:**

.. code-block:: bash

   # Limit VM resources to prevent host exhaustion
   VBoxManage modifyvm "MyVM" --memory 2048      # 2GB RAM
   VBoxManage modifyvm "MyVM" --cpus 2           # 2 CPU cores
   VBoxManage modifyvm "MyVM" --vram 128         # 128MB video RAM

================================================================================
3. Initial System Security Configuration
================================================================================

3.1 Minimal Installation
-------------------------

**Install Only What You Need:**

.. code-block:: bash

   # Check installed packages
   dpkg -l | wc -l                    # Debian/Ubuntu count
   rpm -qa | wc -l                    # RHEL/CentOS count
   
   # List explicitly installed packages (Arch)
   pacman -Qe
   
   # Remove unnecessary packages (Debian/Ubuntu)
   sudo apt autoremove
   sudo apt purge <package-name>
   
   # Remove unnecessary packages (RHEL/CentOS)
   sudo yum autoremove
   sudo yum remove <package-name>

**Disable Unnecessary Services:**

.. code-block:: bash

   # List all services
   systemctl list-unit-files --type=service
   
   # List enabled services
   systemctl list-unit-files --type=service --state=enabled
   
   # List running services
   systemctl list-units --type=service --state=running
   
   # Disable and stop unnecessary service
   sudo systemctl stop <service-name>
   sudo systemctl disable <service-name>
   
   # Check service status
   systemctl status <service-name>
   
   # Common services to disable on servers (if not needed):
   sudo systemctl disable bluetooth.service
   sudo systemctl disable cups.service           # Printing
   sudo systemctl disable avahi-daemon.service   # Zeroconf/mDNS

3.2 Keep System Updated
------------------------

**Automatic Updates:**

.. code-block:: bash

   # Debian/Ubuntu - Install unattended-upgrades
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure unattended-upgrades
   
   # Configuration file
   sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
   
   # RHEL/CentOS - Install yum-cron
   sudo yum install yum-cron
   sudo systemctl enable yum-cron
   sudo systemctl start yum-cron
   
   # Configuration
   sudo nano /etc/yum/yum-cron.conf

**Manual Updates:**

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt update
   sudo apt upgrade              # Standard upgrades
   sudo apt full-upgrade         # Distribution upgrades
   sudo apt dist-upgrade         # Major version upgrade
   
   # RHEL/CentOS
   sudo yum update
   sudo yum upgrade
   
   # Check for security updates only
   sudo yum updateinfo list security
   sudo yum update --security
   
   # Arch Linux
   sudo pacman -Syu

**Kernel Updates:**

.. code-block:: bash

   # Check current kernel
   uname -r
   
   # List available kernels (Debian/Ubuntu)
   apt search linux-image
   
   # Install specific kernel
   sudo apt install linux-image-<version>
   
   # Update GRUB
   sudo update-grub
   
   # Reboot to new kernel
   sudo reboot
   
   # Remove old kernels (careful!)
   sudo apt autoremove --purge

================================================================================
4. Security Auditing Tools
================================================================================

4.1 Lynis - Security Auditing Tool
-----------------------------------

**Installation:**

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install lynis
   
   # RHEL/CentOS
   sudo yum install lynis
   
   # From source (latest version)
   git clone https://github.com/CISOfy/lynis
   cd lynis
   sudo ./lynis audit system

**Running Lynis:**

.. code-block:: bash

   # Full system audit
   sudo lynis audit system
   
   # Audit specific tests
   sudo lynis audit system --tests-from-group security
   sudo lynis audit system --tests-from-group authentication
   
   # Generate report
   sudo lynis audit system --report-file /tmp/lynis-report.txt
   
   # View suggestions
   sudo lynis show suggestions
   
   # Check specific category
   sudo lynis show details <test-id>

**Common Lynis Findings:**

.. code-block:: bash

   # Example hardening based on Lynis recommendations:
   
   # 1. Set file permissions on boot files
   sudo chmod 600 /boot/grub/grub.cfg
   
   # 2. Install fail2ban
   sudo apt install fail2ban
   
   # 3. Configure password aging
   sudo nano /etc/login.defs
   # Set: PASS_MAX_DAYS 90
   
   # 4. Disable USB storage (if not needed)
   echo "install usb-storage /bin/true" | sudo tee /etc/modprobe.d/disable-usb-storage.conf
   
   # 5. Enable process accounting
   sudo apt install acct
   sudo systemctl enable acct

4.2 Rootkit Detection
----------------------

**rkhunter:**

.. code-block:: bash

   # Installation
   sudo apt install rkhunter
   
   # Update database
   sudo rkhunter --update
   
   # Scan system
   sudo rkhunter --check
   
   # Scan with report
   sudo rkhunter --check --report-warnings-only
   
   # Update file properties database
   sudo rkhunter --propupd

**chkrootkit:**

.. code-block:: bash

   # Installation
   sudo apt install chkrootkit
   
   # Run scan
   sudo chkrootkit
   
   # Verbose output
   sudo chkrootkit -x

4.3 ClamAV - Antivirus
----------------------

**Installation and Setup:**

.. code-block:: bash

   # Install ClamAV
   sudo apt install clamav clamav-daemon
   
   # Stop daemon to update
   sudo systemctl stop clamav-freshclam
   
   # Update virus definitions
   sudo freshclam
   
   # Start daemon
   sudo systemctl start clamav-freshclam
   sudo systemctl enable clamav-freshclam

**Scanning:**

.. code-block:: bash

   # Scan directory
   clamscan -r /home
   
   # Scan with virus removal
   clamscan -r --remove /home
   
   # Scan and move infected files
   clamscan -r --move=/tmp/quarantine /home
   
   # Scan entire system (excluding /sys, /proc, /dev)
   sudo clamscan -r --exclude-dir="^/sys" --exclude-dir="^/proc" --exclude-dir="^/dev" /
   
   # Generate report
   clamscan -r --log=/var/log/clamav/scan.log /home

================================================================================
5. Network Security Basics
================================================================================

5.1 Port Scanning and Service Discovery
----------------------------------------

**Check Open Ports:**

.. code-block:: bash

   # netstat (traditional)
   sudo netstat -tulpn
   # -t: TCP, -u: UDP, -l: listening, -p: program, -n: numeric
   
   # ss (modern replacement)
   sudo ss -tulpn
   
   # List only TCP listening ports
   sudo ss -tlpn
   
   # List specific port
   sudo ss -tlpn | grep :22

**nmap - Network Scanner:**

.. code-block:: bash

   # Install nmap
   sudo apt install nmap
   
   # Scan localhost
   nmap localhost
   
   # Scan specific ports
   nmap -p 22,80,443 localhost
   
   # Scan all ports
   nmap -p- localhost
   
   # Service version detection
   nmap -sV localhost
   
   # OS detection
   sudo nmap -O localhost
   
   # Aggressive scan
   sudo nmap -A localhost

5.2 Basic Network Hardening
----------------------------

**Disable IPv6 (if not needed):**

.. code-block:: bash

   # Temporary disable
   sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
   sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
   
   # Permanent disable
   echo "net.ipv6.conf.all.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf
   echo "net.ipv6.conf.default.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p

**TCP/IP Stack Hardening:**

.. code-block:: bash

   # Edit sysctl configuration
   sudo nano /etc/sysctl.conf
   
   # Add these lines:
   
   # Ignore ICMP ping requests
   net.ipv4.icmp_echo_ignore_all = 1
   
   # Ignore ICMP broadcast requests
   net.ipv4.icmp_echo_ignore_broadcasts = 1
   
   # Disable source routing
   net.ipv4.conf.all.accept_source_route = 0
   net.ipv4.conf.default.accept_source_route = 0
   
   # Enable TCP SYN cookies (DDoS protection)
   net.ipv4.tcp_syncookies = 1
   
   # Disable ICMP redirect acceptance
   net.ipv4.conf.all.accept_redirects = 0
   net.ipv4.conf.default.accept_redirects = 0
   
   # Enable reverse path filtering
   net.ipv4.conf.all.rp_filter = 1
   net.ipv4.conf.default.rp_filter = 1
   
   # Log martian packets
   net.ipv4.conf.all.log_martians = 1
   
   # Apply changes
   sudo sysctl -p

================================================================================
6. Security Best Practices Summary
================================================================================

6.1 Essential Security Checklist
---------------------------------

.. code-block:: text

   ☐ Install minimal system (only required packages)
   ☐ Keep system and packages updated
   ☐ Configure automatic security updates
   ☐ Disable unnecessary services
   ☐ Configure firewall (iptables/nftables/firewalld)
   ☐ Use strong passwords and enforce password policies
   ☐ Disable root login (use sudo instead)
   ☐ Configure SSH securely (key-based auth, disable password)
   ☐ Install and configure fail2ban
   ☐ Enable SELinux or AppArmor
   ☐ Configure file permissions correctly
   ☐ Install and run security auditing tools (Lynis)
   ☐ Configure centralized logging
   ☐ Install file integrity monitoring (AIDE)
   ☐ Regular security scans (rkhunter, ClamAV)
   ☐ Monitor system logs
   ☐ Implement backup strategy
   ☐ Document security configurations
   ☐ Regular security audits
   ☐ Incident response plan

6.2 Quick Win Security Improvements
------------------------------------

**Immediate Actions (5 minutes):**

.. code-block:: bash

   # 1. Update system
   sudo apt update && sudo apt upgrade -y
   
   # 2. Install fail2ban
   sudo apt install fail2ban -y
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   
   # 3. Configure automatic updates
   sudo apt install unattended-upgrades -y
   sudo dpkg-reconfigure -plow unattended-upgrades

**Short Term (30 minutes):**

.. code-block:: bash

   # 4. Run security audit
   sudo apt install lynis -y
   sudo lynis audit system > /tmp/security-audit.txt
   
   # 5. Install and configure firewall
   sudo apt install ufw -y
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow ssh
   sudo ufw enable
   
   # 6. Harden SSH
   sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
   sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
   sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
   sudo systemctl restart sshd

**Long Term (Ongoing):**

- Implement SELinux/AppArmor
- Set up intrusion detection (OSSEC/Wazuh)
- Configure centralized logging
- Regular vulnerability scans
- Security awareness training
- Incident response procedures

================================================================================
7. Security Information Resources
================================================================================

7.1 Official Security Resources
--------------------------------

**CVE Databases:**

- https://cve.mitre.org - Common Vulnerabilities and Exposures
- https://nvd.nist.gov - National Vulnerability Database
- https://www.cvedetails.com - CVE details and statistics

**Linux Security:**

- https://www.kernel.org/category/security.html - Kernel security
- https://security.debian.org - Debian security tracker
- https://access.redhat.com/security - Red Hat security
- https://ubuntu.com/security - Ubuntu security notices

**Security News:**

- https://www.schneier.com - Bruce Schneier's security blog
- https://krebsonsecurity.com - Cybersecurity news
- https://www.sans.org/reading-room - SANS reading room

7.2 Security Standards and Frameworks
--------------------------------------

**CIS Benchmarks:**

- https://www.cisecurity.org/cis-benchmarks
- Free security configuration guides for major distributions

**NIST Framework:**

- https://www.nist.gov/cyberframework
- Cybersecurity framework

**PCI DSS:**

- Payment Card Industry Data Security Standard
- Required for handling credit card data

**HIPAA:**

- Health Insurance Portability and Accountability Act
- Required for healthcare data

================================================================================
8. Emergency Response Commands
================================================================================

8.1 Suspected Compromise
-------------------------

**Immediate Actions:**

.. code-block:: bash

   # 1. Disconnect from network (if possible)
   sudo ip link set eth0 down
   
   # 2. Check logged in users
   who
   w
   last
   
   # 3. Check active connections
   sudo netstat -antp
   sudo ss -antp
   
   # 4. Check running processes
   ps aux | less
   top
   htop
   
   # 5. Check for unauthorized cron jobs
   crontab -l
   sudo crontab -l
   ls -la /etc/cron.*
   
   # 6. Check for modified system files
   sudo debsums -c        # Debian/Ubuntu
   sudo rpm -Va           # RHEL/CentOS
   
   # 7. Preserve evidence
   sudo dd if=/dev/sda of=/mnt/backup/disk-image.dd bs=4M
   
   # 8. Review logs
   sudo journalctl -xe
   sudo tail -100 /var/log/auth.log
   sudo tail -100 /var/log/syslog

8.2 Quick Lockdown
-------------------

.. code-block:: bash

   # Block all incoming connections (emergency only!)
   sudo iptables -P INPUT DROP
   sudo iptables -A INPUT -i lo -j ACCEPT
   sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
   
   # Disable all user accounts except yours
   sudo passwd -l <username>
   
   # Kill all user sessions
   sudo pkill -u <username>
   
   # Change passwords immediately
   sudo passwd root
   passwd  # Change your password

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- User_Account_Security.rst - Detailed user and password management
- Firewall_iptables.rst - Comprehensive firewall configuration
- SSH_Hardening.rst - Advanced SSH security
- SELinux_Security.rst - Mandatory Access Control
- Kernel_Hardening.rst - Kernel-level security
- Logging_Log_Security.rst - Log management and analysis
- Vulnerability_Intrusion_Detection.rst - IDS/IPS configuration

================================================================================
END OF LINUX SECURITY BASICS
================================================================================
