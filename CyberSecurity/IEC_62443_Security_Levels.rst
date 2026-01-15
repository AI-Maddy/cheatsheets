🎯 **IEC 62443 — SECURITY LEVELS (SL) IN DETAIL**
═══════════════════════════════════════════════════════════════════════

**Security Level Determination, Requirements & Assessment (62443-3-3)**  
**Purpose:** Risk-driven security classification 📊 | SL-T, SL-C, SL-A ⚖️  
**Scope:** Target levels, capability assessment, achieved verification

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Security Levels (SL 1-4)** define protection against increasingly sophisticated threats.

**Three types:**
- **SL-T (Target):** Required security based on risk assessment
- **SL-C (Capability):** Maximum security product/system can provide
- **SL-A (Achieved):** Actual security after deployment

**Key:** SL-A must be ≥ SL-T (close the gap with compensating controls if needed).

════════════════════════════════════════════════════════════════════════════

🎯 **SECURITY LEVEL DEFINITIONS (SL 1-4)**
─────────────────────────────────────────────────────────────────────────

**IEC 62443-3-3 Section 4: Security Levels**

.. code-block:: text

   SL 1: Protection against CASUAL violations
   ├─ Threat: Curious or careless user, script kiddie
   ├─ Capability: Generic tools (port scanners, password crackers)
   ├─ Means: Low skill, minimal resources
   └─ Motivation: Curiosity, nuisance
   
   SL 2: Protection against INTENTIONAL violations
   ├─ Threat: Disgruntled insider, hacktivist, vandal
   ├─ Capability: Simple custom tools, public exploits
   ├─ Means: Moderate skill, limited resources
   └─ Motivation: Sabotage, theft, disruption
   
   SL 3: Protection against SOPHISTICATED attacks
   ├─ Threat: Organized crime, terrorist, skilled hacker
   ├─ Capability: Advanced tools, zero-day exploits
   ├─ Means: High skill, significant resources
   └─ Motivation: Financial gain, political, competitive advantage
   
   SL 4: Protection against NATION-STATE attacks
   ├─ Threat: State-sponsored actors, APT groups
   ├─ Capability: Custom malware, supply chain attacks
   ├─ Means: Very high skill, nation-state resources
   └─ Motivation: Cyber warfare, espionage, critical infrastructure disruption

**Detailed Threat Actor Characteristics:**

| SL | Skill Level | Resources | Time Investment | Access | Example Attack |
|:---|:------------|:----------|:----------------|:-------|:---------------|
| **SL 1** | Generic | Minimal | Hours-Days | External remote | Default password login, open ports |
| **SL 2** | Specific IACS | Limited | Weeks | Physical access possible | Insider upload malicious firmware |
| **SL 3** | Extended IACS | Moderate to extensive | Months | Extended physical | Custom PLC rootkit, supply chain |
| **SL 4** | Very extended | Very extensive | Years | Persistent insider access | Stuxnet-level attack |

════════════════════════════════════════════════════════════════════════════

🔍 **SL-T: TARGET SECURITY LEVEL DETERMINATION**
─────────────────────────────────────────────────────────────────────────

**Process (62443-3-2 Section 4.2):**

**Step 1: Identify consequences of compromise**

.. code-block:: python

   # SL-T determination based on consequence severity
   class ConsequenceAssessment:
       """IEC 62443-3-2 consequence-based SL-T determination"""
       
       CONSEQUENCE_CATEGORIES = {
           'SAFETY': {
               'catastrophic': 4,  # Loss of life, major environmental damage
               'critical': 3,      # Severe injury, significant environmental impact
               'marginal': 2,      # Minor injury, localized environmental impact
               'negligible': 1     # No injury, minimal environmental impact
           },
           'FINANCIAL': {
               'catastrophic': 4,  # > $10M loss, bankruptcy risk
               'critical': 3,      # $1M - $10M loss
               'marginal': 2,      # $100K - $1M loss
               'negligible': 1     # < $100K loss
           },
           'OPERATIONAL': {
               'catastrophic': 4,  # Complete plant shutdown > 1 week
               'critical': 3,      # Major process disruption > 1 day
               'marginal': 2,      # Minor disruption < 1 day
               'negligible': 1     # Minimal impact
           },
           'REPUTATION': {
               'catastrophic': 4,  # Permanent brand damage, regulatory penalties
               'critical': 3,      # Significant media coverage, customer loss
               'marginal': 2,      # Local news coverage
               'negligible': 1     # Internal incident only
           }
       }
       
       def determine_sl_t(self, zone_name, consequences):
           """
           Determine SL-T for a zone based on consequence assessment.
           
           Args:
               zone_name: Name of the zone (e.g., "Process Control Zone")
               consequences: Dict with categories and severity levels
           
           Returns:
               SL-T (1-4)
           """
           max_sl = 1
           
           for category, severity in consequences.items():
               if category in self.CONSEQUENCE_CATEGORIES:
                   sl = self.CONSEQUENCE_CATEGORIES[category].get(severity, 1)
                   max_sl = max(max_sl, sl)
           
           print(f"Zone: {zone_name}")
           print(f"Consequences: {consequences}")
           print(f"Determined SL-T: {max_sl}")
           
           return max_sl
   
   # Example: Power plant turbine control
   assessor = ConsequenceAssessment()
   
   turbine_zone_consequences = {
       'SAFETY': 'catastrophic',      # Turbine failure could cause explosion
       'FINANCIAL': 'critical',       # $5M turbine damage + lost generation
       'OPERATIONAL': 'catastrophic', # 2-week outage for repairs
       'REPUTATION': 'critical'       # Major regulatory investigation
   }
   
   sl_t = assessor.determine_sl_t("Turbine Control Zone", turbine_zone_consequences)
   # Output: SL-T = 4 (catastrophic safety/operational consequences)

**Step 2: Consider attack likelihood**

.. code-block:: python

   def assess_attack_likelihood(asset_attractiveness, accessibility, vulnerability):
       """
       Attack likelihood factors (not explicit in 62443, but good practice)
       """
       likelihood_score = 0
       
       # Asset attractiveness (1-5)
       # 5 = Critical infrastructure (power plant)
       # 3 = Manufacturing (competitive interest)
       # 1 = Low-value process
       likelihood_score += asset_attractiveness
       
       # Accessibility (1-5)
       # 5 = Internet-facing
       # 3 = VPN access
       # 1 = Air-gapped
       likelihood_score += accessibility
       
       # Known vulnerabilities (1-5)
       # 5 = Multiple unpatched CVEs
       # 3 = Legacy system with design flaws
       # 1 = Hardened, current patches
       likelihood_score += vulnerability
       
       # Adjust SL-T based on likelihood
       if likelihood_score >= 12:
           return +1  # Increase SL-T by 1
       elif likelihood_score <= 5:
           return -1  # Decrease SL-T by 1 (but min SL 1)
       else:
           return 0   # No adjustment
   
   # Example: Internet-facing SCADA server
   adjustment = assess_attack_likelihood(
       asset_attractiveness=4,  # Utility company (attractive target)
       accessibility=5,         # Internet-facing
       vulnerability=3          # Legacy Windows server
   )
   # Total: 12 → Increase SL-T by 1

**Step 3: Document SL-T for each zone**

.. code-block:: python

   class ZoneRegistry:
       def __init__(self):
           self.zones = []
       
       def register_zone(self, zone_name, sl_t, justification):
           """Document SL-T determination"""
           self.zones.append({
               'name': zone_name,
               'sl_t': sl_t,
               'justification': justification,
               'date': datetime.utcnow().isoformat()
           })
       
       def export_to_report(self, filename):
           """Generate IEC 62443-3-2 compliant documentation"""
           with open(filename, 'w') as f:
               f.write("IEC 62443-3-2 Zone Security Level Report\n")
               f.write("=" * 80 + "\n\n")
               
               for zone in self.zones:
                   f.write(f"Zone: {zone['name']}\n")
                   f.write(f"Target Security Level: SL {zone['sl_t']}\n")
                   f.write(f"Justification: {zone['justification']}\n")
                   f.write(f"Assessed on: {zone['date']}\n\n")

════════════════════════════════════════════════════════════════════════════

🏭 **SL-C: CAPABILITY SECURITY LEVEL ASSESSMENT**
─────────────────────────────────────────────────────────────────────────

**IEC 62443-4-2 Component Certification:**

Vendors test products against **62443-4-2 technical requirements** to claim SL-C.

**Example: PLC Certification Process**

.. code-block:: python

   class ComponentSLCAssessment:
       """IEC 62443-4-2 capability assessment for a product"""
       
       # 62443-4-2 Requirements mapped to SL
       REQUIREMENTS = {
           'IAC': {  # Identification & Authentication Control
               'SL1': ['User identification', 'Password authentication'],
               'SL2': ['Password complexity', 'Account lockout'],
               'SL3': ['Multi-factor authentication', 'Hardware token'],
               'SL4': ['Biometric authentication', 'Hardware security module']
           },
           'UC': {  # Use Control
               'SL1': ['Basic access control'],
               'SL2': ['Role-based access control (RBAC)'],
               'SL3': ['Attribute-based access control (ABAC)', 'Least privilege'],
               'SL4': ['Separation of duties', 'Formal access control model']
           },
           'SI': {  # System Integrity
               'SL1': ['Configuration integrity checking'],
               'SL2': ['Software integrity verification (digital signatures)'],
               'SL3': ['Secure boot', 'Trusted execution environment'],
               'SL4': ['Hardware root of trust', 'Formal verification']
           },
           'DC': {  # Data Confidentiality
               'SL1': ['None required'],
               'SL2': ['TLS 1.2+ encryption', 'AES-128'],
               'SL3': ['TLS 1.3', 'AES-256', 'Perfect forward secrecy'],
               'SL4': ['Hardware-backed encryption', 'Quantum-resistant algorithms']
           },
           # ... (FR 5-7 similar structure)
       }
       
       def assess_product_sl_c(self, product_name, implemented_features):
           """
           Assess maximum SL-C a product can achieve.
           
           Args:
               product_name: Name of the product
               implemented_features: Dict mapping FR to list of implemented features
           
           Returns:
               SL-C (1-4)
           """
           min_sl = 4  # Start optimistic
           
           for fr, requirements_by_sl in self.REQUIREMENTS.items():
               product_features = implemented_features.get(fr, [])
               
               # Determine highest SL where all requirements met
               fr_max_sl = 0
               for sl in [1, 2, 3, 4]:
                   required = requirements_by_sl.get(f'SL{sl}', [])
                   if all(req in product_features for req in required):
                       fr_max_sl = sl
                   else:
                       break  # Can't achieve higher SL if lower not met
               
               # Overall SL-C is minimum across all FRs
               min_sl = min(min_sl, fr_max_sl)
           
           print(f"Product: {product_name}")
           print(f"Assessed SL-C: {min_sl}")
           return min_sl
   
   # Example: Modern industrial PLC
   assessor = ComponentSLCAssessment()
   
   plc_features = {
       'IAC': ['User identification', 'Password authentication', 
               'Password complexity', 'Account lockout', 
               'Multi-factor authentication'],
       'UC': ['Basic access control', 'Role-based access control (RBAC)', 
              'Least privilege'],
       'SI': ['Configuration integrity checking', 
              'Software integrity verification (digital signatures)', 
              'Secure boot'],
       'DC': ['TLS 1.2+ encryption', 'AES-128', 'TLS 1.3', 'AES-256']
   }
   
   sl_c = assessor.assess_product_sl_c("ModernPLC X500", plc_features)
   # Output: SL-C = 3 (all requirements up to SL 3 met)

**Vendor Certification Levels:**

| Certification | Scope | Example |
|:--------------|:------|:--------|
| **Component Level** | Single device (PLC, HMI, sensor) | Siemens S7-1500 PLC certified SL 2 |
| **System Level** | Integrated solution (DCS, SCADA) | Honeywell Experion PKS certified SL 2 |
| **Self-Declaration** | Vendor claims compliance (no 3rd party) | Vendor whitepaper |
| **3rd Party Certified** | Independent lab (TÜV, Achilles, etc.) | TÜV Rheinland certificate |

════════════════════════════════════════════════════════════════════════════

✅ **SL-A: ACHIEVED SECURITY LEVEL VERIFICATION**
─────────────────────────────────────────────────────────────────────────

**Post-Deployment Assessment:**

SL-A is determined after system integration and deployment by **auditor or integrator**.

.. code-block:: python

   class SLAVerification:
       """Verify achieved security level in production environment"""
       
       def __init__(self, zone_name, sl_t, sl_c):
           self.zone_name = zone_name
           self.sl_t = sl_t
           self.sl_c = sl_c
           self.findings = []
       
       def verify_requirement(self, fr, requirement, implemented):
           """Check if requirement is actually implemented"""
           if not implemented:
               self.findings.append({
                   'fr': fr,
                   'requirement': requirement,
                   'status': 'NOT_IMPLEMENTED'
               })
               return False
           return True
       
       def verify_sl_a(self):
           """
           Verify SL-A through testing and inspection.
           
           Returns:
               SL-A (1-4) and gap analysis
           """
           # Example verification checks
           checks = {
               'FR1_MFA': self.check_mfa_enabled(),
               'FR2_RBAC': self.check_rbac_configured(),
               'FR3_SECURE_BOOT': self.check_secure_boot(),
               'FR4_ENCRYPTION': self.check_tls_enabled(),
               'FR5_SEGMENTATION': self.check_network_segmentation(),
               'FR6_LOGGING': self.check_audit_logging(),
               'FR7_BACKUP': self.check_backup_configured()
           }
           
           # Determine SL-A based on checks
           if all(checks.values()):
               sl_a = 3  # All SL 3 requirements met
           elif checks['FR1_MFA'] == False:
               sl_a = 2  # MFA missing (required for SL 3)
           else:
               sl_a = 1
           
           # Gap analysis
           gap = self.sl_t - sl_a
           
           report = {
               'zone': self.zone_name,
               'sl_t': self.sl_t,
               'sl_c': self.sl_c,
               'sl_a': sl_a,
               'gap': gap,
               'findings': self.findings,
               'checks': checks
           }
           
           return sl_a, report
       
       def check_mfa_enabled(self):
           """FR 1.5: Multi-factor authentication (SL 3+)"""
           # In real audit: Test login process, check config files
           # For example: Check if RADIUS server requires token
           return True  # Placeholder
       
       def check_secure_boot(self):
           """FR 3.9: Secure boot (SL 3+)"""
           # In real audit: Inspect boot logs, verify signature chain
           return True  # Placeholder
   
   # Example: Power plant control zone
   verifier = SLAVerification(
       zone_name="Turbine Control Zone",
       sl_t=3,  # Target
       sl_c=2   # PLC vendor claims SL 2
   )
   
   sl_a, report = verifier.verify_sl_a()
   
   print(f"SL-T: {report['sl_t']}")
   print(f"SL-C: {report['sl_c']}")
   print(f"SL-A: {report['sl_a']}")
   print(f"Gap: {report['gap']} security level(s)")
   
   if report['gap'] > 0:
       print("\nGap mitigation required:")
       print("- Add network-based IDS/IPS (compensating control)")
       print("- Implement additional access controls")
       print("- Document residual risk acceptance")

════════════════════════════════════════════════════════════════════════════

🔧 **COMPENSATING CONTROLS**
─────────────────────────────────────────────────────────────────────────

**When SL-C < SL-T:**

Legacy equipment often cannot meet modern SL requirements → Use **compensating controls**.

.. code-block:: python

   class CompensatingControlStrategy:
       """Strategies to close SL gap with network/procedural controls"""
       
       def propose_compensating_controls(self, gap, zone_type):
           """
           Propose compensating controls based on SL gap.
           
           Args:
               gap: SL-T - SL-A (e.g., 3 - 2 = 1)
               zone_type: Type of industrial zone
           
           Returns:
               List of recommended controls
           """
           controls = []
           
           if gap >= 1:
               # Basic gap (SL 2 → SL 3)
               controls.extend([
                   {
                       'control': 'Network IDS/IPS',
                       'rationale': 'Compensates for lack of device-level intrusion detection',
                       'fr': 'FR 6 (Timely Response to Events)'
                   },
                   {
                       'control': 'Unidirectional gateway',
                       'rationale': 'Prevents write access from untrusted zones',
                       'fr': 'FR 5 (Restricted Data Flow)'
                   },
                   {
                       'control': 'Enhanced monitoring (SIEM)',
                       'rationale': 'Aggregates logs from legacy devices',
                       'fr': 'FR 6 (Timely Response to Events)'
                   }
               ])
           
           if gap >= 2:
               # Major gap (SL 2 → SL 4)
               controls.extend([
                   {
                       'control': 'Air-gap / physical isolation',
                       'rationale': 'Eliminates network attack surface',
                       'fr': 'FR 5 (Restricted Data Flow)'
                   },
                   {
                       'control': 'Hardware firewall with deep packet inspection',
                       'rationale': 'Validates industrial protocol commands',
                       'fr': 'FR 5 (Restricted Data Flow)'
                   },
                   {
                       'control': 'Continuous vulnerability scanning',
                       'rationale': 'Identifies new vulnerabilities in legacy systems',
                       'fr': 'FR 3 (System Integrity)'
                   }
               ])
           
           return controls
   
   # Example: Legacy PLC (SL-C = 1) in critical zone (SL-T = 3)
   strategy = CompensatingControlStrategy()
   controls = strategy.propose_compensating_controls(gap=2, zone_type="Process Control")
   
   print("Compensating Controls for 2-level gap:")
   for ctrl in controls:
       print(f"- {ctrl['control']} ({ctrl['fr']})")
       print(f"  Rationale: {ctrl['rationale']}\n")

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: A manufacturing plant has a PLC controlling a paint mixing process. Risk assessment determines: Loss of production = $50K/day, No safety impact. What SL-T should be assigned?**

**A1:**

**Step 1: Consequence Assessment**
```
Safety: Negligible (no injury risk) → SL 1
Financial: $50K/day loss = ~$350K/week → Marginal ($100K-$1M) → SL 2
Operational: Paint mixing disruption → Minor (< 1 day recovery) → SL 2
Reputation: Local customer impact → Marginal → SL 2
```

**Step 2: Maximum Consequence**
Highest SL across categories = **SL 2**

**Step 3: Likelihood Adjustment**
- Asset attractiveness: 2 (standard manufacturing)
- Accessibility: 3 (internal network, VPN access)
- Vulnerability: 3 (older PLC, unpatched)
- Total: 8 → No adjustment

**Result: SL-T = SL 2**

**Justification:** Financial and operational consequences are marginal, no safety impact, moderate likelihood.

---

**Q2: Explain why overall system SL-C is the MINIMUM across all Foundational Requirements, not the average.**

**A2:**

**Security chain is only as strong as weakest link.**

**Example:**

```
Product X security features:
├─ FR 1 (Authentication): Excellent MFA → SL 3
├─ FR 2 (Access Control): Strong RBAC → SL 3
├─ FR 3 (Integrity): Secure boot → SL 3
├─ FR 4 (Confidentiality): No encryption → SL 1  ← WEAK LINK
├─ FR 5 (Segmentation): Network firewall → SL 2
└─ FR 6 (Logging): Comprehensive audit → SL 3

Overall SL-C = SL 1 (due to FR 4)
```

**Why?**
Attacker exploits weakest FR:
- Perfect authentication (SL 3) doesn't matter if attacker sniffs unencrypted passwords on network (FR 4 = SL 1)
- Secure boot (SL 3) doesn't prevent malicious firmware upload if no encryption validates source (FR 4 = SL 1)

**IEC 62443 principle:** All FRs must meet target SL.

---

**Q3: A critical infrastructure site has SL-T = 4 but can only procure PLCs with SL-C = 2. What options exist?**

**A3:**

**Option 1: Compensating Controls (Most Common)**
```
Network-level controls:
├─ Unidirectional gateway (prevents commands from IT network)
├─ Industrial firewall with protocol whitelisting
├─ IDS/IPS with industrial protocol inspection
├─ SIEM with behavioral analytics
└─ Air-gap critical networks

Procedural controls:
├─ 2-person rule for PLC configuration changes
├─ Hardware-based code signing (external HSM)
├─ Enhanced monitoring (24/7 SOC)
└─ Strict change management
```

**Option 2: Residual Risk Acceptance**
Document and formally accept gap with executive approval (not recommended for SL 4).

**Option 3: Upgrade Equipment**
Replace legacy PLCs with SL 4-capable models (expensive, may require plant shutdown).

**Option 4: Hybrid Approach**
- Keep legacy PLCs for non-critical functions (SL 2)
- Add new SL 4 PLCs for critical functions (turbine control, safety systems)
- Segment network to isolate critical zone

**Recommendation for SL 4:** Combination of Option 1 (compensating controls) + Option 4 (hybrid), with annual penetration testing.

---

**Q4: How do you verify SL-A during commissioning?**

**A4:**

**Verification Process (IEC 62443-3-3 Annex A):**

**1. Document Review**
```
├─ Configuration backups
├─ Network diagrams (as-built)
├─ Firewall rules
├─ User accounts and roles
└─ Patch levels
```

**2. Functional Testing**
```
FR 1 (Authentication):
├─ Test MFA login (if SL 3+)
├─ Verify account lockout after 3 failures
└─ Attempt default password login (should fail)

FR 2 (Access Control):
├─ Verify operator cannot modify PLC program
├─ Test least privilege (engineer only accesses assigned equipment)

FR 3 (Integrity):
├─ Upload unsigned firmware (should be rejected)
├─ Check secure boot enabled (inspect boot logs)

FR 4 (Confidentiality):
├─ Capture network traffic (Wireshark)
├─ Verify TLS encryption (no plaintext passwords)

FR 5 (Segmentation):
├─ Attempt cross-zone access (should be blocked)
├─ Test firewall rules (port scan from untrusted zone)

FR 6 (Logging):
├─ Generate security event (failed login)
├─ Verify event appears in SIEM within 1 minute

FR 7 (Availability):
├─ Trigger DoS condition (flood with requests)
├─ Verify rate limiting engages
```

**3. Penetration Testing (SL 3-4)**
- External pentest (simulate remote attacker)
- Internal pentest (simulate insider threat)
- Industrial protocol fuzzing (Modbus, OPC UA)

**4. Gap Documentation**
- Compare findings vs. SL-T requirements
- Propose compensating controls for gaps
- Document residual risks

**5. SL-A Declaration**
Issue formal statement: "Zone X achieved SL-A = Y as of [date]"

---

**Q5: Can a zone have different SL-T values for different Foundational Requirements?**

**A5:**

**No, not in standard 62443-3-3.**

**Reason:** Simplicity and consistency. A zone has **one SL-T** that applies to all 7 FRs.

**However, in practice:**

Some organizations use **FR-specific SL** for risk management:

```
Example: DMZ Zone
├─ FR 1-3 (Authentication, Access, Integrity): SL-T = 3 (high risk)
├─ FR 4 (Confidentiality): SL-T = 2 (data already public)
└─ FR 5-7 (Segmentation, Logging, Availability): SL-T = 3
```

**IEC 62443 approach:** Use **highest** SL-T across all consequence scenarios.

**If truly different requirements:**
→ Split into **separate zones** with different SL-T
```
Zone 3A (Sensitive data): SL-T = 3
Zone 3B (Public data): SL-T = 2
```

This maintains zone-level consistency while allowing FR-appropriate security.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~750
