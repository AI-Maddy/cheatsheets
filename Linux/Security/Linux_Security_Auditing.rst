===================================
Linux Security Auditing Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: System auditing, compliance, and security monitoring

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Audit Commands
-------------------------

.. code-block:: bash

   # auditd service
   sudo systemctl start auditd
   sudo systemctl status auditd
   
   # View audit logs
   sudo ausearch -m USER_LOGIN
   sudo ausearch -k sshd_config
   sudo aureport --summary
   
   # Add audit rule
   sudo auditctl -w /etc/passwd -p wa -k passwd_changes
   sudo auditctl -a always,exit -F arch=b64 -S openat -k file_access
   
   # List rules
   sudo auditctl -l
   
   # Delete all rules
   sudo auditctl -D
   
   # Generate report
   sudo aureport --file
   sudo aureport --login
   sudo aureport --failed

Quick Audit Setup
-----------------

.. code-block:: bash

   #!/bin/bash
   # Basic audit configuration
   
   # Install auditd
   sudo apt install auditd audispd-plugins  # Debian/Ubuntu
   sudo yum install audit audit-libs        # RHEL/CentOS
   
   # Enable and start
   sudo systemctl enable auditd
   sudo systemctl start auditd
   
   # Add critical file watches
   auditctl -w /etc/passwd -p wa -k passwd_changes
   auditctl -w /etc/group -p wa -k group_changes
   auditctl -w /etc/shadow -p wa -k shadow_changes
   auditctl -w /etc/sudoers -p wa -k sudoers_changes
   auditctl -w /etc/ssh/sshd_config -p wa -k sshd_config
   
   # Monitor privileged commands
   auditctl -a always,exit -F path=/usr/bin/sudo -F perm=x -k sudo_usage
   auditctl -a always,exit -F path=/usr/bin/passwd -F perm=x -k passwd_usage
   
   # Save rules
   sudo sh -c "auditctl -l > /etc/audit/rules.d/custom.rules"

auditd Fundamentals
===================

Installation and Configuration
-------------------------------

.. code-block:: bash

   # Install auditd
   # Debian/Ubuntu
   sudo apt update
   sudo apt install auditd audispd-plugins
   
   # RHEL/CentOS/Rocky
   sudo yum install audit audit-libs
   
   # Enable service
   sudo systemctl enable auditd
   sudo systemctl start auditd
   
   # Service management (special commands for auditd)
   sudo service auditd start
   sudo service auditd stop
   sudo service auditd restart
   sudo service auditd rotate  # Rotate logs

Configuration Files
-------------------

.. code-block:: bash

   # Main configuration
   /etc/audit/auditd.conf
   
   # Audit rules
   /etc/audit/rules.d/*.rules
   /etc/audit/audit.rules
   
   # Log files
   /var/log/audit/audit.log

auditd.conf Settings
--------------------

.. code-block:: bash

   # /etc/audit/auditd.conf
   
   # Log file location
   log_file = /var/log/audit/audit.log
   
   # Log format (RAW, NOLOG)
   log_format = RAW
   
   # Log group
   log_group = root
   
   # Priority boost
   priority_boost = 4
   
   # Flush to disk (NONE, INCREMENTAL, INCREMENTAL_ASYNC, DATA, SYNC)
   flush = INCREMENTAL_ASYNC
   
   # Frequency of explicit flush
   freq = 50
   
   # Max log file size (MB)
   max_log_file = 8
   
   # Action when log file full (IGNORE, SYSLOG, SUSPEND, ROTATE, KEEP_LOGS)
   max_log_file_action = ROTATE
   
   # Space left on disk (MB)
   space_left = 75
   
   # Action when space low
   space_left_action = SYSLOG
   
   # Admin space left
   admin_space_left = 50
   admin_space_left_action = SUSPEND
   
   # Disk full action
   disk_full_action = SUSPEND
   
   # Disk error action
   disk_error_action = SUSPEND
   
   # Number of log files to keep
   num_logs = 5
   
   # Dispatcher
   dispatcher = /sbin/audispd

Audit Rules
===========

Rule Syntax
-----------

.. code-block:: bash

   # File/directory watches
   -w path -p permissions -k key_name
   
   # System call auditing
   -a action,filter -S syscall -F field=value -k key_name
   
   # Permissions:
   # r = read
   # w = write
   # x = execute
   # a = attribute change
   
   # Actions:
   # always = always create audit record
   # never = never create audit record
   
   # Filters:
   # task = fork/clone
   # exit = syscall exit
   # user = user-space events
   # exclude = exclude events

File System Watches
-------------------

.. code-block:: bash

   # Watch file for changes
   auditctl -w /etc/passwd -p wa -k passwd_changes
   
   # Watch directory
   auditctl -w /etc/ -p wa -k etc_changes
   
   # Watch with all permissions
   auditctl -w /etc/ssh/sshd_config -p rwxa -k sshd_config
   
   # Common file watches
   auditctl -w /etc/passwd -p wa -k passwd_changes
   auditctl -w /etc/group -p wa -k group_changes
   auditctl -w /etc/shadow -p wa -k shadow_changes
   auditctl -w /etc/sudoers -p wa -k sudoers_changes
   auditctl -w /etc/sudoers.d/ -p wa -k sudoers_changes
   auditctl -w /etc/ssh/sshd_config -p wa -k sshd_config
   auditctl -w /etc/pam.d/ -p wa -k pam_changes
   auditctl -w /etc/security/ -p wa -k security_changes
   auditctl -w /var/log/lastlog -p wa -k logins
   auditctl -w /var/run/faillock/ -p wa -k logins

System Call Auditing
--------------------

.. code-block:: bash

   # Audit specific syscall
   auditctl -a always,exit -F arch=b64 -S open -S openat -k file_open
   
   # Audit file deletions
   auditctl -a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -k file_deletion
   
   # Audit executions
   auditctl -a always,exit -F arch=b64 -S execve -k exec
   
   # Audit network connections
   auditctl -a always,exit -F arch=b64 -S socket -S connect -k network
   
   # Architecture (b32 for 32-bit, b64 for 64-bit)
   # For 64-bit systems, often need both:
   auditctl -a always,exit -F arch=b64 -S open -k file_open
   auditctl -a always,exit -F arch=b32 -S open -k file_open

Privileged Command Auditing
----------------------------

.. code-block:: bash

   # Find SUID/SGID files
   find / -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null > /tmp/suid_sgid_files.txt
   
   # Audit privileged commands
   auditctl -a always,exit -F path=/usr/bin/sudo -F perm=x -k sudo_usage
   auditctl -a always,exit -F path=/usr/bin/passwd -F perm=x -k passwd_usage
   auditctl -a always,exit -F path=/usr/bin/su -F perm=x -k su_usage
   auditctl -a always,exit -F path=/usr/sbin/usermod -F perm=x -k usermod
   auditctl -a always,exit -F path=/usr/sbin/useradd -F perm=x -k useradd
   auditctl -a always,exit -F path=/usr/sbin/userdel -F perm=x -k userdel
   auditctl -a always,exit -F path=/usr/sbin/groupadd -F perm=x -k groupadd
   auditctl -a always,exit -F path=/usr/sbin/groupdel -F perm=x -k groupdel
   
   # Generate rules for all SUID/SGID files
   find / -type f -perm -4000 2>/dev/null | awk '{print "-a always,exit -F path=" $1 " -F perm=x -k privileged"}'

User and Authentication Auditing
---------------------------------

.. code-block:: bash

   # Login/logout events
   auditctl -w /var/log/lastlog -p wa -k logins
   auditctl -w /var/run/faillock/ -p wa -k logins
   
   # Session events
   auditctl -w /var/log/wtmp -p wa -k session
   auditctl -w /var/log/btmp -p wa -k session
   
   # Authentication events (automatic via pam_audit)
   # Check /etc/pam.d/ configuration

Kernel Module Auditing
-----------------------

.. code-block:: bash

   # Module loading/unloading
   auditctl -a always,exit -F arch=b64 -S init_module -S delete_module -k kernel_modules
   
   # Or watch module files
   auditctl -w /sbin/insmod -p x -k kernel_modules
   auditctl -w /sbin/rmmod -p x -k kernel_modules
   auditctl -w /sbin/modprobe -p x -k kernel_modules

Managing Rules
==============

Runtime Rules
-------------

.. code-block:: bash

   # List current rules
   sudo auditctl -l
   
   # List with more detail
   sudo auditctl -s
   
   # Add rule
   sudo auditctl -w /etc/hosts -p wa -k hosts_changes
   
   # Delete specific rule
   sudo auditctl -W /etc/hosts -p wa -k hosts_changes
   
   # Delete all rules
   sudo auditctl -D
   
   # Make immutable (cannot be changed until reboot)
   sudo auditctl -e 2
   
   # Enable auditing
   sudo auditctl -e 1
   
   # Disable auditing
   sudo auditctl -e 0

Persistent Rules
----------------

.. code-block:: bash

   # Rules directory
   /etc/audit/rules.d/
   
   # Create custom rules file
   sudo nano /etc/audit/rules.d/custom.rules
   
   # Example custom.rules:
   ## Delete all existing rules
   -D
   
   ## Buffer size
   -b 8192
   
   ## Failure mode (0=silent, 1=printk, 2=panic)
   -f 1
   
   ## File watches
   -w /etc/passwd -p wa -k passwd_changes
   -w /etc/group -p wa -k group_changes
   -w /etc/shadow -p wa -k shadow_changes
   
   ## Syscall rules
   -a always,exit -F arch=b64 -S openat -k file_access
   
   ## Make immutable
   -e 2
   
   # Generate rules from runtime
   sudo sh -c "auditctl -l > /etc/audit/rules.d/current.rules"
   
   # Reload rules
   sudo augenrules --load
   
   # Or restart service
   sudo service auditd restart

Searching Logs
==============

ausearch Tool
-------------

.. code-block:: bash

   # Search by message type
   sudo ausearch -m USER_LOGIN
   sudo ausearch -m USER_AUTH
   sudo ausearch -m EXECVE
   
   # Search by key
   sudo ausearch -k passwd_changes
   sudo ausearch -k sshd_config
   
   # Search by timestamp
   sudo ausearch -ts today
   sudo ausearch -ts this-month
   sudo ausearch -ts 10:00:00
   sudo ausearch -ts yesterday -te today
   
   # Search by user
   sudo ausearch -ua username
   sudo ausearch -ui 1000
   
   # Search by process ID
   sudo ausearch -p 1234
   
   # Search by system call
   sudo ausearch -sc open
   sudo ausearch -sc execve
   
   # Search by success/failure
   sudo ausearch -m USER_LOGIN -sv yes    # Successful
   sudo ausearch -m USER_LOGIN -sv no     # Failed
   
   # Combine criteria
   sudo ausearch -k passwd_changes -ts today -i
   
   # Interpret output (-i for human-readable)
   sudo ausearch -k passwd_changes -i
   
   # Format as raw logs
   sudo ausearch -k passwd_changes --raw

Common Search Patterns
----------------------

.. code-block:: bash

   # Failed login attempts
   sudo ausearch -m USER_LOGIN -sv no
   sudo ausearch -m USER_AUTH -sv no
   
   # Successful logins
   sudo ausearch -m USER_LOGIN -sv yes
   
   # User commands
   sudo ausearch -m EXECVE -ua username
   
   # File access
   sudo ausearch -k file_access -ts today
   
   # Privilege escalation
   sudo ausearch -k sudo_usage -ts today
   
   # Security changes
   sudo ausearch -k passwd_changes -k shadow_changes -k group_changes

Generating Reports
==================

aureport Tool
-------------

.. code-block:: bash

   # Summary report
   sudo aureport --summary
   
   # Login report
   sudo aureport --login
   sudo aureport --login --summary
   
   # Authentication report
   sudo aureport --auth
   
   # File access report
   sudo aureport --file
   
   # Executable report
   sudo aureport --executable
   
   # User report
   sudo aureport --user
   
   # Terminal report
   sudo aureport --terminal
   
   # Failed events
   sudo aureport --failed
   
   # Anomaly report
   sudo aureport --anomaly
   
   # Time range
   sudo aureport --start today --end now
   sudo aureport --start this-month
   
   # Input from file
   sudo aureport -if /var/log/audit/audit.log.1

Custom Reports
--------------

.. code-block:: bash

   # Generate report script
   #!/bin/bash
   
   REPORT_FILE="/var/log/audit/daily_report_$(date +%Y%m%d).txt"
   
   {
     echo "=== Audit Report for $(date) ==="
     echo ""
     
     echo "Summary:"
     aureport --summary
     echo ""
     
     echo "Failed Login Attempts:"
     aureport --login --failed
     echo ""
     
     echo "Authentication Failures:"
     aureport --auth --failed
     echo ""
     
     echo "File Modifications:"
     ausearch -k passwd_changes -k shadow_changes -k group_changes -ts today
     echo ""
     
     echo "Privileged Command Usage:"
     ausearch -k sudo_usage -k su_usage -ts today
     echo ""
     
   } > "$REPORT_FILE"
   
   echo "Report generated: $REPORT_FILE"

Compliance Frameworks
=====================

CIS Benchmark Rules
-------------------

.. code-block:: bash

   # /etc/audit/rules.d/cis.rules
   
   # 4.1.3 Ensure changes to system administration scope are collected
   -w /etc/sudoers -p wa -k scope
   -w /etc/sudoers.d/ -p wa -k scope
   
   # 4.1.4 Ensure login and logout events are collected
   -w /var/log/lastlog -p wa -k logins
   -w /var/run/faillock/ -p wa -k logins
   
   # 4.1.5 Ensure session initiation information is collected
   -w /var/run/utmp -p wa -k session
   -w /var/log/wtmp -p wa -k session
   -w /var/log/btmp -p wa -k session
   
   # 4.1.6 Ensure events that modify date and time are collected
   -a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
   -a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change
   -a always,exit -F arch=b64 -S clock_settime -k time-change
   -a always,exit -F arch=b32 -S clock_settime -k time-change
   -w /etc/localtime -p wa -k time-change
   
   # 4.1.7 Ensure events that modify user/group information are collected
   -w /etc/group -p wa -k identity
   -w /etc/passwd -p wa -k identity
   -w /etc/gshadow -p wa -k identity
   -w /etc/shadow -p wa -k identity
   -w /etc/security/opasswd -p wa -k identity
   
   # 4.1.8 Ensure events that modify the system's network environment are collected
   -a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale
   -a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale
   -w /etc/issue -p wa -k system-locale
   -w /etc/issue.net -p wa -k system-locale
   -w /etc/hosts -p wa -k system-locale
   -w /etc/sysconfig/network -p wa -k system-locale
   
   # 4.1.9 Ensure discretionary access control permission modification events are collected
   -a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
   -a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
   -a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
   -a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
   -a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
   -a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
   
   # 4.1.10 Ensure unsuccessful unauthorized file access attempts are collected
   -a always,exit -F arch=b64 -S open -S openat -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
   -a always,exit -F arch=b32 -S open -S openat -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
   -a always,exit -F arch=b64 -S open -S openat -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access
   -a always,exit -F arch=b32 -S open -S openat -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access
   
   # 4.1.11 Ensure use of privileged commands is collected
   # (Generate with find)
   
   # 4.1.13 Ensure successful file system mounts are collected
   -a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
   -a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
   
   # 4.1.14 Ensure file deletion events are collected
   -a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
   -a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
   
   # 4.1.15 Ensure kernel module loading and unloading is collected
   -w /sbin/insmod -p x -k modules
   -w /sbin/rmmod -p x -k modules
   -w /sbin/modprobe -p x -k modules
   -a always,exit -F arch=b64 -S init_module -S delete_module -k modules

PCI-DSS Requirements
--------------------

.. code-block:: bash

   # Requirement 10.2.2 - All actions by privileged users
   -a always,exit -F euid=0 -F arch=b64 -S execve -k root_commands
   
   # Requirement 10.2.3 - All access to audit trails
   -w /var/log/audit/ -p rwxa -k audit_log_access
   
   # Requirement 10.2.4 - Invalid logical access attempts
   # (Handled by PAM and covered by login auditing)
   
   # Requirement 10.2.5 - Changes to identification and authentication
   -w /etc/passwd -p wa -k identity
   -w /etc/group -p wa -k identity
   -w /etc/shadow -p wa -k identity
   -w /etc/security/ -p wa -k pam_changes
   
   # Requirement 10.2.7 - Creation and deletion of system-level objects
   -a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -k object_delete

Advanced Auditing
=================

Audisp (Audit Dispatcher)
--------------------------

.. code-block:: bash

   # Configuration
   /etc/audisp/audispd.conf
   /etc/audisp/plugins.d/
   
   # Syslog plugin
   # /etc/audisp/plugins.d/syslog.conf
   active = yes
   direction = out
   path = /sbin/audisp-syslog
   type = always
   args = LOG_INFO
   format = string
   
   # Remote logging plugin
   # /etc/audisp/plugins.d/au-remote.conf
   active = yes
   direction = out
   path = /sbin/audisp-remote
   type = always
   format = string
   
   # /etc/audisp/audisp-remote.conf
   remote_server = 192.168.1.100
   port = 60
   transport = tcp

Real-time Alerts
----------------

.. code-block:: bash

   # Script to monitor audit log
   #!/bin/bash
   # /usr/local/bin/audit-monitor.sh
   
   tail -F /var/log/audit/audit.log | while read line; do
     # Alert on failed logins
     if echo "$line" | grep -q "USER_LOGIN.*res=failed"; then
       echo "ALERT: Failed login detected: $line" | \
         mail -s "Security Alert: Failed Login" admin@example.com
     fi
     
     # Alert on passwd changes
     if echo "$line" | grep -q "passwd_changes"; then
       echo "ALERT: Password file modified: $line" | \
         mail -s "Security Alert: Password Change" admin@example.com
     fi
   done

Best Practices
==============

1. **Enable auditd** at boot and keep it running
2. **Audit critical files** - /etc/passwd, /etc/shadow, /etc/sudoers
3. **Monitor privileged commands** - sudo, su, passwd
4. **Track user activity** - logins, logouts, command execution
5. **Log to remote server** for tamper-resistance
6. **Regular log review** - daily/weekly reports
7. **Sufficient log retention** - comply with requirements
8. **Protect audit logs** - restrict access, monitor modifications
9. **Test audit rules** - verify they work as expected
10. **Immutable rules** - use -e 2 in production

Common Pitfalls
===============

1. **Too many rules** - performance impact
2. **Not enough disk space** - logs fill filesystem
3. **Not rotating logs** - single huge file
4. **Forgetting -i flag** - hard to read UID/GID numbers
5. **Not making rules persistent** - lost on reboot
6. **No alerting** - audit data not acted upon
7. **Auditing loopback** - can create noise

Quick Reference
===============

.. code-block:: bash

   # Service
   systemctl start/stop/status auditd
   service auditd rotate
   
   # Rules
   auditctl -l             # List
   auditctl -D             # Delete all
   auditctl -w path -p perms -k key   # Watch file
   auditctl -a action,filter -S syscall -k key   # System call
   
   # Search
   ausearch -k key         # By key
   ausearch -m type        # By message type
   ausearch -ts timestamp  # By time
   ausearch -ua user       # By user
   ausearch -i             # Interpret
   
   # Report
   aureport --summary
   aureport --login
   aureport --failed

See Also
========

- Linux_Security_Hardening.rst
- Linux_SELinux.rst
- Linux_Intrusion_Detection.rst

References
==========

- man auditd
- man auditctl
- man ausearch
- man aureport
- https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/auditing-the-system_security-hardening
