================================================================================
ARINC Standards - Real-World Project Experience
================================================================================

:Author: Madhavan Vivekanandan
:Date: January 21, 2026
:Projects: 10 Avionics Systems (2007-Present)
:Certification: DO-178B/C Level A/B/C Compliance

================================================================================
Overview
================================================================================

This document captures hands-on implementation experience across 9 ARINC standards
from actual production avionics systems deployed on commercial and military aircraft.

**Projects Covered:**
- Fuel Quantity Gauging System (FQGS)
- Flight Deck Video Displays (FDVD)
- AFIRS Satellite Data Unit
- Main Deck Cargo Loading System (MDCLS)
- Electronic Engine Control (EEC)
- Auxiliary Fuel Control Unit (AFCU)
- Data Loader for IMA Systems
- Intel Atom Avionics Platform

================================================================================
ARINC 429 - Digital Information Transfer System
================================================================================

**Standard:** ARINC 429 (Mark 33 Digital Information Transfer System)
**Experience:** 6+ projects
**Certification Level:** DO-178B/C Level A, B, C

Real-World Implementation
--------------------------------------------------------------------------------

**1. Fuel Quantity Gauging System**

**System Architecture:**
- Dual-channel ARINC 429 buses for redundancy
- 100 kbps low-speed bus for fuel data
- 32-bit word format: Label (8) + SDI (2) + Data (19) + SSM (2) + Parity (1)

**Data Types Transmitted:**
- Fuel quantity in gallons/kilograms (BNR format)
- Fuel temperature (BCD format)
- Tank identification and status
- System health monitoring

**Hardware Interface:**
- DDC BU-65591 ARINC 429 transceiver
- Differential twisted pair (78Ω impedance)
- 10V peak-to-peak signaling

**Software Implementation:**

.. code-block:: c

    // ARINC 429 Word Structure
    typedef struct {
        uint8_t  label;      // Octal label (8 bits)
        uint8_t  sdi;        // Source/Destination Identifier (2 bits)
        uint32_t data;       // Data field (19 bits)
        uint8_t  ssm;        // Sign/Status Matrix (2 bits)
        uint8_t  parity;     // Odd parity (1 bit)
    } arinc429_word_t;
    
    // Fuel Quantity Transmission (Label 104)
    void transmit_fuel_quantity(float fuel_gallons) {
        arinc429_word_t word;
        word.label = 0104;  // Octal 104 = Fuel Quantity
        word.sdi = 0;       // Main tank
        word.data = convert_bnr(fuel_gallons, 20);  // BNR format, 20-bit
        word.ssm = SSM_NORMAL_OPERATION;
        word.parity = calculate_odd_parity(&word);
        
        arinc429_tx(CHANNEL_A, &word);
        arinc429_tx(CHANNEL_B, &word);  // Redundant transmission
    }

**Label Mapping Used:**
- 104 (Octal): Fuel Quantity
- 105 (Octal): Fuel Temperature
- 106 (Octal): Fuel Flow Rate
- 270 (Octal): System Status
- 350 (Octal): Discrete Status

**Timing Requirements:**
- Update rate: 1 Hz for fuel quantity
- Response time: <50ms for critical alerts
- Bus arbitration: Round-robin scheduling

**Testing & Validation:**
- HIL testing with AIM GmbH test equipment
- Bus monitoring with Condor Engineering analyzer
- BER (Bit Error Rate) < 10^-9 required
- DO-178C coverage: Statement (100%), Branch (100%), MCDC (100%)

**2. Electronic Engine Control**

**Usage:**
- Engine parameters to/from FADEC
- Throttle position commands
- Engine health monitoring
- Vibration data transmission

**Critical Labels:**
- 011: N1 (Fan Speed)
- 012: N2 (Core Speed)
- 013: EGT (Exhaust Gas Temperature)
- 014: Fuel Flow
- 015: Oil Pressure

**3. AFIRS Satellite Data Unit**

**Interface:**
- Aircraft systems to SDU
- Flight data recording labels
- Position and altitude data
- Discrete aircraft events

**Implementation Notes:**
- Buffered architecture for satellite latency
- Label filtering for bandwidth optimization
- CRC validation beyond parity
- Non-volatile storage for critical messages

Lessons Learned
--------------------------------------------------------------------------------

**Do's:**
✓ Always implement dual-channel redundancy for safety-critical data
✓ Use hardware transceivers (DDC, Holt) for compliance
✓ Implement comprehensive BIT (Built-In Test)
✓ Follow DO-178C for label assignment and data encoding
✓ Use bus monitoring tools during integration

**Don'ts:**
✗ Don't rely solely on parity for error detection
✗ Don't exceed bus loading (use bus utilization analysis)
✗ Don't mix high-speed and low-speed on same bus
✗ Don't ignore SSM (Sign/Status Matrix) status

**Common Pitfalls:**
- Incorrect BNR/BCD encoding
- Parity calculation errors
- Bus loading exceeding 50% utilization
- Label collision between systems
- Timing violations in periodic transmission

================================================================================
ARINC 615A - Portable Data Loader
================================================================================

**Standard:** ARINC 615A (Software Data Loader)
**Experience:** Data Loader for IMA Systems
**Certification Level:** DO-178C Level C

Real-World Implementation
--------------------------------------------------------------------------------

**Project: IMA Data Loader**

**System Overview:**
- Portable data loading for Integrated Modular Avionics
- USB and Ethernet transfer media
- Target file servers on LRUs (Line Replaceable Units)

**Architecture:**

::

    ┌─────────────────┐
    │  Ground Station │
    │  (Laptop/PDL)   │
    └────────┬────────┘
             │ USB/Ethernet
    ┌────────▼────────┐
    │  Data Loader    │  ← ARINC 615A Protocol Handler
    │  Application    │
    └────────┬────────┘
             │ TFTP
    ┌────────▼────────┐
    │  Target File    │
    │  Server (LRU)   │
    └─────────────────┘

**Protocol Implementation:**

**1. File Transfer Protocol (TFTP-based)**

.. code-block:: c

    // ARINC 615A Load Session
    typedef enum {
        LOAD_INIT,
        LOAD_HEADER,
        LOAD_DATA,
        LOAD_VERIFY,
        LOAD_COMPLETE
    } load_state_t;
    
    // Transfer Header
    typedef struct {
        char part_number[32];
        char hardware_id[16];
        uint32_t file_size;
        uint16_t crc16;
        uint8_t  load_ratio;
    } arinc615a_header_t;
    
    // Data Loading Function
    int arinc615a_load_software(const char *filepath) {
        load_state_t state = LOAD_INIT;
        
        // Initialize transfer
        tftp_session_t *session = tftp_open(target_ip, ARINC615A_PORT);
        
        // Send load initialization
        arinc615a_send_init_request(session);
        
        // Upload header
        arinc615a_header_t header;
        fill_header(&header, filepath);
        tftp_write(session, &header, sizeof(header));
        
        // Transfer data blocks
        while (state != LOAD_COMPLETE) {
            switch(state) {
                case LOAD_DATA:
                    bytes_sent = tftp_send_block(session, data_buffer, BLOCK_SIZE);
                    update_progress(bytes_sent);
                    break;
                    
                case LOAD_VERIFY:
                    if (verify_crc(session)) {
                        state = LOAD_COMPLETE;
                    }
                    break;
            }
        }
        
        return LOAD_SUCCESS;
    }

**2. Status and Upload Information Files**

**Status File Format:**

.. code-block:: text

    ARINC615A-3
    STATUS_FILE_NAME=status.txt
    TARGET_HARDWARE=GE_IMA_LRU_001
    LOAD_STATUS=IN_PROGRESS
    PERCENT_COMPLETE=45
    ERROR_CODE=0x0000

**Upload Information File:**

.. code-block:: text

    UPLOAD_INFO_FILE_NAME=upload.txt
    PART_NUMBER=ABC123-456
    SERIAL_NUMBER=SN987654321
    SOFTWARE_VERSION=3.2.1
    LOAD_RATIO=100

**3. Error Handling**

**Common Error Codes:**
- 0x01: Header CRC Failure
- 0x02: Incompatible Hardware
- 0x03: Insufficient Memory
- 0x04: File System Error
- 0x05: Load Ratio Exceeded

**Recovery Mechanisms:**
- Automatic retry (max 3 attempts)
- Resume from last good block
- Fallback to previous software version

**Security Features:**
- Digital signature verification
- Part number validation
- Hardware compatibility check
- Software version dependency check

**Performance Metrics:**
- USB 2.0: ~10 MB/min typical
- Ethernet 100Base-T: ~30 MB/min typical
- Load verification: ~2 min for 50MB image

Lessons Learned
--------------------------------------------------------------------------------

**Critical Implementation Points:**
✓ Implement robust timeout handling for network interruptions
✓ Use CRC32 instead of CRC16 for large files
✓ Provide detailed progress feedback (operator visibility)
✓ Validate hardware compatibility before loading
✓ Keep previous software version as fallback

**Common Issues:**
- Network interruptions during large transfers
- Incompatible software/hardware versions
- Insufficient storage space on target
- CRC mismatches (cosmic ray hits during transfer)

================================================================================
ARINC 664 (AFDX) - Avionics Full Duplex Switched Ethernet
================================================================================

**Standard:** ARINC 664 Part 7 (AFDX)
**Experience:** 3+ projects (Intel Atom Platform, MDCLS, FDVD)
**Certification Level:** DO-178C Level B/C

Real-World Implementation
--------------------------------------------------------------------------------

**Project 1: Intel Atom Avionics Platform**

**System Architecture:**

::

    ┌─────────────────────────────────────────────────────────┐
    │                   AFDX Network Backbone                  │
    │  (Redundant Network A & B - 100 Mbps Full Duplex)      │
    └──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬───┘
       │      │      │      │      │      │      │      │
    ┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐
    │ IMA ││FDAU ││ FMS ││ FCU ││ WXR ││TCAS ││ GPU ││ SDU │
    └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘

**Virtual Link (VL) Configuration:**

.. code-block:: c

    // AFDX Virtual Link Definition
    typedef struct {
        uint16_t vl_id;                 // Virtual Link ID
        uint32_t bandwidth_mbps;         // BAG (Bandwidth Allocation Gap)
        uint8_t  mac_address[6];        // Multicast MAC
        uint32_t bag_us;                // Burst Allocation Gap (microseconds)
        uint16_t max_frame_size;        // Maximum Ethernet frame size
        uint8_t  redundancy_mode;       // Network A/B redundancy
    } afdx_virtual_link_t;
    
    // Example VL Configuration
    const afdx_virtual_link_t vl_config[] = {
        // VL_ID  BW    MAC_ADDR                BAG     MaxFrame  Redund
        {  1001,  10,  {0x03,0x00,0x00,0x01,0x00,0x01}, 1000,   1518,    REDUNDANT },
        {  1002,  50,  {0x03,0x00,0x00,0x01,0x00,0x02}, 2000,   1518,    REDUNDANT },
        {  2001,   5,  {0x03,0x00,0x00,0x02,0x00,0x01}, 4000,   512,     REDUNDANT },
    };

**BAG (Bandwidth Allocation Gap) Values:**
- 128 µs (7.8 kHz) - High-priority control data
- 1 ms (1 kHz) - Flight control, navigation
- 2 ms (500 Hz) - Sensor data
- 4 ms (250 Hz) - Display updates
- 8-128 ms - Lower priority data

**Software Implementation:**

**1. VL Transmission:**

.. code-block:: c

    // AFDX Transmit on Virtual Link
    int afdx_transmit_vl(uint16_t vl_id, const uint8_t *data, uint16_t len) {
        afdx_frame_t frame;
        
        // Get VL configuration
        afdx_virtual_link_t *vl = get_vl_config(vl_id);
        
        // Build Ethernet frame
        memcpy(frame.dst_mac, vl->mac_address, 6);
        memcpy(frame.src_mac, interface_mac, 6);
        frame.ethertype = 0x0800;  // IPv4
        
        // Add UDP/IP headers
        frame.ip_header.protocol = IPPROTO_UDP;
        frame.udp_header.dst_port = vl->udp_port;
        
        // Sequence number (for integrity checking)
        frame.sequence_number = vl->tx_sequence++;
        
        // Copy payload
        memcpy(frame.payload, data, len);
        frame.payload_len = len;
        
        // Transmit on both networks
        ethernet_transmit(NETWORK_A, &frame);
        ethernet_transmit(NETWORK_B, &frame);
        
        // Update BAG timer
        start_timer(vl->bag_us);
        
        return AFDX_SUCCESS;
    }

**2. VL Reception with Redundancy Management:**

.. code-block:: c

    // AFDX Receive Handler
    void afdx_receive_handler(afdx_frame_t *frame, network_id_t network) {
        uint16_t vl_id = extract_vl_id(frame);
        afdx_vl_state_t *vl_state = &vl_states[vl_id];
        
        // Sequence number check
        if (frame->sequence_number != vl_state->expected_seq) {
            log_error("VL %d: Sequence error (exp=%d, got=%d)",
                      vl_id, vl_state->expected_seq, frame->sequence_number);
            vl_state->error_count++;
        }
        
        // Redundancy management (select first arriving frame)
        if (vl_state->frame_received_this_bag) {
            // Already received on other network, discard
            return;
        }
        
        // Process frame
        process_afdx_data(vl_id, frame->payload, frame->payload_len);
        
        // Update state
        vl_state->frame_received_this_bag = true;
        vl_state->last_rx_network = network;
        vl_state->expected_seq = (frame->sequence_number + 1) & 0xFF;
        
        // Skew detection (network health)
        if (network == NETWORK_A) {
            vl_state->network_a_count++;
        } else {
            vl_state->network_b_count++;
        }
    }

**3. Network Health Monitoring:**

.. code-block:: c

    // AFDX Network Health Monitoring
    typedef struct {
        uint32_t frames_received;
        uint32_t frames_lost;
        uint32_t sequence_errors;
        uint32_t crc_errors;
        float    network_a_ratio;  // Should be ~50% in healthy system
        float    network_b_ratio;
        uint32_t bag_violations;
    } afdx_health_stats_t;
    
    void afdx_monitor_network_health(void) {
        for (int vl = 0; vl < num_vls; vl++) {
            afdx_vl_state_t *state = &vl_states[vl];
            
            // Calculate network skew
            float total = state->network_a_count + state->network_b_count;
            float skew = fabs(state->network_a_count / total - 0.5);
            
            if (skew > 0.3) {
                // One network significantly delayed
                report_health_issue(vl, NETWORK_SKEW_HIGH);
            }
            
            // Check for BAG violations
            if (state->last_rx_time > state->expected_rx_time + BAG_TOLERANCE) {
                report_health_issue(vl, BAG_VIOLATION);
            }
        }
    }

**AFDX End System Requirements:**

**Hardware:**
- Dual Ethernet MACs (Network A & B)
- Hardware timestamping capability
- VLAN tagging support
- Priority queuing (802.1p)

**Bandwidth Allocation:**
- VL bandwidth < 75% of link capacity
- BAG compliance within ±500 µs (jitter)
- Maximum frame size: 1518 bytes (Ethernet) + VLAN tag

**Redundancy:**
- Frame sent on both networks simultaneously
- First-arriving frame used, duplicate discarded
- Network skew monitoring (should be ~50/50)

**Project 2: Main Deck Cargo Loading System (MDCLS)**

**Usage:**
- Cargo control commands (VL 1050, BAG=2ms)
- Position feedback (VL 1051, BAG=4ms)
- Status monitoring (VL 1052, BAG=16ms)
- Video surveillance (VL 2000-2003, BAG=8ms)

**Critical VLs:**
- Emergency stop: BAG=128µs, max latency 500µs
- ULD position: BAG=2ms, tolerance ±1mm
- Load cell data: BAG=4ms, 16-bit resolution

**Project 3: Flight Deck Video Displays (FDVD)**

**Video Streaming over AFDX:**
- H.264 compressed video streams
- Multiple VLs per camera (4 cameras)
- Adaptive bitrate based on BAG availability
- Synchronization across displays

**VL Assignment:**
- Camera 1: VL 5001-5004 (multiple sub-VLs for fragmentation)
- Camera 2: VL 5011-5014
- Camera 3: VL 5021-5024
- Camera 4: VL 5031-5034

**Frame Fragmentation:**
- H.264 NAL units split across multiple AFDX frames
- Reassembly at receiver with sequence validation
- Typical video VL: 1 Mbps bandwidth, BAG=1ms

Lessons Learned
--------------------------------------------------------------------------------

**Best Practices:**
✓ Always use redundant networks (A & B)
✓ Monitor network skew continuously
✓ Implement BAG compliance checking
✓ Use hardware timestamping for accurate timing
✓ Perform bandwidth allocation analysis (AFDX design tools)
✓ Test with network analyzers (AIM GmbH, Techsat)

**Common Pitfalls:**
✗ BAG violations under high CPU load
✗ Incorrect VL bandwidth allocation causing congestion
✗ Missing sequence number checks
✗ Not handling network skew (one network consistently slower)
✗ Insufficient switch port buffer sizing

**Tools Used:**
- AFDX Designer (configuration)
- TechSAT AFDX Analyzer
- Wireshark with AFDX plugin
- HIL test benches with AFDX simulators

================================================================================
ARINC 653 - Avionics Application Software Standard Interface
================================================================================

**Standard:** ARINC 653 (APEX - Application Executive)
**Experience:** IMA Data Loader, Intel Atom Platform
**Certification Level:** DO-178C Level C

Real-World Implementation
--------------------------------------------------------------------------------

**Integrated Modular Avionics (IMA) Platform**

**System Architecture:**

::

    ┌───────────────────────────────────────────────────────┐
    │             IMA Cabinet (Common Compute Module)        │
    ├───────────────────────────────────────────────────────┤
    │                ARINC 653 Operating System              │
    │   (Partitioned OS - Spatial & Temporal Isolation)     │
    ├────────┬────────┬────────┬────────┬────────┬─────────┤
    │Part 1  │Part 2  │Part 3  │Part 4  │Part 5  │ Part 6  │
    │ FMS    │ FADEC  │ FCS    │ Nav    │ Comms  │ Video   │
    │(ASIL-D)│(ASIL-D)│(ASIL-D)│(ASIL-B)│(ASIL-A)│ (QM)    │
    └────────┴────────┴────────┴────────┴────────┴─────────┘

**ARINC 653 Partition Configuration:**

.. code-block:: c

    // Partition Configuration Table
    typedef struct {
        char name[32];
        uint32_t partition_id;
        uint64_t memory_base;
        uint64_t memory_size;
        uint32_t duration_us;          // Major frame slot
        uint32_t period_us;            // Partition period
        uint32_t criticality_level;    // ASIL level
        uint8_t  num_processes;
    } arinc653_partition_config_t;
    
    const arinc653_partition_config_t partitions[] = {
        // Name     ID   Mem_Base    Mem_Size    Duration  Period   Criticality  Procs
        {"FMS",     1,   0x10000000, 0x2000000,  5000,     10000,   ASIL_D,      4},
        {"FADEC",   2,   0x12000000, 0x1000000,  3000,     10000,   ASIL_D,      3},
        {"NAV",     4,   0x14000000, 0x1000000,  2000,     20000,   ASIL_B,      2},
    };

**Major Frame Schedule (Time Partitioning):**

::

    Major Frame = 10 ms
    
    |<---- 10 ms ---->|<---- 10 ms ---->|<---- 10 ms ---->|
    |  FMS  |FADEC|NAV|  FMS  |FADEC|NAV|  FMS  |FADEC|NAV|
    | 5ms   | 3ms |2ms| 5ms   | 3ms |2ms| 5ms   | 3ms |2ms|
    0      5     8  10  10    15   18  20  20    25   28  30

**APEX API Implementation:**

**1. Process Management:**

.. code-block:: c

    // ARINC 653 Process Creation
    #include <arinc653/apex.h>
    
    void partition_main(void) {
        PROCESS_ID_TYPE pid;
        PROCESS_ATTRIBUTE_TYPE attr;
        RETURN_CODE_TYPE rc;
        
        // Configure process attributes
        strcpy(attr.NAME, "DataProcessor");
        attr.ENTRY_POINT = data_processor_task;
        attr.STACK_SIZE = 64 * 1024;
        attr.BASE_PRIORITY = 10;
        attr.PERIOD = 100 * MILLISECOND;
        attr.TIME_CAPACITY = 50 * MILLISECOND;
        attr.DEADLINE = SOFT;
        
        // Create periodic process
        CREATE_PROCESS(&attr, &pid, &rc);
        if (rc != NO_ERROR) {
            // Handle error
        }
        
        // Start the process
        START(pid, &rc);
        
        // Set partition mode to NORMAL
        SET_PARTITION_MODE(NORMAL, &rc);
    }

**2. Inter-Partition Communication (Sampling Port):**

.. code-block:: c

    // Sampling Port (non-blocking, latest value)
    SAMPLING_PORT_ID_TYPE port_id;
    
    // Producer partition
    void send_navigation_data(nav_data_t *data) {
        MESSAGE_SIZE_TYPE len = sizeof(nav_data_t);
        RETURN_CODE_TYPE rc;
        
        WRITE_SAMPLING_MESSAGE(
            port_id,
            (MESSAGE_ADDR_TYPE)data,
            len,
            &rc
        );
    }
    
    // Consumer partition
    void receive_navigation_data(nav_data_t *data) {
        MESSAGE_SIZE_TYPE len;
        VALIDITY_TYPE validity;
        RETURN_CODE_TYPE rc;
        
        READ_SAMPLING_MESSAGE(
            port_id,
            (MESSAGE_ADDR_TYPE)data,
            &len,
            &validity,
            &rc
        );
        
        if (validity == VALID) {
            // Use fresh data
            process_nav_data(data);
        } else {
            // Data stale or not yet received
            use_default_nav_data();
        }
    }

**3. Inter-Partition Communication (Queuing Port):**

.. code-block:: c

    // Queuing Port (blocking, FIFO queue)
    QUEUING_PORT_ID_TYPE cmd_port_id;
    
    // Sender
    void send_command(command_t *cmd) {
        RETURN_CODE_TYPE rc;
        
        SEND_QUEUING_MESSAGE(
            cmd_port_id,
            (MESSAGE_ADDR_TYPE)cmd,
            sizeof(command_t),
            0,  // No timeout (blocking)
            &rc
        );
    }
    
    // Receiver
    void receive_command(command_t *cmd) {
        MESSAGE_SIZE_TYPE len;
        RETURN_CODE_TYPE rc;
        
        RECEIVE_QUEUING_MESSAGE(
            cmd_port_id,
            100 * MILLISECOND,  // 100ms timeout
            (MESSAGE_ADDR_TYPE)cmd,
            &len,
            &rc
        );
        
        if (rc == NO_ERROR) {
            execute_command(cmd);
        } else if (rc == TIMED_OUT) {
            // No command received
        }
    }

**4. Health Monitoring:**

.. code-block:: c

    // Partition Health Monitor
    void health_monitor_callback(
        SYSTEM_STATE_TYPE state,
        ERROR_CODE_TYPE error_code
    ) {
        switch (state) {
            case MODULE_LEVEL:
                // Module-level failure (restart required)
                log_critical_error(error_code);
                RAISE_APPLICATION_ERROR(error_code, NULL, 0);
                break;
                
            case PARTITION_LEVEL:
                // Partition failure (restart partition)
                log_partition_error(error_code);
                break;
                
            case PROCESS_LEVEL:
                // Process failure (restart process)
                restart_failed_process();
                break;
        }
    }
    
    // Register error handler
    void init_health_monitoring(void) {
        RETURN_CODE_TYPE rc;
        
        CREATE_ERROR_HANDLER(
            health_monitor_callback,
            STACK_SIZE_ERROR_HANDLER,
            &rc
        );
    }

**Spatial Partitioning (Memory Protection):**

.. code-block:: c

    // Memory regions are hardware-enforced via MPU/MMU
    // Partition cannot access memory outside its allocated region
    
    // Example: FMS Partition Memory Layout
    // Base: 0x10000000, Size: 32 MB
    //
    // 0x10000000 - 0x10100000: Code (.text)     - 1 MB  - Read/Execute
    // 0x10100000 - 0x10200000: Const (.rodata)  - 1 MB  - Read Only
    // 0x10200000 - 0x10A00000: Data (.data+bss) - 8 MB  - Read/Write
    // 0x10A00000 - 0x12000000: Heap/Stack       - 22 MB - Read/Write
    
    // Any access outside 0x10000000-0x12000000 triggers MMU fault
    // → Partition error → Health monitor → Recovery action

**Temporal Partitioning (Time Slicing):**

::

    Major Frame Scheduler:
    
    Time  Partition   Action
    ────────────────────────────────
    0ms   [Context]   Save FMS context
    0ms   FMS         Execute FMS partition (5ms slot)
    5ms   [Context]   Save FMS, Load FADEC
    5ms   FADEC       Execute FADEC partition (3ms slot)
    8ms   [Context]   Save FADEC, Load NAV
    8ms   NAV         Execute NAV partition (2ms slot)
    10ms  [Frame]     End of major frame, repeat

**Partition overrun detection:**
- If partition exceeds time slot → forcibly preempted
- Health monitor notified
- Error logged and recovery initiated

**Port Configuration File (XML):**

.. code-block:: xml

    <ARINC653Module>
      <Partition Name="FMS" ID="1">
        <SamplingPort Name="NAV_DATA_OUT" Direction="SOURCE">
          <MaxMessageSize>256</MaxMessageSize>
          <Refresh>100ms</Refresh>
        </SamplingPort>
        
        <QueuingPort Name="CMD_IN" Direction="DESTINATION">
          <MaxMessageSize>128</MaxMessageSize>
          <MaxNbMessage>10</MaxNbMessage>
        </QueuingPort>
      </Partition>
      
      <Channel>
        <Source>FMS.NAV_DATA_OUT</Source>
        <Destination>Display.NAV_DATA_IN</Destination>
      </Channel>
    </ARINC653Module>

**Testing & Certification:**

**DO-178C Requirements:**
- Partition independence verification
- Timing analysis (WCET - Worst Case Execution Time)
- Memory budget verification
- Fault injection testing

**Test Cases:**
1. Partition overrun → verify forcible termination
2. Invalid memory access → verify MPU trap
3. Inter-partition message loss → verify timeout handling
4. Partition crash → verify isolation (other partitions unaffected)

Lessons Learned
--------------------------------------------------------------------------------

**Critical Success Factors:**
✓ WCET analysis mandatory for time budget compliance
✓ Inter-partition communication: prefer sampling ports for performance
✓ Health monitoring: implement at all three levels (module, partition, process)
✓ Memory budgeting: include OS overhead (typically 20-30%)

**Common Issues:**
✗ Partition time overruns (insufficient WCET analysis)
✗ Port configuration mismatches between partitions
✗ Insufficient queue depths causing message loss
✗ Context switch overhead not accounted in schedule

**Tools:**
- RapiTime: WCET analysis
- VectorCAST: DO-178C structural coverage
- ARINC 653 Configuration Tools: XML generation and validation

================================================================================
Summary of ARINC Standards Experience
================================================================================

Project Distribution by ARINC Standard
--------------------------------------------------------------------------------

**ARINC 429:** 6 projects
- FQGS
- EEC
- AFCU
- AFIRS SDU
- FDVD
- Intel Atom Platform

**ARINC 664 (AFDX):** 3 projects
- Intel Atom Platform
- MDCLS
- FDVD

**ARINC 653:** 2 projects
- Data Loader
- Intel Atom Platform

**ARINC 615A:** 1 project
- Data Loader

**ARINC 665:** 1 project
- Data Loader

**ARINC 600:** 2 projects
- FQGS
- AFCU

**ARINC 818:** 1 project
- FDVD

**ARINC 661:** 1 project
- FDVD

**ARINC 825 (CAN Aerospace):** 3 projects
- FQGS
- MDCLS
- Intel Atom Platform

================================================================================
References & Resources
================================================================================

**Standards Documents:**
- ARINC 429: Digital Information Transfer System (Mark 33)
- ARINC 615A: Software Data Loader
- ARINC 653: Avionics Application Software Standard Interface
- ARINC 664 Part 7: Aircraft Data Network (AFDX)
- ARINC 818: Avionics Digital Video Bus

**Tools & Vendors:**
- DDC, Holt Integrated Circuits: ARINC 429 transceivers
- AIM GmbH: ARINC test equipment
- Condor Engineering: Bus analyzers
- TechSAT: AFDX analyzers
- Wind River VxWorks 653: ARINC 653 RTOS

**Certification:**
- DO-178B/C: Software Considerations in Airborne Systems
- DO-254: Hardware Considerations in Airborne Systems
- DO-160: Environmental Conditions

================================================================================
