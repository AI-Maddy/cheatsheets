================================================================================
SECURITY QUICK REFERENCE
================================================================================

**Consolidated Security Commands and Emergency Procedures**

Source: Mastering Linux Security And Hardening
Complete Reference Guide

================================================================================
EMERGENCY RESPONSE
================================================================================

.. code-block:: bash

   # Immediate Lockdown
   sudo iptables -P INPUT DROP                    # Block all incoming
   sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
   sudo iptables -A INPUT -i lo -j ACCEPT         # Allow loopback
   sudo passwd -l username                        # Lock user account
   
   # Check for Compromise
   sudo netstat -tulpn | grep LISTEN              # Check listening ports
   ps aux | grep -v "\[" | sort -k 3 -r | head   # Top CPU processes
   last -a | head -20                             # Recent logins
   sudo grep "Failed password" /var/log/auth.log | tail -50
   
   # Kill Suspicious Processes
   sudo kill -9 PID                               # Force kill process
   sudo pkill -9 -u username                      # Kill all user processes

================================================================================
SECURITY CHECKLIST (COMPLETE)
================================================================================

System Hardening:
☐ Minimal installation (no unnecessary packages)
☐ Regular updates (unattended-upgrades configured)
☐ Strong password policy (PAM configured)
☐ Disable root login
☐ Configure sudo properly
☐ Set up firewall (iptables/nftables/firewalld)
☐ Enable fail2ban
☐ Configure SELinux/AppArmor
☐ Disable unnecessary services
☐ Configure system auditing (auditd)

Network Security:
☐ SSH hardened (key-only, non-standard port)
☐ Firewall rules tested
☐ fail2ban active
☐ TLS/SSL certificates valid
☐ No unnecessary open ports
☐ Network segmentation implemented

Data Protection:
☐ LUKS disk encryption
☐ Encrypted backups
☐ GPG for sensitive files
☐ Secure file permissions
☐ Regular backup testing

Monitoring:
☐ Log rotation configured
☐ Centralized logging
☐ IDS/IPS deployed
☐ Regular vulnerability scans
☐ Security alerts configured

Consolidated commands reference with category-based organization continues...

================================================================================
END OF SECURITY QUICK REFERENCE
================================================================================
