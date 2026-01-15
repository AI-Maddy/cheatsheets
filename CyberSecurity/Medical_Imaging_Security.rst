====================================================================
Medical Imaging Security - CT, MRI, X-Ray Systems
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: DICOM, HIPAA, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Medical Imaging Systems:**

- CT (Computed Tomography), MRI, X-ray, Ultrasound
- **Protocol:** DICOM (Digital Imaging and Communications in Medicine)
- **Storage:** PACS (Picture Archiving and Communication System)

**Security Threats:**

- **Ransomware:** Encrypt imaging systems → halt diagnostics
- **Data breach:** Patient images contain PHI (HIPAA violation)
- **Image tampering:** Modify scans → misdiagnosis

**Security Controls:**

✅ **DICOM TLS:** Encrypt image transmission
✅ **Digital signatures:** Verify image integrity
✅ **Access control:** Role-based PACS access

Introduction
============

**Attack Impact:**

- Ransomware shuts down radiology department
- Tampered images lead to incorrect treatment
- Privacy breach exposes patient medical history

DICOM Security
===============

**Secure DICOM Transmission:**

.. code-block:: python

    import pydicom
    import ssl
    
    # Connect to PACS with TLS
    def send_dicom_secure(dicom_file, pacs_server):
        # Load DICOM image
        ds = pydicom.dcmread(dicom_file)
        
        # Create TLS context
        context = ssl.create_default_context()
        context.load_cert_chain('hospital.crt', 'hospital.key')
        
        # Send via DICOM TLS (port 11112)
        from pynetdicom import AE
        ae = AE()
        ae.add_requested_context('CTImageStorage')
        
        # Associate with TLS
        assoc = ae.associate(pacs_server, 11112, tls_args=(context,))
        
        if assoc.is_established:
            assoc.send_c_store(ds)
            assoc.release()

**Image Integrity (Digital Signature):**

.. code-block:: c

    #include <openssl/evp.h>
    
    // Sign DICOM image with RSA
    void sign_dicom_image(uint8_t *image_data, size_t len, uint8_t *signature) {
        EVP_MD_CTX *ctx = EVP_MD_CTX_new();
        EVP_PKEY *pkey = load_private_key("radiologist.key");
        
        // Compute SHA-256 hash
        uint8_t hash[32];
        EVP_DigestInit(ctx, EVP_sha256());
        EVP_DigestUpdate(ctx, image_data, len);
        EVP_DigestFinal(ctx, hash, NULL);
        
        // Sign hash with RSA
        size_t sig_len;
        EVP_SignFinal(ctx, signature, &sig_len, pkey);
        
        // Embed signature in DICOM metadata
        embed_signature_in_dicom(signature, sig_len);
    }

Attack: Image Tampering
=========================

**Scenario:** Attacker modifies CT scan to add/remove tumors.

.. code-block:: python

    # Research demonstration: Inject fake nodules into CT scan
    import numpy as np
    from PIL import Image
    
    def tamper_ct_scan(ct_image_path):
        # Load CT DICOM
        ds = pydicom.dcmread(ct_image_path)
        pixel_array = ds.pixel_array
        
        # Add fake nodule (malicious)
        pixel_array[200:220, 300:320] = 255  # White blob
        
        # Update DICOM
        ds.PixelData = pixel_array.tobytes()
        ds.save_as("tampered_ct.dcm")

**Defense: Blockchain-Based Audit Trail**

.. code-block:: python

    import hashlib
    import time
    
    class ImagingBlockchain:
        def __init__(self):
            self.chain = []
        
        def add_image(self, dicom_file, radiologist_id):
            # Compute hash of image
            image_hash = hashlib.sha256(open(dicom_file, 'rb').read()).hexdigest()
            
            # Create block
            block = {
                'timestamp': time.time(),
                'image_hash': image_hash,
                'radiologist': radiologist_id,
                'previous_hash': self.chain[-1]['hash'] if self.chain else '0'
            }
            
            # Compute block hash
            block['hash'] = hashlib.sha256(str(block).encode()).hexdigest()
            
            # Add to chain
            self.chain.append(block)
        
        def verify_image(self, dicom_file):
            # Check if image hash exists in blockchain
            image_hash = hashlib.sha256(open(dicom_file, 'rb').read()).hexdigest()
            
            for block in self.chain:
                if block['image_hash'] == image_hash:
                    return True  # Image verified
            
            return False  # Image not in chain (possibly tampered)

Ransomware Defense
===================

**Backup Strategy:**

.. code-block:: bash

    #!/bin/bash
    # Backup PACS every 6 hours
    
    PACS_DATA="/var/pacs/data"
    BACKUP_DIR="/mnt/offsite/pacs_backup"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    # Incremental backup
    rsync -avz --link-dest=$BACKUP_DIR/latest \
        $PACS_DATA $BACKUP_DIR/$TIMESTAMP
    
    # Update 'latest' symlink
    ln -sfn $BACKUP_DIR/$TIMESTAMP $BACKUP_DIR/latest
    
    # Encrypt backup
    tar -czf - $BACKUP_DIR/$TIMESTAMP | \
        openssl enc -aes-256-cbc -pbkdf2 | \
        aws s3 cp - s3://hospital-backups/pacs_$TIMESTAMP.tar.gz.enc

**Network Segmentation:**

.. code-block:: text

    Hospital Network (WiFi, Admin)
           ↓ (Firewall)
    Radiology VLAN
           ├─ CT Scanner (192.168.10.10)
           ├─ MRI System (192.168.10.11)
           └─ PACS Server (192.168.10.100)
    
    # Firewall rules: Deny internet access from imaging devices

Exam Questions
==============

**Q1: DICOM TLS Deployment (Medium)**

A hospital has 50 imaging devices (CT, MRI, X-ray). Half are 10+ years old with no TLS support. Design migration plan.

**Answer:**

**Phase 1: Inventory**
- Identify devices supporting DICOM TLS
- Identify legacy devices (no TLS)

**Phase 2: Hybrid Deployment**
- Deploy DICOM TLS proxy/gateway
- Legacy devices → Proxy (plaintext, isolated VLAN)
- Proxy → PACS (TLS)
- Modern devices → PACS (direct TLS)

**Phase 3: Gradual Replacement**
- Replace legacy devices during refresh cycles (5 years)

**Q2: Image Tampering Detection (Hard)**

An attacker modifies a lung CT scan to hide a tumor. How can hospital detect this?

**Answer:**

**Technical Controls:**
1. **Digital signatures:** Radiologist signs image at acquisition
2. **Blockchain audit:** Image hash recorded immutably
3. **Version control:** Track all modifications to DICOM files

**Procedural Controls:**
1. **Dual review:** Two radiologists review critical findings
2. **Original media:** Preserve raw scanner output (separate from PACS)
3. **Audit logs:** Log all access to PACS (who viewed/modified images)

Standards
=========

- **DICOM Standard:** Digital imaging protocol
- **HIPAA Security Rule:** PHI protection
- **IEC 62443:** Medical device security

**END OF DOCUMENT**
