====================================================================
DevSecOps Pipeline - Security in CI/CD
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NIST SP 800-218, OWASP DevSecOps

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**DevSecOps Principles:**

1. **Shift left:** Find security issues early (design, code)
2. **Automate:** Security gates in CI/CD pipeline
3. **Continuous monitoring:** Runtime security (production)

**Security Tools in Pipeline:**

✅ **SAST:** Static Application Security Testing (code analysis)
✅ **DAST:** Dynamic Application Security Testing (runtime)
✅ **SCA:** Software Composition Analysis (dependency scanning)
✅ **Container scanning:** Docker image vulnerabilities
✅ **Secrets detection:** Prevent hardcoded credentials

Introduction
============

**DevSecOps** integrates security into DevOps (Development + Operations).

**Traditional Approach:**

.. code-block:: text

    Develop → Test → Security Review (1 month) → Deploy
                      ↑ (Vulnerabilities found late, expensive to fix)

**DevSecOps:**

.. code-block:: text

    Develop → Commit → SAST → Unit Tests → DAST → Deploy
               ↑        ↑                    ↑
             (Security checks automated in pipeline)

CI/CD Pipeline with Security Gates
====================================

**Example: GitHub Actions + Security Tools**

.. code-block:: yaml

    # .github/workflows/devsecops.yml
    name: DevSecOps Pipeline
    
    on: [push, pull_request]
    
    jobs:
      security-scan:
        runs-on: ubuntu-latest
        steps:
          # 1. Checkout code
          - uses: actions/checkout@v3
          
          # 2. Secret scanning (detect hardcoded passwords)
          - name: Run Gitleaks
            uses: gitleaks/gitleaks-action@v2
          
          # 3. SAST (static code analysis)
          - name: Run Semgrep
            run: |
              pip install semgrep
              semgrep --config=auto --error
          
          # 4. SCA (dependency vulnerabilities)
          - name: Run OWASP Dependency-Check
            run: |
              dependency-check --project myproject --scan ./
              # Fail build if HIGH/CRITICAL vulnerabilities
          
          # 5. Build firmware
          - name: Build
            run: make firmware.bin
          
          # 6. Firmware signing
          - name: Sign firmware
            run: |
              openssl dgst -sha256 -sign private_key.pem \
                -out firmware.sig firmware.bin
          
          # 7. Container scanning (if using Docker)
          - name: Scan Docker image
            run: |
              docker build -t myapp:latest .
              trivy image --severity HIGH,CRITICAL myapp:latest
          
          # 8. Deploy (only if all security checks pass)
          - name: Deploy
            if: success()
            run: ./deploy.sh

SAST (Static Application Security Testing)
============================================

**Tool: Semgrep**

.. code-block:: yaml

    # semgrep-rules.yml
    rules:
      - id: hardcoded-password
        pattern: |
          password = "..."
        message: "Hardcoded password detected"
        severity: ERROR
        languages: [c, cpp, python]
      
      - id: buffer-overflow
        pattern: |
          strcpy($BUF, $SRC)
        message: "Use strncpy() to prevent buffer overflow"
        severity: WARNING
        languages: [c]
      
      - id: sql-injection
        pattern: |
          execute("SELECT * FROM users WHERE id=" + $ID)
        message: "SQL injection vulnerability"
        severity: ERROR

**Custom Rule for Embedded C:**

.. code-block:: yaml

    rules:
      - id: missing-bounds-check
        pattern: |
          for ($I = 0; $I < $N; $I++) {
            $ARRAY[$I] = ...;
          }
        message: "Missing bounds check on array access"
        severity: WARNING

SCA (Software Composition Analysis)
=====================================

**Scan Dependencies for Known CVEs:**

.. code-block:: bash

    # For Python
    pip install safety
    safety check --json > vulnerabilities.json
    
    # For Node.js
    npm audit --audit-level=high
    
    # For C/C++ (Conan packages)
    conan install . --build=missing
    dependency-check --project myproject --scan ~/.conan/data

**Example Output:**

.. code-block:: json

    {
      "vulnerabilities": [
        {
          "package": "openssl",
          "version": "1.1.1k",
          "cve": "CVE-2021-3711",
          "severity": "HIGH",
          "fix": "Upgrade to 1.1.1l"
        }
      ]
    }

**Auto-Remediation:**

.. code-block:: python

    # Auto-upgrade vulnerable dependencies
    def auto_remediate(vulnerabilities):
        for vuln in vulnerabilities:
            if vuln['severity'] in ['HIGH', 'CRITICAL']:
                # Update package version
                update_package(vuln['package'], vuln['fix_version'])
                
                # Run tests
                if not run_tests():
                    # Rollback if tests fail
                    rollback_package(vuln['package'])

Container Security
===================

**Scan Docker Images for Vulnerabilities:**

.. code-block:: dockerfile

    # Dockerfile with security best practices
    FROM ubuntu:22.04
    
    # Install only necessary packages
    RUN apt-get update && apt-get install -y \
        openssl \
        && rm -rf /var/lib/apt/lists/*
    
    # Run as non-root user
    RUN useradd -m appuser
    USER appuser
    
    # Copy application
    COPY --chown=appuser:appuser ./app /home/appuser/app
    
    # Expose only necessary ports
    EXPOSE 8080
    
    CMD ["/home/appuser/app/server"]

**Scan with Trivy:**

.. code-block:: bash

    # Scan Docker image
    trivy image --severity HIGH,CRITICAL myapp:latest
    
    # Example output:
    # CVE-2022-1234 | HIGH | openssl 1.1.1k (upgrade to 1.1.1l)

Secrets Management
===================

**Problem:** Developers hardcode credentials in code.

.. code-block:: c

    // BAD: Hardcoded API key
    const char *api_key = "sk_live_51H2Abc...";

**Solution 1: Environment Variables**

.. code-block:: c

    // Load from environment
    const char *api_key = getenv("API_KEY");
    if (!api_key) {
        fprintf(stderr, "API_KEY not set\n");
        exit(1);
    }

**Solution 2: Secrets Vault (HashiCorp Vault)**

.. code-block:: python

    import hvac
    
    # Connect to Vault
    client = hvac.Client(url='https://vault.example.com')
    client.token = os.environ['VAULT_TOKEN']
    
    # Retrieve secret
    secret = client.secrets.kv.v2.read_secret_version(path='myapp/api_key')
    api_key = secret['data']['data']['key']

**Detection: Gitleaks**

.. code-block:: bash

    # Scan Git history for leaked secrets
    gitleaks detect --source . --verbose
    
    # Example detection:
    # Line 42: api_key = "sk_live_51H2Abc..." (AWS API Key)

Runtime Security (Production)
===============================

**Monitor for Anomalies in Production:**

.. code-block:: python

    import syslog
    
    class RuntimeMonitor:
        def __init__(self):
            self.baseline_cpu = 30  # %
            self.baseline_mem = 100  # MB
        
        def monitor(self):
            while True:
                cpu = get_cpu_usage()
                mem = get_memory_usage()
                
                # Detect crypto-mining malware (high CPU)
                if cpu > 90:
                    syslog.syslog(syslog.LOG_ALERT, "CPU spike detected")
                    self.investigate(cpu, mem)
                
                # Detect memory leak
                if mem > 2 * self.baseline_mem:
                    syslog.syslog(syslog.LOG_WARNING, "Memory leak suspected")
                
                time.sleep(60)

**Embedded Device: Runtime Integrity Check**

.. code-block:: c

    // Verify firmware integrity at runtime
    void runtime_integrity_check(void) {
        uint32_t crc = compute_firmware_crc(FIRMWARE_ADDR, FIRMWARE_SIZE);
        
        if (crc != EXPECTED_CRC) {
            // Firmware tampered!
            trigger_alert("Firmware integrity violation");
            enter_safe_mode();
        }
    }

Exam Questions
==============

**Q1: SAST vs DAST (Medium)**

Compare SAST and DAST. When to use each?

**Answer:**

+-------------------+---------------------------+------------------------+
| Feature           | SAST                      | DAST                   |
+===================+===========================+========================+
| Analysis          | Source code (white-box)   | Running app (black-box)|
+-------------------+---------------------------+------------------------+
| Timing            | During development        | After deployment       |
+-------------------+---------------------------+------------------------+
| Coverage          | All code paths            | Only executed paths    |
+-------------------+---------------------------+------------------------+
| False positives   | ⚠️  High                  | ✅ Low                 |
+-------------------+---------------------------+------------------------+

**Use SAST for:**
- Buffer overflows (C/C++)
- SQL injection (source code patterns)
- Hardcoded secrets

**Use DAST for:**
- Authentication bypass (runtime behavior)
- Session management flaws
- Server misconfigurations

**Best Practice:** Use both (SAST early, DAST before release).

**Q2: Secure Firmware Update Pipeline (Hard)**

Design CI/CD pipeline for automotive ECU firmware with secure update mechanism.

**Answer:**

.. code-block:: yaml

    # CI/CD Pipeline
    1. Developer commits code → GitHub
    2. SAST (Semgrep) scans for vulnerabilities
    3. Unit tests run
    4. Build firmware.bin
    5. Sign firmware with HSM (ECDSA)
       └─ openssl dgst -sha256 -sign hsm_key -out firmware.sig firmware.bin
    6. Encrypt firmware (AES-256)
       └─ openssl enc -aes-256-cbc -in firmware.bin -out firmware.enc
    7. Upload to OTA server (HTTPS)
    8. Vehicle downloads firmware
    9. Verify signature (bootloader)
    10. Decrypt and flash

**Security Measures:**

- **Code signing:** Prevents malicious firmware
- **Encryption:** Protects against MITM during download
- **Rollback protection:** Firmware version must be newer
- **Secure boot:** Bootloader verifies signature before execution

**Rollback Strategy:**

.. code-block:: c

    // Bootloader checks signature
    if (!verify_ecdsa_signature(firmware, signature)) {
        // Invalid signature → rollback to previous firmware
        load_backup_firmware();
    }

Standards
=========

- **NIST SP 800-218:** Secure Software Development Framework
- **OWASP DevSecOps Guideline:** Security in CI/CD
- **ISO 27034:** Application security

**END OF DOCUMENT**
