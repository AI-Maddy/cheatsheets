===================================
Linux SELinux Security Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: Security-Enhanced Linux (SELinux) - Mandatory Access Control

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential SELinux Commands
---------------------------

.. code-block:: bash

   # Check SELinux status
   getenforce
   sestatus
   
   # Set SELinux mode (temporary)
   setenforce 0  # Permissive
   setenforce 1  # Enforcing
   
   # View file contexts
   ls -Z /var/www/html/
   ps -eZ
   
   # Restore default context
   restorecon -Rv /var/www/html/
   
   # Change file context
   semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"
   restorecon -Rv /web
   
   # View denials
   ausearch -m avc -ts recent
   grep AVC /var/log/audit/audit.log
   
   # Allow denied access (generate policy)
   ausearch -m avc -ts recent | audit2allow -M mypolicy
   semodule -i mypolicy.pp
   
   # Boolean management
   getsebool -a | grep httpd
   setsebool -P httpd_can_network_connect on

Quick Troubleshooting
----------------------

.. code-block:: bash

   # Service won't start - check SELinux denials
   ausearch -m avc -ts recent
   
   # Web server can't access files
   restorecon -Rv /var/www/html/
   chcon -R -t httpd_sys_content_t /var/www/html/
   
   # Allow specific action temporarily
   setenforce 0  # Test in permissive mode
   # If it works, SELinux is the issue
   setenforce 1
   
   # Create custom policy for denial
   grep denied /var/log/audit/audit.log | audit2allow -M mycustom
   semodule -i mycustom.pp

SELinux Basics
==============

SELinux Modes
-------------

.. code-block:: bash

   # Three modes:
   # - Enforcing: SELinux policy is enforced
   # - Permissive: SELinux prints warnings but doesn't enforce
   # - Disabled: SELinux is turned off
   
   # Check current mode
   getenforce
   
   # Set mode temporarily (until reboot)
   setenforce 0  # Permissive
   setenforce 1  # Enforcing
   
   # Set mode permanently
   # /etc/selinux/config
   SELINUX=enforcing
   # or
   SELINUX=permissive
   # or
   SELINUX=disabled
   
   # View full status
   sestatus
   
   # Output shows:
   # - SELinux status
   # - Current mode
   # - Mode from config file
   # - Policy version
   # - Policy MLS status

SELinux Contexts
----------------

.. code-block:: text

   SELinux context format: user:role:type:level
   
   Example: system_u:object_r:httpd_sys_content_t:s0
   
   - user: SELinux user (system_u, user_u, etc.)
   - role: SELinux role (object_r for files, system_r for processes)
   - type: SELinux type (most important for access control)
   - level: MLS/MCS security level (s0, s0-s0:c0.c1023)

.. code-block:: bash

   # View file contexts
   ls -Z
   ls -lZ /var/www/html/
   
   # View process contexts
   ps -eZ
   ps auxZ | grep httpd
   
   # View user contexts
   id -Z
   
   # View port contexts
   semanage port -l
   
   # View all contexts
   seinfo -t  # All types
   seinfo -r  # All roles
   seinfo -u  # All users

File Contexts
=============

Viewing and Setting Contexts
-----------------------------

.. code-block:: bash

   # View context of files
   ls -Z /var/www/html/
   stat -c %C /var/www/html/index.html
   
   # Change context temporarily (until relabel)
   chcon -t httpd_sys_content_t /var/www/html/index.html
   chcon -R -t httpd_sys_content_t /var/www/html/
   
   # Copy context from another file
   chcon --reference=/var/www/html/reference.html /var/www/html/new.html
   
   # Restore default context
   restorecon /var/www/html/index.html
   restorecon -Rv /var/www/html/
   
   # Restore entire filesystem (use carefully)
   restorecon -Rv /

Permanent Context Rules
-----------------------

.. code-block:: bash

   # Add permanent context rule
   semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"
   
   # Apply the rule
   restorecon -Rv /web
   
   # View custom rules
   semanage fcontext -l -C
   
   # View all rules
   semanage fcontext -l
   
   # Delete rule
   semanage fcontext -d "/web(/.*)?"
   
   # Modify existing rule
   semanage fcontext -m -t httpd_sys_rw_content_t "/web/uploads(/.*)?"
   restorecon -Rv /web/uploads

Common File Types
-----------------

.. code-block:: text

   httpd_sys_content_t        - Web server read-only content
   httpd_sys_rw_content_t     - Web server read-write content
   httpd_sys_script_exec_t    - CGI scripts
   httpd_log_t                - Web server logs
   user_home_t                - User home directories
   tmp_t                      - Temporary files
   var_t                      - /var directory
   etc_t                      - /etc configuration files
   bin_t                      - Executable binaries
   lib_t                      - Libraries

Port Contexts
=============

Managing Port Labels
--------------------

.. code-block:: bash

   # View port contexts
   semanage port -l
   semanage port -l | grep http
   
   # Add port to context
   semanage port -a -t http_port_t -p tcp 8080
   
   # Allow httpd to listen on non-standard port
   semanage port -a -t http_port_t -p tcp 8888
   
   # Modify port context
   semanage port -m -t http_port_t -p tcp 8080
   
   # Delete port context
   semanage port -d -t http_port_t -p tcp 8080
   
   # Common port types
   http_port_t                # HTTP (80, 443, 488, 8008, 8009, 8443)
   ssh_port_t                 # SSH (22)
   smtp_port_t                # SMTP (25, 465, 587)
   postgresql_port_t          # PostgreSQL (5432)
   mysqld_port_t              # MySQL (3306)

SELinux Booleans
================

Boolean Management
------------------

.. code-block:: bash

   # List all booleans
   getsebool -a
   
   # List booleans for specific service
   getsebool -a | grep httpd
   getsebool -a | grep ftp
   getsebool -a | grep samba
   
   # Check specific boolean
   getsebool httpd_can_network_connect
   
   # Set boolean temporarily
   setsebool httpd_can_network_connect on
   
   # Set boolean permanently (-P)
   setsebool -P httpd_can_network_connect on
   
   # Set multiple booleans
   setsebool -P httpd_can_network_connect on \
             httpd_can_sendmail on \
             httpd_enable_cgi on

Common Booleans
---------------

.. code-block:: bash

   # Apache/HTTP
   httpd_can_network_connect      # Allow httpd to make network connections
   httpd_can_network_connect_db   # Allow httpd to connect to databases
   httpd_can_sendmail             # Allow httpd to send mail
   httpd_enable_cgi               # Allow httpd to run CGI scripts
   httpd_enable_homedirs          # Allow httpd to access user home directories
   httpd_execmem                  # Allow httpd to execute programs requiring memory
   httpd_unified                  # Unify httpd handling of all content
   
   # FTP
   ftpd_full_access               # Allow ftp servers to login to local users
   ftp_home_dir                   # Allow ftp to read/write user home directories
   
   # Samba
   samba_enable_home_dirs         # Allow Samba to share user home directories
   samba_export_all_ro            # Allow Samba to share all files/directories (read-only)
   samba_export_all_rw            # Allow Samba to share all files/directories (read-write)
   
   # NFS
   nfs_export_all_ro              # Allow NFS to export all files (read-only)
   nfs_export_all_rw              # Allow NFS to export all files (read-write)

SELinux Users and Roles
=======================

User Management
---------------

.. code-block:: bash

   # List SELinux users
   semanage user -l
   
   # Map Linux user to SELinux user
   semanage login -l
   
   # Add user mapping
   semanage login -a -s user_u username
   
   # Modify user mapping
   semanage login -m -s staff_u username
   
   # Delete user mapping
   semanage login -d username
   
   # Common SELinux users:
   # - unconfined_u: Unconfined user (most permissions)
   # - user_u: Regular user (restricted)
   # - staff_u: Staff user (can sudo to sysadm_r)
   # - sysadm_u: System administrator (unrestricted admin)
   # - system_u: System user (for daemons)

Troubleshooting SELinux
========================

Finding Denials
---------------

.. code-block:: bash

   # View recent denials
   ausearch -m avc -ts recent
   ausearch -m avc -ts today
   
   # Search audit log
   grep AVC /var/log/audit/audit.log
   grep denied /var/log/audit/audit.log
   
   # Follow denials in real-time
   tail -f /var/log/audit/audit.log | grep AVC
   
   # Search for denials by service
   ausearch -m avc -c httpd
   
   # Use sealert (setroubleshoot)
   sealert -a /var/log/audit/audit.log
   
   # View alerts
   sealert -l "*"

Analyzing Denials
-----------------

.. code-block:: bash

   # Install analysis tools
   yum install setroubleshoot setroubleshoot-server
   
   # Analyze denials
   sealert -a /var/log/audit/audit.log
   
   # Get specific alert details
   sealert -l <alert-id>
   
   # Example denial:
   type=AVC msg=audit(1234567890.123:456): avc: denied { write } for
     pid=1234 comm="httpd" name="index.html" dev="sda1" ino=12345
     scontext=system_u:system_r:httpd_t:s0
     tcontext=system_u:object_r:user_home_t:s0
     tclass=file permissive=0
   
   # This shows:
   # - httpd_t tried to write to user_home_t
   # - Action: denied
   # - File: index.html

Creating Custom Policies
=========================

Using audit2allow
-----------------

.. code-block:: bash

   # Generate policy from denials
   ausearch -m avc -ts recent | audit2allow
   
   # Generate and compile module
   ausearch -m avc -ts recent | audit2allow -M mypolicy
   
   # This creates:
   # - mypolicy.te (type enforcement file)
   # - mypolicy.pp (compiled policy package)
   
   # Install policy module
   semodule -i mypolicy.pp
   
   # View installed modules
   semodule -l
   
   # Remove module
   semodule -r mypolicy
   
   # Disable module
   semodule -d mypolicy
   
   # Enable module
   semodule -e mypolicy

Manual Policy Creation
----------------------

.. code-block:: bash

   # Create type enforcement file
   # myapp.te
   cat > myapp.te <<EOF
   module myapp 1.0;
   
   require {
       type httpd_t;
       type user_home_t;
       class file { read write };
   }
   
   # Allow httpd to read/write user home files
   allow httpd_t user_home_t:file { read write };
   EOF
   
   # Compile policy
   checkmodule -M -m -o myapp.mod myapp.te
   semodule_package -o myapp.pp -m myapp.mod
   
   # Install
   semodule -i myapp.pp

Common Scenarios
================

Web Server (Apache/Nginx)
--------------------------

.. code-block:: bash

   # Allow web server to access custom directory
   semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"
   restorecon -Rv /srv/www
   
   # Allow web server to connect to database
   setsebool -P httpd_can_network_connect_db on
   
   # Allow web server to send email
   setsebool -P httpd_can_sendmail on
   
   # Allow web server to connect to network
   setsebool -P httpd_can_network_connect on
   
   # Allow web server writable directory
   semanage fcontext -a -t httpd_sys_rw_content_t "/srv/www/uploads(/.*)?"
   restorecon -Rv /srv/www/uploads
   
   # Allow CGI scripts
   semanage fcontext -a -t httpd_sys_script_exec_t "/srv/www/cgi-bin(/.*)?"
   restorecon -Rv /srv/www/cgi-bin
   setsebool -P httpd_enable_cgi on

Database (MySQL/PostgreSQL)
----------------------------

.. code-block:: bash

   # Custom database directory
   semanage fcontext -a -t mysqld_db_t "/data/mysql(/.*)?"
   restorecon -Rv /data/mysql
   
   # Allow database to listen on custom port
   semanage port -a -t mysqld_port_t -p tcp 3307
   
   # PostgreSQL custom directory
   semanage fcontext -a -t postgresql_db_t "/data/pgsql(/.*)?"
   restorecon -Rv /data/pgsql

SSH Server
----------

.. code-block:: bash

   # Custom SSH port
   semanage port -a -t ssh_port_t -p tcp 2222
   
   # Allow SSH to use user home directories
   setsebool -P ssh_chroot_rw_homedirs on

Docker/Containers
-----------------

.. code-block:: bash

   # Allow containers to use NFS
   setsebool -P virt_use_nfs on
   
   # Allow containers to use Samba
   setsebool -P virt_use_samba on
   
   # Container volumes
   chcon -Rt svirt_sandbox_file_t /path/to/volume

SELinux Policy Development
===========================

Policy Types
------------

.. code-block:: text

   Targeted Policy (default):
   - Most processes run unconfined
   - Network-facing services are confined
   - Used in RHEL/CentOS/Fedora
   
   MLS Policy:
   - Multi-Level Security
   - Based on Bell-LaPadula model
   - Used in high-security environments
   
   Minimum Policy:
   - Minimal set of confined domains
   - Less protection than targeted

Development Tools
-----------------

.. code-block:: bash

   # Install development tools
   yum install selinux-policy-devel
   
   # Policy source location
   cd /usr/share/selinux/devel
   
   # Create new policy module
   sepolicy generate --init /usr/sbin/myapp
   
   # This generates:
   # - myapp.te (type enforcement)
   # - myapp.if (interface)
   # - myapp.fc (file context)
   
   # Build and install
   make -f /usr/share/selinux/devel/Makefile myapp.pp
   semodule -i myapp.pp

Best Practices
==============

1. **Start with permissive mode** when troubleshooting
2. **Use restorecon** instead of chcon for permanent changes
3. **Use semanage** for persistent configuration
4. **Always use -P flag** with setsebool for persistence
5. **Analyze denials carefully** before creating policies
6. **Avoid using audit2allow blindly** - understand the policy
7. **Test custom policies** in non-production first
8. **Document custom policies** and booleans
9. **Regular policy updates** with system updates
10. **Monitor audit logs** for unexpected denials

Common Pitfalls
===============

1. **Disabling SELinux** instead of fixing issues
2. **Using chcon** instead of semanage (not persistent)
3. **Overly permissive policies** from blind audit2allow use
4. **Not testing** in permissive mode first
5. **Forgetting -P flag** with setsebool (not persistent)
6. **Not running restorecon** after changing contexts
7. **Incorrect regex** in semanage fcontext rules

Quick Troubleshooting Workflow
===============================

.. code-block:: bash

   # 1. Reproduce the issue
   # 2. Check if SELinux is the problem
   setenforce 0  # Permissive
   # Try again - if it works, SELinux is involved
   setenforce 1  # Back to enforcing
   
   # 3. Find the denial
   ausearch -m avc -ts recent
   
   # 4. Analyze with sealert
   sealert -a /var/log/audit/audit.log
   
   # 5. Try suggested solution:
   #    - Boolean change
   #    - File context fix
   #    - Port label
   
   # 6. If no suggestion, create policy
   ausearch -m avc -ts recent | audit2allow -M mypolicy
   semodule -i mypolicy.pp
   
   # 7. Test and document

Reference Commands
==================

.. code-block:: bash

   # Status and mode
   getenforce, setenforce, sestatus
   
   # Contexts
   ls -Z, ps -Z, id -Z, stat -c %C
   chcon, restorecon
   
   # Permanent rules
   semanage fcontext, semanage port, semanage login
   
   # Booleans
   getsebool, setsebool
   
   # Modules
   semodule -l, semodule -i, semodule -r
   
   # Troubleshooting
   ausearch, grep AVC, sealert
   
   # Policy development
   audit2allow, checkmodule, semodule_package

See Also
========

- Linux_Security_Hardening.rst
- Linux_AppArmor.rst
- Linux_Security_Auditing.rst

References
==========

- Red Hat SELinux User's and Administrator's Guide
- https://selinuxproject.org/
- man selinux
- man semanage
- man setsebool
