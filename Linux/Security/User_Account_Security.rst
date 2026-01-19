================================================================================
USER ACCOUNT SECURITY
================================================================================

**Complete Guide to Linux User and Group Management, Password Policies, and sudo**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 2

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # User Management
   sudo useradd -m -s /bin/bash username     # Create user with home dir
   sudo passwd username                       # Set password
   sudo userdel -r username                   # Delete user and home dir
   sudo usermod -L username                   # Lock account
   sudo usermod -U username                   # Unlock account
   
   # Group Management
   sudo groupadd developers                   # Create group
   sudo usermod -aG developers username       # Add user to group
   sudo gpasswd -d username developers        # Remove user from group
   groups username                            # Show user's groups
   
   # Password Management
   sudo chage -l username                     # Check password aging
   sudo chage -M 90 username                  # Set password expiry (90 days)
   sudo passwd -e username                    # Force password change on next login
   
   # sudo Configuration
   sudo visudo                                # Edit sudoers file (safe)
   sudo usermod -aG sudo username             # Add user to sudo group (Debian/Ubuntu)
   sudo usermod -aG wheel username            # Add user to wheel group (RHEL/CentOS)
   
   # Account Auditing
   last                                       # Login history
   lastlog                                    # Last login for all users
   faillog                                    # Failed login attempts
   sudo aureport --auth                       # Authentication report (if auditd enabled)

================================================================================
1. User Account Management
================================================================================

1.1 Creating Users
------------------

**useradd Command:**

.. code-block:: bash

   # Basic user creation
   sudo useradd username
   
   # Create user with home directory
   sudo useradd -m username
   
   # Create user with specific shell
   sudo useradd -m -s /bin/bash username
   
   # Create user with specific UID
   sudo useradd -m -u 1500 username
   
   # Create user with specific home directory
   sudo useradd -m -d /custom/home/username username
   
   # Create user with comment
   sudo useradd -m -c "John Doe" username
   
   # Create user with expiry date
   sudo useradd -m -e 2026-12-31 username
   
   # Create system user (no home, no login)
   sudo useradd -r -s /usr/sbin/nologin serviceuser
   
   # Complete example
   sudo useradd -m -s /bin/bash -c "Developer Account" -G developers,docker developer1

**adduser Command (Debian/Ubuntu - Interactive):**

.. code-block:: bash

   # Interactive user creation with prompts
   sudo adduser username
   
   # This will:
   # - Create home directory
   # - Copy skeleton files
   # - Prompt for password
   # - Prompt for user information
   # - Create user's group

**Set Password:**

.. code-block:: bash

   # Set password interactively
   sudo passwd username
   
   # Set password from command line (not recommended - visible in history)
   echo "password" | sudo passwd --stdin username    # RHEL/CentOS
   echo "username:password" | sudo chpasswd          # All distributions
   
   # Generate random password
   NEWPASS=$(openssl rand -base64 12)
   echo "$NEWPASS"
   echo "username:$NEWPASS" | sudo chpasswd

1.2 Modifying Users
-------------------

**usermod Command:**

.. code-block:: bash

   # Change user's shell
   sudo usermod -s /bin/zsh username
   
   # Change user's home directory
   sudo usermod -d /new/home/path username
   
   # Move home directory contents to new location
   sudo usermod -d /new/home/path -m username
   
   # Change user's UID
   sudo usermod -u 2000 username
   
   # Change user's primary group
   sudo usermod -g developers username
   
   # Add user to supplementary group (append mode - keeps existing groups)
   sudo usermod -aG sudo username
   sudo usermod -aG wheel,developers,docker username
   
   # Set account expiry date
   sudo usermod -e 2026-12-31 username
   
   # Lock user account (disable login)
   sudo usermod -L username
   
   # Unlock user account
   sudo usermod -U username
   
   # Change username
   sudo usermod -l newusername oldusername

**Lock/Unlock Accounts:**

.. code-block:: bash

   # Lock account (using passwd)
   sudo passwd -l username
   
   # Unlock account
   sudo passwd -u username
   
   # Check if account is locked
   sudo passwd -S username
   # Output: username L ... (L = locked, P = password set)
   
   # Expire account immediately
   sudo usermod -e 1 username
   
   # Remove account expiry
   sudo usermod -e "" username

1.3 Deleting Users
------------------

.. code-block:: bash

   # Delete user (keep home directory)
   sudo userdel username
   
   # Delete user and home directory
   sudo userdel -r username
   
   # Delete user and all files owned by user
   sudo userdel -r username
   sudo find / -user username -exec rm -rf {} \;
   
   # Force delete (even if logged in - dangerous!)
   sudo userdel -f username
   
   # Before deleting, check user's processes
   ps -u username
   sudo pkill -u username    # Kill all user's processes

1.4 Viewing User Information
-----------------------------

.. code-block:: bash

   # Show user information
   id username
   # Output: uid=1001(username) gid=1001(username) groups=1001(username),27(sudo)
   
   # Show current user
   whoami
   id
   
   # List all users
   cat /etc/passwd
   getent passwd
   
   # List only real users (UID >= 1000)
   awk -F: '$3 >= 1000 {print $1}' /etc/passwd
   
   # Show user's groups
   groups username
   id -Gn username
   
   # Show user's home directory
   getent passwd username | cut -d: -f6
   
   # Show user's shell
   getent passwd username | cut -d: -f7
   
   # Show currently logged in users
   who
   w
   users
   
   # Show last logins
   last
   last username
   lastlog
   lastlog -u username

================================================================================
2. Group Management
================================================================================

2.1 Creating Groups
-------------------

.. code-block:: bash

   # Create group
   sudo groupadd groupname
   
   # Create group with specific GID
   sudo groupadd -g 5000 groupname
   
   # Create system group
   sudo groupadd -r systemgroup

2.2 Modifying Groups
--------------------

.. code-block:: bash

   # Add user to group
   sudo usermod -aG groupname username
   sudo gpasswd -a username groupname     # Alternative method
   
   # Remove user from group
   sudo gpasswd -d username groupname
   
   # Change group name
   sudo groupmod -n newname oldname
   
   # Change group GID
   sudo groupmod -g 6000 groupname
   
   # Set group password (rarely used)
   sudo gpasswd groupname
   
   # Set group administrators
   sudo gpasswd -A admin1,admin2 groupname

2.3 Deleting Groups
-------------------

.. code-block:: bash

   # Delete group
   sudo groupdel groupname
   
   # Find files owned by group before deleting
   sudo find / -group groupname

2.4 Viewing Group Information
------------------------------

.. code-block:: bash

   # List all groups
   cat /etc/group
   getent group
   
   # Show group members
   getent group groupname
   grep ^groupname: /etc/group
   
   # Show all members of a group
   members groupname          # If 'members' package installed
   lid -g groupname           # Alternative
   
   # Show user's groups
   groups username
   id username

================================================================================
3. Password Policies and Aging
================================================================================

3.1 Password Aging Configuration
---------------------------------

**/etc/login.defs Configuration:**

.. code-block:: bash

   # Edit system-wide password aging defaults
   sudo nano /etc/login.defs
   
   # Key settings:
   PASS_MAX_DAYS   90      # Maximum password age in days
   PASS_MIN_DAYS   7       # Minimum days between password changes
   PASS_WARN_AGE   14      # Warning days before password expires
   PASS_MIN_LEN    12      # Minimum password length
   
   # UID/GID ranges
   UID_MIN         1000    # Minimum UID for regular users
   UID_MAX         60000   # Maximum UID for regular users
   GID_MIN         1000    # Minimum GID for regular groups
   GID_MAX         60000   # Maximum GID for regular groups
   
   # System accounts
   SYS_UID_MIN     100
   SYS_UID_MAX     999
   
   # Home directory permissions
   UMASK           077     # Restrictive umask for new users
   
   # Password hashing algorithm
   ENCRYPT_METHOD  SHA512

**chage Command - Per-User Password Aging:**

.. code-block:: bash

   # View password aging information
   sudo chage -l username
   
   # Set password expiry (90 days)
   sudo chage -M 90 username
   
   # Set minimum days between password changes
   sudo chage -m 7 username
   
   # Set warning days before expiry
   sudo chage -W 14 username
   
   # Set account expiry date
   sudo chage -E 2026-12-31 username
   
   # Remove account expiry
   sudo chage -E -1 username
   
   # Set inactive days (account locked N days after password expires)
   sudo chage -I 30 username
   
   # Force password change on next login
   sudo chage -d 0 username
   
   # Set last password change date
   sudo chage -d 2026-01-01 username
   
   # Interactive mode
   sudo chage username

**Example Password Aging Policy:**

.. code-block:: bash

   # Corporate password policy: 
   # - 90 day expiry
   # - 7 day minimum between changes
   # - 14 day warning
   # - 30 day inactive period
   
   sudo chage -M 90 -m 7 -W 14 -I 30 username
   
   # Check settings
   sudo chage -l username

3.2 Password Complexity Requirements
-------------------------------------

**PAM Configuration (pam_pwquality):**

.. code-block:: bash

   # Install password quality library
   sudo apt install libpam-pwquality     # Debian/Ubuntu
   sudo yum install libpwquality         # RHEL/CentOS
   
   # Edit PAM password configuration
   sudo nano /etc/pam.d/common-password  # Debian/Ubuntu
   sudo nano /etc/pam.d/system-auth      # RHEL/CentOS
   
   # Add/modify this line:
   password requisite pam_pwquality.so retry=3 minlen=12 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1
   
   # Parameters explained:
   # retry=3        - 3 attempts to set password
   # minlen=12      - Minimum 12 characters
   # difok=3        - At least 3 different characters from old password
   # ucredit=-1     - Require at least 1 uppercase letter
   # lcredit=-1     - Require at least 1 lowercase letter
   # dcredit=-1     - Require at least 1 digit
   # ocredit=-1     - Require at least 1 special character
   # maxrepeat=3    - Maximum 3 consecutive identical characters
   # maxclassrepeat=4 - Maximum 4 consecutive characters from same class

**Alternative Configuration File:**

.. code-block:: bash

   # Edit pwquality configuration file
   sudo nano /etc/security/pwquality.conf
   
   # Settings:
   minlen = 12
   minclass = 4
   maxrepeat = 3
   maxclassrepeat = 4
   lcredit = -1
   ucredit = -1
   dcredit = -1
   ocredit = -1
   difok = 3
   gecoscheck = 1        # Check password against GECOS field
   dictcheck = 1         # Check against dictionary
   usercheck = 1         # Check if contains username
   enforcing = 1         # Enforce for root as well

**Password History:**

.. code-block:: bash

   # Prevent password reuse
   sudo nano /etc/pam.d/common-password
   
   # Add to password line:
   password required pam_pwhistory.so remember=5 use_authtok
   
   # This prevents reusing last 5 passwords

3.3 Account Lockout Policy
---------------------------

**pam_faillock (Modern Method):**

.. code-block:: bash

   # Edit auth configuration
   sudo nano /etc/pam.d/common-auth      # Debian/Ubuntu
   sudo nano /etc/pam.d/system-auth      # RHEL/CentOS
   
   # Add these lines (order matters):
   auth required pam_faillock.so preauth audit silent deny=5 unlock_time=900
   auth [default=die] pam_faillock.so authfail audit deny=5 unlock_time=900
   account required pam_faillock.so
   
   # Parameters:
   # deny=5         - Lock after 5 failed attempts
   # unlock_time=900 - Unlock after 900 seconds (15 minutes)
   # audit          - Log to audit system
   # silent         - Don't show failure count to user

**Check Failed Login Attempts:**

.. code-block:: bash

   # View failed attempts
   sudo faillock
   sudo faillock --user username
   
   # Reset failed attempts for user
   sudo faillock --user username --reset
   
   # Reset all failed attempts
   sudo faillock --reset

**pam_tally2 (Legacy Method):**

.. code-block:: bash

   # View failed login attempts
   sudo pam_tally2 --user=username
   
   # Reset counter for user
   sudo pam_tally2 --user=username --reset
   
   # Reset all counters
   sudo pam_tally2 --reset

================================================================================
4. sudo Configuration
================================================================================

4.1 sudo Basics
---------------

**Add User to sudo Group:**

.. code-block:: bash

   # Debian/Ubuntu
   sudo usermod -aG sudo username
   
   # RHEL/CentOS/Fedora
   sudo usermod -aG wheel username
   
   # Verify group membership
   groups username
   id username

**Edit sudoers File:**

.. code-block:: bash

   # ALWAYS use visudo (checks syntax before saving)
   sudo visudo
   
   # Never edit directly:
   # sudo nano /etc/sudoers  # DON'T DO THIS!

4.2 sudoers File Syntax
------------------------

**Basic Syntax:**

.. code-block:: text

   user    host=(runas) command
   
   Examples:
   john    ALL=(ALL:ALL) ALL
   ^user   ^host ^runas  ^command
   
   john    ALL=(ALL:ALL) ALL
   # User 'john' on ALL hosts can run ALL commands as ALL users

**Group Syntax:**

.. code-block:: text

   %groupname  ALL=(ALL:ALL) ALL
   
   # % prefix indicates a group
   %sudo       ALL=(ALL:ALL) ALL
   %wheel      ALL=(ALL:ALL) ALL

4.3 sudo Examples and Use Cases
--------------------------------

**Grant Full sudo Access:**

.. code-block:: bash

   # In sudoers file:
   john    ALL=(ALL:ALL) ALL
   
   # Or add to sudo/wheel group:
   sudo usermod -aG sudo john

**Grant sudo Without Password:**

.. code-block:: bash

   # In sudoers file:
   john    ALL=(ALL:ALL) NOPASSWD: ALL
   
   # For group:
   %developers ALL=(ALL:ALL) NOPASSWD: ALL
   
   # WARNING: Security risk - use sparingly

**Grant Specific Commands Only:**

.. code-block:: bash

   # Allow only systemctl restart for apache2
   john    ALL=(ALL) /bin/systemctl restart apache2
   
   # Multiple commands
   john    ALL=(ALL) /bin/systemctl restart apache2, /bin/systemctl status apache2
   
   # Allow all systemctl commands
   john    ALL=(ALL) /bin/systemctl *
   
   # Database admin can restart mysql
   %dba    ALL=(ALL) /bin/systemctl restart mysql, /bin/systemctl status mysql

**Command Aliases:**

.. code-block:: bash

   # Define command aliases at top of sudoers file
   Cmnd_Alias NETWORKING = /sbin/route, /sbin/ifconfig, /bin/ping
   Cmnd_Alias SOFTWARE = /bin/rpm, /usr/bin/yum, /usr/bin/apt
   Cmnd_Alias SERVICES = /bin/systemctl start, /bin/systemctl stop, /bin/systemctl restart
   Cmnd_Alias PROCESSES = /bin/kill, /usr/bin/killall
   
   # Use aliases
   john    ALL = NETWORKING, SOFTWARE
   %operators ALL = SERVICES
   %developers ALL = PROCESSES

**User Aliases:**

.. code-block:: bash

   # Define user aliases
   User_Alias ADMINS = john, jane, bob
   User_Alias WEBMASTERS = alice, charlie
   
   # Use aliases
   ADMINS      ALL=(ALL:ALL) ALL
   WEBMASTERS  ALL=(ALL) /bin/systemctl restart apache2

**Host Aliases:**

.. code-block:: bash

   # Define host aliases
   Host_Alias WEBSERVERS = web1, web2, web3
   Host_Alias DBSERVERS = db1, db2
   
   # Use aliases
   john    WEBSERVERS = /bin/systemctl restart apache2
   jane    DBSERVERS = /bin/systemctl restart mysql

**Runas Aliases:**

.. code-block:: bash

   # Define runas aliases
   Runas_Alias OP = root, operator
   Runas_Alias DB = postgres, mysql
   
   # Use aliases
   john    ALL = (OP) ALL
   jane    ALL = (DB) /usr/bin/psql

**Prevent Specific Commands:**

.. code-block:: bash

   # Allow all commands EXCEPT shell access
   john    ALL=(ALL) ALL, !/bin/bash, !/bin/sh, !/bin/zsh
   
   # Allow systemctl but not stop for critical service
   john    ALL=(ALL) /bin/systemctl, !/bin/systemctl stop critical-service

4.4 sudo Security Best Practices
---------------------------------

**Require Password After Timeout:**

.. code-block:: bash

   # In sudoers file (default is 15 minutes)
   Defaults    timestamp_timeout=5    # 5 minutes
   Defaults    timestamp_timeout=0    # Always require password
   Defaults    timestamp_timeout=-1   # Never timeout (INSECURE)

**Log sudo Commands:**

.. code-block:: bash

   # Enable logging
   Defaults    logfile="/var/log/sudo.log"
   Defaults    log_year, log_host, loglinelen=0
   
   # Send to syslog
   Defaults    syslog=auth
   
   # Log command input/output
   Defaults    log_input, log_output
   Defaults    iolog_dir="/var/log/sudo-io"

**Additional Security Options:**

.. code-block:: bash

   # Require TTY (prevents some attacks)
   Defaults    requiretty
   
   # Use secure path
   Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
   
   # Set environment variables
   Defaults    env_reset
   Defaults    env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS"
   
   # Mail on sudo violations
   Defaults    mailto="admin@example.com"
   Defaults    mail_badpass
   Defaults    mail_no_user

**Example Secure sudoers Configuration:**

.. code-block:: bash

   # /etc/sudoers.d/custom-sudo (create separate file)
   
   # Security settings
   Defaults    env_reset
   Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
   Defaults    timestamp_timeout=5
   Defaults    logfile="/var/log/sudo.log"
   Defaults    log_year, log_host
   
   # Command aliases
   Cmnd_Alias APACHE = /bin/systemctl restart apache2, /bin/systemctl reload apache2, /bin/systemctl status apache2
   Cmnd_Alias MYSQL = /bin/systemctl restart mysql, /bin/systemctl status mysql
   Cmnd_Alias LOGS = /bin/journalctl, /bin/tail, /bin/less, /bin/grep
   
   # User aliases
   User_Alias WEBADMINS = alice, bob
   User_Alias DBADMINS = charlie, dave
   
   # Permissions
   WEBADMINS   ALL = APACHE, LOGS
   DBADMINS    ALL = MYSQL, LOGS
   
   # Senior admins get full access
   john        ALL=(ALL:ALL) ALL

================================================================================
5. PAM (Pluggable Authentication Modules)
================================================================================

5.1 PAM Basics
--------------

**PAM Configuration Files:**

.. code-block:: text

   /etc/pam.d/              - PAM configuration directory
   /etc/pam.d/common-*      - Common configurations (Debian/Ubuntu)
   /etc/pam.d/system-auth   - System authentication (RHEL/CentOS)
   /etc/security/           - PAM module configurations

**PAM Module Types:**

.. code-block:: text

   auth      - Authentication (verify identity)
   account   - Account management (access control, expiry)
   password  - Password management (password changes)
   session   - Session management (setup/cleanup)

**Control Flags:**

.. code-block:: text

   required    - Must succeed, continue processing
   requisite   - Must succeed, stop if fails
   sufficient  - Success skips remaining modules
   optional    - Result doesn't matter
   include     - Include another PAM file

5.2 Common PAM Configurations
------------------------------

**Limit Login Attempts (pam_faillock):**

.. code-block:: bash

   # /etc/pam.d/common-auth (Debian/Ubuntu)
   auth    required        pam_faillock.so preauth audit deny=5 unlock_time=900
   auth    [success=1 default=bad] pam_unix.so nullok
   auth    [default=die]   pam_faillock.so authfail audit deny=5
   auth    sufficient      pam_faillock.so authsucc
   account required        pam_faillock.so

**Password Quality (pam_pwquality):**

.. code-block:: bash

   # /etc/pam.d/common-password
   password requisite pam_pwquality.so retry=3 minlen=12 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1

**Time-Based Access Control (pam_time):**

.. code-block:: bash

   # /etc/pam.d/sshd
   account required pam_time.so
   
   # /etc/security/time.conf
   # Allow login Monday-Friday 8am-6pm only
   *;*;username;MoTuWeThFr0800-1800

**Resource Limits (pam_limits):**

.. code-block:: bash

   # /etc/pam.d/common-session
   session required pam_limits.so
   
   # /etc/security/limits.conf
   # Limit processes for user
   username    soft    nproc    100
   username    hard    nproc    200
   
   # Limit open files
   username    soft    nofile   1024
   username    hard    nofile   2048
   
   # Limit memory (KB)
   username    hard    as       1000000

**Access Control (pam_access):**

.. code-block:: bash

   # /etc/pam.d/sshd
   account required pam_access.so
   
   # /etc/security/access.conf
   # Allow admin from specific IPs
   + : admin : 192.168.1.0/24
   
   # Deny all other access
   - : ALL : ALL

================================================================================
6. Root Account Protection
================================================================================

6.1 Disable Root Login
-----------------------

**Disable Root SSH Login:**

.. code-block:: bash

   # Edit SSH configuration
   sudo nano /etc/ssh/sshd_config
   
   # Set:
   PermitRootLogin no
   
   # Restart SSH
   sudo systemctl restart sshd

**Disable Root Console Login:**

.. code-block:: bash

   # Lock root account
   sudo passwd -l root
   
   # Verify
   sudo passwd -S root

**Allow Root Only from Console (Physical Access):**

.. code-block:: bash

   # Edit securetty
   sudo nano /etc/securetty
   
   # List only physical consoles:
   tty1
   tty2
   # Remove pts/* entries

6.2 sudo Instead of Root
-------------------------

**Best Practices:**

.. code-block:: bash

   # Use sudo for single commands
   sudo command
   
   # Use sudo -i for interactive root shell (better logging)
   sudo -i
   
   # Avoid: sudo su -  (bypasses sudo logging)
   
   # Use sudo -E to preserve environment
   sudo -E command
   
   # Run command as specific user
   sudo -u username command

================================================================================
7. Account Monitoring and Auditing
================================================================================

7.1 Login Monitoring
--------------------

.. code-block:: bash

   # View login history
   last | head -20
   
   # View failed login attempts
   sudo lastb | head -20
   
   # Check last login for all users
   lastlog
   
   # Check currently logged in users
   who
   w
   users
   
   # View user's recent commands (if history enabled)
   sudo cat /home/username/.bash_history

7.2 Automated Monitoring Scripts
---------------------------------

**Monitor Failed Logins:**

.. code-block:: bash

   #!/bin/bash
   # /usr/local/bin/check-failed-logins.sh
   
   THRESHOLD=5
   EMAIL="admin@example.com"
   
   FAILED=$(lastb | wc -l)
   
   if [ $FAILED -gt $THRESHOLD ]; then
       echo "WARNING: $FAILED failed login attempts detected" | \
       mail -s "Security Alert: Failed Logins" $EMAIL
   fi
   
   # Add to crontab to run hourly:
   # 0 * * * * /usr/local/bin/check-failed-logins.sh

**Monitor New Users:**

.. code-block:: bash

   #!/bin/bash
   # /usr/local/bin/check-new-users.sh
   
   BASELINE="/var/log/user-baseline.txt"
   CURRENT="/tmp/current-users.txt"
   
   awk -F: '$3 >= 1000 {print $1}' /etc/passwd | sort > $CURRENT
   
   if [ -f $BASELINE ]; then
       DIFF=$(diff $BASELINE $CURRENT)
       if [ -n "$DIFF" ]; then
           echo "New users detected: $DIFF" | \
           mail -s "Security Alert: New Users" admin@example.com
       fi
   fi
   
   cp $CURRENT $BASELINE

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- Linux_Security_Basics.rst - Overall security principles
- SSH_Hardening.rst - SSH-specific user authentication
- File_Permissions_DAC.rst - File ownership and permissions
- SELinux_Security.rst - Mandatory access control for users
- Logging_Log_Security.rst - User activity logging

================================================================================
END OF USER ACCOUNT SECURITY
================================================================================
