===================================
Linux Encryption Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: Disk encryption, file encryption, and cryptographic tools

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Encryption Commands
------------------------------

.. code-block:: bash

   # LUKS disk encryption
   sudo cryptsetup luksFormat /dev/sdb1
   sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk
   sudo mkfs.ext4 /dev/mapper/encrypted_disk
   sudo mount /dev/mapper/encrypted_disk /mnt/encrypted
   
   # Close encrypted disk
   sudo umount /mnt/encrypted
   sudo cryptsetup luksClose encrypted_disk
   
   # GPG file encryption
   gpg --encrypt --recipient user@example.com file.txt
   gpg --decrypt file.txt.gpg > file.txt
   
   # Symmetric encryption
   gpg --symmetric file.txt
   gpg --decrypt file.txt.gpg > file.txt
   
   # OpenSSL file encryption
   openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc
   openssl enc -aes-256-cbc -d -in file.txt.enc -out file.txt

Quick Full Disk Encryption Setup
---------------------------------

.. code-block:: bash

   #!/bin/bash
   # Encrypt and mount a partition
   
   DEVICE="/dev/sdb1"
   MAPPER_NAME="encrypted_data"
   MOUNT_POINT="/mnt/encrypted"
   
   # Format with LUKS
   sudo cryptsetup luksFormat "$DEVICE"
   
   # Open the encrypted device
   sudo cryptsetup luksOpen "$DEVICE" "$MAPPER_NAME"
   
   # Create filesystem
   sudo mkfs.ext4 /dev/mapper/"$MAPPER_NAME"
   
   # Mount
   sudo mkdir -p "$MOUNT_POINT"
   sudo mount /dev/mapper/"$MAPPER_NAME" "$MOUNT_POINT"
   
   echo "Encrypted partition mounted at $MOUNT_POINT"

LUKS Disk Encryption
====================

LUKS Basics
-----------

.. code-block:: bash

   # Install cryptsetup
   sudo apt install cryptsetup  # Debian/Ubuntu
   sudo yum install cryptsetup  # RHEL/CentOS
   
   # Check if device is LUKS
   sudo cryptsetup isLuks /dev/sdb1
   echo $?  # 0 = LUKS device, 1 = not LUKS
   
   # Get LUKS header info
   sudo cryptsetup luksDump /dev/sdb1

Creating Encrypted Partition
-----------------------------

.. code-block:: bash

   # Format partition with LUKS (DESTROYS DATA!)
   sudo cryptsetup luksFormat /dev/sdb1
   
   # With specific cipher
   sudo cryptsetup luksFormat --cipher aes-xts-plain64 --key-size 512 --hash sha256 /dev/sdb1
   
   # LUKS2 (default in newer versions)
   sudo cryptsetup luksFormat --type luks2 /dev/sdb1
   
   # LUKS1 (for compatibility)
   sudo cryptsetup luksFormat --type luks1 /dev/sdb1

Opening and Mounting
--------------------

.. code-block:: bash

   # Open encrypted device
   sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk
   
   # Now appears as /dev/mapper/encrypted_disk
   
   # Create filesystem (first time only)
   sudo mkfs.ext4 /dev/mapper/encrypted_disk
   
   # Mount
   sudo mkdir -p /mnt/encrypted
   sudo mount /dev/mapper/encrypted_disk /mnt/encrypted
   
   # Use the encrypted disk normally
   ls /mnt/encrypted

Closing Encrypted Device
-------------------------

.. code-block:: bash

   # Unmount
   sudo umount /mnt/encrypted
   
   # Close LUKS device
   sudo cryptsetup luksClose encrypted_disk
   
   # Verify closed
   ls /dev/mapper/encrypted_disk  # Should not exist

Key Management
--------------

.. code-block:: bash

   # List key slots
   sudo cryptsetup luksDump /dev/sdb1 | grep "Key Slot"
   
   # Add new passphrase (key slot)
   sudo cryptsetup luksAddKey /dev/sdb1
   
   # Change existing passphrase
   sudo cryptsetup luksChangeKey /dev/sdb1
   
   # Remove key slot
   sudo cryptsetup luksRemoveKey /dev/sdb1
   
   # Kill specific key slot
   sudo cryptsetup luksKillSlot /dev/sdb1 1
   
   # Add key from file
   sudo cryptsetup luksAddKey /dev/sdb1 /path/to/keyfile
   
   # Open with keyfile
   sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk --key-file /path/to/keyfile

Creating Keyfiles
-----------------

.. code-block:: bash

   # Generate random keyfile
   sudo dd if=/dev/urandom of=/root/keyfile bs=1024 count=4
   sudo chmod 400 /root/keyfile
   
   # Add keyfile to LUKS
   sudo cryptsetup luksAddKey /dev/sdb1 /root/keyfile
   
   # Open with keyfile (no password prompt)
   sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk --key-file /root/keyfile

Automatic Mounting with /etc/crypttab
--------------------------------------

.. code-block:: bash

   # /etc/crypttab format:
   # <target> <source device> <key file> <options>
   
   # Example entries:
   # With password prompt at boot
   encrypted_data UUID=12345678-1234-1234-1234-123456789abc none luks
   
   # With keyfile (no prompt)
   encrypted_data UUID=12345678-1234-1234-1234-123456789abc /root/keyfile luks
   
   # Find UUID
   sudo blkid /dev/sdb1
   
   # /etc/fstab entry
   /dev/mapper/encrypted_data /mnt/encrypted ext4 defaults 0 2

Backup and Restore Header
--------------------------

.. code-block:: bash

   # Backup LUKS header (CRITICAL!)
   sudo cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file /root/luks-header-backup-sdb1.img
   
   # Store backup safely (encrypted USB, secure location)
   
   # Restore header (if corrupted)
   sudo cryptsetup luksHeaderRestore /dev/sdb1 --header-backup-file /root/luks-header-backup-sdb1.img
   
   # IMPORTANT: Without header, data is UNRECOVERABLE!

Resize Encrypted Partition
---------------------------

.. code-block:: bash

   # Grow filesystem (after growing partition)
   sudo cryptsetup resize encrypted_disk
   sudo resize2fs /dev/mapper/encrypted_disk
   
   # Or for XFS
   sudo xfs_growfs /mnt/encrypted

Full Disk Encryption (System)
==============================

During Installation
-------------------

.. code-block:: text

   Most Linux distributions support encrypted installation:
   
   Ubuntu/Debian:
   - Choose "Encrypt the new Ubuntu installation for security"
   - Or manual partitioning with LUKS
   
   Fedora/RHEL:
   - Check "Encrypt my data" during installation
   
   Arch Linux:
   - Manual setup with cryptsetup before pacstrap

Post-Installation Encryption
-----------------------------

.. code-block:: bash

   # Complex process - requires:
   # 1. Boot from live USB
   # 2. Shrink existing partition
   # 3. Create LUKS container
   # 4. Copy data
   # 5. Update bootloader and initramfs
   
   # Recommended: Backup and reinstall with encryption

File and Directory Encryption
==============================

eCryptfs
--------

.. code-block:: bash

   # Install eCryptfs
   sudo apt install ecryptfs-utils
   
   # Mount encrypted directory
   sudo mount -t ecryptfs /source/dir /dest/dir
   
   # Will prompt for:
   # - Passphrase
   # - Cipher (aes recommended)
   # - Key bytes (16/32)
   # - Enable filename encryption
   
   # Or use ecryptfs-setup-private for home directory
   ecryptfs-setup-private
   
   # Unmount
   sudo umount /dest/dir

EncFS (FUSE-based)
------------------

.. code-block:: bash

   # Install EncFS
   sudo apt install encfs
   
   # Create encrypted filesystem
   encfs ~/.encrypted ~/encrypted
   
   # Configure paranoia mode or standard
   
   # Use directory normally
   cd ~/encrypted
   # Files stored encrypted in ~/.encrypted
   
   # Unmount
   fusermount -u ~/encrypted
   
   # Mount again
   encfs ~/.encrypted ~/encrypted

gocryptfs (Modern Alternative)
-------------------------------

.. code-block:: bash

   # Install gocryptfs
   sudo apt install gocryptfs
   
   # Initialize
   gocryptfs -init ~/encrypted_storage
   
   # Mount
   gocryptfs ~/encrypted_storage ~/decrypted
   
   # Use
   cd ~/decrypted
   
   # Unmount
   fusermount -u ~/decrypted

File Encryption with GPG
=========================

GPG Basics
----------

.. code-block:: bash

   # Install GPG
   sudo apt install gnupg
   
   # Generate key pair
   gpg --full-generate-key
   
   # List keys
   gpg --list-keys
   gpg --list-secret-keys
   
   # Export public key
   gpg --export --armor user@example.com > pubkey.asc
   
   # Import public key
   gpg --import pubkey.asc
   
   # Delete key
   gpg --delete-key user@example.com
   gpg --delete-secret-key user@example.com

Encrypting Files
----------------

.. code-block:: bash

   # Encrypt for recipient (asymmetric)
   gpg --encrypt --recipient user@example.com file.txt
   # Creates file.txt.gpg
   
   # Encrypt for multiple recipients
   gpg --encrypt --recipient alice@example.com --recipient bob@example.com file.txt
   
   # Symmetric encryption (password only)
   gpg --symmetric file.txt
   gpg --output file.txt.gpg --symmetric file.txt
   
   # Encrypt and sign
   gpg --encrypt --sign --recipient user@example.com file.txt

Decrypting Files
----------------

.. code-block:: bash

   # Decrypt file
   gpg --decrypt file.txt.gpg > file.txt
   
   # Or
   gpg --output file.txt --decrypt file.txt.gpg
   
   # Verify signature
   gpg --verify file.txt.sig file.txt

Archive Encryption
------------------

.. code-block:: bash

   # Encrypt directory
   tar czf - /path/to/dir | gpg --encrypt --recipient user@example.com > backup.tar.gz.gpg
   
   # Decrypt and extract
   gpg --decrypt backup.tar.gz.gpg | tar xzf -
   
   # With symmetric encryption
   tar czf - /path/to/dir | gpg --symmetric > backup.tar.gz.gpg

OpenSSL Encryption
==================

File Encryption
---------------

.. code-block:: bash

   # Encrypt file (AES-256-CBC)
   openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc
   
   # Decrypt file
   openssl enc -aes-256-cbc -d -in file.txt.enc -out file.txt
   
   # Use password from file
   openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc -pass file:/path/to/passfile
   
   # Use key and IV
   openssl enc -aes-256-cbc -in file.txt -out file.txt.enc -K <key> -iv <iv>
   
   # Other ciphers
   openssl enc -aes-128-cbc ...
   openssl enc -aes-256-cfb ...
   openssl enc -des3 ...
   
   # List available ciphers
   openssl enc -list

Generate Keys
-------------

.. code-block:: bash

   # Generate random password
   openssl rand -base64 32
   
   # Generate hex key
   openssl rand -hex 16
   
   # RSA key pair
   openssl genrsa -out private.key 2048
   openssl rsa -in private.key -pubout -out public.key
   
   # Encrypt with public key
   openssl rsautl -encrypt -pubin -inkey public.key -in file.txt -out file.enc
   
   # Decrypt with private key
   openssl rsautl -decrypt -inkey private.key -in file.enc -out file.txt

Hashing and Checksums
---------------------

.. code-block:: bash

   # Generate hash
   openssl dgst -sha256 file.txt
   openssl sha256 file.txt
   
   # MD5 (not recommended for security)
   openssl md5 file.txt
   
   # HMAC
   openssl dgst -sha256 -hmac "secret_key" file.txt

SSH and SSL/TLS
===============

SSH Key Management
------------------

.. code-block:: bash

   # Generate SSH key pair
   ssh-keygen -t ed25519 -C "user@example.com"
   ssh-keygen -t rsa -b 4096 -C "user@example.com"
   
   # With passphrase
   ssh-keygen -t ed25519 -C "user@example.com" -f ~/.ssh/id_ed25519_work
   
   # Copy public key to server
   ssh-copy-id user@server
   
   # Or manually
   cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
   
   # Change passphrase
   ssh-keygen -p -f ~/.ssh/id_ed25519
   
   # Show fingerprint
   ssh-keygen -lf ~/.ssh/id_ed25519.pub

SSL/TLS Certificates
--------------------

.. code-block:: bash

   # Generate self-signed certificate
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout server.key -out server.crt
   
   # Generate CSR (Certificate Signing Request)
   openssl req -new -newkey rsa:2048 -nodes \
     -keyout server.key -out server.csr
   
   # View certificate
   openssl x509 -in server.crt -text -noout
   
   # Verify certificate
   openssl verify server.crt
   
   # Check certificate expiration
   openssl x509 -in server.crt -noout -enddate
   
   # Convert formats
   # PEM to DER
   openssl x509 -in cert.pem -outform der -out cert.der
   
   # DER to PEM
   openssl x509 -in cert.der -inform der -out cert.pem
   
   # PEM to PKCS12
   openssl pkcs12 -export -out cert.p12 -inkey server.key -in server.crt

Secure Deletion
===============

shred
-----

.. code-block:: bash

   # Securely delete file
   shred -vfz -n 10 sensitive_file.txt
   
   # Options:
   # -v: verbose
   # -f: force permissions
   # -z: zero final pass
   # -n: number of overwrite passes
   
   # Shred and remove
   shred -vfz -n 10 --remove sensitive_file.txt

dd for Wiping Disks
-------------------

.. code-block:: bash

   # Zero entire disk (DESTROYS ALL DATA!)
   sudo dd if=/dev/zero of=/dev/sdb bs=4M status=progress
   
   # Random data
   sudo dd if=/dev/urandom of=/dev/sdb bs=4M status=progress
   
   # Wipe specific partition
   sudo dd if=/dev/zero of=/dev/sdb1 bs=4M status=progress

wipe
----

.. code-block:: bash

   # Install wipe
   sudo apt install wipe
   
   # Wipe file
   wipe -rf sensitive_file.txt
   
   # Wipe directory
   wipe -rf /path/to/sensitive/dir

Best Practices
==============

1. **Use strong passphrases** - 20+ characters, random
2. **Backup LUKS headers** - essential for recovery
3. **Use keyfiles for servers** - no manual intervention needed
4. **Encrypt sensitive data** at rest and in transit
5. **Regular key rotation** - change encryption keys periodically
6. **Secure key storage** - never store keys with encrypted data
7. **Test restore procedures** - verify you can decrypt
8. **Use modern algorithms** - AES-256, avoid DES/3DES
9. **Enable TRIM for SSDs** with caution (may leak data)
10. **Physical security** - encryption doesn't help if system is compromised while running

Common Pitfalls
===============

1. **Losing LUKS header** - data is unrecoverable
2. **Forgetting passphrases** - no recovery without backup key
3. **Storing keys insecurely** - defeats purpose of encryption
4. **Not testing recovery** - discover issues during emergency
5. **Weak passphrases** - easily brute-forced
6. **TRIM on encrypted SSDs** - may leak information
7. **Using outdated algorithms** - MD5, DES are weak

Troubleshooting
===============

.. code-block:: bash

   # LUKS device won't open
   sudo cryptsetup luksDump /dev/sdb1  # Check if LUKS
   sudo cryptsetup luksOpen -v /dev/sdb1 test  # Verbose output
   
   # Device busy
   sudo lsof | grep /dev/mapper/encrypted_disk
   sudo fuser -mv /dev/mapper/encrypted_disk
   
   # Can't mount
   sudo cryptsetup status encrypted_disk
   ls -l /dev/mapper/encrypted_disk
   sudo fsck /dev/mapper/encrypted_disk
   
   # GPG decryption fails
   gpg --list-keys  # Verify key exists
   gpg --decrypt file.gpg 2>&1  # See error message

Quick Reference
===============

.. code-block:: bash

   # LUKS
   cryptsetup luksFormat /dev/sdX
   cryptsetup luksOpen /dev/sdX name
   cryptsetup luksClose name
   cryptsetup luksAddKey /dev/sdX
   
   # GPG
   gpg --encrypt --recipient user file
   gpg --decrypt file.gpg > file
   gpg --symmetric file
   
   # OpenSSL
   openssl enc -aes-256-cbc -in file -out file.enc
   openssl enc -aes-256-cbc -d -in file.enc -out file

See Also
========

- Linux_Security_Hardening.rst
- Linux_Kernel_Security.rst

References
==========

- man cryptsetup
- man gpg
- man openssl
- https://gitlab.com/cryptsetup/cryptsetup
- https://gnupg.org/documentation/
