================================================================================
Embedded Linux: Security & Hardening - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch13-14)
:Target: Secure Boot, Encryption, System Hardening
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Secure Boot (U-Boot):**

.. code-block:: bash

   # Generate keys
   openssl genrsa -out keys/dev.key 2048
   openssl req -new -x509 -key keys/dev.key -out keys/dev.crt
   
   # Sign FIT image
   mkimage -f kernel.its -k keys -K u-boot.dtb -r kernel.itb
   
   # U-Boot config
   CONFIG_FIT_SIGNATURE=y
   CONFIG_RSA=y

**dm-crypt Encryption:**

.. code-block:: bash

   # Setup encrypted partition
   cryptsetup luksFormat /dev/mmcblk0p2
   cryptsetup luksOpen /dev/mmcblk0p2 cryptroot
   mkfs.ext4 /dev/mapper/cryptroot
   
   # Mount
   cryptsetup luksOpen /dev/mmcblk0p2 cryptroot
   mount /dev/mapper/cryptroot /mnt

**SELinux:**

.. code-block:: bash

   # Status
   sestatus
   getenforce
   
   # Set mode
   setenforce 0  # Permissive
   setenforce 1  # Enforcing
   
   # Context
   ls -Z /path/to/file
   chcon -t httpd_sys_content_t /var/www/html/index.html

**System Hardening:**

.. code-block:: bash

   # Disable root login
   passwd -l root
   
   # Firewall
   iptables -P INPUT DROP
   iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Remove SUID
   find / -perm -4000 -exec chmod u-s {} \;

================================================================================
1. Secure Boot
================================================================================

1.1 Secure Boot Chain
----------------------

**Boot Process:**

.. code-block:: text

   1. ROM Code (immutable)
      ↓ Verifies
   2. Bootloader (U-Boot)
      ↓ Verifies
   3. Kernel + DTB
      ↓ Verifies
   4. Root Filesystem
      ↓ Verifies (optional)
   5. Applications

**Goals:**

.. code-block:: text

   ✓ Prevent unauthorized code execution
   ✓ Detect tampering
   ✓ Ensure trusted boot chain
   ✓ Protect firmware updates
   ✓ Secure key storage

1.2 U-Boot Secure Boot (FIT)
-----------------------------

**Generate Keys:**

.. code-block:: bash

   # Create key directory
   mkdir -p keys
   
   # Generate RSA key pair
   openssl genrsa -F4 -out keys/dev.key 2048
   openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt
   
   # Generate production key (store securely!)
   openssl genrsa -F4 -out keys/prod.key 4096
   openssl req -batch -new -x509 -key keys/prod.key -out keys/prod.crt

**Create FIT Image:**

.. code-block:: dts

   /dts-v1/;
   
   / {
       description = "Signed kernel image";
       #address-cells = <1>;
       
       images {
           kernel@1 {
               description = "Linux kernel";
               data = /incbin/("zImage");
               type = "kernel";
               arch = "arm";
               os = "linux";
               compression = "none";
               load = <0x80008000>;
               entry = <0x80008000>;
               hash@1 {
                   algo = "sha256";
               };
           };
           
           fdt@1 {
               description = "Device tree";
               data = /incbin/("imx6q-wandboard.dtb");
               type = "flat_dt";
               arch = "arm";
               compression = "none";
               hash@1 {
                   algo = "sha256";
               };
           };
       };
       
       configurations {
           default = "conf@1";
           conf@1 {
               description = "Boot Linux kernel with FDT";
               kernel = "kernel@1";
               fdt = "fdt@1";
               signature@1 {
                   algo = "sha256,rsa2048";
                   key-name-hint = "dev";
                   sign-images = "fdt", "kernel";
               };
           };
       };
   };

**Sign and Boot:**

.. code-block:: bash

   # Build U-Boot with signature support
   CONFIG_FIT_SIGNATURE=y
   CONFIG_RSA=y
   CONFIG_OF_CONTROL=y
   CONFIG_OF_SEPARATE=y
   
   # Sign FIT image
   mkimage -f kernel.its -k keys -K u-boot.dtb -r kernel.itb
   
   # U-Boot commands
   => load mmc 0:1 ${loadaddr} kernel.itb
   => bootm ${loadaddr}
   # Signature verified automatically

1.3 Kernel Signature Verification
----------------------------------

**Kernel Module Signing:**

.. code-block:: bash

   # Kernel config
   CONFIG_MODULE_SIG=y
   CONFIG_MODULE_SIG_FORCE=y  # Reject unsigned modules
   CONFIG_MODULE_SIG_ALL=y    # Auto-sign all modules
   CONFIG_MODULE_SIG_SHA256=y
   
   # Keys generated during build
   # Or use custom key:
   CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"
   
   # Sign module manually
   scripts/sign-file sha256 certs/signing_key.pem \
       certs/signing_key.x509 module.ko

**IMA (Integrity Measurement Architecture):**

.. code-block:: bash

   # Kernel config
   CONFIG_IMA=y
   CONFIG_IMA_APPRAISE=y
   
   # Boot parameter
   ima_policy=tcb ima_appraise=enforce
   
   # Sign binaries
   evmctl sign -a sha256 --key /etc/keys/privkey.pem /bin/myapp

================================================================================
2. Encryption
================================================================================

2.1 Disk Encryption (dm-crypt/LUKS)
------------------------------------

**Setup:**

.. code-block:: bash

   # Install cryptsetup
   apt-get install cryptsetup
   
   # Format partition
   cryptsetup luksFormat /dev/mmcblk0p2
   # Enter passphrase
   
   # Open encrypted device
   cryptsetup luksOpen /dev/mmcblk0p2 cryptroot
   
   # Create filesystem
   mkfs.ext4 /dev/mapper/cryptroot
   
   # Mount
   mount /dev/mapper/cryptroot /mnt
   
   # Unmount and close
   umount /mnt
   cryptsetup luksClose cryptroot

**Automated Unlock:**

.. code-block:: bash

   # /etc/crypttab
   cryptroot /dev/mmcblk0p2 none luks
   
   # With key file (stored on separate device)
   cryptroot /dev/mmcblk0p2 /etc/keys/root.key luks
   
   # /etc/fstab
   /dev/mapper/cryptroot / ext4 defaults 0 1
   
   # Generate key file
   dd if=/dev/urandom of=/etc/keys/root.key bs=512 count=4
   chmod 400 /etc/keys/root.key
   cryptsetup luksAddKey /dev/mmcblk0p2 /etc/keys/root.key

**Performance:**

.. code-block:: bash

   # Benchmark
   cryptsetup benchmark
   
   # Use hardware acceleration (if available)
   CONFIG_CRYPTO_DEV_FSL_CAAM=y  # Freescale CAAM
   CONFIG_CRYPTO_AES_ARM_CE=y    # ARM Crypto Extensions

2.2 File Encryption
-------------------

**eCryptfs:**

.. code-block:: bash

   # Mount encrypted directory
   mount -t ecryptfs /home/user/Private /home/user/Private
   
   # Options: aes, key size, passphrase

**EncFS:**

.. code-block:: bash

   # Create encrypted filesystem
   encfs ~/.encrypted ~/Private
   
   # Mount
   encfs ~/.encrypted ~/Private
   
   # Unmount
   fusermount -u ~/Private

2.3 TPM (Trusted Platform Module)
----------------------------------

**TPM Usage:**

.. code-block:: bash

   # Kernel config
   CONFIG_TCG_TPM=y
   CONFIG_TCG_TIS=y
   
   # Install tools
   apt-get install tpm2-tools
   
   # Seal data to TPM
   tpm2_createprimary -C o -g sha256 -G rsa -c primary.ctx
   tpm2_create -C primary.ctx -g sha256 -G aes -r seal.priv \
       -u seal.pub -i secret.txt
   
   # Unseal
   tpm2_load -C primary.ctx -r seal.priv -u seal.pub -c seal.ctx
   tpm2_unseal -c seal.ctx -o unsealed.txt

================================================================================
3. Access Control
================================================================================

3.1 SELinux
-----------

**Basic Configuration:**

.. code-block:: bash

   # Kernel config
   CONFIG_SECURITY_SELINUX=y
   CONFIG_SECURITY_SELINUX_BOOTPARAM=y
   CONFIG_DEFAULT_SECURITY_SELINUX=y
   
   # Boot parameter
   security=selinux selinux=1
   
   # Status
   sestatus
   getenforce
   
   # Modes
   setenforce 0  # Permissive (log only)
   setenforce 1  # Enforcing
   
   # Permanent mode (/etc/selinux/config)
   SELINUX=enforcing
   SELINUXTYPE=targeted

**SELinux Context:**

.. code-block:: bash

   # View context
   ls -Z /path/to/file
   ps -eZ
   id -Z
   
   # Change context
   chcon -t httpd_sys_content_t /var/www/html/index.html
   
   # Restore default context
   restorecon -v /var/www/html/index.html
   restorecon -Rv /var/www/html/
   
   # Make permanent
   semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"
   restorecon -Rv /web

**Troubleshooting:**

.. code-block:: bash

   # View denials
   ausearch -m avc -ts recent
   grep "avc:.*denied" /var/log/audit/audit.log
   
   # Generate policy
   audit2allow -a
   audit2allow -a -M mypolicy
   semodule -i mypolicy.pp
   
   # Allow specific action
   setsebool -P httpd_can_network_connect 1

3.2 AppArmor
------------

**Configuration:**

.. code-block:: bash

   # Kernel config
   CONFIG_SECURITY_APPARMOR=y
   
   # Install
   apt-get install apparmor apparmor-utils
   
   # Status
   aa-status
   
   # Profiles location
   /etc/apparmor.d/
   
   # Modes
   aa-enforce /etc/apparmor.d/usr.bin.myapp    # Enforce
   aa-complain /etc/apparmor.d/usr.bin.myapp   # Complain
   aa-disable /etc/apparmor.d/usr.bin.myapp    # Disable

**Create Profile:**

.. code-block:: bash

   # Generate profile
   aa-genprof /usr/bin/myapp
   
   # Example profile
   #include <tunables/global>
   
   /usr/bin/myapp {
       #include <abstractions/base>
       
       /usr/bin/myapp mr,
       /etc/myapp/* r,
       /var/lib/myapp/** rw,
       /tmp/** rw,
       
       capability net_bind_service,
       
       network inet tcp,
   }

3.3 Capabilities
----------------

**Linux Capabilities:**

.. code-block:: bash

   # View capabilities
   getcap /usr/bin/myapp
   getpcaps <pid>
   
   # Set capabilities
   setcap cap_net_bind_service=+ep /usr/bin/myapp
   
   # Remove SUID, grant capability
   chmod u-s /usr/bin/ping
   setcap cap_net_raw+ep /usr/bin/ping
   
   # Drop capabilities in code
   #include <sys/capability.h>
   cap_t caps = cap_get_proc();
   cap_set_flag(caps, CAP_EFFECTIVE, 1, &cap, CAP_CLEAR);
   cap_set_proc(caps);

================================================================================
4. Network Security
================================================================================

4.1 Firewall (iptables)
------------------------

**Basic Rules:**

.. code-block:: bash

   # Default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Allow established connections
   iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
   
   # Allow loopback
   iptables -A INPUT -i lo -j ACCEPT
   
   # Allow SSH
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Allow HTTP/HTTPS
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   iptables -A INPUT -p tcp --dport 443 -j ACCEPT
   
   # Save rules
   iptables-save > /etc/iptables.rules
   
   # Restore rules
   iptables-restore < /etc/iptables.rules

**Rate Limiting:**

.. code-block:: bash

   # Limit SSH connections
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
       -m recent --set --name SSH
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
       -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

4.2 SSH Hardening
-----------------

.. code-block:: bash

   # /etc/ssh/sshd_config
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   AllowUsers user1 user2
   Protocol 2
   Port 22222  # Non-standard port
   ClientAliveInterval 300
   ClientAliveCountMax 2
   
   # Key-based authentication only
   ssh-keygen -t ed25519 -C "user@host"
   ssh-copy-id -i ~/.ssh/id_ed25519.pub user@target
   
   # Restart SSH
   systemctl restart sshd

4.3 SSL/TLS
-----------

.. code-block:: bash

   # Generate self-signed certificate
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout server.key -out server.crt
   
   # Generate CSR for CA
   openssl req -new -key server.key -out server.csr
   
   # Test SSL connection
   openssl s_client -connect example.com:443

================================================================================
5. System Hardening
================================================================================

5.1 User and Access Control
----------------------------

.. code-block:: bash

   # Disable root login
   passwd -l root
   
   # Remove unnecessary users
   userdel -r games
   
   # Password policies (/etc/login.defs)
   PASS_MAX_DAYS 90
   PASS_MIN_DAYS 1
   PASS_MIN_LEN 12
   PASS_WARN_AGE 7
   
   # Enforce password quality
   apt-get install libpam-pwquality
   # /etc/pam.d/common-password
   password requisite pam_pwquality.so retry=3 minlen=12 difok=3

5.2 Remove Unnecessary Services
--------------------------------

.. code-block:: bash

   # List services
   systemctl list-unit-files --type=service
   
   # Disable unnecessary services
   systemctl disable bluetooth
   systemctl disable cups
   systemctl mask bluetooth  # Prevent manual start
   
   # BusyBox init
   chmod -x /etc/init.d/S50telnet
   rm /etc/init.d/S50telnet

5.3 File System Hardening
--------------------------

.. code-block:: bash

   # /etc/fstab - mount options
   /dev/mmcblk0p1 /boot ext4 defaults,ro 0 2
   /dev/mmcblk0p2 / ext4 defaults,nodev 0 1
   tmpfs /tmp tmpfs defaults,nodev,nosuid,noexec 0 0
   tmpfs /var/tmp tmpfs defaults,nodev,nosuid,noexec 0 0
   
   # Remove SUID/SGID
   find / -perm -4000 -exec chmod u-s {} \;
   find / -perm -2000 -exec chmod g-s {} \;
   
   # Protect sensitive files
   chmod 600 /boot/grub/grub.cfg
   chmod 600 /etc/ssh/sshd_config
   chmod 400 /etc/shadow
   
   # Immutable files
   chattr +i /etc/passwd
   chattr +i /etc/shadow

5.4 Kernel Hardening
---------------------

.. code-block:: bash

   # /etc/sysctl.conf or /etc/sysctl.d/hardening.conf
   
   # Disable IP forwarding
   net.ipv4.ip_forward = 0
   
   # Ignore ICMP redirects
   net.ipv4.conf.all.accept_redirects = 0
   net.ipv6.conf.all.accept_redirects = 0
   
   # Ignore source routes
   net.ipv4.conf.all.accept_source_route = 0
   net.ipv6.conf.all.accept_source_route = 0
   
   # SYN flood protection
   net.ipv4.tcp_syncookies = 1
   net.ipv4.tcp_max_syn_backlog = 2048
   
   # Prevent address spoofing
   net.ipv4.conf.all.rp_filter = 1
   
   # Ignore ICMP ping
   net.ipv4.icmp_echo_ignore_all = 1
   
   # Kernel address space randomization
   kernel.randomize_va_space = 2
   
   # Restrict dmesg
   kernel.dmesg_restrict = 1
   
   # Apply settings
   sysctl -p

================================================================================
6. Secure Updates
================================================================================

6.1 OTA Update Security
------------------------

**Signed Updates:**

.. code-block:: bash

   # Sign update package
   openssl dgst -sha256 -sign private.key -out update.sig update.img
   
   # Verify signature
   openssl dgst -sha256 -verify public.key -signature update.sig update.img
   
   # A/B partition for atomic updates
   # Fallback to previous version if update fails

**Update Process:**

.. code-block:: text

   1. Download update package (HTTPS)
   2. Verify signature
   3. Verify checksum
   4. Apply update to inactive partition
   5. Set boot flag
   6. Reboot
   7. Verify boot success
   8. Commit or rollback

6.2 SWUpdate
------------

.. code-block:: bash

   # SWUpdate framework
   # .swu file with signed metadata
   
   # sw-description
   software = {
       version = "1.0.0";
       images: ({
           filename = "rootfs.ext4";
           device = "/dev/mmcblk0p2";
           sha256 = "abc123...";
       });
   };
   
   # Signature verification
   CONFIG_SIGNED_IMAGES=y
   CONFIG_SIGALG_RSA=y

================================================================================
7. Key Takeaways
================================================================================

.. code-block:: text

   Secure Boot:
   ============
   U-Boot FIT signature verification
   Kernel module signing
   IMA/EVM for runtime integrity
   
   Encryption:
   ===========
   LUKS disk encryption
   dm-crypt for partitions
   TPM for key storage
   
   Access Control:
   ===============
   SELinux or AppArmor
   Capabilities instead of SUID
   Minimal user privileges
   
   Network Security:
   =================
   iptables firewall (default DROP)
   SSH hardening (key-only, non-standard port)
   Disable unnecessary services
   
   System Hardening:
   =================
   Remove SUID binaries
   Read-only root filesystem
   Kernel hardening (sysctl)
   Secure mount options (nodev, nosuid, noexec)
   
   Updates:
   ========
   Signed update packages
   A/B partitions
   Rollback capability
   HTTPS delivery

================================================================================
END OF CHEATSHEET
================================================================================
