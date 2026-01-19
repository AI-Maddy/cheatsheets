================================================================================
ENCRYPTION TECHNOLOGIES
================================================================================

**Complete Guide to Linux Encryption: LUKS, GPG, TLS/SSL, and Encrypted Filesystems**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 5

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # LUKS Disk Encryption
   sudo cryptsetup luksFormat /dev/sdb1           # Create encrypted partition
   sudo cryptsetup open /dev/sdb1 encrypted_disk  # Open encrypted partition
   sudo mkfs.ext4 /dev/mapper/encrypted_disk      # Format
   sudo mount /dev/mapper/encrypted_disk /mnt     # Mount
   
   # GPG Encryption
   gpg --gen-key                                  # Generate GPG key
   gpg --encrypt --recipient user@email file.txt  # Encrypt file
   gpg --decrypt file.txt.gpg > file.txt          # Decrypt file
   gpg --list-keys                                # List public keys
   
   # OpenSSL File Encryption
   openssl enc -aes-256-cbc -salt -in file.txt -out file.enc  # Encrypt
   openssl enc -aes-256-cbc -d -in file.enc -out file.txt     # Decrypt
   
   # Generate SSL Certificate
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

================================================================================
PART 1: LUKS (Linux Unified Key Setup)
================================================================================

1. LUKS Fundamentals
====================

1.1 What is LUKS?
-----------------

**LUKS** provides:
- Full disk encryption
- Multiple key slots (up to 8 users)
- Secure key management
- Protection against data theft
- Transparent encryption/decryption

**Use Cases:**
- Laptop hard drives
- External USB drives
- Cloud storage
- Backup drives
- Sensitive data partitions

1.2 Installation
----------------

.. code-block:: bash

   # Install cryptsetup
   sudo apt install cryptsetup                    # Debian/Ubuntu
   sudo dnf install cryptsetup                    # RHEL/CentOS/Fedora
   
   # Check version
   cryptsetup --version

================================================================================
2. LUKS Disk Encryption
================================================================================

2.1 Create Encrypted Partition
-------------------------------

.. code-block:: bash

   # WARNING: This will DESTROY all data on the partition!
   
   # Create LUKS container
   sudo cryptsetup luksFormat /dev/sdb1
   # Enter passphrase when prompted
   
   # Verify LUKS header
   sudo cryptsetup luksDump /dev/sdb1
   
   # Open encrypted partition
   sudo cryptsetup open /dev/sdb1 encrypted_disk
   # Or: sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk
   
   # Create filesystem
   sudo mkfs.ext4 /dev/mapper/encrypted_disk
   
   # Mount
   sudo mkdir /mnt/encrypted
   sudo mount /dev/mapper/encrypted_disk /mnt/encrypted
   
   # Use normally
   sudo chown $USER:$USER /mnt/encrypted
   
   # Unmount when done
   sudo umount /mnt/encrypted
   sudo cryptsetup close encrypted_disk

2.2 Advanced LUKS Options
--------------------------

.. code-block:: bash

   # Specify encryption algorithm and key size
   sudo cryptsetup luksFormat /dev/sdb1 \
       --cipher aes-xts-plain64 \
       --key-size 512 \
       --hash sha512 \
       --iter-time 5000
   
   # Use key file instead of passphrase
   dd if=/dev/urandom of=/root/keyfile bs=1024 count=4
   chmod 600 /root/keyfile
   sudo cryptsetup luksFormat /dev/sdb1 /root/keyfile
   
   # Open with key file
   sudo cryptsetup open /dev/sdb1 encrypted_disk --key-file /root/keyfile

2.3 Key Management
------------------

.. code-block:: bash

   # Add new key (allows multiple users/passwords)
   sudo cryptsetup luksAddKey /dev/sdb1
   # Enter existing passphrase, then new passphrase
   
   # Add key from file
   sudo cryptsetup luksAddKey /dev/sdb1 /root/newkeyfile
   
   # Remove key
   sudo cryptsetup luksRemoveKey /dev/sdb1
   # Enter passphrase to remove
   
   # Change passphrase
   sudo cryptsetup luksChangeKey /dev/sdb1
   
   # Kill key slot
   sudo cryptsetup luksKillSlot /dev/sdb1 1
   # Warning: Will make key irrecoverable!
   
   # View key slots
   sudo cryptsetup luksDump /dev/sdb1 | grep "Key Slot"

2.4 Auto-Mount at Boot
-----------------------

.. code-block:: bash

   # Get UUID of encrypted partition
   sudo blkid /dev/sdb1
   # Note the UUID
   
   # Edit crypttab
   sudo nano /etc/crypttab
   
   # Add line:
   encrypted_disk UUID=<partition-uuid> none luks,timeout=180
   
   # Or with key file:
   encrypted_disk UUID=<partition-uuid> /root/keyfile luks
   
   # Edit fstab
   sudo nano /etc/fstab
   
   # Add line:
   /dev/mapper/encrypted_disk /mnt/encrypted ext4 defaults 0 2
   
   # Test (without rebooting)
   sudo cryptdisks_start encrypted_disk
   sudo mount -a

2.5 Encrypted Swap
------------------

.. code-block:: bash

   # Disable current swap
   sudo swapoff -a
   
   # Create encrypted swap
   sudo cryptsetup open --type plain --key-file /dev/urandom /dev/sdb2 swap
   sudo mkswap /dev/mapper/swap
   
   # Edit crypttab
   echo "swap /dev/sdb2 /dev/urandom swap,cipher=aes-xts-plain64,size=256" | sudo tee -a /etc/crypttab
   
   # Edit fstab
   echo "/dev/mapper/swap none swap sw 0 0" | sudo tee -a /etc/fstab
   
   # Enable
   sudo swapon -a

================================================================================
3. Encrypted Home Directory
================================================================================

3.1 eCryptfs (per-user)
-----------------------

.. code-block:: bash

   # Install ecryptfs
   sudo apt install ecryptfs-utils
   
   # Encrypt home directory for new user
   sudo adduser --encrypt-home newuser
   
   # Encrypt existing user (must not be logged in)
   sudo ecryptfs-migrate-home -u username
   
   # Mount encrypted home
   ecryptfs-mount-private
   
   # Unmount
   ecryptfs-umount-private
   
   # Get recovery passphrase
   ecryptfs-unwrap-passphrase

3.2 Encrypt Private Directory
------------------------------

.. code-block:: bash

   # Create encrypted private directory
   ecryptfs-setup-private
   
   # Location: ~/Private
   # Auto-mounts on login
   
   # Manual mount/unmount
   ecryptfs-mount-private
   ecryptfs-umount-private

================================================================================
PART 2: GPG (GNU Privacy Guard)
================================================================================

4. GPG Basics
=============

4.1 Key Generation
------------------

.. code-block:: bash

   # Generate key pair
   gpg --full-generate-key
   # Or: gpg --gen-key (simplified)
   
   # Options:
   # 1. RSA and RSA (default)
   # 2. Key size: 4096 bits
   # 3. Expiration: 1y (1 year) or 0 (never)
   # 4. Name, email, comment
   # 5. Passphrase
   
   # Generate with specific options
   gpg --full-generate-key --expert

4.2 Key Management
------------------

.. code-block:: bash

   # List public keys
   gpg --list-keys
   gpg -k
   
   # List private keys
   gpg --list-secret-keys
   gpg -K
   
   # Delete public key
   gpg --delete-key user@email.com
   
   # Delete private key
   gpg --delete-secret-key user@email.com
   
   # Edit key (change passphrase, expiry, etc.)
   gpg --edit-key user@email.com

4.3 Key Import/Export
----------------------

.. code-block:: bash

   # Export public key (ASCII)
   gpg --armor --export user@email.com > public-key.asc
   
   # Export public key (binary)
   gpg --export user@email.com > public-key.gpg
   
   # Export private key (KEEP SECURE!)
   gpg --armor --export-secret-keys user@email.com > private-key.asc
   
   # Import key
   gpg --import public-key.asc
   gpg --import private-key.asc
   
   # Send key to keyserver
   gpg --send-keys KEY-ID --keyserver keys.openpgp.org
   
   # Receive key from keyserver
   gpg --recv-keys KEY-ID --keyserver keys.openpgp.org
   
   # Search keyserver
   gpg --search-keys user@email.com --keyserver keys.openpgp.org

================================================================================
5. File Encryption with GPG
================================================================================

5.1 Symmetric Encryption
-------------------------

.. code-block:: bash

   # Encrypt with password (no keys needed)
   gpg --symmetric file.txt
   # Creates file.txt.gpg
   
   # Specify cipher
   gpg --symmetric --cipher-algo AES256 file.txt
   
   # Decrypt
   gpg --decrypt file.txt.gpg > file.txt
   # Or: gpg file.txt.gpg

5.2 Asymmetric Encryption
--------------------------

.. code-block:: bash

   # Encrypt for recipient
   gpg --encrypt --recipient user@email.com file.txt
   # Creates file.txt.gpg
   
   # Encrypt and sign
   gpg --encrypt --sign --recipient user@email.com file.txt
   
   # Encrypt for multiple recipients
   gpg --encrypt --recipient alice@email.com --recipient bob@email.com file.txt
   
   # Decrypt
   gpg --decrypt file.txt.gpg > file.txt
   
   # Encrypt to ASCII
   gpg --armor --encrypt --recipient user@email.com file.txt
   # Creates file.txt.asc

5.3 Signing and Verification
-----------------------------

.. code-block:: bash

   # Sign file (creates file.txt.gpg)
   gpg --sign file.txt
   
   # Create detached signature
   gpg --detach-sign file.txt
   # Creates file.txt.sig
   
   # ASCII-armored signature
   gpg --armor --detach-sign file.txt
   # Creates file.txt.asc
   
   # Verify signature
   gpg --verify file.txt.gpg
   gpg --verify file.txt.sig file.txt
   
   # Clear-sign (text remains readable)
   gpg --clearsign message.txt

5.4 Directory Encryption
-------------------------

.. code-block:: bash

   # Create encrypted tar archive
   tar czf - directory/ | gpg --encrypt --recipient user@email.com > directory.tar.gz.gpg
   
   # Decrypt and extract
   gpg --decrypt directory.tar.gz.gpg | tar xzf -
   
   # Encrypt all files in directory
   for file in directory/*; do
       gpg --encrypt --recipient user@email.com "$file"
   done

================================================================================
PART 3: OpenSSL File Encryption
================================================================================

6. OpenSSL Symmetric Encryption
================================

6.1 Encrypt Files
-----------------

.. code-block:: bash

   # Encrypt with AES-256-CBC
   openssl enc -aes-256-cbc -salt -in file.txt -out file.enc
   # Enter password when prompted
   
   # Encrypt with password on command line (INSECURE)
   openssl enc -aes-256-cbc -salt -in file.txt -out file.enc -pass pass:mypassword
   
   # Encrypt with key file
   openssl enc -aes-256-cbc -salt -in file.txt -out file.enc -pass file:/path/to/keyfile
   
   # Available ciphers
   openssl list-cipher-algorithms

6.2 Decrypt Files
-----------------

.. code-block:: bash

   # Decrypt
   openssl enc -aes-256-cbc -d -in file.enc -out file.txt
   
   # Decrypt with password
   openssl enc -aes-256-cbc -d -in file.enc -out file.txt -pass pass:mypassword
   
   # Decrypt with key file
   openssl enc -aes-256-cbc -d -in file.enc -out file.txt -pass file:/path/to/keyfile

6.3 Base64 Encoding
-------------------

.. code-block:: bash

   # Encrypt and base64 encode (for email)
   openssl enc -aes-256-cbc -salt -in file.txt -out file.enc -a
   
   # Decrypt base64
   openssl enc -aes-256-cbc -d -in file.enc -out file.txt -a

================================================================================
PART 4: TLS/SSL Certificates
================================================================================

7. SSL Certificate Generation
==============================

7.1 Self-Signed Certificates
-----------------------------

.. code-block:: bash

   # Generate self-signed certificate (all-in-one)
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   
   # With passphrase protection
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
   
   # From existing key
   openssl req -x509 -key existing-key.pem -out cert.pem -days 365

7.2 Certificate Signing Request (CSR)
--------------------------------------

.. code-block:: bash

   # Generate private key
   openssl genrsa -out private-key.pem 4096
   
   # Generate CSR
   openssl req -new -key private-key.pem -out request.csr
   
   # Generate key and CSR together
   openssl req -newkey rsa:4096 -keyout private-key.pem -out request.csr -nodes
   
   # View CSR
   openssl req -text -noout -in request.csr

7.3 Certificate Operations
---------------------------

.. code-block:: bash

   # View certificate
   openssl x509 -text -noout -in cert.pem
   
   # Check certificate expiry
   openssl x509 -enddate -noout -in cert.pem
   
   # Verify certificate
   openssl verify cert.pem
   
   # Check certificate against CA
   openssl verify -CAfile ca-cert.pem cert.pem
   
   # Convert formats
   # PEM to DER
   openssl x509 -in cert.pem -outform DER -out cert.der
   
   # DER to PEM
   openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem
   
   # PEM to PKCS12
   openssl pkcs12 -export -in cert.pem -inkey key.pem -out cert.p12

7.4 Test SSL/TLS Connection
----------------------------

.. code-block:: bash

   # Connect to HTTPS server
   openssl s_client -connect example.com:443
   
   # Show certificate chain
   openssl s_client -showcerts -connect example.com:443
   
   # Test specific TLS version
   openssl s_client -connect example.com:443 -tls1_2
   openssl s_client -connect example.com:443 -tls1_3
   
   # Check certificate expiry of remote server
   echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

================================================================================
8. Let's Encrypt (Free SSL Certificates)
=========================================

8.1 Certbot Installation
-------------------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install certbot python3-certbot-apache  # For Apache
   sudo apt install certbot python3-certbot-nginx   # For Nginx
   
   # RHEL/CentOS
   sudo dnf install certbot python3-certbot-apache
   sudo dnf install certbot python3-certbot-nginx

8.2 Obtain Certificate
-----------------------

.. code-block:: bash

   # Apache (auto-configure)
   sudo certbot --apache -d example.com -d www.example.com
   
   # Nginx (auto-configure)
   sudo certbot --nginx -d example.com -d www.example.com
   
   # Standalone (stops web server temporarily)
   sudo systemctl stop apache2
   sudo certbot certonly --standalone -d example.com
   sudo systemctl start apache2
   
   # Webroot (no downtime)
   sudo certbot certonly --webroot -w /var/www/html -d example.com
   
   # Wildcard certificate
   sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com" -d example.com

8.3 Certificate Renewal
------------------------

.. code-block:: bash

   # Dry run (test renewal)
   sudo certbot renew --dry-run
   
   # Renew all certificates
   sudo certbot renew
   
   # Auto-renewal (systemd timer)
   sudo systemctl status certbot.timer
   
   # List certificates
   sudo certbot certificates
   
   # Revoke certificate
   sudo certbot revoke --cert-path /etc/letsencrypt/live/example.com/cert.pem
   
   # Delete certificate
   sudo certbot delete --cert-name example.com

================================================================================
9. Encryption Best Practices
=============================

9.1 Password Management
-----------------------

.. code-block:: bash

   # Generate strong random passwords
   openssl rand -base64 32
   
   # Or using pwgen
   sudo apt install pwgen
   pwgen -s 32 1                # Secure 32-char password
   
   # Generate passphrase
   pwgen -s -y 20 1            # 20 chars with symbols

9.2 Key Storage
---------------

**Best Practices:**

1. **Private Keys:**
   - Never share private keys
   - Protect with strong passphrases
   - Store in secure location (chmod 600)
   - Backup encrypted
   - Use key files on removable media for LUKS

2. **Passwords:**
   - Use password managers (KeePassXC, Bitwarden)
   - Different passwords for different systems
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols

3. **GPG Keys:**
   - Backup to secure offline storage
   - Generate revocation certificate
   - Set expiry dates
   - Use subkeys for daily operations

9.3 Encryption Checklist
-------------------------

.. code-block:: text

   ☐ Encrypt laptop/desktop hard drives (LUKS)
   ☐ Encrypt external backup drives
   ☐ Encrypt cloud storage sync folders
   ☐ Use GPG for sensitive documents
   ☐ Enable HTTPS for web services
   ☐ Use SSH keys (encrypted)
   ☐ Encrypt email (GPG)
   ☐ Encrypted swap partition
   ☐ Secure key backups
   ☐ Test recovery procedures

================================================================================
10. Practical Examples
======================

10.1 Encrypted USB Backup Drive
--------------------------------

.. code-block:: bash

   # Create encrypted backup drive
   sudo cryptsetup luksFormat /dev/sdc1
   sudo cryptsetup open /dev/sdc1 backup
   sudo mkfs.ext4 /dev/mapper/backup
   sudo mount /dev/mapper/backup /mnt/backup
   
   # Backup
   sudo rsync -av /home/user/ /mnt/backup/
   
   # Unmount
   sudo umount /mnt/backup
   sudo cryptsetup close backup

10.2 Encrypted Email
--------------------

.. code-block:: bash

   # Generate GPG key
   gpg --full-generate-key
   
   # Export public key for sharing
   gpg --armor --export your@email.com > public-key.asc
   
   # Import recipient's public key
   gpg --import recipient-public-key.asc
   
   # Encrypt email body
   gpg --armor --encrypt --recipient recipient@email.com email-body.txt
   
   # Send email-body.txt.asc via email client

10.3 Secure File Transfer
--------------------------

.. code-block:: bash

   # Encrypt file for transfer
   gpg --armor --encrypt --recipient recipient@email.com sensitive-data.pdf
   
   # Transfer via SCP
   scp sensitive-data.pdf.asc user@server:/tmp/
   
   # Recipient decrypts
   gpg --decrypt sensitive-data.pdf.asc > sensitive-data.pdf

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- SSH_Hardening.rst - SSH key management and encryption
- File_Permissions_DAC.rst - File security and access control
- Linux_Security_Basics.rst - Overall security principles
- User_Account_Security.rst - Password policies

================================================================================
END OF ENCRYPTION TECHNOLOGIES
================================================================================
