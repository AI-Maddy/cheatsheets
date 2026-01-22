======================================================
OTA Updates & Boot Management Complete Guide
======================================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

OTA (Over-The-Air) updates enable remote firmware/software updates without physical access. Critical for IoT, embedded systems, mobile devices, and automotive platforms.

Update Strategies
-----------------

+---------------------------+----------------------------------+--------------------------------+
| **Strategy**              | **Advantages**                   | **Disadvantages**              |
+===========================+==================================+================================+
| **Full Image**            | Simple, complete replacement     | Large downloads, slow          |
+---------------------------+----------------------------------+--------------------------------+
| **Delta/Differential**    | Small size, fast                 | Complex, requires base version |
+---------------------------+----------------------------------+--------------------------------+
| **A/B (Seamless)**        | Safe rollback, zero downtime     | 2x storage required            |
+---------------------------+----------------------------------+--------------------------------+
| **Recovery Partition**    | Fallback available               | Extra partition needed         |
+---------------------------+----------------------------------+--------------------------------+
| **Container/Package**     | Modular updates                  | Dependency management          |
+---------------------------+----------------------------------+--------------------------------+

Boot Flow Types
---------------

.. code-block:: text

   Traditional Single Boot:
   ┌─────────────┐
   │ Bootloader  │
   ├─────────────┤
   │   System    │  ← Single rootfs, risky updates
   └─────────────┘
   
   Recovery Partition:
   ┌─────────────┐
   │ Bootloader  │
   ├─────────────┤──┬─────────────┐
   │   System    │  │  Recovery   │  ← Fallback partition
   └─────────────┘  └─────────────┘
   
   A/B Dual Boot:
   ┌─────────────┐
   │ Bootloader  │
   ├─────────────┤──┬─────────────┐
   │  System A   │  │  System B   │  ← Active/Inactive slots
   └─────────────┘  └─────────────┘
   
   Golden Image:
   ┌─────────────┐
   │ Bootloader  │
   ├─────────────┤──┬─────────────┬─────────────┐
   │  System A   │  │  System B   │ Golden (RO) │
   └─────────────┘  └─────────────┴─────────────┘

🔄 A/B Update System
=====================

Concept
-------

Two complete system partitions (A and B). Active slot runs while inactive slot gets updated. Atomically switch on success.

Partition Layout
----------------

.. code-block:: text

   /dev/mmcblk0p1  boot_a      (Kernel A)
   /dev/mmcblk0p2  boot_b      (Kernel B)
   /dev/mmcblk0p3  system_a    (RootFS A)
   /dev/mmcblk0p4  system_b    (RootFS B)
   /dev/mmcblk0p5  data        (Shared user data)
   /dev/mmcblk0p6  misc        (Boot control)

U-Boot A/B Configuration
-------------------------

**Environment Variables:**

.. code-block:: bash

   # Boot slot tracking
   setenv boot_slot a
   setenv boot_tries 3
   setenv bootcount 0
   
   # Partition UUIDs or numbers
   setenv boot_a_part 1
   setenv boot_b_part 2
   setenv system_a_part 3
   setenv system_b_part 4
   
   # Boot command with fallback
   setenv bootcmd 'run ab_select; run do_boot || run fallback_boot'
   
   # A/B selection logic
   setenv ab_select '
       if test "${boot_slot}" = "a"; then
           setenv boot_part ${boot_a_part}
           setenv system_part ${system_a_part}
       else
           setenv boot_part ${boot_b_part}
           setenv system_part ${system_b_part}
       fi
   '
   
   # Boot from selected slot
   setenv do_boot '
       ext4load mmc 0:${boot_part} ${kernel_addr_r} Image
       ext4load mmc 0:${boot_part} ${fdt_addr_r} dtb
       setenv bootargs "root=/dev/mmcblk0p${system_part} ro"
       booti ${kernel_addr_r} - ${fdt_addr_r}
   '
   
   # Fallback to other slot
   setenv fallback_boot '
       echo "Boot failed, trying other slot..."
       if test "${boot_slot}" = "a"; then
           setenv boot_slot b
       else
           setenv boot_slot a
       fi
       saveenv
       reset
   '
   
   saveenv

**Boot Counter (Watchdog Protection):**

.. code-block:: bash

   # In U-Boot config
   CONFIG_BOOTCOUNT_LIMIT=y
   CONFIG_BOOTCOUNT_ENV=y
   
   # Environment
   setenv bootlimit 3
   setenv upgrade_available 0
   
   # Boot logic with counter
   setenv bootcmd '
       if test ${bootcount} -gt ${bootlimit}; then
           echo "Boot limit exceeded, switching slots"
           if test "${boot_slot}" = "a"; then
               setenv boot_slot b
           else
               setenv boot_slot a
           fi
           setenv bootcount 0
       fi
       run ab_select
       run do_boot
   '

GRUB A/B Configuration
----------------------

.. code-block:: grub

   # /etc/grub.d/40_custom
   
   # Read boot slot from file
   set boot_slot_file="/boot/slot"
   if [ -f $boot_slot_file ]; then
       source $boot_slot_file
   else
       set boot_slot="a"
   fi
   
   # Boot from slot A
   menuentry 'System Slot A' {
       if [ "$boot_slot" = "a" ]; then
           set default=0
       fi
       insmod gzio
       insmod part_gpt
       insmod ext2
       set root='hd0,gpt3'
       linux /boot/vmlinuz root=/dev/sda3 ro quiet
       initrd /boot/initrd.img
   }
   
   # Boot from slot B
   menuentry 'System Slot B' {
       if [ "$boot_slot" = "b" ]; then
           set default=0
       fi
       insmod gzio
       insmod part_gpt
       insmod ext2
       set root='hd0,gpt4'
       linux /boot/vmlinuz root=/dev/sda4 ro quiet
       initrd /boot/initrd.img
   }

Android A/B Updates
-------------------

**Partition Scheme:**

.. code-block:: text

   boot_a      bootloader_a      system_a      vendor_a
   boot_b      bootloader_b      system_b      vendor_b
   
   userdata (shared)
   metadata (slot info)

**Slot Metadata:**

.. code-block:: c

   // bootable/recovery/bootloader_message/include/bootloader_message/bootloader_message.h
   
   struct slot_metadata {
       uint8_t priority;       // 0-15 (15 = highest)
       uint8_t tries_remaining; // Boot attempts left
       uint8_t successful_boot; // 1 if boot succeeded
       uint8_t reserved;
   };
   
   struct boot_ctrl {
       char magic[4];          // "\0AB0"
       uint8_t version;
       uint8_t nb_slot;
       uint8_t recovery_tries_remaining;
       uint8_t reserved[9];
       struct slot_metadata slot_info[2];
   };

**Boot Control HAL:**

.. code-block:: cpp

   // hardware/interfaces/boot/1.0/IBootControl.hal
   
   // Get active slot
   Slot getCurrentSlot();
   
   // Mark slot successful
   markBootSuccessful();
   
   // Set active slot
   setActiveBootSlot(Slot slot);
   
   // Get slot info
   bool isSlotBootable(Slot slot);
   bool isSlotMarkedSuccessful(Slot slot);

**Update Engine:**

.. code-block:: bash

   # Trigger OTA update
   adb root
   adb shell
   
   # Check current slot
   bootctl get-current-slot
   bootctl get-suffix
   
   # Get slot info
   bootctl get-slot-info 0
   bootctl get-slot-info 1
   
   # Mark successful
   bootctl mark-boot-successful
   
   # Set active slot
   bootctl set-active-boot-slot 1

📦 OTA Update Frameworks
=========================

RAUC (Robust Auto-Update Controller)
-------------------------------------

**System Configuration (/etc/rauc/system.conf):**

.. code-block:: ini

   [system]
   compatible=MyProduct 2023.01
   bootloader=uboot
   mountprefix=/mnt/rauc
   
   [keyring]
   path=/etc/rauc/keyring.pem
   
   [slot.rootfs.0]
   device=/dev/mmcblk0p3
   type=ext4
   bootname=A
   
   [slot.rootfs.1]
   device=/dev/mmcblk0p4
   type=ext4
   bootname=B
   
   [slot.kernel.0]
   device=/dev/mmcblk0p1
   type=raw
   parent=rootfs.0
   
   [slot.kernel.1]
   device=/dev/mmcblk0p2
   type=raw
   parent=rootfs.1

**Bundle Manifest (manifest.raucm):**

.. code-block:: ini

   [update]
   compatible=MyProduct 2023.01
   version=2023.01.15
   description=System Update v1.5
   build=2023-01-15T10:30:00Z
   
   [bundle]
   format=verity
   
   [image.rootfs]
   filename=rootfs.ext4
   size=524288000
   sha256=1234567890abcdef...
   
   [image.kernel]
   filename=kernel.img
   size=8388608
   sha256=fedcba0987654321...

**Create Bundle:**

.. code-block:: bash

   # Create bundle directory
   mkdir -p bundle
   cd bundle
   
   # Copy images
   cp /path/to/rootfs.ext4 .
   cp /path/to/kernel.img .
   
   # Create manifest
   cat > manifest.raucm << EOF
   [update]
   compatible=MyProduct 2023.01
   version=2023.01.15
   EOF
   
   # Generate bundle
   rauc bundle \
       --cert=cert.pem \
       --key=key.pem \
       --keyring=ca.pem \
       bundle/ \
       update-2023.01.15.raucb

**Install Update:**

.. code-block:: bash

   # Check status
   rauc status
   rauc status --detailed
   
   # Install bundle
   rauc install update.raucb
   
   # Monitor installation
   rauc status --detailed
   
   # Mark as good (after testing)
   rauc status mark-good
   
   # Service mode (D-Bus)
   systemctl start rauc
   dbus-send --system --print-reply \
       --dest=de.pengutronix.rauc / \
       de.pengutronix.rauc.Installer.Install \
       string:"/path/to/update.raucb"

SWUpdate
--------

**Configuration (swupdate.cfg):**

.. code-block:: json

   {
       "software": {
           "version": "1.0.0",
           "hardware-compatibility": ["1.0"],
           "description": "System Update"
       },
       "images": [
           {
               "filename": "rootfs.ext4.gz",
               "device": "/dev/mmcblk0p3",
               "filesystem": "ext4",
               "compressed": "zlib"
           },
           {
               "filename": "kernel.img",
               "device": "/dev/mmcblk0p1",
               "type": "raw"
           }
       ],
       "scripts": [
           {
               "filename": "post_install.sh",
               "type": "postinstall",
               "data": "check_installation"
           }
       ]
   }

**sw-description (Embedded):**

.. code-block:: text

   software =
   {
       version = "1.0.0";
       
       hardware-compatibility: [ "1.0" ];
       
       images: (
           {
               filename = "rootfs.ext4.gz";
               device = "/dev/mmcblk0p3";
               type = "raw";
               compressed = "zlib";
               sha256 = "abc123...";
           },
           {
               filename = "kernel.img";
               device = "/dev/mmcblk0p1";
               type = "raw";
               sha256 = "def456...";
           }
       );
       
       scripts: (
           {
               filename = "post_install.sh";
               type = "postinstall";
           }
       );
   }

**Create Update Package:**

.. code-block:: bash

   # Create sw-description
   cat > sw-description << EOF
   software =
   {
       version = "1.0.0";
       images: (
           {
               filename = "rootfs.ext4.gz";
               device = "/dev/mmcblk0p3";
           }
       );
   }
   EOF
   
   # Create CPIO archive
   for i in sw-description rootfs.ext4.gz kernel.img; do
       echo $i
   done | cpio -ov -H crc > update.swu
   
   # Or with signing
   openssl dgst -sha256 -sign private.key sw-description > sw-description.sig
   
   for i in sw-description sw-description.sig rootfs.ext4.gz kernel.img; do
       echo $i
   done | cpio -ov -H crc > update.swu

**Install Update:**

.. code-block:: bash

   # Direct installation
   swupdate -i update.swu
   
   # With web interface
   swupdate -w "-document_root /www"
   # Then upload via http://device-ip:8080
   
   # Progress monitoring
   swupdate-progress
   
   # Hawkbit integration
   swupdate -u "http://hawkbit-server/default/controller/v1/device-id"

Mender
------

**Device Configuration (/etc/mender/mender.conf):**

.. code-block:: json

   {
       "ServerURL": "https://mender.example.com",
       "ServerCertificate": "/etc/mender/server.crt",
       "TenantToken": "eyJhbGciOiJSUzI1...",
       "InventoryPollIntervalSeconds": 1800,
       "UpdatePollIntervalSeconds": 600,
       "RetryPollIntervalSeconds": 300,
       "RootfsPartA": "/dev/mmcblk0p3",
       "RootfsPartB": "/dev/mmcblk0p4"
   }

**Artifact Creation:**

.. code-block:: bash

   # Single file artifact
   mender-artifact write rootfs-image \
       --artifact-name release-v1.0 \
       --device-type mydevice \
       --file rootfs.ext4 \
       --output-path artifact.mender
   
   # With scripts
   mender-artifact write rootfs-image \
       --artifact-name release-v1.0 \
       --device-type mydevice \
       --file rootfs.ext4 \
       --script ArtifactInstall_Enter_00 \
       --script ArtifactInstall_Leave_99 \
       --output-path artifact.mender
   
   # Module update
   mender-artifact write module-image \
       --artifact-name docker-v1.0 \
       --device-type mydevice \
       --type docker \
       --file docker-compose.yml \
       --output-path docker-artifact.mender

**State Scripts:**

.. code-block:: bash

   # /etc/mender/scripts/
   # Download states:
   #   Download_Enter_*, Download_Leave_*, Download_Error_*
   # ArtifactInstall states:
   #   ArtifactInstall_Enter_*, ArtifactInstall_Leave_*, ArtifactInstall_Error_*
   # ArtifactReboot states:
   #   ArtifactReboot_Enter_*, ArtifactReboot_Leave_*, ArtifactReboot_Error_*
   # ArtifactCommit states:
   #   ArtifactCommit_Enter_*, ArtifactCommit_Leave_*, ArtifactCommit_Error_*
   
   # Example: /etc/mender/scripts/ArtifactInstall_Enter_00
   #!/bin/bash
   echo "Pre-installation checks"
   df -h
   free -m
   
   # Example: /etc/mender/scripts/ArtifactCommit_Leave_99
   #!/bin/bash
   echo "Update successful, cleaning up"
   systemctl restart myservice

**Client Commands:**

.. code-block:: bash

   # Manual update check
   mender check-update
   
   # Force update
   mender install https://server.com/artifact.mender
   
   # Show artifact info
   mender show-artifact
   
   # Commit update (mark as good)
   mender commit
   
   # Rollback
   mender rollback
   
   # Daemon management
   systemctl start mender-client
   systemctl enable mender-client
   
   # Bootstrap (first-time setup)
   mender bootstrap

OSTree (libostree)
------------------

**Repository Setup:**

.. code-block:: bash

   # Initialize repository
   ostree --repo=/ostree/repo init --mode=archive-z2
   
   # Commit filesystem
   ostree --repo=/ostree/repo commit \
       --branch=myos/x86_64/stable \
       --subject="Version 1.0.0" \
       /path/to/rootfs
   
   # List commits
   ostree --repo=/ostree/repo log myos/x86_64/stable
   
   # Serve repository
   ostree trivial-httpd --autoexit --port=8000 /ostree/repo

**Client Configuration:**

.. code-block:: ini

   # /etc/ostree/remotes.d/myos.conf
   [remote "myos"]
   url=http://server.example.com:8000
   gpg-verify=true
   gpg-verify-summary=true

**Update Operations:**

.. code-block:: bash

   # Pull updates
   ostree pull myos:myos/x86_64/stable
   
   # Deploy update
   ostree admin deploy myos:myos/x86_64/stable
   
   # List deployments
   ostree admin status
   
   # Rollback
   ostree admin undeploy 0
   
   # Cleanup old deployments
   ostree admin cleanup
   
   # Boot into specific deployment
   ostree admin set-default 1

🔐 Secure OTA Updates
======================

Signature Verification
----------------------

**Create Signing Keys:**

.. code-block:: bash

   # RSA keys
   openssl genrsa -out private.pem 4096
   openssl rsa -in private.pem -pubout -out public.pem
   
   # Ed25519 keys (modern, smaller)
   openssl genpkey -algorithm Ed25519 -out private_ed25519.pem
   openssl pkey -in private_ed25519.pem -pubout -out public_ed25519.pem

**Sign Update Package:**

.. code-block:: bash

   # Create signature
   openssl dgst -sha256 -sign private.pem -out update.sig update.img
   
   # Verify signature
   openssl dgst -sha256 -verify public.pem -signature update.sig update.img
   
   # Embedded signature (combined file)
   cat update.img update.sig > update_signed.pkg

**Verification in Code:**

.. code-block:: c

   #include <openssl/rsa.h>
   #include <openssl/pem.h>
   #include <openssl/sha.h>
   
   int verify_signature(const char *public_key_file,
                        const char *data_file,
                        const char *sig_file)
   {
       FILE *fp;
       EVP_PKEY *pubkey;
       EVP_MD_CTX *ctx;
       unsigned char hash[SHA256_DIGEST_LENGTH];
       unsigned char *signature;
       size_t sig_len;
       int ret;
       
       // Load public key
       fp = fopen(public_key_file, "r");
       pubkey = PEM_read_PUBKEY(fp, NULL, NULL, NULL);
       fclose(fp);
       
       // Read signature
       fp = fopen(sig_file, "rb");
       fseek(fp, 0, SEEK_END);
       sig_len = ftell(fp);
       fseek(fp, 0, SEEK_SET);
       signature = malloc(sig_len);
       fread(signature, 1, sig_len, fp);
       fclose(fp);
       
       // Hash data file
       SHA256_File(data_file, hash);
       
       // Verify signature
       ctx = EVP_MD_CTX_new();
       EVP_DigestVerifyInit(ctx, NULL, EVP_sha256(), NULL, pubkey);
       EVP_DigestVerifyUpdate(ctx, hash, SHA256_DIGEST_LENGTH);
       ret = EVP_DigestVerifyFinal(ctx, signature, sig_len);
       
       EVP_MD_CTX_free(ctx);
       EVP_PKEY_free(pubkey);
       free(signature);
       
       return (ret == 1);
   }

Hash Verification
-----------------

**Manifest with Hashes:**

.. code-block:: json

   {
       "version": "1.0.0",
       "files": [
           {
               "name": "bootloader.bin",
               "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
               "size": 524288
           },
           {
               "name": "kernel.img",
               "sha256": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce",
               "size": 8388608
           },
           {
               "name": "rootfs.squashfs",
               "sha256": "f7fbba6e0636f890e56fbbf3283e524c6fa3204ae298382d624741d0dc6638326",
               "size": 268435456
           }
       ]
   }

**Verification Script:**

.. code-block:: python

   #!/usr/bin/env python3
   import hashlib
   import json
   import sys
   
   def verify_file(filepath, expected_hash, expected_size):
       """Verify file hash and size"""
       # Check size
       import os
       if os.path.getsize(filepath) != expected_size:
           return False
       
       # Calculate SHA256
       sha256 = hashlib.sha256()
       with open(filepath, 'rb') as f:
           while True:
               data = f.read(65536)  # 64KB chunks
               if not data:
                   break
               sha256.update(data)
       
       return sha256.hexdigest() == expected_hash
   
   def verify_update(manifest_file):
       """Verify all files in update package"""
       with open(manifest_file, 'r') as f:
           manifest = json.load(f)
       
       for file_info in manifest['files']:
           filepath = file_info['name']
           expected_hash = file_info['sha256']
           expected_size = file_info['size']
           
           print(f"Verifying {filepath}...")
           if not verify_file(filepath, expected_hash, expected_size):
               print(f"ERROR: Verification failed for {filepath}")
               return False
           print(f"OK: {filepath}")
       
       return True
   
   if __name__ == '__main__':
       if verify_update('manifest.json'):
           print("Update package verification successful")
           sys.exit(0)
       else:
           print("Update package verification FAILED")
           sys.exit(1)

Chain of Trust
--------------

.. code-block:: text

   Root CA Certificate (Factory)
       ↓ (signs)
   Intermediate CA Certificate (Company)
       ↓ (signs)
   Update Signing Certificate (Team)
       ↓ (signs)
   Update Package

**Certificate Chain Verification:**

.. code-block:: bash

   # Verify certificate chain
   openssl verify -CAfile root_ca.pem -untrusted intermediate_ca.pem signing_cert.pem
   
   # Extract public key from certificate
   openssl x509 -in signing_cert.pem -pubkey -noout > public_key.pem

🔄 Delta/Differential Updates
==============================

Binary Diff (bsdiff/bspatch)
----------------------------

**Create Delta:**

.. code-block:: bash

   # Install bsdiff
   sudo apt install bsdiff
   
   # Create binary diff
   bsdiff oldfile.img newfile.img delta.patch
   
   # File sizes comparison
   ls -lh oldfile.img newfile.img delta.patch

**Apply Delta:**

.. code-block:: bash

   # Apply patch
   bspatch oldfile.img newfile.img delta.patch
   
   # Verify
   sha256sum newfile.img

**In Code:**

.. code-block:: c

   #include <bspatch.h>
   
   int apply_delta_update(const char *old_file,
                          const char *new_file,
                          const char *patch_file)
   {
       FILE *old_fp = fopen(old_file, "rb");
       FILE *new_fp = fopen(new_file, "wb");
       FILE *patch_fp = fopen(patch_file, "rb");
       
       int ret = bspatch(old_fp, new_fp, patch_fp);
       
       fclose(old_fp);
       fclose(new_fp);
       fclose(patch_fp);
       
       return ret;
   }

Block-Level Delta (rsync algorithm)
------------------------------------

**Using rdiff:**

.. code-block:: bash

   # Create signature from old file
   rdiff signature oldfile.img oldfile.sig
   
   # Create delta using signature
   rdiff delta oldfile.sig newfile.img delta.rdiff
   
   # Apply delta
   rdiff patch oldfile.img delta.rdiff newfile.img

Casync (Content-Addressable Data Synchronization)
--------------------------------------------------

.. code-block:: bash

   # Create index and chunks
   casync make --store=store.castr oldfile.img.caidx oldfile.img
   
   # Create new version
   casync make --store=store.castr newfile.img.caidx newfile.img
   
   # Extract (downloads only changed chunks)
   casync extract --store=store.castr newfile.img.caidx newfile_restored.img

📡 OTA Delivery Mechanisms
===========================

HTTP/HTTPS Download
-------------------

**Simple Download Script:**

.. code-block:: bash

   #!/bin/bash
   
   UPDATE_URL="https://updates.example.com/firmware/latest.img"
   UPDATE_FILE="/tmp/update.img"
   UPDATE_SIG="/tmp/update.sig"
   PUBLIC_KEY="/etc/update-keys/public.pem"
   
   # Download update
   echo "Downloading update..."
   curl -L -o "$UPDATE_FILE" "$UPDATE_URL"
   curl -L -o "$UPDATE_SIG" "$UPDATE_URL.sig"
   
   # Verify signature
   echo "Verifying signature..."
   if openssl dgst -sha256 -verify "$PUBLIC_KEY" \
       -signature "$UPDATE_SIG" "$UPDATE_FILE"; then
       echo "Signature valid"
   else
       echo "ERROR: Invalid signature"
       exit 1
   fi
   
   # Install update
   echo "Installing update..."
   dd if="$UPDATE_FILE" of=/dev/mmcblk0p4 bs=1M status=progress
   
   # Mark for boot
   echo "b" > /boot/slot
   
   echo "Update complete. Reboot to apply."

**With Resume Support:**

.. code-block:: python

   #!/usr/bin/env python3
   import requests
   import os
   
   def download_with_resume(url, output_file):
       """Download file with resume support"""
       headers = {}
       mode = 'wb'
       
       if os.path.exists(output_file):
           # Resume from existing file
           existing_size = os.path.getsize(output_file)
           headers['Range'] = f'bytes={existing_size}-'
           mode = 'ab'
       
       response = requests.get(url, headers=headers, stream=True)
       
       if response.status_code in [200, 206]:  # OK or Partial Content
           total_size = int(response.headers.get('content-length', 0))
           
           with open(output_file, mode) as f:
               downloaded = existing_size if mode == 'ab' else 0
               
               for chunk in response.iter_content(chunk_size=8192):
                   if chunk:
                       f.write(chunk)
                       downloaded += len(chunk)
                       
                       # Progress
                       percent = (downloaded / total_size) * 100
                       print(f'\rDownload progress: {percent:.1f}%', end='')
           
           print('\nDownload complete')
           return True
       else:
           print(f'Download failed: HTTP {response.status_code}')
           return False

MQTT-Based OTA
--------------

**Publisher (Server):**

.. code-block:: python

   #!/usr/bin/env python3
   import paho.mqtt.client as mqtt
   import json
   import hashlib
   
   def publish_update(broker, topic, firmware_file):
       """Publish firmware update via MQTT"""
       
       # Calculate hash
       with open(firmware_file, 'rb') as f:
           firmware_data = f.read()
           firmware_hash = hashlib.sha256(firmware_data).hexdigest()
       
       # Publish metadata
       metadata = {
           'version': '1.0.5',
           'size': len(firmware_data),
           'sha256': firmware_hash,
           'url': f'https://updates.example.com/{firmware_file}'
       }
       
       client = mqtt.Client()
       client.connect(broker, 1883, 60)
       
       # Publish update notification
       client.publish(f'{topic}/available', json.dumps(metadata))
       
       # Optionally publish firmware in chunks
       chunk_size = 4096
       for i in range(0, len(firmware_data), chunk_size):
           chunk = firmware_data[i:i+chunk_size]
           client.publish(f'{topic}/firmware/{i}', chunk)
       
       client.disconnect()

**Subscriber (Device):**

.. code-block:: python

   #!/usr/bin/env python3
   import paho.mqtt.client as mqtt
   import json
   import hashlib
   
   def on_message(client, userdata, msg):
       """Handle incoming MQTT messages"""
       
       if msg.topic.endswith('/available'):
           # New update available
           metadata = json.loads(msg.payload)
           print(f"Update available: version {metadata['version']}")
           
           # Download and install
           download_and_install(metadata)
       
       elif '/firmware/' in msg.topic:
           # Firmware chunk received
           chunk_id = int(msg.topic.split('/')[-1])
           userdata['chunks'][chunk_id] = msg.payload
   
   def download_and_install(metadata):
       """Download and install firmware update"""
       # Implementation here
       pass
   
   client = mqtt.Client(userdata={'chunks': {}})
   client.on_message = on_message
   client.connect('broker.example.com', 1883, 60)
   client.subscribe('devices/+/ota/#')
   client.loop_forever()

Cellular OTA (CoAP)
-------------------

**CoAP Server:**

.. code-block:: python

   #!/usr/bin/env python3
   from aiocoap import *
   import asyncio
   
   class FirmwareResource(resource.Resource):
       """CoAP resource for firmware download"""
       
       def __init__(self, firmware_file):
           super().__init__()
           with open(firmware_file, 'rb') as f:
               self.firmware_data = f.read()
       
       async def render_get(self, request):
           """Handle GET request for firmware"""
           
           # Support block-wise transfer for large files
           if request.opt.block2 is not None:
               block_num = request.opt.block2.block_num
               block_size = request.opt.block2.size_exponent
               size = 2 ** (block_size + 4)
               
               start = block_num * size
               end = start + size
               
               payload = self.firmware_data[start:end]
               more = end < len(self.firmware_data)
               
               response = Message(code=CONTENT, payload=payload)
               response.opt.block2 = aiocoap.optiontypes.BlockOption.BlockwiseTuple(
                   block_num, more, block_size
               )
               return response
           
           return Message(code=CONTENT, payload=self.firmware_data)
   
   async def main():
       root = resource.Site()
       root.add_resource(['firmware', 'latest'], FirmwareResource('firmware.bin'))
       
       await aiocoap.Context.create_server_context(root)
       await asyncio.get_running_loop().create_future()
   
   if __name__ == '__main__':
       asyncio.run(main())

🔧 Bootloader Integration
===========================

U-Boot OTA Support
------------------

**Environment for OTA:**

.. code-block:: bash

   # Update information
   setenv update_available 0
   setenv update_version ""
   setenv update_url ""
   
   # Check for updates on boot
   setenv check_update '
       if tftp ${loadaddr} update_check.txt; then
           env import -t ${loadaddr} ${filesize}
           if test ${update_available} -eq 1; then
               echo "Update available: ${update_version}"
               echo "Run: run do_update"
           fi
       fi
   '
   
   # Download and install update
   setenv do_update '
       echo "Downloading update..."
       if tftp ${loadaddr} ${update_url}; then
           echo "Installing to inactive slot..."
           if test "${boot_slot}" = "a"; then
               mmc write ${loadaddr} 0x4000 0x10000
               setenv boot_slot b
           else
               mmc write ${loadaddr} 0x2000 0x10000
               setenv boot_slot a
           fi
           saveenv
           echo "Update installed. Rebooting..."
           reset
       else
           echo "Update download failed"
       fi
   '

GRUB OTA Support
----------------

.. code-block:: bash

   # /usr/local/bin/grub-ota-update
   #!/bin/bash
   
   INACTIVE_SLOT=""
   ACTIVE_SLOT=$(cat /boot/slot)
   
   if [ "$ACTIVE_SLOT" = "a" ]; then
       INACTIVE_SLOT="b"
       INACTIVE_PART="/dev/sda4"
   else
       INACTIVE_SLOT="a"
       INACTIVE_PART="/dev/sda3"
   fi
   
   # Download update
   echo "Downloading update to slot $INACTIVE_SLOT..."
   curl -o /tmp/update.img https://updates.example.com/latest.img
   
   # Verify
   curl -o /tmp/update.sig https://updates.example.com/latest.sig
   if ! openssl dgst -sha256 -verify /etc/update-key.pem \
           -signature /tmp/update.sig /tmp/update.img; then
       echo "ERROR: Signature verification failed"
       exit 1
   fi
   
   # Write to inactive partition
   echo "Installing update..."
   dd if=/tmp/update.img of=$INACTIVE_PART bs=1M status=progress
   
   # Switch boot slot
   echo "boot_slot=\"$INACTIVE_SLOT\"" > /boot/slot
   
   # Update GRUB default
   grub-reboot "System Slot $INACTIVE_SLOT"
   grub-set-default "System Slot $INACTIVE_SLOT"
   
   echo "Update complete. Reboot to activate."

📊 Monitoring & Rollback
=========================

Health Checks
-------------

**System Health Script:**

.. code-block:: python

   #!/usr/bin/env python3
   import os
   import time
   import subprocess
   
   def check_system_health():
       """Perform system health checks"""
       checks = []
       
       # Check connectivity
       ret = subprocess.call(['ping', '-c', '1', '8.8.8.8'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
       checks.append(('network', ret == 0))
       
       # Check services
       services = ['networking', 'ssh', 'myapp']
       for service in services:
           ret = subprocess.call(['systemctl', 'is-active', service],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
           checks.append((f'service_{service}', ret == 0))
       
       # Check disk space
       stat = os.statvfs('/')
       free_percent = (stat.f_bavail / stat.f_blocks) * 100
       checks.append(('disk_space', free_percent > 10))
       
       # Check memory
       with open('/proc/meminfo') as f:
           meminfo = dict(line.strip().split(':', 1) for line in f)
       mem_available = int(meminfo['MemAvailable'].split()[0])
       mem_total = int(meminfo['MemTotal'].split()[0])
       mem_percent = (mem_available / mem_total) * 100
       checks.append(('memory', mem_percent > 10))
       
       return all(result for _, result in checks), checks
   
   def main():
       """Monitor health and mark boot successful"""
       
       # Wait for system to stabilize
       time.sleep(30)
       
       # Run health checks
       healthy, checks = check_system_health()
       
       if healthy:
           print("System healthy, marking boot successful")
           # Mark boot successful (framework-specific)
           os.system('rauc status mark-good')  # RAUC
           # or
           os.system('mender commit')  # Mender
           # or
           os.system('fw_setenv upgrade_available 0')  # U-Boot
       else:
           print("System unhealthy:")
           for name, result in checks:
               print(f"  {name}: {'OK' if result else 'FAIL'}")
           print("System will rollback on next boot")
   
   if __name__ == '__main__':
       main()

Automatic Rollback
------------------

**Systemd Service (health-check.service):**

.. code-block:: ini

   [Unit]
   Description=System Health Check
   After=network.target multi-user.target
   
   [Service]
   Type=oneshot
   ExecStart=/usr/local/bin/health-check.py
   RemainAfterExit=yes
   
   [Install]
   WantedBy=multi-user.target

**Watchdog Integration:**

.. code-block:: python

   #!/usr/bin/env python3
   import systemd.daemon
   import time
   
   def main():
       """Watchdog-enabled service"""
       
       # Notify systemd we're ready
       systemd.daemon.notify('READY=1')
       
       while True:
           # Do work
           perform_tasks()
           
           # Notify watchdog
           systemd.daemon.notify('WATCHDOG=1')
           
           time.sleep(10)
   
   if __name__ == '__main__':
       main()

📚 Best Practices
==================

Update Strategy
---------------

1. **Always use A/B partitioning** for critical systems
2. **Verify signatures** before applying updates
3. **Test updates** in staging environment first
4. **Implement health checks** post-update
5. **Enable automatic rollback** on failure
6. **Use delta updates** to minimize bandwidth
7. **Maintain golden image** as last resort
8. **Version tracking** to prevent downgrades
9. **Atomic updates** - all or nothing
10. **User notification** before/during updates

Security Checklist
------------------

- [ ] Cryptographic signature verification
- [ ] Secure communication channel (TLS/HTTPS)
- [ ] Certificate pinning for critical servers
- [ ] Hash verification for integrity
- [ ] Anti-rollback protection
- [ ] Secure boot chain integration
- [ ] Key rotation capability
- [ ] Revocation mechanism for compromised keys
- [ ] Encrypted update packages (optional)
- [ ] Audit logging for update events

Reliability Checklist
---------------------

- [ ] Redundant boot slots (A/B)
- [ ] Power-loss resilience
- [ ] Network failure recovery
- [ ] Partial update recovery
- [ ] Rollback mechanism
- [ ] Golden image backup
- [ ] Health monitoring post-update
- [ ] Boot counter with automatic fallback
- [ ] Update retry logic
- [ ] Progress indicators

📖 References
==============

Frameworks & Tools
------------------

* **RAUC**: https://rauc.io/
* **SWUpdate**: https://sbabic.github.io/swupdate/
* **Mender**: https://mender.io/
* **OSTree**: https://ostreedev.github.io/ostree/
* **Balena**: https://www.balena.io/
* **Hawkbit**: https://www.eclipse.org/hawkbit/

Standards & Protocols
---------------------

* **SUIT (Software Updates for IoT)**: RFC 9019
* **LwM2M Firmware Update**: OMA TS LightweightM2M
* **CoAP**: RFC 7252
* **DFU (USB)**: USB DFU Class Specification
* **Android A/B**: https://source.android.com/devices/tech/ota/ab

Books & Articles
----------------

* "Embedded Linux Systems with Yocto Project" - OTA chapters
* "Building Embedded Linux Systems" - Update mechanisms
* "Linux System Programming" - Atomic operations

================================
Last Updated: January 2026
Version: 3.0
================================
