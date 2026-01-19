===================================
Linux Intrusion Detection Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: Host-based intrusion detection, file integrity monitoring, and incident response

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential IDS Commands
-----------------------

.. code-block:: bash

   # AIDE (Advanced Intrusion Detection Environment)
   sudo aide --init
   sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
   sudo aide --check
   sudo aide --update
   
   # Tripwire
   sudo tripwire --init
   sudo tripwire --check
   sudo tripwire --update
   
   # Fail2Ban
   sudo fail2ban-client status
   sudo fail2ban-client status sshd
   sudo fail2ban-client set sshd unbanip 192.168.1.100
   
   # OSSEC
   sudo /var/ossec/bin/ossec-control start
   sudo /var/ossec/bin/agent_control -l
   
   # Logwatch
   sudo logwatch --detail High --range today

Quick AIDE Setup
----------------

.. code-block:: bash

   #!/bin/bash
   # Quick AIDE file integrity monitoring setup
   
   # Install
   sudo apt install aide aide-common  # Debian/Ubuntu
   sudo yum install aide              # RHEL/CentOS
   
   # Initialize database
   sudo aideinit
   # or
   sudo aide --init
   sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
   
   # Run first check
   sudo aide --check
   
   # Schedule daily checks
   echo "0 2 * * * root /usr/bin/aide --check | mail -s 'AIDE Daily Report' admin@example.com" | sudo tee -a /etc/crontab

AIDE - File Integrity Monitoring
=================================

Installation
------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt update
   sudo apt install aide aide-common
   
   # RHEL/CentOS/Rocky
   sudo yum install aide
   
   # Configuration file
   /etc/aide/aide.conf        # Debian/Ubuntu
   /etc/aide.conf             # RHEL/CentOS

Configuration
-------------

.. code-block:: bash

   # /etc/aide/aide.conf
   
   # Database location
   database=file:/var/lib/aide/aide.db
   database_out=file:/var/lib/aide/aide.db.new
   
   # Report URL
   report_url=stdout
   # report_url=file:/var/log/aide/aide.log
   # report_url=mailto:admin@example.com
   
   # Gzip database
   gzip_dbout=yes
   
   # Rules (what to monitor)
   # p = permissions
   # i = inode
   # n = number of links
   # u = user
   # g = group
   # s = size
   # m = mtime
   # a = atime
   # c = ctime
   # S = check for growing size
   # md5 = md5 checksum
   # sha256 = sha256 checksum
   
   # Define custom rules
   FIPSR = p+i+n+u+g+s+m+c+md5+sha256
   NORMAL = p+i+n+u+g+s+m+c+md5+sha256
   DIR = p+i+n+u+g
   
   # What to check
   /bin FIPSR
   /sbin FIPSR
   /usr/bin FIPSR
   /usr/sbin FIPSR
   /lib FIPSR
   /lib64 FIPSR
   /etc NORMAL
   /boot NORMAL
   
   # Exclude directories
   !/proc
   !/sys
   !/dev
   !/tmp
   !/var/tmp
   !/var/log
   !/var/spool
   !/var/cache
   !/home

Initializing Database
---------------------

.. code-block:: bash

   # Initialize AIDE database
   sudo aideinit
   
   # Or manually
   sudo aide --init
   
   # Move new database to production
   sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
   
   # Verify initialization
   ls -lh /var/lib/aide/aide.db

Running Checks
--------------

.. code-block:: bash

   # Check for changes
   sudo aide --check
   
   # Verbose output
   sudo aide --check --verbose
   
   # Output to file
   sudo aide --check > /var/log/aide/aide_check_$(date +%Y%m%d).log
   
   # Check specific files/directories
   sudo aide --check --limit /etc
   
   # Update database (after legitimate changes)
   sudo aide --update
   sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
   
   # Compare two databases
   sudo aide --compare

Understanding Output
--------------------

.. code-block:: text

   AIDE Check Output:
   
   added: File added since last check
   removed: File removed since last check
   changed: File changed since last check
   
   Change indicators:
   p = permissions
   u = user (ownership)
   g = group
   s = size
   m = mtime
   c = ctime
   a = atime
   md5 = MD5 checksum
   sha256 = SHA256 checksum
   
   Example:
   changed: /etc/passwd
   Detailed information about changes:
     Perm     : -rw-r--r--                       , -rw-rw-r--
     Mtime    : 2026-01-15 10:30:00              , 2026-01-15 14:45:00
     SHA256   : abcd1234...                      , efgh5678...

Automated Monitoring
--------------------

.. code-block:: bash

   # Daily check cron job
   # /etc/cron.daily/aide-check
   #!/bin/bash
   
   /usr/bin/aide --check | mail -s "AIDE Daily Report - $(hostname)" admin@example.com
   
   sudo chmod +x /etc/cron.daily/aide-check
   
   # Or systemd timer
   # /etc/systemd/system/aide-check.service
   [Unit]
   Description=AIDE File Integrity Check
   
   [Service]
   Type=oneshot
   ExecStart=/usr/bin/aide --check
   
   # /etc/systemd/system/aide-check.timer
   [Unit]
   Description=Run AIDE check daily
   
   [Timer]
   OnCalendar=daily
   Persistent=true
   
   [Install]
   WantedBy=timers.target
   
   sudo systemctl enable aide-check.timer
   sudo systemctl start aide-check.timer

Tripwire
========

Installation
------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install tripwire
   
   # RHEL/CentOS
   sudo yum install tripwire
   
   # During installation, configure:
   # - Site passphrase (protects site key)
   # - Local passphrase (protects local key)

Configuration
-------------

.. code-block:: bash

   # Policy file (what to monitor)
   /etc/tripwire/twpol.txt
   
   # Configuration file
   /etc/tripwire/twcfg.txt
   
   # Edit policy
   sudo nano /etc/tripwire/twpol.txt
   
   # Compile policy
   sudo twadmin --create-polfile /etc/tripwire/twpol.txt
   
   # Edit configuration
   sudo nano /etc/tripwire/twcfg.txt
   sudo twadmin --create-cfgfile -S /etc/tripwire/site.key /etc/tripwire/twcfg.txt

Initialize Database
-------------------

.. code-block:: bash

   # Initialize Tripwire database
   sudo tripwire --init
   
   # Verify database created
   ls -lh /var/lib/tripwire/*.twd

Running Checks
--------------

.. code-block:: bash

   # Check for changes
   sudo tripwire --check
   
   # Email report
   sudo tripwire --check | mail -s "Tripwire Report" admin@example.com
   
   # Interactive mode
   sudo tripwire --check --interactive
   
   # Update database (after accepting changes)
   sudo tripwire --update --twrfile /var/lib/tripwire/report/hostname-YYYYMMDD-HHMMSS.twr

Fail2Ban
========

Installation
------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install fail2ban
   
   # RHEL/CentOS
   sudo yum install epel-release
   sudo yum install fail2ban
   
   # Enable and start
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban

Configuration
-------------

.. code-block:: bash

   # Main configuration (don't edit directly)
   /etc/fail2ban/fail2ban.conf
   /etc/fail2ban/jail.conf
   
   # Local overrides (edit these)
   /etc/fail2ban/jail.local
   /etc/fail2ban/jail.d/*.local
   
   # Create jail.local
   sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   sudo nano /etc/fail2ban/jail.local

Basic jail.local Configuration
-------------------------------

.. code-block:: ini

   # /etc/fail2ban/jail.local
   
   [DEFAULT]
   # Ban duration (seconds, -1 = permanent)
   bantime = 3600
   
   # Find time window
   findtime = 600
   
   # Max retries before ban
   maxretry = 5
   
   # Ignore IP addresses
   ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24
   
   # Ban action
   banaction = iptables-multiport
   # banaction = nftables-multiport  # For nftables
   
   # Email alerts
   destemail = admin@example.com
   sendername = Fail2Ban
   sender = fail2ban@example.com
   action = %(action_mwl)s
   
   # SSH jail
   [sshd]
   enabled = true
   port = ssh
   logpath = /var/log/auth.log  # Debian/Ubuntu
   # logpath = /var/log/secure   # RHEL/CentOS
   maxretry = 3
   bantime = 3600
   
   # Apache jails
   [apache-auth]
   enabled = true
   port = http,https
   logpath = /var/log/apache*/*error.log
   
   [apache-noscript]
   enabled = true
   port = http,https
   logpath = /var/log/apache*/*error.log
   
   [apache-overflows]
   enabled = true
   port = http,https
   logpath = /var/log/apache*/*error.log
   
   # Nginx
   [nginx-http-auth]
   enabled = true
   port = http,https
   logpath = /var/log/nginx/error.log

Managing Fail2Ban
-----------------

.. code-block:: bash

   # Service control
   sudo systemctl start fail2ban
   sudo systemctl stop fail2ban
   sudo systemctl restart fail2ban
   sudo systemctl status fail2ban
   
   # Check status
   sudo fail2ban-client status
   
   # Check specific jail
   sudo fail2ban-client status sshd
   
   # Unban IP
   sudo fail2ban-client set sshd unbanip 192.168.1.100
   
   # Ban IP manually
   sudo fail2ban-client set sshd banip 10.0.0.1
   
   # Reload configuration
   sudo fail2ban-client reload
   
   # Reload specific jail
   sudo fail2ban-client reload sshd
   
   # Get current bans
   sudo fail2ban-client status sshd | grep "Banned IP"
   
   # View log
   sudo tail -f /var/log/fail2ban.log

Custom Filters
--------------

.. code-block:: ini

   # /etc/fail2ban/filter.d/custom-app.conf
   
   [Definition]
   failregex = ^.*Failed login from <HOST>.*$
               ^.*Invalid user .* from <HOST>.*$
   ignoreregex =
   
   # Test filter
   fail2ban-regex /var/log/custom-app.log /etc/fail2ban/filter.d/custom-app.conf

OSSEC HIDS
==========

Installation (Agent)
--------------------

.. code-block:: bash

   # Download and install
   wget https://github.com/ossec/ossec-hids/archive/3.7.0.tar.gz
   tar xzf 3.7.0.tar.gz
   cd ossec-hids-3.7.0
   sudo ./install.sh
   
   # Choose:
   # - agent (for monitored systems)
   # - server (for central manager)
   # - local (standalone)

Configuration
-------------

.. code-block:: xml

   <!-- /var/ossec/etc/ossec.conf -->
   
   <ossec_config>
     <!-- Log analysis -->
     <localfile>
       <log_format>syslog</log_format>
       <location>/var/log/auth.log</location>
     </localfile>
     
     <localfile>
       <log_format>syslog</log_format>
       <location>/var/log/syslog</location>
     </localfile>
     
     <!-- File integrity monitoring -->
     <syscheck>
       <frequency>79200</frequency>  <!-- 22 hours -->
       <directories check_all="yes">/etc,/usr/bin,/usr/sbin</directories>
       <directories check_all="yes">/bin,/sbin</directories>
       <ignore>/etc/mtab</ignore>
       <ignore>/etc/hosts.deny</ignore>
     </syscheck>
     
     <!-- Rootkit detection -->
     <rootcheck>
       <frequency>79200</frequency>
       <rootkit_files>/var/ossec/etc/shared/rootkit_files.txt</rootkit_files>
       <rootkit_trojans>/var/ossec/etc/shared/rootkit_trojans.txt</rootkit_trojans>
     </rootcheck>
     
     <!-- Active response -->
     <active-response>
       <command>firewall-drop</command>
       <location>local</location>
       <level>6</level>
       <timeout>600</timeout>
     </active-response>
   </ossec_config>

Managing OSSEC
--------------

.. code-block:: bash

   # Start/stop service
   sudo /var/ossec/bin/ossec-control start
   sudo /var/ossec/bin/ossec-control stop
   sudo /var/ossec/bin/ossec-control restart
   sudo /var/ossec/bin/ossec-control status
   
   # Manage agents (on server)
   sudo /var/ossec/bin/manage_agents
   
   # List agents
   sudo /var/ossec/bin/agent_control -l
   
   # View alerts
   sudo /var/ossec/bin/ossec-logtest  # Test log messages
   tail -f /var/ossec/logs/alerts/alerts.log

Log Analysis Tools
==================

Logwatch
--------

.. code-block:: bash

   # Install
   sudo apt install logwatch
   
   # Run manually
   sudo logwatch --detail High --range today
   sudo logwatch --detail Med --range yesterday
   sudo logwatch --service sshd --range today
   
   # Email report
   sudo logwatch --output mail --mailto admin@example.com --detail High --range today
   
   # Configuration
   /etc/logwatch/conf/logwatch.conf
   
   # Custom settings
   # /etc/logwatch/conf/logwatch.conf
   Detail = High
   MailTo = admin@example.com
   MailFrom = logwatch@example.com
   Range = today

Logcheck
--------

.. code-block:: bash

   # Install
   sudo apt install logcheck
   
   # Run manually
   sudo -u logcheck logcheck -o -t
   
   # Configuration
   /etc/logcheck/logcheck.conf
   /etc/logcheck/logcheck.logfiles  # Files to check
   
   # Ignore patterns
   /etc/logcheck/ignore.d.server/
   /etc/logcheck/ignore.d.workstation/

Syslog-ng / Rsyslog Monitoring
-------------------------------

.. code-block:: bash

   # Centralized logging with rsyslog
   # On clients - /etc/rsyslog.conf
   *.* @@log-server:514  # TCP
   *.* @log-server:514   # UDP
   
   # On server - /etc/rsyslog.conf
   # Enable reception
   module(load="imtcp")
   input(type="imtcp" port="514")
   
   # Template for remote logs
   $template RemoteLogs,"/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log"
   *.* ?RemoteLogs
   
   sudo systemctl restart rsyslog

Rootkit Detection
=================

rkhunter (Rootkit Hunter)
--------------------------

.. code-block:: bash

   # Install
   sudo apt install rkhunter
   
   # Update database
   sudo rkhunter --update
   
   # Run check
   sudo rkhunter --check
   
   # Check specific tests
   sudo rkhunter --check --enable all --disable none
   
   # Configuration
   /etc/rkhunter.conf
   
   # Update file properties after system update
   sudo rkhunter --propupd
   
   # Schedule daily checks
   # /etc/cron.daily/rkhunter
   #!/bin/bash
   /usr/bin/rkhunter --check --skip-keypress --report-warnings-only | \
     mail -s "rkhunter Daily Report" admin@example.com

chkrootkit
----------

.. code-block:: bash

   # Install
   sudo apt install chkrootkit
   
   # Run check
   sudo chkrootkit
   
   # Check specific rootkit
   sudo chkrootkit -r /path/to/rootkit
   
   # Quiet mode (only suspicious findings)
   sudo chkrootkit -q

Lynis (Security Auditing)
--------------------------

.. code-block:: bash

   # Install
   sudo apt install lynis
   
   # Run audit
   sudo lynis audit system
   
   # With custom profile
   sudo lynis audit system --profile /path/to/profile
   
   # Generate report
   sudo lynis audit system > /var/log/lynis-report.txt
   
   # View suggestions
   grep Suggestion /var/log/lynis.log

Network Intrusion Detection
============================

Snort (Brief)
-------------

.. code-block:: bash

   # Install (complex setup)
   sudo apt install snort
   
   # Configure
   /etc/snort/snort.conf
   
   # Run in IDS mode
   sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
   
   # View alerts
   tail -f /var/log/snort/alert

Suricata (Modern Alternative)
------------------------------

.. code-block:: bash

   # Install
   sudo apt install suricata
   
   # Update rules
   sudo suricata-update
   
   # Run
   sudo suricata -c /etc/suricata/suricata.yaml -i eth0
   
   # View logs
   tail -f /var/log/suricata/fast.log
   tail -f /var/log/suricata/eve.json

Incident Response
=================

Initial Assessment
------------------

.. code-block:: bash

   # Check logged-in users
   who
   w
   last
   
   # Active connections
   ss -tulpn
   netstat -tulpn
   
   # Running processes
   ps auxf
   top
   
   # Check cron jobs
   crontab -l  # Current user
   sudo crontab -l  # Root
   cat /etc/crontab
   ls -la /etc/cron.*
   
   # Check for SUID/SGID files
   find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null
   
   # Recent file modifications
   find /etc -type f -mtime -1 -ls
   find /bin /sbin /usr/bin /usr/sbin -type f -mtime -1 -ls

Evidence Collection
-------------------

.. code-block:: bash

   # Collect system state
   #!/bin/bash
   EVIDENCE_DIR="/tmp/evidence_$(date +%Y%m%d_%H%M%S)"
   mkdir -p "$EVIDENCE_DIR"
   
   # System info
   uname -a > "$EVIDENCE_DIR/uname.txt"
   uptime > "$EVIDENCE_DIR/uptime.txt"
   date > "$EVIDENCE_DIR/timestamp.txt"
   
   # Users
   w > "$EVIDENCE_DIR/logged_users.txt"
   last > "$EVIDENCE_DIR/last_logins.txt"
   
   # Network
   ss -tulpn > "$EVIDENCE_DIR/network_connections.txt"
   iptables-save > "$EVIDENCE_DIR/iptables_rules.txt"
   
   # Processes
   ps auxf > "$EVIDENCE_DIR/processes.txt"
   
   # Files
   find / -type f -mtime -1 2>/dev/null > "$EVIDENCE_DIR/recent_files.txt"
   
   # Logs
   cp -r /var/log "$EVIDENCE_DIR/"
   
   # Create archive
   tar czf "evidence_$(date +%Y%m%d_%H%M%S).tar.gz" "$EVIDENCE_DIR"

Best Practices
==============

1. **Layer defense** - use multiple detection methods
2. **Regular updates** - keep IDS signatures current
3. **Baseline first** - establish normal before detecting abnormal
4. **Minimize false positives** - tune rules to reduce noise
5. **Centralized logging** - collect logs from all systems
6. **Automated alerts** - real-time notification of incidents
7. **Regular audits** - scheduled integrity checks
8. **Incident response plan** - documented procedures
9. **Test restores** - verify backup integrity
10. **Log retention** - comply with requirements

Common Pitfalls
===============

1. **Alert fatigue** - too many false positives ignored
2. **Incomplete coverage** - missing critical files/logs
3. **No baseline** - can't distinguish normal from abnormal
4. **Ignoring updates** - outdated signatures miss new threats
5. **Poor log management** - logs not rotated or archived
6. **No response plan** - panic during incident
7. **Single point of monitoring** - no redundancy

Quick Reference
===============

.. code-block:: bash

   # AIDE
   aide --init
   aide --check
   aide --update
   
   # Tripwire
   tripwire --init
   tripwire --check
   
   # Fail2Ban
   fail2ban-client status
   fail2ban-client set jail unbanip IP
   
   # rkhunter
   rkhunter --update
   rkhunter --check
   
   # Logwatch
   logwatch --detail High --range today

See Also
========

- Linux_Security_Hardening.rst
- Linux_Security_Auditing.rst
- Linux_Firewall_iptables.rst
- Linux_Network_Configuration.rst

References
==========

- man aide
- man tripwire
- man fail2ban-client
- https://www.aide.org/
- https://www.fail2ban.org/
- https://www.ossec.net/
