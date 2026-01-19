===================================
Linux AppArmor Security Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: AppArmor - Application-level Mandatory Access Control

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential AppArmor Commands
----------------------------

.. code-block:: bash

   # Check AppArmor status
   sudo aa-status
   sudo apparmor_status
   
   # Modes: enforce, complain, disable
   # Put profile in complain mode
   sudo aa-complain /etc/apparmor.d/usr.bin.firefox
   
   # Put profile in enforce mode
   sudo aa-enforce /etc/apparmor.d/usr.bin.firefox
   
   # Disable profile
   sudo aa-disable /etc/apparmor.d/usr.bin.firefox
   
   # Reload profile
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.firefox
   
   # View denials
   sudo aa-logprof
   sudo dmesg | grep -i apparmor
   sudo journalctl | grep -i apparmor
   
   # Generate profile
   sudo aa-genprof /usr/bin/myapp
   
   # Update profile from logs
   sudo aa-logprof

Quick Profile Creation
-----------------------

.. code-block:: bash

   # Interactive profile generation
   sudo aa-genprof /usr/bin/myapp
   
   # Steps:
   # 1. Runs in separate terminal: sudo /usr/bin/myapp
   # 2. Exercise all functionality
   # 3. In aa-genprof terminal: press 's' to scan logs
   # 4. Review and allow/deny each access
   # 5. Save profile
   
   # Profile saved to: /etc/apparmor.d/usr.bin.myapp
   
   # Enable profile
   sudo aa-enforce /etc/apparmor.d/usr.bin.myapp

AppArmor Basics
===============

AppArmor Architecture
---------------------

.. code-block:: text

   AppArmor Components:
   
   1. Kernel Module: Enforces policies
   2. Profiles: Define access rules (/etc/apparmor.d/)
   3. Parser: Loads profiles into kernel
   4. Utilities: Management tools (aa-*)
   
   Profile Modes:
   - Enforce: Actively blocks violations
   - Complain: Logs violations but allows
   - Disabled: Profile not loaded

Installation
------------

.. code-block:: bash

   # Debian/Ubuntu (usually pre-installed)
   sudo apt install apparmor apparmor-utils apparmor-profiles
   
   # Check if running
   sudo systemctl status apparmor
   
   # Enable AppArmor
   sudo systemctl enable apparmor
   sudo systemctl start apparmor
   
   # Check kernel support
   cat /sys/module/apparmor/parameters/enabled
   # Should show: Y

Status and Information
----------------------

.. code-block:: bash

   # Detailed status
   sudo aa-status
   
   # Output shows:
   # - Profiles loaded
   # - Profiles in enforce mode
   # - Profiles in complain mode
   # - Processes with profiles
   # - Processes in enforce mode
   # - Processes in complain mode
   # - Processes unconfined
   
   # Check specific process
   cat /proc/$(pidof nginx)/attr/current
   
   # List all profiles
   ls /etc/apparmor.d/
   
   # Check profile syntax
   sudo apparmor_parser -p /etc/apparmor.d/usr.bin.firefox

Profile Management
==================

Profile Locations
-----------------

.. code-block:: bash

   # Main profiles
   /etc/apparmor.d/
   
   # Abstractions (reusable components)
   /etc/apparmor.d/abstractions/
   
   # Tunables (variables)
   /etc/apparmor.d/tunables/
   
   # Local overrides
   /etc/apparmor.d/local/
   
   # Disabled profiles
   /etc/apparmor.d/disable/
   
   # Cache
   /var/cache/apparmor/

Loading and Reloading Profiles
-------------------------------

.. code-block:: bash

   # Load profile
   sudo apparmor_parser -a /etc/apparmor.d/usr.bin.myapp
   
   # Reload profile (after editing)
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.myapp
   
   # Reload all profiles
   sudo systemctl reload apparmor
   
   # Remove profile from kernel
   sudo apparmor_parser -R /etc/apparmor.d/usr.bin.myapp
   
   # Force reload (clears cache)
   sudo apparmor_parser -r -W /etc/apparmor.d/usr.bin.myapp

Profile Modes
-------------

.. code-block:: bash

   # Set to complain mode (log only)
   sudo aa-complain /etc/apparmor.d/usr.bin.firefox
   sudo aa-complain /usr/bin/firefox  # Can use binary path
   
   # Set to enforce mode
   sudo aa-enforce /etc/apparmor.d/usr.bin.firefox
   
   # Disable profile (creates symlink in disable/)
   sudo aa-disable /etc/apparmor.d/usr.bin.firefox
   
   # Re-enable disabled profile
   sudo rm /etc/apparmor.d/disable/usr.bin.firefox
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.firefox
   
   # Check mode
   sudo aa-status | grep firefox

Creating Profiles
=================

Automated Profile Generation
-----------------------------

.. code-block:: bash

   # Generate profile interactively
   sudo aa-genprof /usr/bin/myapp
   
   # Workflow:
   # 1. aa-genprof starts in learning mode
   # 2. Run application in another terminal
   # 3. Exercise all functionality
   # 4. Press 's' in aa-genprof to scan logs
   # 5. Review each logged event
   # 6. Choose: (A)llow, (D)eny, (I)gnore, (G)lob
   # 7. Save profile when done
   
   # Update existing profile from logs
   sudo aa-logprof
   
   # This reviews logged events and updates profiles

Manual Profile Creation
-----------------------

.. code-block:: bash

   # Create new profile file
   sudo nano /etc/apparmor.d/usr.bin.myapp
   
   # Basic profile structure:
   #include <tunables/global>
   
   /usr/bin/myapp {
     #include <abstractions/base>
     
     # Capabilities
     capability net_bind_service,
     
     # File access
     /usr/bin/myapp mr,
     /etc/myapp/** r,
     /var/log/myapp/* w,
     /var/lib/myapp/** rw,
     
     # Network
     network inet stream,
     network inet6 stream,
     
     # Execute
     /bin/bash ix,
     /usr/bin/python3 Px,
   }
   
   # Load profile
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.myapp

Profile Syntax
==============

File Access Rules
-----------------

.. code-block:: text

   File Access Modes:
   r  - read
   w  - write
   a  - append
   x  - execute
   m  - memory map with PROT_EXEC
   k  - lock
   l  - link
   ix - execute and inherit profile
   Px - execute under separate profile
   Ux - execute unconfined
   px - execute under separate profile (fallback to ix)
   ux - execute unconfined (fallback to ix)

.. code-block:: bash

   # Examples:
   /etc/passwd r,                    # Read only
   /tmp/** rw,                       # Read/write in /tmp recursively
   /var/log/app.log w,               # Write only
   /usr/bin/python3 ix,              # Execute and inherit
   /usr/bin/helper Px,               # Execute with own profile
   owner /home/*/.bashrc r,          # Read if owner
   deny /etc/shadow r,               # Explicitly deny

Capability Rules
----------------

.. code-block:: bash

   # Common capabilities
   capability setuid,                 # Change UID
   capability setgid,                 # Change GID
   capability net_bind_service,       # Bind to ports < 1024
   capability net_admin,              # Network administration
   capability sys_admin,              # System administration
   capability dac_override,           # Bypass file permissions
   capability dac_read_search,        # Bypass read permissions
   capability chown,                  # Change file ownership
   capability kill,                   # Send signals
   capability sys_ptrace,             # Trace processes

Network Rules
-------------

.. code-block:: bash

   # Network access
   network,                           # All networking
   network inet stream,               # IPv4 TCP
   network inet dgram,                # IPv4 UDP
   network inet6 stream,              # IPv6 TCP
   network inet6 dgram,               # IPv6 UDP
   network unix stream,               # Unix socket stream
   network unix dgram,                # Unix socket datagram
   network netlink raw,               # Netlink sockets

Signal Rules
------------

.. code-block:: bash

   # Signal permissions
   signal,                            # All signals
   signal send,                       # Send signals
   signal receive,                    # Receive signals
   signal send set=(term, kill),      # Send specific signals
   signal (send) peer=/usr/bin/app,   # Send to specific process

DBus Rules
----------

.. code-block:: bash

   # DBus access
   dbus,                              # All DBus access
   dbus send,                         # Send messages
   dbus receive,                      # Receive messages
   dbus (send) bus=system,            # System bus
   dbus (send, receive) bus=session,  # Session bus

Common Abstractions
===================

Using Abstractions
------------------

.. code-block:: bash

   # Include abstractions in profiles
   #include <abstractions/base>           # Basic system access
   #include <abstractions/nameservice>    # DNS, /etc/hosts, nsswitch
   #include <abstractions/openssl>        # OpenSSL libraries
   #include <abstractions/ssl_certs>      # SSL certificates
   #include <abstractions/apache2-common> # Apache common files
   #include <abstractions/mysql>          # MySQL client
   #include <abstractions/python>         # Python runtime
   #include <abstractions/perl>           # Perl runtime
   #include <abstractions/bash>           # Bash shell
   
   # View abstraction contents
   cat /etc/apparmor.d/abstractions/base

Local Customizations
--------------------

.. code-block:: bash

   # Local overrides for profiles
   # /etc/apparmor.d/local/usr.bin.myapp
   
   # Add custom rules without modifying main profile
   # Main profile includes:
   #include <local/usr.bin.myapp>
   
   # Example local file:
   # Allow access to custom directory
   /opt/custom/** rw,

Example Profiles
================

Web Server (Nginx)
------------------

.. code-block:: bash

   # /etc/apparmor.d/usr.sbin.nginx
   #include <tunables/global>
   
   /usr/sbin/nginx {
     #include <abstractions/base>
     #include <abstractions/nameservice>
     #include <abstractions/openssl>
     
     capability net_bind_service,
     capability setgid,
     capability setuid,
     capability dac_override,
     
     # Binary
     /usr/sbin/nginx mr,
     
     # Configuration
     /etc/nginx/** r,
     /etc/ssl/certs/** r,
     /etc/ssl/private/** r,
     
     # Content
     /var/www/** r,
     /usr/share/nginx/** r,
     
     # Logs
     /var/log/nginx/** w,
     
     # Runtime
     /run/nginx.pid w,
     /var/cache/nginx/** rw,
     
     # Network
     network inet stream,
     network inet6 stream,
     
     # Local customizations
     #include <local/usr.sbin.nginx>
   }

Database (MySQL)
----------------

.. code-block:: bash

   # /etc/apparmor.d/usr.sbin.mysqld
   #include <tunables/global>
   
   /usr/sbin/mysqld {
     #include <abstractions/base>
     #include <abstractions/nameservice>
     #include <abstractions/mysql>
     
     capability setuid,
     capability setgid,
     capability dac_override,
     capability sys_resource,
     
     # Binary
     /usr/sbin/mysqld mr,
     
     # Configuration
     /etc/mysql/** r,
     
     # Data
     /var/lib/mysql/** rwk,
     /var/lib/mysql-files/** rw,
     
     # Logs
     /var/log/mysql/** rw,
     
     # Runtime
     /run/mysqld/** rw,
     
     # Network
     network inet stream,
     network inet6 stream,
     network unix stream,
     
     #include <local/usr.sbin.mysqld>
   }

Application Server
------------------

.. code-block:: bash

   # Custom application
   #include <tunables/global>
   
   /opt/myapp/bin/server {
     #include <abstractions/base>
     #include <abstractions/nameservice>
     #include <abstractions/python>
     
     capability net_bind_service,
     
     # Application files
     /opt/myapp/** r,
     /opt/myapp/bin/server mr,
     
     # Configuration
     /etc/myapp/** r,
     
     # Data
     owner /var/lib/myapp/** rw,
     
     # Logs
     owner /var/log/myapp/** w,
     
     # Temporary
     owner /tmp/myapp-* rw,
     
     # Network
     network inet stream,
     network inet6 stream,
     
     # Database connection
     network unix stream,
     /run/mysqld/mysqld.sock rw,
     
     #include <local/opt.myapp.bin.server>
   }

Troubleshooting
===============

Viewing Denials
---------------

.. code-block:: bash

   # AppArmor logs to kernel log and audit
   sudo dmesg | grep -i apparmor
   sudo journalctl | grep -i apparmor
   sudo journalctl -k | grep -i apparmor
   
   # Recent denials
   sudo dmesg | grep -i "apparmor.*denied" | tail -20
   
   # Specific profile
   sudo journalctl | grep "profile=\"/usr/bin/firefox\""
   
   # With aa-logprof
   sudo aa-logprof
   # Interactively review and update profiles

Common Issues
-------------

.. code-block:: bash

   # Application doesn't start
   # 1. Check if AppArmor is blocking
   sudo aa-complain /etc/apparmor.d/usr.bin.myapp
   # Try again - if it works, AppArmor is the issue
   
   # 2. View denials
   sudo dmesg | grep -i "apparmor.*denied" | grep myapp
   
   # 3. Add missing permissions to profile
   
   # 4. Switch back to enforce
   sudo aa-enforce /etc/apparmor.d/usr.bin.myapp
   
   # Permission denied errors
   # Check for DENIED in logs
   sudo dmesg | grep -i denied
   
   # Profile won't load
   # Check syntax
   sudo apparmor_parser -p /etc/apparmor.d/usr.bin.myapp
   
   # Clear cache and reload
   sudo apparmor_parser -r -W /etc/apparmor.d/usr.bin.myapp

Debugging Workflow
------------------

.. code-block:: bash

   # 1. Put profile in complain mode
   sudo aa-complain /usr/bin/myapp
   
   # 2. Clear kernel log
   sudo dmesg -c
   
   # 3. Run application and exercise functionality
   /usr/bin/myapp
   
   # 4. Check what was logged
   sudo dmesg | grep -i apparmor
   
   # 5. Update profile with aa-logprof
   sudo aa-logprof
   
   # 6. Test in enforce mode
   sudo aa-enforce /usr/bin/myapp
   
   # 7. Repeat if needed

Tools and Utilities
===================

Profile Tools
-------------

.. code-block:: bash

   # aa-genprof: Generate new profile
   sudo aa-genprof /usr/bin/myapp
   
   # aa-logprof: Update profiles from logs
   sudo aa-logprof
   
   # aa-enforce: Set to enforce mode
   sudo aa-enforce /etc/apparmor.d/usr.bin.myapp
   
   # aa-complain: Set to complain mode
   sudo aa-complain /etc/apparmor.d/usr.bin.myapp
   
   # aa-disable: Disable profile
   sudo aa-disable /etc/apparmor.d/usr.bin.myapp
   
   # aa-status: Show AppArmor status
   sudo aa-status
   
   # aa-notify: Desktop notifications for denials
   aa-notify -p

Analysis Tools
--------------

.. code-block:: bash

   # apparmor_parser: Load/check profiles
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.myapp
   sudo apparmor_parser -p /etc/apparmor.d/usr.bin.myapp  # Check only
   
   # aa-exec: Execute program under specific profile
   sudo aa-exec -p /etc/apparmor.d/usr.bin.myapp -- /usr/bin/myapp
   
   # aa-unconfined: Show unconfined processes
   sudo aa-unconfined
   
   # aa-audit: Enable auditing for profile
   sudo aa-audit /etc/apparmor.d/usr.bin.myapp

Best Practices
==============

1. **Start in complain mode** for new profiles
2. **Use abstractions** to simplify profiles
3. **Test thoroughly** before enforcing
4. **Use aa-logprof** to refine profiles
5. **Document custom rules** in local/ files
6. **Regular updates** with aa-logprof
7. **Principle of least privilege** - grant minimal access
8. **Use owner keyword** for user-specific files
9. **Test after updates** - system or application
10. **Monitor logs** for unexpected denials

Common Pitfalls
===============

1. **Too permissive profiles** - defeats purpose
2. **Not testing** in complain mode first
3. **Forgetting to reload** after editing
4. **Ignoring abstractions** - reinventing the wheel
5. **Not using local/** for customizations
6. **Overly broad globs** (/**) without thought
7. **Not monitoring** after deployment

Quick Reference
===============

.. code-block:: bash

   # Status
   sudo aa-status
   
   # Create profile
   sudo aa-genprof /usr/bin/app
   
   # Update from logs
   sudo aa-logprof
   
   # Modes
   sudo aa-complain /etc/apparmor.d/profile
   sudo aa-enforce /etc/apparmor.d/profile
   sudo aa-disable /etc/apparmor.d/profile
   
   # Reload
   sudo apparmor_parser -r /etc/apparmor.d/profile
   
   # Check denials
   sudo dmesg | grep -i denied
   sudo journalctl | grep -i apparmor

See Also
========

- Linux_Security_Hardening.rst
- Linux_SELinux.rst
- Linux_Security_Auditing.rst

References
==========

- Ubuntu AppArmor Guide
- https://apparmor.net/
- https://gitlab.com/apparmor
- man apparmor
- man aa-genprof
- man aa-logprof
