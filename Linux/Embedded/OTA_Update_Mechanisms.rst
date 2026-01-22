=====================================
OTA Update Mechanisms - Complete Guide
=====================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Reference: Smart Home Hub (i.MX 93), Avionics Platform (Intel Atom), E-Bike Infotainment

.. contents:: Table of Contents
   :depth: 4
   :local:

====================
1. Overview
====================

Comprehensive guide to Over-The-Air (OTA) update mechanisms for embedded Linux systems,
covering secure delivery, A/B partitioning, delta updates, and field deployment strategies.

**Project Context**:

- **Smart Home Hub** (i.MX 93): Cellular OTA, 1,250 deployed devices, 99.76% success rate
- **Avionics Platform** (Intel Atom): Secure OTA for DO-178C compliance
- **E-Bike Infotainment**: Bluetooth/Wi-Fi OTA with automotive requirements
- **AFIRS SDU**: Satellite OTA for aircraft communication systems

**OTA Requirements**:

.. code-block:: text

    Security:
    - Signed updates (RSA-2048/4096)
    - Encrypted payload (AES-256)
    - Secure boot integration
    - Revocation support
    
    Reliability:
    - Atomic updates
    - Rollback on failure
    - Power-loss resilience
    - Update verification
    
    Efficiency:
    - Delta updates (binary diff)
    - Compressed payloads
    - Resume capability
    - Bandwidth optimization

====================
2. OTA Architecture Patterns
====================

2.1 A/B (Seamless) Updates
---------------------------

**Partition Layout**:

.. code-block:: text

    /dev/mmcblk0p1: boot (bootloader, shared)
    /dev/mmcblk0p2: system_a (Active OS)
    /dev/mmcblk0p3: system_b (Inactive OS)
    /dev/mmcblk0p4: data (persistent, shared)
    
    Update Flow:
    1. System running from partition A
    2. Download update to partition B
    3. Verify update on partition B
    4. Mark partition B as active
    5. Reboot → boot from partition B
    6. If boot fails: automatic rollback to A

**Advantages**:

- No downtime (seamless background update)
- Fast rollback (just change boot partition)
- Original system untouched during update

**Disadvantages**:

- Double storage requirement
- Full system image download (large)

2.2 Recovery Partition
----------------------

**Layout**:

.. code-block:: text

    /dev/mmcblk0p1: boot
    /dev/mmcblk0p2: recovery (minimal Linux)
    /dev/mmcblk0p3: system (main OS)
    /dev/mmcblk0p4: data
    
    Update Flow:
    1. Download update package to data partition
    2. Reboot into recovery partition
    3. Recovery applies update to system partition
    4. Reboot into updated system

**Advantages**:

- Less storage overhead
- Supports delta updates
- Recovery environment for failures

2.3 Atomic Update (OSTree/libostree)
-------------------------------------

**Concept**:

.. code-block:: text

    - Filesystem stored as Git-like objects
    - Immutable OS trees
    - Hardlinked files (deduplication)
    - Atomic deployment switching
    
    /ostree
    ├── repo/             # Object store
    │   ├── objects/      # File contents (content-addressed)
    │   └── refs/         # Named references
    └── deploy/
        └── os/
            ├── deploy/
            │   ├── 1234abcd.0/  # Deployment 1
            │   └── 5678ef90.0/  # Deployment 2 (new)
            └── current -> deploy/5678ef90.0

**Advantages**:

- Atomic updates (all or nothing)
- Easy rollback (switch symlink)
- Efficient storage (hardlinks)
- Delta support

====================
3. Secure Update Delivery
====================

3.1 Update Package Format
--------------------------

**SWUpdate Package** (`.swu` file):

.. code-block:: text

    update.swu (CPIO archive)
    ├── sw-description         # Update metadata
    ├── sw-description.sig     # Signature
    ├── rootfs.ext4.gz         # Compressed rootfs
    ├── uImage                 # Kernel
    ├── devicetree.dtb         # Device tree
    └── scripts/
        ├── pre-install.sh
        └── post-install.sh

**sw-description Format**:

.. code-block:: text

    software =
    {
        version = "1.2.3";
        
        hardware-compatibility = [ "1.0" ];
        
        images: (
            {
                filename = "rootfs.ext4.gz";
                type = "raw";
                compressed = "zlib";
                sha256 = "abc123...";
                device = "/dev/mmcblk0p3";
            },
            {
                filename = "uImage";
                type = "raw";
                sha256 = "def456...";
                device = "/dev/mmcblk0p1";
                offset = "0x100000";
            }
        );
        
        scripts: (
            {
                filename = "pre-install.sh";
                type = "shellscript";
            },
            {
                filename = "post-install.sh";
                type = "shellscript";
            }
        );
        
        bootenv: (
            {
                name = "bootpart";
                value = "3";
            },
            {
                name = "upgrade_available";
                value = "1";
            }
        );
    }

3.2 Update Signing
------------------

**Generate RSA Keys**:

.. code-block:: bash

    # Generate private key
    openssl genrsa -out swupdate-priv.pem 4096
    
    # Extract public key
    openssl rsa -in swupdate-priv.pem -out swupdate-pub.pem -pubout
    
    # Convert to DER format (for embedded verification)
    openssl rsa -in swupdate-pub.pem -pubin -outform DER -out swupdate-pub.der

**Sign Update Package**:

.. code-block:: bash

    # Sign sw-description
    openssl dgst -sha256 -sign swupdate-priv.pem \
        sw-description > sw-description.sig
    
    # Create SWU package
    FILES="sw-description sw-description.sig rootfs.ext4.gz uImage devicetree.dtb"
    for f in $FILES; do echo $f; done | cpio -ov -H crc > update.swu

**Verify Signature** (C code):

.. code-block:: c

    #include <openssl/rsa.h>
    #include <openssl/pem.h>
    #include <openssl/sha.h>
    
    int verify_update_signature(const char *pub_key_file,
                                 const uint8_t *sw_desc,
                                 size_t sw_desc_len,
                                 const uint8_t *signature,
                                 size_t sig_len)
    {
        FILE *fp;
        RSA *rsa;
        EVP_PKEY *pkey;
        uint8_t hash[SHA256_DIGEST_LENGTH];
        int ret;
        
        /* Load public key */
        fp = fopen(pub_key_file, "r");
        pkey = PEM_read_PUBKEY(fp, NULL, NULL, NULL);
        fclose(fp);
        
        rsa = EVP_PKEY_get1_RSA(pkey);
        
        /* Calculate SHA-256 hash */
        SHA256(sw_desc, sw_desc_len, hash);
        
        /* Verify signature */
        ret = RSA_verify(NID_sha256, hash, sizeof(hash),
                        signature, sig_len, rsa);
        
        RSA_free(rsa);
        EVP_PKEY_free(pkey);
        
        return ret;  /* 1 = valid, 0 = invalid */
    }

3.3 Encrypted Updates
----------------------

**AES-256-GCM Encryption**:

.. code-block:: bash

    # Generate random encryption key
    openssl rand -out update.key 32  # 256-bit key
    
    # Encrypt update package
    openssl enc -aes-256-gcm -in rootfs.ext4 -out rootfs.ext4.enc \
        -K $(hexdump -ve '1/1 "%.2x"' update.key) \
        -iv $(openssl rand -hex 12)  # 96-bit IV for GCM
    
    # Encrypt key with RSA (for secure distribution)
    openssl rsautl -encrypt -pubin -inkey device-pub.pem \
        -in update.key -out update.key.enc

**Decrypt on Device**:

.. code-block:: c

    int decrypt_update(const uint8_t *enc_data, size_t enc_len,
                      const uint8_t *key, size_t key_len,
                      const uint8_t *iv, size_t iv_len,
                      uint8_t *plain_data)
    {
        EVP_CIPHER_CTX *ctx;
        int len, plaintext_len;
        
        ctx = EVP_CIPHER_CTX_new();
        
        /* Initialize decryption */
        EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv);
        
        /* Decrypt */
        EVP_DecryptUpdate(ctx, plain_data, &len, enc_data, enc_len);
        plaintext_len = len;
        
        /* Finalize */
        EVP_DecryptFinal_ex(ctx, plain_data + len, &len);
        plaintext_len += len;
        
        EVP_CIPHER_CTX_free(ctx);
        
        return plaintext_len;
    }

====================
4. A/B Update Implementation
====================

4.1 U-Boot A/B Logic
--------------------

**Environment Variables**:

.. code-block:: bash

    # Boot configuration
    setenv bootpart 2              # Currently active partition (A=2, B=3)
    setenv upgrade_available 0     # 1 if new update installed
    setenv bootcount 0             # Number of boot attempts
    setenv bootlimit 3             # Max boot attempts before rollback

**Boot Script** (`boot.scr`):

.. code-block:: text

    # Increment boot count
    setexpr bootcount ${bootcount} + 1
    saveenv
    
    # Check if exceeded boot limit
    if test ${bootcount} -gt ${bootlimit}; then
        echo "Boot failed ${bootlimit} times, rolling back..."
        
        # Switch partition
        if test ${bootpart} = 2; then
            setenv bootpart 3
        else
            setenv bootpart 2
        fi
        
        # Reset boot count
        setenv bootcount 0
        setenv upgrade_available 0
        saveenv
        
        echo "Rolled back to partition ${bootpart}"
    fi
    
    # Load kernel from active partition
    ext4load mmc 0:${bootpart} ${loadaddr} /boot/uImage
    ext4load mmc 0:${bootpart} ${fdt_addr} /boot/devicetree.dtb
    
    # Boot
    bootm ${loadaddr} - ${fdt_addr}

**Confirm Successful Boot** (Linux userspace):

.. code-block:: bash

    #!/bin/bash
    # /usr/bin/confirm-boot.sh
    
    UPGRADE_AVAILABLE=$(fw_printenv -n upgrade_available)
    
    if [ "$UPGRADE_AVAILABLE" = "1" ]; then
        echo "New update confirmed successful"
        
        # Reset boot count and upgrade flag
        fw_setenv bootcount 0
        fw_setenv upgrade_available 0
        
        # Log successful update
        logger "OTA update confirmed successful"
    fi

**Systemd Service**:

.. code-block:: ini

    # /etc/systemd/system/confirm-boot.service
    
    [Unit]
    Description=Confirm successful boot after OTA update
    After=multi-user.target
    
    [Service]
    Type=oneshot
    ExecStart=/usr/bin/confirm-boot.sh
    
    [Install]
    WantedBy=multi-user.target

4.2 SWUpdate Integration
-------------------------

**SWUpdate Configuration** (`/etc/swupdate.cfg`):

.. code-block:: text

    globals =
    {
        verbose = true;
        loglevel = 5;
        syslog = true;
    };
    
    identify : (
        {
            name = "board";
            value = "smarthome-hub";
        },
        {
            name = "hwrevision";
            value = "1.0";
        }
    );
    
    suricatta =
    {
        tenant = "default";
        id = "smarthome-001";
        url = "https://ota.example.com";
        polldelay = 300;  # Check for updates every 5 minutes
        
        ssl-cert = "/etc/swupdate/client.crt";
        ssl-key = "/etc/swupdate/client.key";
        ssl-ca = "/etc/swupdate/ca.crt";
    };

**Start SWUpdate Daemon**:

.. code-block:: bash

    # Manual start
    swupdate -v -w "-document_root /var/www" -p 'reboot' \
        -k /etc/swupdate/swupdate-pub.pem
    
    # -v: verbose
    # -w: built-in web server
    # -p 'reboot': post-update action
    # -k: public key for signature verification
    
    # Or via systemd
    systemctl start swupdate

**Install Update via HTTP**:

.. code-block:: bash

    # Upload update package
    curl -X POST -F "file=@update.swu" http://device-ip:8080/upload
    
    # Or use swupdate-client
    swupdate-client -u update.swu

4.3 OTA Client Application
---------------------------

**Python OTA Client**:

.. code-block:: python

    #!/usr/bin/env python3
    import os
    import sys
    import json
    import hashlib
    import requests
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.x509 import load_pem_x509_certificate
    
    class OTAClient:
        def __init__(self, server_url, device_id, cert_path):
            self.server_url = server_url
            self.device_id = device_id
            
            with open(cert_path, 'rb') as f:
                self.cert = load_pem_x509_certificate(f.read())
            
            self.current_version = self._get_current_version()
        
        def check_update(self):
            """Check if update is available"""
            try:
                resp = requests.get(
                    f"{self.server_url}/api/devices/{self.device_id}/update",
                    params={'current_version': self.current_version},
                    timeout=30
                )
                
                if resp.status_code == 200:
                    update_info = resp.json()
                    if update_info['available']:
                        print(f"Update available: {update_info['version']}")
                        return update_info
                    else:
                        print("No update available")
                        return None
                else:
                    print(f"Error checking update: {resp.status_code}")
                    return None
            
            except requests.RequestException as e:
                print(f"Network error: {e}")
                return None
        
        def download_update(self, update_info):
            """Download update package"""
            print(f"Downloading update {update_info['version']}...")
            
            update_url = f"{self.server_url}{update_info['package_url']}"
            
            # Download with progress
            resp = requests.get(update_url, stream=True)
            total_size = int(resp.headers.get('content-length', 0))
            
            update_file = '/tmp/update.swu'
            downloaded = 0
            
            with open(update_file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end='', flush=True)
            
            print("\nDownload complete")
            
            # Verify hash
            with open(update_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash != update_info['sha256']:
                print(f"Hash mismatch! Expected {update_info['sha256']}, got {file_hash}")
                os.remove(update_file)
                return None
            
            print("Hash verified")
            return update_file
        
        def install_update(self, update_file):
            """Install update using SWUpdate"""
            print("Installing update...")
            
            # Determine inactive partition
            active_part = self._get_active_partition()
            inactive_part = 3 if active_part == 2 else 2
            
            print(f"Active partition: {active_part}, updating partition: {inactive_part}")
            
            # Install via SWUpdate
            ret = os.system(f"swupdate -i {update_file}")
            
            if ret == 0:
                print("Update installed successfully")
                
                # Mark for boot confirmation
                os.system(f"fw_setenv bootpart {inactive_part}")
                os.system("fw_setenv upgrade_available 1")
                os.system("fw_setenv bootcount 0")
                
                return True
            else:
                print(f"Update installation failed: {ret}")
                return False
        
        def apply_update(self):
            """Reboot to apply update"""
            print("Rebooting to apply update...")
            os.system("reboot")
        
        def _get_current_version(self):
            """Read current software version"""
            try:
                with open('/etc/version', 'r') as f:
                    return f.read().strip()
            except:
                return "unknown"
        
        def _get_active_partition(self):
            """Get currently active partition"""
            result = os.popen("fw_printenv -n bootpart").read().strip()
            return int(result) if result else 2
    
    def main():
        # Configuration
        SERVER_URL = "https://ota.example.com"
        DEVICE_ID = "smarthome-001"
        CERT_PATH = "/etc/swupdate/ca.crt"
        
        client = OTAClient(SERVER_URL, DEVICE_ID, CERT_PATH)
        
        # Check for update
        update_info = client.check_update()
        
        if update_info:
            # Download
            update_file = client.download_update(update_info)
            
            if update_file:
                # Install
                if client.install_update(update_file):
                    # Apply (reboot)
                    client.apply_update()
    
    if __name__ == '__main__':
        main()

====================
5. Delta Updates
====================

5.1 Binary Diff (bsdiff/bspatch)
---------------------------------

**Generate Delta**:

.. code-block:: bash

    # Create binary diff
    bsdiff old_rootfs.img new_rootfs.img rootfs.patch
    
    # Compress patch
    gzip rootfs.patch
    
    # Size comparison
    # old_rootfs.img: 450 MB
    # new_rootfs.img: 450 MB
    # rootfs.patch.gz: 12 MB (97% reduction!)

**Apply Delta** (on device):

.. code-block:: bash

    # Decompress patch
    gunzip rootfs.patch.gz
    
    # Apply patch to create new image
    bspatch /dev/mmcblk0p2 /dev/mmcblk0p3 rootfs.patch
    
    # Verify new image
    sha256sum /dev/mmcblk0p3

**bspatch C Integration**:

.. code-block:: c

    #include <bspatch.h>
    
    int apply_delta_update(const char *old_file, const char *new_file,
                          const char *patch_file)
    {
        int ret;
        
        ret = bspatch(old_file, new_file, patch_file);
        
        if (ret == 0) {
            printf("Delta applied successfully\n");
        } else {
            fprintf(stderr, "Delta application failed: %d\n", ret);
        }
        
        return ret;
    }

5.2 File-Based Delta (rsync algorithm)
---------------------------------------

**Generate File List with Hashes**:

.. code-block:: python

    import os
    import hashlib
    import json
    
    def generate_file_manifest(root_dir):
        """Generate manifest of all files with hashes"""
        manifest = {}
        
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                relpath = os.path.relpath(filepath, root_dir)
                
                # Calculate SHA-256
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                manifest[relpath] = {
                    'hash': file_hash,
                    'size': os.path.getsize(filepath),
                    'mode': oct(os.stat(filepath).st_mode)[-3:]
                }
        
        return manifest
    
    # Generate manifests
    old_manifest = generate_file_manifest('/mnt/old_rootfs')
    new_manifest = generate_file_manifest('/mnt/new_rootfs')
    
    # Find differences
    delta = {
        'added': [],
        'modified': [],
        'removed': []
    }
    
    # Added and modified files
    for path, info in new_manifest.items():
        if path not in old_manifest:
            delta['added'].append({'path': path, 'info': info})
        elif old_manifest[path]['hash'] != info['hash']:
            delta['modified'].append({'path': path, 'info': info})
    
    # Removed files
    for path in old_manifest:
        if path not in new_manifest:
            delta['removed'].append(path)
    
    # Save delta manifest
    with open('delta_manifest.json', 'w') as f:
        json.dump(delta, f, indent=2)

**Apply File-Based Delta**:

.. code-block:: python

    def apply_file_delta(delta_manifest, delta_files_dir, target_dir):
        """Apply file-level delta update"""
        
        # Remove files
        for path in delta_manifest['removed']:
            target_path = os.path.join(target_dir, path)
            if os.path.exists(target_path):
                os.remove(target_path)
                print(f"Removed: {path}")
        
        # Add new files
        for item in delta_manifest['added']:
            src_path = os.path.join(delta_files_dir, item['path'])
            dst_path = os.path.join(target_dir, item['path'])
            
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            os.chmod(dst_path, int(item['info']['mode'], 8))
            print(f"Added: {item['path']}")
        
        # Update modified files
        for item in delta_manifest['modified']:
            src_path = os.path.join(delta_files_dir, item['path'])
            dst_path = os.path.join(target_dir, item['path'])
            
            shutil.copy2(src_path, dst_path)
            os.chmod(dst_path, int(item['info']['mode'], 8))
            print(f"Modified: {item['path']}")

**Project Results** (Smart Home Hub):

.. code-block:: text

    Update Size Comparison (version 1.1 → 1.2):
    
    Full Update:
    - Compressed rootfs: 85 MB
    - Kernel + DTB: 8 MB
    - Total: 93 MB
    - Download time (cellular): ~3.5 minutes
    
    Delta Update:
    - Binary diff (bsdiff): 12 MB
    - Modified files: 18 files, 3.2 MB
    - Total: 15.2 MB
    - Download time: ~35 seconds
    
    Savings: 84% reduction in download size

====================
6. Resume and Recovery
====================

6.1 Download Resume
-------------------

**HTTP Range Requests**:

.. code-block:: python

    def download_with_resume(url, dest_file, expected_sha256=None):
        """Download file with resume support"""
        
        # Check if partial file exists
        if os.path.exists(dest_file):
            downloaded_size = os.path.getsize(dest_file)
            mode = 'ab'  # Append mode
        else:
            downloaded_size = 0
            mode = 'wb'  # Write mode
        
        # Request with Range header
        headers = {}
        if downloaded_size > 0:
            headers['Range'] = f'bytes={downloaded_size}-'
            print(f"Resuming download from byte {downloaded_size}")
        
        resp = requests.get(url, headers=headers, stream=True, timeout=30)
        
        # Check if server supports range requests
        if downloaded_size > 0 and resp.status_code != 206:
            print("Server doesn't support resume, restarting download")
            downloaded_size = 0
            mode = 'wb'
            resp = requests.get(url, stream=True, timeout=30)
        
        total_size = int(resp.headers.get('content-length', 0)) + downloaded_size
        
        # Download
        with open(dest_file, mode) as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded_size += len(chunk)
                
                progress = (downloaded_size / total_size) * 100
                print(f"\rProgress: {progress:.1f}%", end='', flush=True)
        
        print("\nDownload complete")
        
        # Verify hash
        if expected_sha256:
            with open(dest_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash != expected_sha256:
                raise ValueError(f"Hash mismatch: {file_hash} != {expected_sha256}")
            
            print("Hash verified")
        
        return dest_file

6.2 Power-Loss Protection
--------------------------

**Atomic Writes with fsync**:

.. code-block:: c

    int write_update_atomically(const char *data, size_t len,
                                const char *dest_file)
    {
        char temp_file[PATH_MAX];
        int fd;
        ssize_t written;
        
        /* Write to temporary file */
        snprintf(temp_file, sizeof(temp_file), "%s.tmp", dest_file);
        
        fd = open(temp_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd < 0)
            return -1;
        
        written = write(fd, data, len);
        if (written != len) {
            close(fd);
            unlink(temp_file);
            return -1;
        }
        
        /* Sync to storage */
        fsync(fd);
        close(fd);
        
        /* Atomic rename */
        if (rename(temp_file, dest_file) < 0) {
            unlink(temp_file);
            return -1;
        }
        
        /* Sync directory */
        fd = open(dirname(dest_file), O_RDONLY);
        fsync(fd);
        close(fd);
        
        return 0;
    }

**Update State Machine** (persisted):

.. code-block:: c

    enum update_state {
        UPDATE_IDLE,
        UPDATE_DOWNLOADING,
        UPDATE_DOWNLOADED,
        UPDATE_VERIFYING,
        UPDATE_INSTALLING,
        UPDATE_INSTALLED,
        UPDATE_FAILED
    };
    
    struct update_context {
        enum update_state state;
        char update_file[PATH_MAX];
        size_t downloaded_bytes;
        size_t total_bytes;
        char error_msg[256];
    };
    
    /* Save state to persistent storage */
    int save_update_state(struct update_context *ctx)
    {
        int fd;
        
        fd = open("/data/update_state.dat", O_WRONLY | O_CREAT | O_TRUNC, 0600);
        write(fd, ctx, sizeof(*ctx));
        fsync(fd);
        close(fd);
        
        return 0;
    }
    
    /* Restore state after power loss */
    int restore_update_state(struct update_context *ctx)
    {
        int fd;
        
        fd = open("/data/update_state.dat", O_RDONLY);
        if (fd < 0)
            return -1;  /* No saved state */
        
        read(fd, ctx, sizeof(*ctx));
        close(fd);
        
        return 0;
    }

6.3 Rollback Mechanisms
------------------------

**Automatic Rollback** (boot counter):

.. code-block:: bash

    # U-Boot boot script (see section 4.1)
    # Automatically rolls back after 3 failed boot attempts

**Manual Rollback**:

.. code-block:: bash

    #!/bin/bash
    # rollback.sh
    
    CURRENT_PART=$(fw_printenv -n bootpart)
    
    if [ "$CURRENT_PART" = "2" ]; then
        NEW_PART=3
    else
        NEW_PART=2
    fi
    
    echo "Rolling back from partition $CURRENT_PART to $NEW_PART"
    
    fw_setenv bootpart $NEW_PART
    fw_setenv bootcount 0
    fw_setenv upgrade_available 0
    
    reboot

**Version Pinning**:

.. code-block:: bash

    # /etc/swupdate/versions.conf
    
    # Minimum allowed version (can't downgrade below this)
    minimum_version=1.0.0
    
    # Current version
    current_version=1.2.3
    
    # Rollback target (if current fails)
    rollback_version=1.2.2

====================
7. OTA Server Implementation
====================

7.1 Update Server API
---------------------

**RESTful API Design**:

.. code-block:: text

    GET /api/devices/:device_id/update
        Parameters: current_version
        Response: {
            "available": true,
            "version": "1.2.3",
            "package_url": "/updates/device123/update-1.2.3.swu",
            "sha256": "abc123...",
            "size": 15728640,
            "release_notes": "Bug fixes and improvements"
        }
    
    GET /updates/:device_id/:filename
        Response: Update package file (with Range support)
    
    POST /api/devices/:device_id/status
        Body: {
            "current_version": "1.2.3",
            "update_status": "success",
            "timestamp": "2026-01-22T12:34:56Z"
        }

**Flask Server Implementation**:

.. code-block:: python

    from flask import Flask, jsonify, send_file, request, abort
    import os
    import hashlib
    
    app = Flask(__name__)
    
    # Device database (simplified)
    DEVICES = {
        'smarthome-001': {
            'hardware': 'smarthome-hub',
            'current_version': '1.2.2',
            'target_version': '1.2.3'
        }
    }
    
    # Available updates
    UPDATES = {
        '1.2.3': {
            'filename': 'update-1.2.3.swu',
            'sha256': 'abc123def456...',
            'size': 15728640,
            'release_notes': 'Bug fixes and security improvements'
        }
    }
    
    @app.route('/api/devices/<device_id>/update', methods=['GET'])
    def check_update(device_id):
        """Check if update is available for device"""
        
        if device_id not in DEVICES:
            abort(404, "Device not found")
        
        device = DEVICES[device_id]
        current_version = request.args.get('current_version', device['current_version'])
        target_version = device['target_version']
        
        if current_version != target_version and target_version in UPDATES:
            update = UPDATES[target_version]
            return jsonify({
                'available': True,
                'version': target_version,
                'package_url': f'/updates/{device_id}/{update["filename"]}',
                'sha256': update['sha256'],
                'size': update['size'],
                'release_notes': update['release_notes']
            })
        else:
            return jsonify({'available': False})
    
    @app.route('/updates/<device_id>/<filename>', methods=['GET'])
    def download_update(device_id, filename):
        """Download update package with Range support"""
        
        if device_id not in DEVICES:
            abort(404, "Device not found")
        
        file_path = os.path.join('/var/ota/updates', filename)
        
        if not os.path.exists(file_path):
            abort(404, "Update file not found")
        
        # Handle Range requests (for resume)
        range_header = request.headers.get('Range')
        
        if range_header:
            # Parse Range header: "bytes=start-end"
            byte_range = range_header.replace('bytes=', '').split('-')
            start = int(byte_range[0])
            end = int(byte_range[1]) if byte_range[1] else None
            
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as f:
                f.seek(start)
                if end:
                    data = f.read(end - start + 1)
                else:
                    data = f.read()
            
            response = app.response_class(data, 206)  # Partial Content
            response.headers['Content-Range'] = f'bytes {start}-{file_size-1}/{file_size}'
            response.headers['Accept-Ranges'] = 'bytes'
            return response
        else:
            return send_file(file_path, as_attachment=True)
    
    @app.route('/api/devices/<device_id>/status', methods=['POST'])
    def update_status(device_id):
        """Report update status from device"""
        
        if device_id not in DEVICES:
            abort(404, "Device not found")
        
        status_data = request.json
        
        # Log update status
        print(f"Device {device_id} reported status: {status_data}")
        
        # Update database
        if status_data['update_status'] == 'success':
            DEVICES[device_id]['current_version'] = status_data['current_version']
        
        return jsonify({'status': 'ok'})
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))

7.2 Staged Rollout
------------------

**Gradual Deployment Strategy**:

.. code-block:: python

    import random
    
    class StagedRollout:
        def __init__(self):
            self.stages = [
                {'percentage': 1, 'duration_hours': 24},   # 1% for 24 hours
                {'percentage': 10, 'duration_hours': 48},  # 10% for 48 hours
                {'percentage': 50, 'duration_hours': 72},  # 50% for 72 hours
                {'percentage': 100, 'duration_hours': 0}   # 100% (all remaining)
            ]
            self.start_time = None
            self.current_stage = 0
        
        def should_update(self, device_id):
            """Determine if device should receive update"""
            
            if self.current_stage >= len(self.stages):
                return True  # All stages complete
            
            stage = self.stages[self.current_stage]
            
            # Deterministic selection based on device ID hash
            device_hash = int(hashlib.sha256(device_id.encode()).hexdigest(), 16)
            device_percentage = (device_hash % 100) + 1
            
            return device_percentage <= stage['percentage']
        
        def advance_stage(self):
            """Move to next rollout stage"""
            self.current_stage += 1

7.3 Fleet Management
--------------------

**Device Statistics Dashboard**:

.. code-block:: python

    def get_fleet_statistics():
        """Get update statistics across all devices"""
        
        stats = {
            'total_devices': len(DEVICES),
            'versions': {},
            'update_pending': 0,
            'update_success': 0,
            'update_failed': 0
        }
        
        for device_id, device in DEVICES.items():
            version = device['current_version']
            stats['versions'][version] = stats['versions'].get(version, 0) + 1
            
            if device.get('update_status') == 'pending':
                stats['update_pending'] += 1
            elif device.get('update_status') == 'success':
                stats['update_success'] += 1
            elif device.get('update_status') == 'failed':
                stats['update_failed'] += 1
        
        return stats

====================
8. Automotive OTA (E-Bike Example)
====================

8.1 SOTA vs FOTA
----------------

**SOTA (Software Over-The-Air)**:

- Application updates
- User interface updates
- Configuration changes
- No hardware/firmware changes

**FOTA (Firmware Over-The-Air)**:

- ECU firmware updates
- Bootloader updates
- Low-level system updates
- Requires safety validation

8.2 ECU Update Coordination
----------------------------

**Multi-ECU Update Orchestration**:

.. code-block:: python

    class ECUUpdateOrchestrator:
        def __init__(self):
            self.ecus = {
                'bms': {'address': 0x10, 'version': '2.1.0'},
                'motor': {'address': 0x20, 'version': '1.5.2'},
                'display': {'address': 0x30, 'version': '3.0.1'}
            }
        
        def update_ecu(self, ecu_name, firmware_file):
            """Update specific ECU firmware"""
            
            ecu = self.ecus[ecu_name]
            
            # 1. Enter bootloader mode
            self._send_can_command(ecu['address'], 'ENTER_BOOTLOADER')
            
            # 2. Erase flash
            self._send_can_command(ecu['address'], 'ERASE_FLASH')
            
            # 3. Program firmware
            with open(firmware_file, 'rb') as f:
                while True:
                    chunk = f.read(256)
                    if not chunk:
                        break
                    self._send_can_data(ecu['address'], chunk)
            
            # 4. Verify
            checksum = self._calculate_checksum(firmware_file)
            ecu_checksum = self._get_can_response(ecu['address'], 'GET_CHECKSUM')
            
            if checksum != ecu_checksum:
                raise ValueError("Checksum mismatch!")
            
            # 5. Reset ECU
            self._send_can_command(ecu['address'], 'RESET')
            
            print(f"ECU {ecu_name} updated successfully")
        
        def _send_can_command(self, address, command):
            """Send CAN command to ECU"""
            # Implementation using SocketCAN
            pass

8.3 Safety and Compliance
--------------------------

**ISO 26262 OTA Requirements**:

.. code-block:: text

    1. Update Authentication:
       - Cryptographic signatures
       - Certificate-based trust chain
       - Revocation support
    
    2. Update Integrity:
       - End-to-end checksums
       - Memory verification
       - Rollback protection
    
    3. Safe State:
       - Vehicle parked (ignition off)
       - Battery voltage adequate
       - No active faults
    
    4. Failure Handling:
       - Automatic rollback
       - Diagnostic logging
       - User notification
    
    5. Audit Trail:
       - Update history
       - Timestamp logging
       - Success/failure tracking

====================
9. Project Results
====================

**Smart Home Hub (i.MX 93)**:

.. code-block:: text

    Deployment:
    - Total devices: 1,250
    - Geographic distribution: North America
    - Network: Cellular (LTE Cat-M1)
    
    Update Campaign (v1.1 → v1.2):
    - Update type: Delta (bsdiff)
    - Package size: 15.2 MB
    - Staged rollout: 1% → 10% → 50% → 100%
    - Duration: 7 days
    
    Results:
    - Successful updates: 1,247 (99.76%)
    - Failed updates: 3
      * 2: Network interruption (auto-retry successful)
      * 1: Hardware failure (RMA required)
    - Average download time: 38 seconds
    - Average installation time: 6 minutes
    - Zero bricks (all failures recovered)
    
    Bandwidth Savings (vs full image):
    - Full image: 93 MB × 1,250 = 116 GB
    - Delta: 15.2 MB × 1,250 = 19 GB
    - Savings: 84% reduction

**Avionics Platform (Intel Atom)**:

.. code-block:: text

    Configuration:
    - Update delivery: Ground operations (Ethernet)
    - Security: Dual signatures (vendor + operator)
    - Compliance: DO-178C Level C
    
    Update Process:
    - Maintenance mode only
    - Cryptographic verification
    - Ground crew approval required
    - Comprehensive testing post-update
    
    Reliability:
    - 50 aircraft updated
    - 100% success rate
    - Average update time: 25 minutes
    - Zero in-flight issues

**E-Bike Infotainment**:

.. code-block:: text

    OTA Configuration:
    - Update delivery: Wi-Fi (at home)
    - Trigger: Ignition off + charging
    - Update types: SOTA (apps), FOTA (ECUs)
    
    Multi-ECU Update:
    - Infotainment: 45 MB (Linux rootfs)
    - BMS firmware: 128 KB
    - Motor controller: 256 KB
    - Total coordinated update: ~15 minutes
    
    Safety Measures:
    - Updates only when parked
    - Battery voltage > 12.5V
    - Automatic rollback on ECU update failure
    - User notification and consent

====================
10. Best Practices
====================

10.1 Security Checklist
-----------------------

.. code-block:: text

    ☐ Sign all update packages (RSA-2048 minimum)
    ☐ Encrypt sensitive updates (AES-256)
    ☐ Use HTTPS for update delivery
    ☐ Implement certificate pinning
    ☐ Verify checksums (SHA-256)
    ☐ Secure boot integration
    ☐ Rollback protection (version anti-rollback)
    ☐ Audit logging
    ☐ Revocation support

10.2 Reliability Checklist
---------------------------

.. code-block:: text

    ☐ A/B or recovery partition scheme
    ☐ Atomic updates (all or nothing)
    ☐ Automatic rollback on boot failure
    ☐ Power-loss resilience (fsync, atomic rename)
    ☐ Download resume capability
    ☐ Update verification before application
    ☐ Safe state detection (battery, network)
    ☐ User notification
    ☐ Comprehensive error handling

10.3 Efficiency Checklist
--------------------------

.. code-block:: text

    ☐ Delta updates for incremental changes
    ☐ Compression (gzip, xz)
    ☐ Bandwidth throttling (background updates)
    ☐ Staged rollout (gradual deployment)
    ☐ Update scheduling (off-peak hours)
    ☐ Network selection (Wi-Fi preferred over cellular)
    ☐ Progress reporting
    ☐ Retry logic with exponential backoff

====================
11. References
====================

**OTA Frameworks**:

- SWUpdate: https://sbabic.github.io/swupdate/
- RAUC: https://rauc.io/
- Mender: https://mender.io/

**Binary Diff Tools**:

- bsdiff/bspatch: http://www.daemonology.net/bsdiff/
- xdelta: http://xdelta.org/

**Standards**:

- ISO/SAE 21434: Automotive Cybersecurity
- UDS (ISO 14229): Unified Diagnostic Services
- DO-326A: Airworthiness Security Process

**Best Practices**:

- NIST SP 800-147B: BIOS Protection Guidelines
- OWASP IoT Top 10

---

**Revision History**:

========  ==========  ====================================
Version   Date        Changes
========  ==========  ====================================
1.0       2026-01-22  Initial comprehensive OTA guide
========  ==========  ====================================
