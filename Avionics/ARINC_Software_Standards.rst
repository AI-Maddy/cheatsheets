====================================================================
ARINC Software Standards — 613/614/615/615A/645/665/667
====================================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC Software Standards** define the **lifecycle, distribution, and management** of avionics software from development through operational deployment.

**Core Standards:**

.. code-block:: text

   Standard  Title                          Focus
   ────────  ─────────────────────────────  ──────────────────────────
   ARINC 613 Ada Programming Language       Historical (1987)
   ARINC 614 Firmware Loader Protocol       Shop-level loading (1989)
   ARINC 615  Software Data Loader (PDL)    Serial/floppy (1992)
   ARINC 615A Software Loader (Ethernet)    Modern Ethernet (2023)
   ARINC 645 Software Terminology           Standard definitions
   ARINC 665 Loadable Software Parts (LSP)  Part numbering, compatibility
   ARINC 667 File Loading System (FLS)      Lifecycle management

**Key Concepts:**

1. **LSP (Loadable Software Part):**
   - Standard format for avionics software packages
   - Part number, version, compatibility rules
   - Used by: FMS databases, flight control software, display applications

2. **LSAP (Loadable Software Airplane Part):**
   - LSP + aircraft-specific configuration
   - Signed with ARINC 835 digital signatures
   - Distributed via ARINC 827 secure channels

3. **Data Loading Evolution:**

.. code-block:: text

   Year  Standard    Media                Speed        Security
   ────  ──────────  ───────────────────  ───────────  ──────────
   1989  ARINC 614   RS-232 serial        9.6 kbps     None
   1992  ARINC 615   3.5" floppy disk     ~50 kB/s     Checksum
   2002  ARINC 615-4 PCMCIA card          ~500 kB/s    CRC-32
   2023  ARINC 615A  Ethernet (RJ-45)     100 Mbps     ARINC 827

4. **FLS (File Loading System) — ARINC 667:**
   - **Upload:** Transfer LSAPs to aircraft (databases, software updates)
   - **Download:** Retrieve logs, configuration data
   - **Lifecycle:** Distribution → Installation → Activation → Rollback

================================================================================
1. ARINC 613 — Ada Programming Language (1987)
================================================================================

**1.1 Historical Context**
---------------------------

**Background:**
- **1983:** US Department of Defense mandates Ada for embedded systems
- **1986:** Airlines (AEEC) select Ada as high-order language for avionics
- **Dec 31, 1987:** ARINC 613 published (Ada guidance for commercial aviation)

**Why Ada?**
- **Type Safety:** Strong typing prevents common bugs (buffer overflows)
- **Concurrency:** Built-in tasking model for real-time systems
- **Standardized:** Single language across vendors (vs C dialects)
- **DO-178B Compatible:** Easy to certify for DAL A (critical software)

**1.2 ARINC 613 Content**
--------------------------

**Compiler Requirements:**
- **Validation:** Must pass ACVC (Ada Compiler Validation Capability) tests
- **Annex Support:** Real-Time Annex (tasking), Systems Programming Annex
- **Optimization:** -O2 maximum (higher levels may break timing)

**Programming Practices:**
- **Tasking:** Use protected types (Ada 95+) for shared data
- **Exception Handling:** Minimize exceptions (performance penalty)
- **Memory Management:** Static allocation preferred (no `new` in flight-critical code)

**Example Code:**

.. code-block:: ada

   -- ARINC 613 compliant flight control task
   
   with Ada.Real_Time; use Ada.Real_Time;
   
   package body Flight_Control is
      
      -- Protected object for shared data (thread-safe)
      protected Airspeed_Monitor is
         procedure Update (New_Speed : Float);
         function Get_Speed return Float;
      private
         Current_Speed : Float := 0.0;
      end Airspeed_Monitor;
      
      protected body Airspeed_Monitor is
         procedure Update (New_Speed : Float) is
         begin
            Current_Speed := New_Speed;
         end Update;
         
         function Get_Speed return Float is
         begin
            return Current_Speed;
         end Get_Speed;
      end Airspeed_Monitor;
      
      -- Periodic task (10 Hz update rate)
      task body Control_Loop is
         Period : constant Time_Span := Milliseconds (100);
         Next_Time : Time := Clock;
      begin
         loop
            -- Read sensors
            declare
               Speed : constant Float := Airspeed_Monitor.Get_Speed;
            begin
               -- Control logic (omitted)
               null;
            end;
            
            -- Wait for next period
            Next_Time := Next_Time + Period;
            delay until Next_Time;
         end loop;
      end Control_Loop;
      
   end Flight_Control;

**1.3 Modern Status**
----------------------

**Decline of Ada:**
- **2000s:** Industry shift to C/C++ (better tooling, larger talent pool)
- **Modern Avionics:** C (DO-178C), C++ (A350, 787), Rust (experimental)
- **Legacy Systems:** Ada still in F-22, A400M, some Boeing systems

**ARINC 613 Legacy:**
- **Historical Reference:** Rarely used in new projects
- **Lessons Learned:** Influenced MISRA C (type safety, concurrency patterns)

================================================================================
2. ARINC 614 — Firmware Loader Protocol (1989)
================================================================================

**2.1 Overview**
-----------------

**Purpose:**
Shop-level firmware loading for Line Replaceable Modules (LRMs) using serial RS-232.

**Typical Use Case:**
- Avionics shop receives LRM (e.g., flight control computer) needing software update
- Connect RS-232 cable from loader (PC) to LRM
- Transfer firmware binary (OBRM - On-Board Replaceable Module format)

**2.2 Protocol Details**
-------------------------

**Physical Layer:**
- **Interface:** RS-232 (EIA-232)
- **Connector:** DB-9 or DB-25
- **Baud Rate:** 9600 bps (standard), up to 115200 bps (extended)
- **Parity:** Even, 8 data bits, 1 stop bit

**Message Format:**

.. code-block:: text

   [STX][CMD][DATA...][CRC][ETX]
   
   STX: Start of Text (0x02)
   CMD: Command byte (0x10 = Start Load, 0x20 = Data Block, 0x30 = End)
   DATA: Firmware data (128-byte blocks typical)
   CRC: 16-bit CRC (polynomial 0x1021 - CCITT)
   ETX: End of Text (0x03)

**Example C Code:**

.. code-block:: c

   #include <stdint.h>
   #include <stdio.h>
   
   // ARINC 614 command codes
   #define CMD_START_LOAD  0x10
   #define CMD_DATA_BLOCK  0x20
   #define CMD_END_LOAD    0x30
   #define CMD_ACK         0x06
   #define CMD_NAK         0x15
   
   // CRC-CCITT calculation
   uint16_t crc_ccitt(uint8_t *data, size_t len) {
       uint16_t crc = 0xFFFF;
       for (size_t i = 0; i < len; i++) {
           crc ^= (data[i] << 8);
           for (int j = 0; j < 8; j++) {
               if (crc & 0x8000)
                   crc = (crc << 1) ^ 0x1021;
               else
                   crc <<= 1;
           }
       }
       return crc;
   }
   
   // Send ARINC 614 data block
   int send_data_block(int serial_fd, uint8_t *data, size_t len) {
       uint8_t packet[256];
       size_t idx = 0;
       
       // Build packet
       packet[idx++] = 0x02;  // STX
       packet[idx++] = CMD_DATA_BLOCK;
       memcpy(&packet[idx], data, len);
       idx += len;
       
       // Add CRC
       uint16_t crc = crc_ccitt(&packet[1], idx - 1);
       packet[idx++] = (crc >> 8) & 0xFF;
       packet[idx++] = crc & 0xFF;
       packet[idx++] = 0x03;  // ETX
       
       // Transmit
       write(serial_fd, packet, idx);
       
       // Wait for ACK/NAK
       uint8_t response;
       read(serial_fd, &response, 1);
       return (response == CMD_ACK) ? 0 : -1;
   }

**2.3 Limitations**
--------------------

- **Slow:** 9600 bps = ~1 KB/s (10 MB file = 3 hours!)
- **No Security:** No authentication, encryption
- **Shop-Only:** Requires physical access to LRM (not suitable for aircraft)

**Superseded by ARINC 615/615A** for aircraft loading.

================================================================================
3. ARINC 615 — Software Data Loader (PDL/ADL)
================================================================================

**3.1 Introduction**
---------------------

**Key Innovation:**
Portable Data Loader (PDL) + Airborne Data Loader (ADL) architecture.

.. code-block:: text

   Ground Network → PDL (portable) → Aircraft → ADL (installed)
   
   PDL: Laptop/tablet with 3.5" floppy drive
   ADL: Airborne computer with data loader interface

**Publication Dates:**
- **ARINC 615-3:** Jul 31, 1992 (original, floppy-based)
- **ARINC 615-4:** Apr 30, 2002 (PCMCIA cards, USB flash)

**3.2 PDL (Portable Data Loader)**
------------------------------------

**Hardware:**
- **1992 Version:** Ruggedized laptop, 3.5" floppy drive (1.44 MB)
- **2002 Version:** Panasonic Toughbook, PCMCIA Type II slot
- **Display:** VGA screen showing load progress

**Software:**
- **OS:** DOS (1992), Windows XP (2002), Linux (modern)
- **Application:** PDL software validates LSP, manages upload/download

**Physical Connection:**

.. code-block:: text

   PDL ──[RS-422]─→ Aircraft Data Loader Port (ARINC 600 connector)
                    
   Pin Assignments:
   Pin 1: +28 VDC (aircraft power)
   Pin 2: GND
   Pin 3: TX+ (differential RS-422)
   Pin 4: TX-
   Pin 5: RX+
   Pin 6: RX-

**3.3 ADL (Airborne Data Loader)**
------------------------------------

**Functions:**
1. **Upload:** Receive LSP from PDL → Store in NVM (non-volatile memory)
2. **Validate:** Check CRC, part number compatibility
3. **Activate:** Copy LSP to active partition, reboot target LRU
4. **Download:** Transfer logs/config data to PDL for analysis

**Data Format:**

.. code-block:: text

   LSP File Structure:
   
   ┌────────────────────────────────┐
   │  Header (256 bytes)            │
   │  - Part number (ASCII)         │
   │  - Version (major.minor.patch) │
   │  - Build date/time             │
   │  - CRC-32 checksum             │
   │  - Target LRU type             │
   ├────────────────────────────────┤
   │  Software Binary (1-100 MB)    │
   │  - Compressed (gzip)           │
   │  - Encrypted (optional)        │
   ├────────────────────────────────┤
   │  Footer (64 bytes)             │
   │  - Digital signature (RSA)     │
   │  - Certificate ID              │
   └────────────────────────────────┘

**3.4 Protocol**
-----------------

**ARINC 615 Message Format:**

.. code-block:: python

   class ARINC615Message:
       def __init__(self, msg_type, sequence, data):
           self.header = 0xA5  # Sync byte
           self.msg_type = msg_type
           self.sequence = sequence  # Packet number (0-65535)
           self.length = len(data)
           self.data = data
           self.crc = self.calculate_crc()
       
       def calculate_crc(self):
           import zlib
           payload = bytes([self.msg_type, self.sequence >> 8, 
                           self.sequence & 0xFF, self.length]) + self.data
           return zlib.crc32(payload) & 0xFFFFFFFF
       
       def to_bytes(self):
           packet = bytearray()
           packet.append(self.header)
           packet.append(self.msg_type)
           packet.append((self.sequence >> 8) & 0xFF)
           packet.append(self.sequence & 0xFF)
           packet.append((self.length >> 8) & 0xFF)
           packet.append(self.length & 0xFF)
           packet.extend(self.data)
           packet.extend(self.crc.to_bytes(4, 'big'))
           return bytes(packet)
   
   # Example: Upload LSP
   def upload_lsp(serial_port, lsp_file):
       with open(lsp_file, 'rb') as f:
           lsp_data = f.read()
       
       # Send in 1024-byte chunks
       chunk_size = 1024
       sequence = 0
       
       for offset in range(0, len(lsp_data), chunk_size):
           chunk = lsp_data[offset:offset+chunk_size]
           msg = ARINC615Message(msg_type=0x10,  # Data transfer
                                 sequence=sequence,
                                 data=chunk)
           serial_port.write(msg.to_bytes())
           
           # Wait for ACK
           ack = serial_port.read(1)
           if ack != b'\x06':
               raise IOError(f"NAK received at sequence {sequence}")
           
           sequence += 1
       
       print(f"Upload complete: {len(lsp_data)} bytes, {sequence} packets")

**3.5 Limitations of ARINC 615**
----------------------------------

- **Speed:** RS-422 at 115200 bps = ~11 KB/s (10 MB = 15 minutes)
- **Media:** Floppy/PCMCIA limited capacity (few hundred MB max)
- **No Remote Loading:** Requires physical access to aircraft

→ **Solved by ARINC 615A (Ethernet-based)**

================================================================================
4. ARINC 615A — Modern Ethernet Data Loader (2023)
================================================================================

**4.1 Key Improvements**
-------------------------

**ARINC 615A-4 (Jul 23, 2023) Features:**

.. code-block:: text

   Feature               ARINC 615           ARINC 615A
   ────────────────────  ──────────────────  ─────────────────────
   Physical Interface    RS-422 serial       Ethernet (RJ-45)
   Speed                 115 kbps            100 Mbps (1000x faster)
   Protocol              Proprietary         FTP/TFTP/HTTP
   Media                 Floppy/PCMCIA       Network (WiFi, LAN)
   Remote Loading        No                  Yes (gate, hangar)
   Security              CRC-32 only         ARINC 827 (PKI, AES)
   File Size             <500 MB             No limit (multi-GB)

**4.2 Architecture**
---------------------

.. code-block:: text

   ┌──────────────────────────────────────────────────────────┐
   │              Ground Network                               │
   │  ┌──────────────┐        ┌──────────────┐                │
   │  │ Airline      │        │  OEM         │                │
   │  │ Server       │───────→│  LSP Repo    │                │
   │  │ (LSP Dist)   │        │  (Signed)    │                │
   │  └──────┬───────┘        └──────────────┘                │
   │         │                                                 │
   │         │ ARINC 827 (encrypted distribution)             │
   │         ▼                                                 │
   │  ┌──────────────┐                                        │
   │  │ Ground       │                                        │
   │  │ Equipment    │                                        │
   │  │ (WiFi/LAN)   │                                        │
   │  └──────┬───────┘                                        │
   └─────────┼──────────────────────────────────────────────────┘
             │
             │ Ethernet (CAT6, WiFi 6)
             ▼
   ┌─────────────────────────────────────────────────────────┐
   │         Aircraft Avionics Network                        │
   │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐ │
   │  │  FMS         │   │  Flight Ctrl │   │  Display     │ │
   │  │  (615A ADL)  │   │  (615A ADL)  │   │  (615A ADL)  │ │
   │  └──────────────┘   └──────────────┘   └──────────────┘ │
   │                                                          │
   │  Each LRU has embedded ARINC 615A server                 │
   └──────────────────────────────────────────────────────────┘

**4.3 Network Protocol**
--------------------------

**FTP-Based Loading:**

.. code-block:: python

   import ftplib
   import hashlib
   
   class ARINC615A_Loader:
       def __init__(self, aircraft_ip, username='admin', password=''):
           """Connect to aircraft ADL via FTP"""
           self.ftp = ftplib.FTP(aircraft_ip)
           self.ftp.login(username, password)
           self.ftp.cwd('/lsp_upload')  # Standard upload directory
       
       def upload_lsp(self, lsp_file, target_lru):
           """
           Upload LSP to specific LRU.
           
           Args:
               lsp_file: Path to LSP file (e.g., FMS_DB_2024_01.lsp)
               target_lru: LRU identifier (e.g., 'FMS1', 'FCPC2')
           """
           # Calculate SHA-256 hash (integrity check)
           with open(lsp_file, 'rb') as f:
               lsp_data = f.read()
               lsp_hash = hashlib.sha256(lsp_data).hexdigest()
           
           # Upload file
           print(f"Uploading {lsp_file} to {target_lru}...")
           with open(lsp_file, 'rb') as f:
               self.ftp.storbinary(f'STOR {target_lru}/{lsp_file}', f)
           
           # Verify upload (retrieve hash from server)
           response = self.ftp.sendcmd(f'VERIFY {target_lru}/{lsp_file}')
           server_hash = response.split()[1]
           
           if server_hash == lsp_hash:
               print(f"Upload verified: SHA-256 {lsp_hash[:16]}...")
               return True
           else:
               print("ERROR: Hash mismatch!")
               return False
       
       def activate_lsp(self, target_lru, lsp_file):
           """Activate uploaded LSP (requires LRU reboot)"""
           cmd = f'ACTIVATE {target_lru}/{lsp_file}'
           response = self.ftp.sendcmd(cmd)
           print(f"Activation response: {response}")
           # LRU will reboot and load new software
       
       def download_logs(self, target_lru, output_file):
           """Download fault logs from LRU"""
           with open(output_file, 'wb') as f:
               self.ftp.retrbinary(f'RETR {target_lru}/fault_log.txt', f.write)
           print(f"Downloaded logs to {output_file}")
   
   # Example usage
   loader = ARINC615A_Loader(aircraft_ip='192.168.10.100')
   loader.upload_lsp('FMS_DB_2026_01.lsp', target_lru='FMS1')
   loader.activate_lsp('FMS1', 'FMS_DB_2026_01.lsp')
   loader.download_logs('FMS1', 'fms_logs.txt')

**4.4 Security (ARINC 827 Integration)**
------------------------------------------

**LSP Signing & Encryption:**

.. code-block:: text

   1. OEM creates LSP → Signs with RSA private key (ARINC 835)
   2. LSP distributed via ARINC 827 (encrypted channel)
   3. Aircraft ADL verifies signature before installation
   4. Rejects tampered/unsigned LSPs

**Certificate Validation:**

.. code-block:: python

   from cryptography.hazmat.primitives import hashes
   from cryptography.hazmat.primitives.asymmetric import rsa, padding
   from cryptography.x509 import load_pem_x509_certificate
   
   def verify_lsp_signature(lsp_file, signature_file, cert_file):
       """Verify LSP digital signature per ARINC 835"""
       # Load LSP data
       with open(lsp_file, 'rb') as f:
           lsp_data = f.read()
       
       # Load signature
       with open(signature_file, 'rb') as f:
           signature = f.read()
       
       # Load OEM certificate
       with open(cert_file, 'rb') as f:
           cert_pem = f.read()
           cert = load_pem_x509_certificate(cert_pem)
       
       # Extract public key
       public_key = cert.public_key()
       
       # Verify signature
       try:
           public_key.verify(
               signature,
               lsp_data,
               padding.PSS(
                   mgf=padding.MGF1(hashes.SHA256()),
                   salt_length=padding.PSS.MAX_LENGTH
               ),
               hashes.SHA256()
           )
           print("✓ LSP signature valid - OEM authenticated")
           return True
       except Exception as e:
           print(f"✗ LSP signature INVALID: {e}")
           return False

================================================================================
5. ARINC 645 — Software Terminology
================================================================================

**5.1 Purpose**
----------------

**Problem:**
Different vendors use conflicting terms (e.g., "software module" vs "loadable part" vs "firmware").

**Solution:**
ARINC 645 standardizes terminology for software lifecycle, enabling clear communication between airlines, OEMs, and regulators.

**5.2 Key Definitions**
------------------------

.. code-block:: text

   Term                  Definition
   ────────────────────  ──────────────────────────────────────────
   LSP                   Loadable Software Part (generic software)
   LSAP                  Loadable Software Airplane Part (aircraft-specific)
   FLS                   File Loading System (ARINC 667)
   PDL                   Portable Data Loader (ground equipment)
   ADL                   Airborne Data Loader (aircraft interface)
   LRU                   Line Replaceable Unit (hardware module)
   LRM                   LRU Replaceable Module (FRU within LRU)
   OBRM                  On-Board Replaceable Module (software image)
   Part Number           Unique identifier (e.g., "ARINC6" format)
   Build Record          Traceability data (compiler, date, engineer)

**5.3 Part Numbering (ARINC 665 Compatible)**
-----------------------------------------------

**Format:**

.. code-block:: text

   ARINC6-XXXX-YYY-ZZZ
   
   ARINC6: Prefix (ARINC 645 standard)
   XXXX: Equipment type (e.g., 4321 = FMS)
   YYY: Software function (e.g., 001 = navigation DB)
   ZZZ: Version (001, 002, ...)
   
   Example: ARINC6-4321-001-015
   → FMS navigation database, version 15

================================================================================
6. ARINC 665 — Loadable Software Parts (LSP)
================================================================================

**6.1 Scope**
--------------

**Purpose:**
Define standard format and metadata for LSPs to ensure compatibility across aircraft and vendors.

**6.2 LSP Metadata**
---------------------

**Required Fields:**

.. code-block:: python

   class LSP_Metadata:
       def __init__(self):
           self.part_number = ""       # ARINC6-XXXX-YYY-ZZZ
           self.version = ""           # Major.Minor.Patch (e.g., "3.2.1")
           self.build_date = ""        # ISO 8601 (2026-01-17T14:30:00Z)
           self.oem = ""               # Manufacturer (Boeing, Airbus, Honeywell)
           self.target_lru = []        # Compatible LRU types
           self.checksum_sha256 = ""   # Integrity verification
           self.signature = ""         # ARINC 835 digital signature
           self.dependencies = []      # Required LSPs (e.g., OS version)
       
       def validate_compatibility(self, installed_lru_type, installed_version):
           """Check if LSP compatible with target LRU"""
           if installed_lru_type not in self.target_lru:
               return False, "Incompatible LRU type"
           
           # Check version dependencies
           for dep in self.dependencies:
               if not self.check_dependency(dep, installed_version):
                   return False, f"Missing dependency: {dep}"
           
           return True, "Compatible"

**6.3 Compatibility Rules**
-----------------------------

**Version Compatibility:**

.. code-block:: text

   Rule 1: Major version change = incompatible (e.g., 2.x → 3.x)
   Rule 2: Minor version change = backward compatible (3.1 → 3.2)
   Rule 3: Patch version change = bug fix only (3.2.1 → 3.2.2)
   
   Example:
   Aircraft has FMS v3.1.5
   LSP requires v3.0.0 or higher → Compatible ✓
   LSP requires v4.0.0 → Incompatible ✗ (major version mismatch)

**6.4 Quality Control**
-------------------------

**Validation Process:**

.. code-block:: python

   def validate_lsp(lsp_file):
       """Comprehensive LSP validation per ARINC 665"""
       errors = []
       
       # 1. File integrity (SHA-256 checksum)
       calculated_hash = calculate_sha256(lsp_file)
       if calculated_hash != lsp.metadata.checksum_sha256:
           errors.append("Checksum mismatch - file corrupted")
       
       # 2. Digital signature (ARINC 835)
       if not verify_signature(lsp_file, lsp.metadata.signature):
           errors.append("Invalid digital signature - unauthorized LSP")
       
       # 3. Part number format (ARINC 645)
       if not re.match(r'ARINC6-\d{4}-\d{3}-\d{3}', lsp.metadata.part_number):
           errors.append("Invalid part number format")
       
       # 4. Version format (semantic versioning)
       if not re.match(r'\d+\.\d+\.\d+', lsp.metadata.version):
           errors.append("Invalid version format")
       
       # 5. Build date (must be within last 2 years for nav databases)
       build_date = parse_iso8601(lsp.metadata.build_date)
       if (datetime.now() - build_date).days > 730:
           errors.append("LSP expired (>2 years old)")
       
       return len(errors) == 0, errors

================================================================================
7. ARINC 667 — File Loading System (FLS) Lifecycle
================================================================================

**7.1 Overview**
-----------------

**FLS Functions:**
1. **Distribution:** OEM → Airline → Aircraft
2. **Installation:** LSP → NVM storage
3. **Activation:** Move LSP to active partition, reboot LRU
4. **Rollback:** Revert to previous version if failure
5. **Removal:** Delete obsolete LSPs

**7.2 Lifecycle Phases**
-------------------------

.. code-block:: text

   Phase          Description                    Tools/Standards
   ─────────────  ─────────────────────────────  ─────────────────
   1. Development OEM creates LSP               DO-178C, ARINC 665
   2. Signing     Digital signature (OEM key)    ARINC 835
   3. Distribution Encrypted delivery to airline ARINC 827
   4. Loading     PDL/Network upload to aircraft ARINC 615A
   5. Validation  Signature check, compatibility ARINC 665/835
   6. Installation Store in NVM (inactive)       ARINC 667
   7. Activation  Copy to active, reboot LRU     ARINC 667
   8. Verification BIT (Built-In Test) passes    Aircraft-specific
   9. Documentation Update CMM (Component Maint) ARINC 667
   10. Audit      Traceability logs              ARINC 842

**7.3 Activation Process**
----------------------------

**State Machine:**

.. code-block:: python

   class LSP_State(Enum):
       UPLOADED = 1      # Uploaded to aircraft, not installed
       INSTALLED = 2     # Stored in NVM, inactive
       ACTIVE = 3        # Running in LRU
       ROLLBACK = 4      # Previous version reactivated
       FAILED = 5        # Activation failed
   
   class FLS_Manager:
       def __init__(self):
           self.lsp_state = LSP_State.UPLOADED
           self.active_version = "3.1.0"
           self.backup_version = "3.0.5"
       
       def activate_lsp(self, new_lsp, new_version):
           """Activate new LSP with rollback on failure"""
           print(f"Activating LSP {new_version}...")
           
           # 1. Backup current active version
           self.backup_version = self.active_version
           
           # 2. Install new LSP to active partition
           self.install_to_active_partition(new_lsp)
           self.lsp_state = LSP_State.INSTALLED
           
           # 3. Reboot LRU
           self.reboot_lru()
           
           # 4. Run Built-In Test (BIT)
           if self.run_bit():
               self.lsp_state = LSP_State.ACTIVE
               self.active_version = new_version
               print(f"✓ Activation successful: {new_version}")
               return True
           else:
               # BIT failed - rollback
               print("✗ BIT failed - rolling back...")
               self.rollback_to_backup()
               return False
       
       def rollback_to_backup(self):
           """Revert to previous version"""
           print(f"Rolling back to {self.backup_version}...")
           self.install_to_active_partition(self.backup_version)
           self.reboot_lru()
           self.lsp_state = LSP_State.ROLLBACK
           print(f"✓ Rollback complete: {self.backup_version}")

**7.4 Documentation Requirements**
------------------------------------

**Records to Maintain:**

.. code-block:: text

   1. Load Report:
      - Date/time of loading
      - LSP part number, version
      - Aircraft tail number
      - Technician ID
      - Loading status (success/failure)
   
   2. Activation Record:
      - Pre-activation BIT results
      - Post-activation BIT results
      - Rollback events (if any)
   
   3. Audit Trail:
      - All LSP installations (current + historical)
      - Signature verification logs
      - Compliance with ARINC 842 (security updates)

**Example Log:**

.. code-block:: text

   ───────────────────────────────────────────────────────────
   LSP Installation Log
   ───────────────────────────────────────────────────────────
   Aircraft:      N12345 (Boeing 737-800)
   Date:          2026-01-17 14:45 UTC
   Technician:    J. Smith (License #987654)
   
   LSP Details:
   - Part Number: ARINC6-4321-001-020
   - Version:     3.2.0
   - OEM:         Honeywell
   - Target LRU:  FMS-1 (Position: E4-1)
   
   Pre-Load BIT:  PASS (all systems nominal)
   Load Status:   SUCCESS (1.2 GB transferred in 120 sec)
   Signature:     VERIFIED (OEM cert #ABC123)
   
   Activation:    SUCCESS
   Post-Load BIT: PASS
   
   Notes:         Replaces v3.1.5 (AIRAC cycle 2601 → 2602)
   ───────────────────────────────────────────────────────────

================================================================================
8. Integration Example: Complete Loading Workflow
================================================================================

**End-to-End Process:**

.. code-block:: python

   # Complete LSP loading workflow (ARINC 615A + 665 + 667 + 835)
   
   import ftplib
   from cryptography.hazmat.primitives import hashes
   from cryptography.hazmat.primitives.asymmetric import padding
   
   class Aircraft_LSP_Loader:
       def __init__(self, aircraft_ip, oem_cert_path):
           self.aircraft_ip = aircraft_ip
           self.oem_cert = load_certificate(oem_cert_path)
           self.fls = FLS_Manager()
       
       def load_lsp_complete(self, lsp_file, signature_file, target_lru):
           """
           Complete LSP loading workflow:
           1. Validate signature (ARINC 835)
           2. Upload via FTP (ARINC 615A)
           3. Validate compatibility (ARINC 665)
           4. Activate (ARINC 667)
           """
           # Step 1: Verify digital signature
           print("[1/4] Verifying LSP signature...")
           if not self.verify_signature(lsp_file, signature_file):
               print("✗ Signature verification failed - ABORT")
               return False
           print("✓ Signature valid")
           
           # Step 2: Upload to aircraft
           print("[2/4] Uploading LSP to aircraft...")
           loader = ARINC615A_Loader(self.aircraft_ip)
           if not loader.upload_lsp(lsp_file, target_lru):
               print("✗ Upload failed - ABORT")
               return False
           print("✓ Upload complete")
           
           # Step 3: Validate compatibility
           print("[3/4] Validating LSP compatibility...")
           lsp_meta = self.parse_lsp_metadata(lsp_file)
           lru_info = self.get_lru_info(target_lru)
           
           compatible, reason = lsp_meta.validate_compatibility(
               lru_info.type, lru_info.version
           )
           if not compatible:
               print(f"✗ Incompatible: {reason} - ABORT")
               return False
           print("✓ LSP compatible with target LRU")
           
           # Step 4: Activate LSP
           print("[4/4] Activating LSP...")
           if not self.fls.activate_lsp(lsp_file, lsp_meta.version):
               print("✗ Activation failed - rolled back to previous version")
               return False
           print("✓ LSP activated successfully")
           
           # Generate load report
           self.generate_load_report(lsp_meta, target_lru)
           return True
       
       def generate_load_report(self, lsp_meta, target_lru):
           """Generate ARINC 667 load report"""
           report = f"""
   ═══════════════════════════════════════════════════════════
   LSP Installation Report (ARINC 667)
   ═══════════════════════════════════════════════════════════
   Aircraft:      {self.aircraft_ip}
   Date:          {datetime.now().isoformat()}
   Target LRU:    {target_lru}
   
   LSP Information:
   - Part Number: {lsp_meta.part_number}
   - Version:     {lsp_meta.version}
   - OEM:         {lsp_meta.oem}
   - Build Date:  {lsp_meta.build_date}
   
   Verification:
   - Signature:   ✓ VALID (ARINC 835)
   - Checksum:    ✓ MATCH (SHA-256)
   - Compatibility: ✓ COMPATIBLE
   
   Activation:
   - Status:      ✓ SUCCESS
   - BIT Result:  PASS
   - Rollback:    Not required
   
   Compliance:
   - ARINC 615A:  ✓ (Ethernet upload)
   - ARINC 665:   ✓ (LSP format)
   - ARINC 667:   ✓ (FLS lifecycle)
   - ARINC 835:   ✓ (Digital signature)
   ═══════════════════════════════════════════════════════════
           """
           print(report)
           with open(f'load_report_{target_lru}.txt', 'w') as f:
               f.write(report)

================================================================================
9. Exam Preparation — 5 Questions
================================================================================

**Question 1: Software Loading Evolution (10 points)**

a) Compare ARINC 615 (1992) vs ARINC 615A (2023) in terms of speed and media. (4 pts)
b) Why is ARINC 615A necessary for modern aircraft? (3 pts)
c) What security enhancement does 615A provide? (3 pts)

**Answer:**

a) **Speed & Media Comparison:**

.. code-block:: text

   ARINC 615 (1992):
   - Media: 3.5" floppy disk (1.44 MB)
   - Interface: RS-422 serial
   - Speed: 115 kbps = ~11 KB/s
   - Time for 10 MB: ~15 minutes
   
   ARINC 615A (2023):
   - Media: Ethernet network (no physical media)
   - Interface: RJ-45 (100 Mbps) or WiFi (1 Gbps)
   - Speed: 100 Mbps = ~10 MB/s
   - Time for 10 MB: ~1 second
   
   Speed improvement: 1000× faster!

b) **Why 615A Necessary:**
   - **File sizes:** Modern avionics software 100 MB - 10 GB (navigation databases, synthetic vision terrain)
   - **Fleet operations:** Need to update hundreds of aircraft quickly (overnight)
   - **Remote loading:** Load software at gate/hangar without physical PDL connection
   - **Reduced maintenance time:** Minutes vs hours per aircraft

c) **Security Enhancement:**
   - **ARINC 827 integration:** PKI-based authentication, AES-256 encryption
   - **Digital signatures (ARINC 835):** Every LSP signed by OEM, verified before installation
   - **Network security:** TLS 1.3 for FTP/HTTP transfers
   - **Prevents:** Malware, unauthorized software, tampering

---

**Question 2: LSP Compatibility (12 points)**

An airline has FMS software version 4.2.3. They receive LSP updates:
- LSP_A: v4.2.5 (bug fix)
- LSP_B: v4.3.0 (new features)
- LSP_C: v5.0.0 (major rewrite)

a) Which LSPs are compatible per ARINC 665 versioning rules? (6 pts)
b) If LSP_B requires dependency "GPS_Driver >= 2.1.0" and aircraft has GPS_Driver 2.0.5, what happens? (3 pts)
c) How does FMS validate compatibility before installation? (3 pts)

**Answer:**

a) **Compatibility Analysis:**

.. code-block:: text

   Current version: 4.2.3
   
   LSP_A: v4.2.5
   - Same major (4), same minor (2), different patch (3→5)
   - COMPATIBLE ✓ (patch = bug fix only, backward compatible)
   
   LSP_B: v4.3.0
   - Same major (4), different minor (2→3)
   - COMPATIBLE ✓ (minor = new features, backward compatible)
   - Note: Will ADD features, won't break existing functionality
   
   LSP_C: v5.0.0
   - Different major (4→5)
   - INCOMPATIBLE ✗ (major = breaking changes, not backward compatible)
   - Requires: Aircraft recertification, pilot retraining, hardware upgrade

b) **Missing Dependency:**

.. code-block:: python

   Required: GPS_Driver >= 2.1.0
   Installed: GPS_Driver 2.0.5
   
   Result: LSP_B installation REJECTED
   
   FMS displays:
   "LOAD FAILED: Missing dependency GPS_Driver 2.1.0 (installed: 2.0.5)"
   
   Action required:
   1. First update GPS_Driver to 2.1.0 or higher
   2. Then install LSP_B

c) **Validation Process:**

.. code-block:: python

   def validate_before_install(lsp, aircraft_config):
       # 1. Check part number compatibility
       if lsp.part_number.equipment_type != aircraft_config.fms_type:
           return False, "Wrong equipment type"
       
       # 2. Check version compatibility (semantic versioning)
       if lsp.version.major != aircraft_config.current_version.major:
           return False, "Major version mismatch"
       
       # 3. Check all dependencies
       for dep in lsp.dependencies:
           if not aircraft_config.has_dependency(dep):
               return False, f"Missing {dep}"
       
       # 4. Check storage space
       if lsp.file_size > aircraft_config.available_nvm:
           return False, "Insufficient NVM space"
       
       return True, "Compatible"

---

**Question 3: FLS Lifecycle (10 points)**

During LSP activation, BIT (Built-In Test) fails.

a) What should the FLS do per ARINC 667? (4 pts)
b) Describe the rollback process. (4 pts)
c) How is this event documented? (2 pts)

**Answer:**

a) **FLS Response to BIT Failure:**

.. code-block:: text

   1. Detect BIT failure immediately after LSP activation
   2. Halt activation process (do NOT proceed to active state)
   3. Trigger automatic rollback to previous version
   4. Log failure event (ARINC 667 audit trail)
   5. Alert crew via EICAS/ECAM: "FMS LSP ACTIVATION FAILED"

b) **Rollback Process:**

.. code-block:: python

   def rollback_procedure():
       """ARINC 667 rollback on BIT failure"""
       # 1. Retrieve backup version from NVM
       backup_lsp = read_from_nvm(partition='backup')
       
       # 2. Copy backup to active partition
       write_to_nvm(backup_lsp, partition='active')
       
       # 3. Reboot LRU
       reboot_lru()
       
       # 4. Verify BIT with backup version
       if run_bit() == PASS:
           log("Rollback successful - previous version restored")
           return True
       else:
           log("CRITICAL: Rollback BIT failed - LRU fault")
           trigger_maintenance_alert()
           return False
   
   Timeline:
   - BIT failure detected: T+0 seconds
   - Rollback initiated: T+1 second
   - LRU reboot: T+2-5 seconds
   - Backup BIT complete: T+10 seconds
   - Aircraft operational: T+15 seconds

c) **Documentation:**

.. code-block:: text

   Event logged in:
   
   1. Aircraft CMM (Component Maintenance Manual) log:
      "LSP activation failed, rolled back to v4.2.3"
   
   2. FLS audit trail (ARINC 667):
      - Timestamp: 2026-01-17T15:30:45Z
      - Event: ACTIVATION_FAILED
      - LSP: ARINC6-4321-001-020 (v4.3.0)
      - Reason: BIT_FAILURE (code 0x1234)
      - Action: ROLLBACK_TO_v4.2.3
      - Result: SUCCESS
   
   3. Maintenance action required:
      - Investigate why new LSP failed BIT
      - Contact OEM for updated LSP or guidance

---

**Question 4: Digital Signatures (8 points)**

a) Why are LSPs digitally signed per ARINC 835? (3 pts)
b) What happens if signature verification fails? (3 pts)
c) How often are OEM signing certificates renewed? (2 pts)

**Answer:**

a) **Purpose of Digital Signatures:**
   1. **Authentication:** Proves LSP from legitimate OEM (not malware)
   2. **Integrity:** Detects any tampering/corruption during distribution
   3. **Non-repudiation:** OEM cannot deny creating/distributing LSP
   4. **Compliance:** DO-326A/DO-356A cybersecurity requirements

b) **Signature Verification Failure:**

.. code-block:: python

   if not verify_signature(lsp_file, signature_file):
       # CRITICAL SECURITY EVENT
       log("SECURITY ALERT: LSP signature invalid!")
       
       # Actions:
       # 1. REJECT installation (do not proceed)
       reject_lsp("Signature verification failed")
       
       # 2. Alert crew
       display_warning("LSP SIGNATURE INVALID - INSTALLATION BLOCKED")
       
       # 3. Log security event (ARINC 842)
       log_security_event(
           type="INVALID_SIGNATURE",
           lsp=lsp_file,
           timestamp=datetime.now()
       )
       
       # 4. Notify airline cybersecurity team
       send_alert_to_ops("Potential malware detected in LSP")
       
       # 5. Quarantine LSP
       move_to_quarantine(lsp_file)
   
   Result: Aircraft protected from unauthorized software

c) **Certificate Renewal:**
   - **Typical lifespan:** 2-5 years (per ARINC 827 PKI policy)
   - **Renewal process:** OEM generates new key pair, distributes updated certificate to airlines
   - **Chain of trust:** Root CA (Certification Authority) validates OEM certificates
   - **Overlap period:** New/old certificates both valid for 90 days during transition

---

**Question 5: Complete Workflow (10 points)**

An airline needs to update FMS navigation database (AIRAC cycle).

a) List the ARINC standards involved in the complete workflow. (4 pts)
b) Describe the process from OEM to aircraft activation. (4 pts)
c) What happens if database effective date is expired? (2 pts)

**Answer:**

a) **ARINC Standards Involved:**

.. code-block:: text

   Standard   Role
   ─────────  ───────────────────────────────────────────────
   ARINC 424  Navigation database format (waypoints, airways)
   ARINC 665  LSP metadata, part numbering
   ARINC 615A Upload LSP to aircraft (Ethernet)
   ARINC 667  FLS lifecycle (install, activate, document)
   ARINC 827  Secure distribution (encryption)
   ARINC 835  Digital signatures (authentication)
   ARINC 842  Audit trail (compliance with security policy)

b) **Complete Process:**

.. code-block:: text

   Step 1: OEM Creates LSP
   - Jeppesen compiles AIRAC cycle 2602 database
   - Format: ARINC 424-22 (latest standard)
   - Part number: ARINC6-4321-001-026 (cycle 26-02)
   - Sign with OEM private key (ARINC 835)
   
   Step 2: Secure Distribution (ARINC 827)
   - Encrypt LSP with AES-256
   - Upload to airline server via TLS 1.3
   - Airline downloads to ground network
   
   Step 3: Aircraft Upload (ARINC 615A)
   - Technician connects laptop to aircraft WiFi
   - FTP transfer to FMS: 1.2 GB in ~2 minutes
   - Verify SHA-256 checksum
   
   Step 4: Validation (ARINC 665)
   - Check part number compatibility
   - Verify digital signature (ARINC 835)
   - Confirm effective dates (2026-02-22 to 2026-03-21)
   
   Step 5: Activation (ARINC 667)
   - Install to NVM inactive partition
   - Reboot FMS
   - Run BIT (verify database loads correctly)
   - If BIT pass: Activate
   - If BIT fail: Rollback to previous database
   
   Step 6: Documentation
   - Log installation in CMM
   - Generate load report (ARINC 667)
   - Update aircraft configuration database

c) **Expired Database:**

.. code-block:: python

   # Check effective dates
   database_effective_start = parse_date("2026-02-22")
   database_effective_end = parse_date("2026-03-21")
   current_date = datetime.now()
   
   if current_date < database_effective_start:
       warning("Database not yet effective - cannot activate")
       # Can be loaded (inactive), but not activated until effective date
   
   elif current_date > database_effective_end:
       warning("Database EXPIRED - flight crew alerted")
       # FMS displays: "NAV DATABASE EXPIRED"
       # Still usable, but crew must verify approach procedure validity
       # Regulatory: May prohibit RNAV/RNP approaches with expired DB
   
   Airline policy: Update database every 28 days (AIRAC cycle)
   Regulatory: FAA requires current database for IFR operations

================================================================================
10. Completion Checklist
================================================================================

□ Understand software loading evolution (614 → 615 → 615A)
□ Know LSP structure and metadata (ARINC 665)
□ Implement ARINC 615 serial protocol (CRC, ACK/NAK)
□ Use ARINC 615A Ethernet loading (FTP/TFTP)
□ Validate LSP digital signatures (ARINC 835)
□ Check version compatibility (semantic versioning)
□ Manage FLS lifecycle (install, activate, rollback - ARINC 667)
□ Generate load reports and audit trails
□ Integrate security standards (827, 835, 842)
□ Handle BIT failures and automatic rollback
□ Understand AIRAC cycle (28-day navigation database updates)
□ Maintain compliance documentation

================================================================================
11. Key Takeaways
================================================================================

1. **ARINC 615A = Modern Standard:** Ethernet replaces serial (1000× faster)

2. **LSP = Standard Package:** ARINC 665 defines format, metadata, compatibility

3. **LSAP = Aircraft-Specific:** LSP + configuration + signatures

4. **FLS (ARINC 667) = Lifecycle:** Distribution → Install → Activate → Rollback

5. **Security Mandatory:** ARINC 835 signatures + ARINC 827 encryption

6. **Semantic Versioning:** Major.Minor.Patch (4.2.3)
   - Patch: Bug fixes only (compatible)
   - Minor: New features (compatible)
   - Major: Breaking changes (incompatible)

7. **Rollback Critical:** BIT failure → automatic revert to previous version

8. **AIRAC Cycle:** Navigation databases updated every 28 days

9. **Documentation Required:** Load reports, audit trails (ARINC 667/842)

10. **Standards Integration:** 615A + 665 + 667 + 827 + 835 = complete system

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 613 — Software Considerations for Airborne Systems and Equipment Using the Ada Programming Language
- ARINC 614 — Firmware Loader Operational Characteristics
- ARINC 615-3/615-4 — Software Data Loader (Portable Data Loader)
- ARINC 615A-4 — Software Data Loader Using Ethernet Interface (Jul 23, 2023)
- ARINC 645 — Aeronautical Radio, Inc. Terminology Document
- ARINC 665 — Loadable Software Part Description (LSPD)
- ARINC 667 — Flight Deck Data File Loading System

**Security:**
- ARINC 827 — Electronic Distribution System (EDS)
- ARINC 835 — Software Upload and Retrieval with Digital Signature
- ARINC 842 — Design Guidance for Continued Airworthiness Security

**Regulatory:**
- DO-178C — Software Considerations in Airborne Systems
- DO-326A — Airworthiness Security Process Specification
- DO-356A — Airworthiness Security Methods and Considerations

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Standards:** ARINC 613/614/615/615A/645/665/667

================================================================================
