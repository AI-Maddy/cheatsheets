====================================================================
SCADA HMI Security - Human-Machine Interface Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEC 62443, NIST SP 800-82

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**HMI Vulnerabilities:**

- **Web-based HMI:** SQL injection, XSS, CSRF
- **VNC/RDP:** Remote access without MFA
- **Default credentials:** admin/admin, root/root
- **Outdated software:** Unpatched Windows XP/7 systems

**Security Controls:**

✅ **Multi-factor authentication (MFA)**
✅ **Role-based access control (RBAC)**
✅ **Input validation:** Prevent SQL injection
✅ **Patch management:** Update OS and HMI software
✅ **Network isolation:** Separate HMI from corporate network

Introduction
============

**SCADA HMI (Human-Machine Interface)** provides operators visibility and control of industrial processes.

**Attack Consequences:**

- Manipulate process setpoints (temperature, pressure, flow)
- Disable alarms/safety systems
- Exfiltrate operational data
- Cause physical damage

HMI Attack Scenarios
====================

**Attack 1: SQL Injection in Web HMI**

.. code-block:: sql

    -- Vulnerable HMI login
    SELECT * FROM users WHERE username='$user' AND password='$pass'
    
    -- Attacker input: username = admin'--
    SELECT * FROM users WHERE username='admin'--' AND password='...'
    -- Comments out password check, logs in as admin

**Mitigation:**

.. code-block:: python

    # Use parameterized queries
    def authenticate_user(username, password):
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        )

**Attack 2: VNC/RDP Brute Force**

.. code-block:: python

    # Attacker brute-forces HMI remote access
    import socket
    
    def brute_force_vnc(target_ip, wordlist):
        for password in wordlist:
            try:
                vnc = connect_vnc(target_ip, 5900)
                if vnc.authenticate(password):
                    print(f"[+] Password found: {password}")
                    return vnc
            except:
                continue

**Mitigation:**

- Disable VNC/RDP from internet
- Require VPN + MFA
- Implement account lockout (3 failed attempts)

**Attack 3: Insider Threat**

Disgruntled operator changes reactor setpoint from safe HMI access.

**Mitigation:**

.. code-block:: python

    # Implement dual-authorization for critical commands
    def execute_critical_command(cmd, operator1, operator2):
        if cmd.is_critical():
            # Require two operators to approve
            approval1 = operator1.approve(cmd)
            approval2 = operator2.approve(cmd)
            
            if approval1 and approval2:
                log_audit(f"Critical command: {cmd} by {operator1}, {operator2}")
                execute(cmd)
            else:
                deny(cmd, "Dual authorization required")

HMI Hardening Best Practices
=============================

**1. Authentication:**

.. code-block:: c

    // Implement MFA for HMI login
    bool hmi_authenticate(char *username, char *password, char *totp_code) {
        if (!verify_password(username, password)) {
            return false;
        }
        
        // Verify TOTP (Time-based One-Time Password)
        if (!verify_totp(username, totp_code)) {
            log_security_event("MFA failed", username);
            return false;
        }
        
        return true;
    }

**2. Input Validation:**

.. code-block:: python

    def validate_setpoint(value, min_val, max_val):
        """Validate operator input to prevent out-of-range values"""
        try:
            value = float(value)
        except ValueError:
            raise ValidationError("Invalid numeric input")
        
        if not (min_val <= value <= max_val):
            raise ValidationError(f"Value {value} outside range [{min_val}, {max_val}]")
        
        return value

**3. Session Management:**

.. code-block:: python

    class HMISession:
        def __init__(self, username, timeout=1800):
            self.username = username
            self.session_id = generate_secure_token()
            self.created_at = time.time()
            self.timeout = timeout
        
        def is_expired(self):
            return (time.time() - self.created_at) > self.timeout
        
        def renew(self):
            self.created_at = time.time()

**4. Audit Logging:**

.. code-block:: python

    def log_hmi_action(user, action, details):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'ip_address': request.remote_addr,
            'action': action,
            'details': details
        }
        
        # Log to SIEM
        siem.send_event('HMI_ACTION', log_entry)
        
        # Also log locally (in case network fails)
        local_log.append(log_entry)

Exam Questions
==============

**Q1: HMI Design Flaw (Medium)**

An HMI allows operators to disable safety alarms. An attacker compromises operator credentials. What design flaw exists?

**Answer:**

**Flaw:** No separation between control and safety functions.

**Fix:**

- Safety-critical functions (alarm disable) should require:
  1. Higher privilege level (safety engineer, not operator)
  2. Physical key switch (cannot be done remotely)
  3. Dual authorization
  4. Time-limited (alarm disable only for 1 hour, then auto-re-enable)

**Q2: Legacy HMI Migration (Hard)**

You must migrate from unsecured legacy HMI (Windows XP, no patches) to secure modern HMI without process downtime. Design migration strategy.

**Answer:**

**Phased Migration:**

.. code-block:: text

    Phase 1: Parallel Operation (2 months)
    ├─ Install new HMI alongside legacy
    ├─ Configure data mirroring (PLC → both HMIs)
    ├─ Operators train on new HMI
    └─ Validate functionality
    
    Phase 2: Transition (1 month)
    ├─ Primary: New HMI
    ├─ Backup: Legacy HMI (read-only)
    └─ Monitor for issues
    
    Phase 3: Decommission (1 week)
    ├─ Remove legacy HMI
    └─ Full cutover to new HMI

**Rollback Plan:** If new HMI fails, operators revert to legacy HMI within 5 minutes.

Standards
=========

- **IEC 62443-3-3:** Network security
- **IEC 62443-4-1:** Secure product development lifecycle
- **NIST SP 800-82:** Guide to ICS security

**END OF DOCUMENT**
