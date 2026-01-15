====================================================================
Medical Device SBOM - Software Bill of Materials
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: FDA Guidance 2023, NTIA, ISO 81001-5-1

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**SBOM for Medical Devices:**

- **Purpose:** Track software components for vulnerability management
- **FDA Requirement:** Mandatory for new device submissions (2023+)
- **Formats:** SPDX, CycloneDX, SWID
- **Content:** Component name, version, supplier, license, vulnerabilities

**SBOM Lifecycle:**

.. code-block:: text

    Design → Development → Submission → Post-Market Surveillance
      ↓           ↓            ↓              ↓
    Plan SBOM   Generate    FDA Review    Update for CVEs

Introduction
============

**FDA 2023 Cybersecurity Guidance** requires medical device manufacturers to provide a **Software Bill of Materials (SBOM)** listing all software components.

**Why SBOM Matters:**

- **Vulnerability tracking:** Quickly identify if device uses vulnerable component (e.g., Log4Shell)
- **License compliance:** Ensure GPL code not in proprietary device
- **Supply chain security:** Detect malicious dependencies

SBOM Formats
=============

**1. SPDX (Software Package Data Exchange)**

.. code-block:: json

    {
      "SPDXID": "SPDXRef-DOCUMENT",
      "spdxVersion": "SPDX-2.3",
      "name": "InsulinPump-v3.2-SBOM",
      "packages": [
        {
          "name": "OpenSSL",
          "versionInfo": "1.1.1k",
          "supplier": "OpenSSL Software Foundation",
          "licenseConcluded": "Apache-2.0",
          "externalRefs": [
            {
              "referenceCategory": "SECURITY",
              "referenceType": "cpe23Type",
              "referenceLocator": "cpe:2.3:a:openssl:openssl:1.1.1k"
            }
          ]
        }
      ]
    }

**2. CycloneDX**

.. code-block:: xml

    <bom>
      <component type="library">
        <name>mbedTLS</name>
        <version>2.28.0</version>
        <hashes>
          <hash alg="SHA-256">a1b2c3...</hash>
        </hashes>
        <licenses>
          <license>
            <id>Apache-2.0</id>
          </license>
        </licenses>
      </component>
    </bom>

Generating SBOM for Embedded Medical Device
============================================

**Python Script: SBOM Generator**

.. code-block:: python

    import json
    import subprocess
    
    class MedicalDeviceSBOM:
        def __init__(self, device_name, version):
            self.device_name = device_name
            self.version = version
            self.components = []
        
        def scan_dependencies(self, build_dir):
            """Scan build artifacts for dependencies"""
            # Example: Parse CMake dependencies
            cmake_output = subprocess.check_output(['cmake', '--build', build_dir, '--target', 'dependencies'])
            
            # Parse output to extract libraries
            for line in cmake_output.decode().split('\n'):
                if 'Linking' in line:
                    lib = self.extract_library_info(line)
                    self.components.append(lib)
        
        def check_vulnerabilities(self, component):
            """Check NVD for known CVEs"""
            cpe = f"cpe:2.3:a:{component['vendor']}:{component['name']}:{component['version']}"
            
            # Query NVD API
            response = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe}")
            cves = response.json().get('vulnerabilities', [])
            
            return [cve['cve']['id'] for cve in cves]
        
        def generate_spdx(self):
            sbom = {
                "spdxVersion": "SPDX-2.3",
                "name": f"{self.device_name}-{self.version}-SBOM",
                "packages": []
            }
            
            for component in self.components:
                pkg = {
                    "name": component['name'],
                    "versionInfo": component['version'],
                    "supplier": component['supplier'],
                    "licenseConcluded": component['license'],
                    "vulnerabilities": self.check_vulnerabilities(component)
                }
                sbom["packages"].append(pkg)
            
            return json.dumps(sbom, indent=2)

**Usage:**

.. code-block:: python

    # Generate SBOM for insulin pump firmware
    sbom = MedicalDeviceSBOM("InsulinPump", "v3.2.1")
    sbom.scan_dependencies("/build/firmware")
    spdx_output = sbom.generate_spdx()
    
    with open("InsulinPump-SBOM.json", "w") as f:
        f.write(spdx_output)

Vulnerability Management with SBOM
===================================

**Scenario: Log4Shell (CVE-2021-44228) Disclosure**

.. code-block:: python

    def assess_log4shell_impact(sbom_file):
        """Check if device uses vulnerable Log4j version"""
        sbom = json.load(open(sbom_file))
        
        for package in sbom['packages']:
            if package['name'] == 'log4j-core':
                version = package['versionInfo']
                
                # Vulnerable versions: 2.0-beta9 to 2.14.1
                if is_vulnerable_version(version, '2.0-beta9', '2.14.1'):
                    print(f"[!] CRITICAL: Device uses vulnerable Log4j {version}")
                    print(f"[!] Action: Issue field safety notice, provide patch")
                    return True
        
        print("[+] Device not affected by Log4Shell")
        return False

**FDA Post-Market Response:**

1. **Identify affected devices** (query SBOM database)
2. **Risk assessment** (is Log4j reachable from network?)
3. **Mitigation:**
   - Firmware update (patch Log4j)
   - Workaround (disable JNDI lookups)
   - Network segmentation (block internet access)
4. **Customer notification** (field safety notice)

Exam Questions
==============

**Q1: SBOM in Regulatory Submission (Medium)**

FDA requests SBOM for cardiac pacemaker. Device uses proprietary RTOS + open-source crypto library. What must SBOM include?

**Answer:**

**Must Include:**

1. **Open-source components:** mbedTLS, FreeRTOS (with versions, licenses)
2. **Commercial components:** Proprietary RTOS (vendor, version, license terms)
3. **Transitive dependencies:** If mbedTLS uses zlib, include zlib
4. **Known vulnerabilities:** CVEs affecting any component
5. **Update mechanism:** How SBOM will be maintained post-market

**Optional but Recommended:**

- Hash of each component (SHA-256)
- CPE (Common Platform Enumeration) for automated vuln scanning
- Supplier contact info for vulnerability disclosure

**Q2: SBOM Update Strategy (Hard)**

A pacemaker has 15-year lifespan. SBOM shows OpenSSL 1.1.1k at launch (2024). By 2030, OpenSSL 1.1.1 reaches end-of-life. How to manage?

**Answer:**

**Approach 1: Proactive Updates**
- Issue firmware updates every 2 years (update OpenSSL)
- Requires OTA update mechanism in device
- Challenge: Patient clinic visits for update

**Approach 2: Risk-Based**
- Monitor CVEs affecting OpenSSL 1.1.1k
- Only update if HIGH/CRITICAL CVE with proven exploit
- Maintain support contract with OpenSSL for backported patches

**Approach 3: Isolation**
- Design pacemaker with no network connectivity (airgap)
- OpenSSL only used for programmer ↔ device communication
- Limit attack surface (crypto only during clinic visits)

**Best Practice:** Combination of Approach 2 + 3 with annual SBOM review.

Standards
=========

- **FDA Cybersecurity Guidance (2023):** SBOM requirements
- **NTIA SBOM Minimum Elements:** Component name, version, supplier, dependencies
- **ISO 81001-5-1:** Health software security lifecycle

**END OF DOCUMENT**
