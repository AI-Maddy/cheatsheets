================================================================================
Linux Platform Drivers & System Simulation - Project Experience
================================================================================

:Author: Madhavan Vivekanandan
:Date: January 21, 2026
:Projects: Linux Kernel Development, System Modeling, Industrial Systems
:Domains: Networking, System Simulation, Industrial Automation

================================================================================
Overview
================================================================================

This document captures hands-on implementation experience across diverse
embedded systems domains:

**Projects:**
1. **Linux PCIe Platform Driver** - ARM SOC access point platform
2. **Behavior Modeling for High-Performance Computer Systems** - Pre-silicon verification
3. **Diesel Monitoring System** - Safety-critical industrial control
4. **Industrial Communication Bridge** - Protocol conversion systems

**Timeline:** 2007-2013

**Domains:** Networking platforms, system simulation, industrial automation

================================================================================
Linux PCIe Platform Driver - Access Point Platform
================================================================================

Project: ARM SOC Wireless Access Point Platform
--------------------------------------------------------------------------------

**Timeline:** January 2013 - July 2013

**Hardware:**
- ARM SOC (Multi-core)
- Multiple PCIe Root Complexes
- Wireless chipsets
- FPGA emulation platform

**Objective:** Develop Linux platform driver for PCIe enumeration on next-gen
access point SOC with multiple root complexes

**Challenge:** SOC not yet available in silicon - validation using FPGA emulation

PCIe Architecture Overview
--------------------------------------------------------------------------------

**PCIe Topology:**

::

    ┌──────────────────────────────────────────────────────────────┐
    │                    ARM SOC (Multi-Core)                      │
    │                                                              │
    │  ┌────────────┐    ┌────────────┐    ┌────────────┐        │
    │  │   CPU 0    │    │   CPU 1    │    │   CPU n    │        │
    │  └─────┬──────┘    └─────┬──────┘    └─────┬──────┘        │
    │        │                 │                 │                │
    │  ┌─────▼─────────────────▼─────────────────▼──────┐        │
    │  │              System Bus / Interconnect          │        │
    │  └───┬────────────┬─────────────┬──────────────────┘        │
    │      │            │             │                           │
    │  ┌───▼────┐  ┌────▼────┐  ┌────▼────┐                      │
    │  │  PCIe  │  │  PCIe   │  │  PCIe   │                      │
    │  │  RC 0  │  │  RC 1   │  │  RC 2   │  (Root Complexes)   │
    │  └───┬────┘  └────┬────┘  └────┬────┘                      │
    └──────┼────────────┼────────────┼──────────────────────────┘
           │            │            │
    ┌──────▼─────┐ ┌────▼──────┐ ┌──▼───────────┐
    │  Wireless  │ │  Wireless │ │  Storage     │
    │  Chipset 0 │ │  Chipset 1│ │  Controller  │
    │  (WiFi 5G) │ │  (WiFi 2G)│ │  (SSD/NVMe)  │
    └────────────┘ └───────────┘ └──────────────┘

**PCIe Generations:**
- Gen1: 2.5 GT/s (250 MB/s per lane)
- Gen2: 5.0 GT/s (500 MB/s per lane)
- Gen3: 8.0 GT/s (1 GB/s per lane)

**Configuration Space:**
- Type 0: Endpoint devices
- Type 1: Bridges/switches

Platform Driver Architecture
--------------------------------------------------------------------------------

**Linux PCIe Subsystem:**

.. code-block:: c

    // PCIe platform driver for custom ARM SOC
    
    #include <linux/module.h>
    #include <linux/platform_device.h>
    #include <linux/pci.h>
    #include <linux/of.h>
    #include <linux/of_pci.h>
    #include <linux/of_address.h>
    
    #define DRIVER_NAME "arm-soc-pcie"
    
    // Custom PCIe root complex structure
    struct arm_pcie_rc {
        void __iomem *base;        // Register base address
        struct device *dev;
        struct pci_bus *bus;       // PCI bus structure
        int irq;
        int rc_id;                 // Root complex ID (0, 1, 2)
        struct resource *cfg_res;  // Configuration space
        struct resource *mem_res;  // Memory space
        struct resource *io_res;   // I/O space
    };
    
    // Device tree match table
    static const struct of_device_id arm_pcie_of_match[] = {
        { .compatible = "arm,soc-pcie-rc", },
        { },
    };
    MODULE_DEVICE_TABLE(of, arm_pcie_of_match);

**Register Definitions:**

.. code-block:: c

    // PCIe root complex registers
    #define PCIE_RC_CTRL_REG           0x0000
    #define PCIE_RC_STATUS_REG         0x0004
    #define PCIE_RC_LINK_STATUS_REG    0x0008
    #define PCIE_RC_INT_STATUS_REG     0x000C
    #define PCIE_RC_INT_MASK_REG       0x0010
    #define PCIE_RC_PHY_CTRL_REG       0x0100
    #define PCIE_RC_LTSSM_STATE_REG    0x0104
    
    // Control register bits
    #define PCIE_RC_CTRL_LTSSM_EN      BIT(0)
    #define PCIE_RC_CTRL_DLL_ACTIVE    BIT(1)
    #define PCIE_RC_CTRL_PHY_RESET     BIT(2)
    
    // Link status bits
    #define PCIE_LINK_UP               BIT(0)
    #define PCIE_LINK_SPEED_MASK       (0x7 << 1)
    #define PCIE_LINK_WIDTH_MASK       (0x3F << 4)
    
    // Helper functions
    static inline u32 pcie_rc_readl(struct arm_pcie_rc *rc, u32 reg)
    {
        return readl(rc->base + reg);
    }
    
    static inline void pcie_rc_writel(struct arm_pcie_rc *rc, u32 val, u32 reg)
    {
        writel(val, rc->base + reg);
    }

**Link Initialization:**

.. code-block:: c

    // Initialize PCIe link
    static int arm_pcie_link_up(struct arm_pcie_rc *rc)
    {
        u32 status;
        int retries = 100;
        
        // Enable PHY
        pcie_rc_writel(rc, 0, PCIE_RC_PHY_CTRL_REG);
        mdelay(10);
        
        // Enable LTSSM (Link Training Status State Machine)
        status = pcie_rc_readl(rc, PCIE_RC_CTRL_REG);
        status |= PCIE_RC_CTRL_LTSSM_EN;
        pcie_rc_writel(rc, status, PCIE_RC_CTRL_REG);
        
        // Wait for link up
        while (retries--) {
            status = pcie_rc_readl(rc, PCIE_RC_LINK_STATUS_REG);
            if (status & PCIE_LINK_UP) {
                u32 speed = (status & PCIE_LINK_SPEED_MASK) >> 1;
                u32 width = (status & PCIE_LINK_WIDTH_MASK) >> 4;
                
                dev_info(rc->dev, "PCIe link up: Gen%d x%d\n", speed + 1, width);
                return 0;
            }
            mdelay(10);
        }
        
        dev_err(rc->dev, "PCIe link training failed\n");
        return -ETIMEDOUT;
    }

**Configuration Space Access:**

.. code-block:: c

    // PCIe configuration space read/write
    static int arm_pcie_config_read(struct pci_bus *bus, unsigned int devfn,
                                     int where, int size, u32 *val)
    {
        struct arm_pcie_rc *rc = bus->sysdata;
        void __iomem *addr;
        
        // Calculate configuration address
        // Type 0: Bus 0 (root bus)
        // Type 1: Bus > 0 (behind bridge)
        if (bus->number == rc->bus->number) {
            // Type 0 configuration (same bus)
            addr = rc->cfg_res->start + (devfn << 12) + where;
        } else {
            // Type 1 configuration (subordinate bus)
            addr = rc->cfg_res->start + (bus->number << 20) + 
                   (devfn << 12) + where;
        }
        
        // Read based on size
        switch (size) {
        case 1:
            *val = readb(addr);
            break;
        case 2:
            *val = readw(addr);
            break;
        case 4:
            *val = readl(addr);
            break;
        default:
            return PCIBIOS_BAD_REGISTER_NUMBER;
        }
        
        return PCIBIOS_SUCCESSFUL;
    }
    
    static int arm_pcie_config_write(struct pci_bus *bus, unsigned int devfn,
                                      int where, int size, u32 val)
    {
        struct arm_pcie_rc *rc = bus->sysdata;
        void __iomem *addr;
        
        // Calculate configuration address (same as read)
        if (bus->number == rc->bus->number) {
            addr = rc->cfg_res->start + (devfn << 12) + where;
        } else {
            addr = rc->cfg_res->start + (bus->number << 20) + 
                   (devfn << 12) + where;
        }
        
        // Write based on size
        switch (size) {
        case 1:
            writeb(val, addr);
            break;
        case 2:
            writew(val, addr);
            break;
        case 4:
            writel(val, addr);
            break;
        default:
            return PCIBIOS_BAD_REGISTER_NUMBER;
        }
        
        return PCIBIOS_SUCCESSFUL;
    }
    
    // PCI operations structure
    static struct pci_ops arm_pcie_ops = {
        .read = arm_pcie_config_read,
        .write = arm_pcie_config_write,
    };

**Bus Enumeration:**

.. code-block:: c

    // Enumerate PCIe bus and devices
    static int arm_pcie_enumerate(struct arm_pcie_rc *rc)
    {
        struct pci_host_bridge *bridge;
        LIST_HEAD(resources);
        int ret;
        
        // Parse ranges from device tree
        ret = of_pci_get_host_bridge_resources(rc->dev->of_node, 0, 0xff,
                                                &resources, NULL);
        if (ret) {
            dev_err(rc->dev, "Failed to parse DT resources\n");
            return ret;
        }
        
        // Create PCI host bridge
        bridge = pci_alloc_host_bridge(0);
        if (!bridge) {
            ret = -ENOMEM;
            goto err_free_res;
        }
        
        // Set bridge properties
        bridge->dev.parent = rc->dev;
        bridge->sysdata = rc;
        bridge->busnr = 0;
        bridge->ops = &arm_pcie_ops;
        
        list_splice_init(&resources, &bridge->windows);
        
        // Scan and add devices
        ret = pci_scan_root_bus_bridge(bridge);
        if (ret) {
            dev_err(rc->dev, "Failed to scan root bus\n");
            goto err_free_bridge;
        }
        
        rc->bus = bridge->bus;
        
        // Assign resources (BARs, memory, I/O)
        pci_bus_size_bridges(rc->bus);
        pci_bus_assign_resources(rc->bus);
        
        // Add devices to system
        pci_bus_add_devices(rc->bus);
        
        dev_info(rc->dev, "PCIe bus enumeration complete\n");
        return 0;
        
    err_free_bridge:
        pci_free_host_bridge(bridge);
    err_free_res:
        pci_free_resource_list(&resources);
        return ret;
    }

**Platform Driver Probe:**

.. code-block:: c

    static int arm_pcie_probe(struct platform_device *pdev)
    {
        struct arm_pcie_rc *rc;
        struct resource *res;
        int ret;
        
        dev_info(&pdev->dev, "Probing ARM PCIe root complex\n");
        
        // Allocate driver data
        rc = devm_kzalloc(&pdev->dev, sizeof(*rc), GFP_KERNEL);
        if (!rc)
            return -ENOMEM;
        
        rc->dev = &pdev->dev;
        platform_set_drvdata(pdev, rc);
        
        // Get register base
        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        rc->base = devm_ioremap_resource(&pdev->dev, res);
        if (IS_ERR(rc->base))
            return PTR_ERR(rc->base);
        
        // Get configuration space
        rc->cfg_res = platform_get_resource(pdev, IORESOURCE_MEM, 1);
        if (!rc->cfg_res) {
            dev_err(&pdev->dev, "Missing configuration space\n");
            return -EINVAL;
        }
        
        // Get IRQ
        rc->irq = platform_get_irq(pdev, 0);
        if (rc->irq < 0) {
            dev_err(&pdev->dev, "Failed to get IRQ\n");
            return rc->irq;
        }
        
        // Initialize link
        ret = arm_pcie_link_up(rc);
        if (ret) {
            dev_err(&pdev->dev, "Failed to bring up link\n");
            return ret;
        }
        
        // Enumerate bus
        ret = arm_pcie_enumerate(rc);
        if (ret) {
            dev_err(&pdev->dev, "Failed to enumerate bus\n");
            return ret;
        }
        
        dev_info(&pdev->dev, "ARM PCIe root complex initialized\n");
        return 0;
    }
    
    static int arm_pcie_remove(struct platform_device *pdev)
    {
        struct arm_pcie_rc *rc = platform_get_drvdata(pdev);
        
        // Remove bus
        if (rc->bus) {
            pci_stop_root_bus(rc->bus);
            pci_remove_root_bus(rc->bus);
        }
        
        return 0;
    }
    
    static struct platform_driver arm_pcie_driver = {
        .driver = {
            .name = DRIVER_NAME,
            .of_match_table = arm_pcie_of_match,
        },
        .probe = arm_pcie_probe,
        .remove = arm_pcie_remove,
    };
    
    module_platform_driver(arm_pcie_driver);
    
    MODULE_AUTHOR("Madhavan Vivekanandan");
    MODULE_DESCRIPTION("ARM SOC PCIe Root Complex Driver");
    MODULE_LICENSE("GPL v2");

**Device Tree Binding:**

.. code-block:: dts

    // arm-soc.dts - PCIe device tree nodes
    
    pcie0: pcie@10000000 {
        compatible = "arm,soc-pcie-rc";
        reg = <0x10000000 0x10000>,    /* Register space */
              <0x20000000 0x1000000>;  /* Configuration space */
        reg-names = "regs", "config";
        
        #address-cells = <3>;
        #size-cells = <2>;
        device_type = "pci";
        
        ranges = <0x81000000 0 0x00000000  0x21000000 0 0x00010000>,  /* I/O */
                 <0x82000000 0 0x22000000  0x22000000 0 0x10000000>;  /* Memory */
        
        interrupts = <GIC_SPI 100 IRQ_TYPE_LEVEL_HIGH>;
        interrupt-names = "msi";
        
        #interrupt-cells = <1>;
        interrupt-map-mask = <0 0 0 7>;
        interrupt-map = <0 0 0 1 &gic GIC_SPI 101 IRQ_TYPE_LEVEL_HIGH>,
                        <0 0 0 2 &gic GIC_SPI 102 IRQ_TYPE_LEVEL_HIGH>,
                        <0 0 0 3 &gic GIC_SPI 103 IRQ_TYPE_LEVEL_HIGH>,
                        <0 0 0 4 &gic GIC_SPI 104 IRQ_TYPE_LEVEL_HIGH>;
        
        status = "okay";
    };
    
    pcie1: pcie@11000000 {
        compatible = "arm,soc-pcie-rc";
        reg = <0x11000000 0x10000>,
              <0x30000000 0x1000000>;
        reg-names = "regs", "config";
        
        // Similar configuration for second root complex
        // ...
        
        status = "okay";
    };

FPGA-Based Validation
--------------------------------------------------------------------------------

**FPGA Emulation Setup:**

.. code-block:: c

    // FPGA validation scripts
    
    #!/bin/bash
    # fpga_test_pcie.sh
    
    # Load driver
    insmod arm_pcie.ko
    
    # Check link status
    lspci -vv
    
    # Expected output:
    # 00:00.0 Network controller: Wireless Chipset
    #     Region 0: Memory at 22000000 (64-bit, non-prefetchable) [size=1M]
    #     Capabilities: [40] Express Endpoint, MSI 00
    #     LnkSta: Speed 5GT/s, Width x4
    
    # Test data transfer
    iperf3 -c <wireless_device_ip> -t 60
    
    # Monitor PCIe bandwidth
    while true; do
        cat /sys/bus/pci/devices/0000:00:00.0/resource
        sleep 1
    done

**Performance Metrics:**

.. code-block:: c

    // PCIe performance monitoring
    static void arm_pcie_dump_stats(struct arm_pcie_rc *rc)
    {
        u32 status = pcie_rc_readl(rc, PCIE_RC_LINK_STATUS_REG);
        u32 speed = (status & PCIE_LINK_SPEED_MASK) >> 1;
        u32 width = (status & PCIE_LINK_WIDTH_MASK) >> 4;
        
        dev_info(rc->dev, "PCIe Statistics:\n");
        dev_info(rc->dev, "  Link Speed: Gen%d (%s GT/s)\n", 
                 speed + 1, speed == 0 ? "2.5" : speed == 1 ? "5.0" : "8.0");
        dev_info(rc->dev, "  Link Width: x%d\n", width);
        dev_info(rc->dev, "  Max Bandwidth: %d MB/s\n", 
                 width * (speed == 0 ? 250 : speed == 1 ? 500 : 1000));
    }

================================================================================
Behavior Modeling - High-Performance Computer Systems
================================================================================

Project: Pre-Silicon Verification of Hypervisor Firmware
--------------------------------------------------------------------------------

**Timeline:** August 2011 - January 2013

**Domain:** System Simulation, Firmware Verification

**Platform:** Simics Full-System Simulator

**Hardware:** High-performance computing systems (unreleased at the time)

**Objective:** Model complex computer system behavior to verify hypervisor
firmware before silicon availability

Simics Simulation Platform
--------------------------------------------------------------------------------

**Simics Architecture:**

::

    ┌─────────────────────────────────────────────────────────────┐
    │                 Simics Simulation Engine                    │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │          Simulated Hardware Platform                 │  │
    │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │  │
    │  │  │  CPU 0   │  │  CPU 1   │  │  CPU n   │           │  │
    │  │  │ (Model)  │  │ (Model)  │  │ (Model)  │           │  │
    │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘           │  │
    │  │       │             │             │                  │  │
    │  │  ┌────▼─────────────▼─────────────▼─────┐           │  │
    │  │  │        Memory Controller Model       │           │  │
    │  │  └──────────────┬───────────────────────┘           │  │
    │  │                 │                                    │  │
    │  │  ┌──────────────▼───────────────────────┐           │  │
    │  │  │         System Memory (RAM)          │           │  │
    │  │  └──────────────┬───────────────────────┘           │  │
    │  │                 │                                    │  │
    │  │  ┌──────────────▼───────────────────────┐           │  │
    │  │  │      I/O Devices (UART, NIC, etc.)   │           │  │
    │  │  └──────────────────────────────────────┘           │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                             │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │           Hypervisor Firmware (Under Test)           │  │
    │  │  - Memory Management                                 │  │
    │  │  - Virtual Machine Management                        │  │
    │  │  │  - Interrupt Handling                             │  │
    │  │  - Partition Isolation                               │  │
    │  └──────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘

DML (Device Modeling Language)
--------------------------------------------------------------------------------

**Simple Device Model:**

.. code-block:: dml

    // uart_device.dml - UART device model
    
    dml 1.2;
    
    device uart;
    
    import "simics/devs/serial.dml";
    import "simics/devs/memory-space.dml";
    
    // Register bank
    bank regs {
        parameter register_size = 4;
        
        // Data register (offset 0x00)
        register data @ 0x00 {
            parameter size = 4;
            
            field tx_data[7:0];
            field rx_data[15:8];
            
            // Write to transmit data
            method write(value) {
                tx_data = value & 0xFF;
                transmit_byte(tx_data);
            }
            
            // Read received data
            method read() -> (value) {
                value = rx_data << 8;
                rx_data = 0;  // Clear after read
            }
        }
        
        // Status register (offset 0x04)
        register status @ 0x04 {
            parameter size = 4;
            
            field tx_empty @ [0];
            field rx_ready @ [1];
            field overrun @ [2];
            
            method read() -> (value) {
                value = (tx_empty << 0) | (rx_ready << 1) | (overrun << 2);
            }
        }
        
        // Control register (offset 0x08)
        register control @ 0x08 {
            parameter size = 4;
            
            field baud_rate[15:0];
            field parity_enable @ [16];
            field stop_bits @ [17];
            
            method write(value) {
                baud_rate = value & 0xFFFF;
                parity_enable = (value >> 16) & 0x1;
                stop_bits = (value >> 17) & 0x1;
                
                configure_uart();
            }
        }
    }
    
    // Transmit byte function
    method transmit_byte(uint8 data) {
        // Simulate UART transmission delay
        after (10000) call {  // 10,000 cycles delay
            SIM_write_byte(serial_device, data);
            regs.status.tx_empty = 1;
        }
    }
    
    // Receive byte callback
    event receive_byte {
        parameter desc = "UART receive event";
        
        method event_callback(data) {
            if (regs.status.rx_ready == 1) {
                // Overrun condition
                regs.status.overrun = 1;
            } else {
                regs.data.rx_data = data;
                regs.status.rx_ready = 1;
                
                // Trigger interrupt if enabled
                if (interrupt_enabled) {
                    SIM_interrupt_cpu(cpu, IRQ_UART_RX);
                }
            }
        }
    }

**Memory Controller Model:**

.. code-block:: dml

    // memory_controller.dml
    
    dml 1.2;
    
    device memory_controller;
    
    import "simics/devs/memory.dml";
    
    bank regs {
        // Memory controller configuration registers
        register mc_config @ 0x00 {
            field memory_size[31:0];
            field ecc_enable @ [32];
            field interleave_enable @ [33];
        }
        
        register mc_timing @ 0x04 {
            field cas_latency[7:0];
            field ras_latency[15:8];
            field refresh_interval[31:16];
        }
        
        register mc_status @ 0x08 {
            field init_complete @ [0];
            field ecc_error @ [1];
            field refresh_pending @ [2];
        }
    }
    
    // Memory transaction modeling
    method memory_access(uint64 address, uint64 size, bool is_write) -> (uint64 latency) {
        uint64 row_hit_latency = regs.mc_timing.cas_latency;
        uint64 row_miss_latency = regs.mc_timing.cas_latency + 
                                   regs.mc_timing.ras_latency;
        
        // Simulate row buffer hit/miss
        if (is_same_row(address, last_accessed_row)) {
            latency = row_hit_latency;
        } else {
            latency = row_miss_latency;
            last_accessed_row = get_row(address);
        }
        
        // ECC overhead
        if (regs.mc_config.ecc_enable) {
            latency += 2;  // Additional cycles for ECC
        }
        
        return latency;
    }

Python Scripting for Automation
--------------------------------------------------------------------------------

**Simics Test Automation:**

.. code-block:: python

    #!/usr/bin/env python3
    # simics_test_hypervisor.py
    
    import simics
    
    # Load simulation configuration
    simics.SIM_load_module("hypervisor-model")
    simics.SIM_load_module("memory-controller")
    simics.SIM_load_module("uart-device")
    
    # Create simulated system
    def create_system():
        # Create processors
        cpu0 = simics.SIM_create_object("processor", "cpu0", 
                                         [["freq_mhz", 2000]])
        cpu1 = simics.SIM_create_object("processor", "cpu1", 
                                         [["freq_mhz", 2000]])
        
        # Create memory (16 GB)
        memory = simics.SIM_create_object("memory", "ram", 
                                           [["size", 0x400000000]])
        
        # Create UART
        uart = simics.SIM_create_object("uart", "uart0", 
                                         [["base_address", 0x10000000]])
        
        # Connect components
        simics.SIM_set_attribute(cpu0, "physical_memory", memory)
        simics.SIM_set_attribute(cpu1, "physical_memory", memory)
        
        return {"cpu0": cpu0, "cpu1": cpu1, "memory": memory, "uart": uart}
    
    # Load hypervisor firmware
    def load_firmware(system):
        firmware_binary = "hypervisor.bin"
        load_address = 0x80000000
        
        simics.SIM_load_binary(system["memory"], firmware_binary, 
                                load_address, 0, 0)
        
        # Set PC to firmware entry point
        simics.SIM_write_phys_memory(system["cpu0"], "pc", load_address)
        print(f"Loaded firmware at 0x{load_address:08x}")
    
    # Run simulation
    def run_simulation(system, cycles):
        print(f"Running simulation for {cycles} cycles...")
        simics.SIM_continue(cycles)
        
        # Check status
        pc = simics.SIM_read_phys_memory(system["cpu0"], "pc")
        print(f"CPU0 PC: 0x{pc:08x}")
    
    # Test case: Virtual machine boot
    def test_vm_boot(system):
        print("\n=== Test: VM Boot ===")
        
        # Set breakpoint at VM entry point
        vm_entry = 0x80100000
        simics.SIM_break_simulation(f"memory:0x{vm_entry:08x}")
        
        # Run until breakpoint
        simics.SIM_continue(0)
        
        # Verify VM isolation
        vm_memory_start = 0x90000000
        vm_memory_size = 0x10000000
        
        # Attempt to access hypervisor memory from VM (should fault)
        hypervisor_addr = 0x80000000
        try:
            data = simics.SIM_read_phys_memory(system["memory"], hypervisor_addr)
            print(f"ERROR: VM accessed hypervisor memory: 0x{data:08x}")
            return False
        except Exception as e:
            print(f"PASS: VM isolation working - {e}")
            return True
    
    # Test case: Interrupt delivery
    def test_interrupt_delivery(system):
        print("\n=== Test: Interrupt Delivery ===")
        
        # Trigger UART interrupt
        simics.SIM_set_attribute(system["uart"], "interrupt", 1)
        
        # Run for a few cycles
        simics.SIM_continue(1000)
        
        # Check if hypervisor handled interrupt
        interrupt_count_addr = 0x80001000  # Hypervisor stats location
        interrupt_count = simics.SIM_read_phys_memory(system["memory"], 
                                                       interrupt_count_addr)
        
        if interrupt_count > 0:
            print(f"PASS: Interrupt delivered (count={interrupt_count})")
            return True
        else:
            print("FAIL: Interrupt not delivered")
            return False
    
    # Test case: Memory isolation
    def test_memory_isolation(system):
        print("\n=== Test: Memory Isolation ===")
        
        vm1_memory = 0x90000000
        vm2_memory = 0xA0000000
        
        # Write pattern to VM1 memory
        test_pattern = 0xDEADBEEF
        simics.SIM_write_phys_memory(system["memory"], vm1_memory, 
                                      test_pattern)
        
        # Verify VM2 cannot read VM1 memory
        try:
            data = simics.SIM_read_phys_memory(system["memory"], vm1_memory)
            if data == test_pattern:
                print("FAIL: Memory isolation broken")
                return False
        except Exception as e:
            print(f"PASS: Memory isolation working - {e}")
            return True
    
    # Main test suite
    def main():
        print("Creating simulated system...")
        system = create_system()
        
        print("Loading hypervisor firmware...")
        load_firmware(system)
        
        # Run boot sequence
        print("Booting hypervisor...")
        run_simulation(system, 1000000)  # 1M cycles
        
        # Run tests
        tests = [
            test_vm_boot,
            test_interrupt_delivery,
            test_memory_isolation
        ]
        
        results = []
        for test in tests:
            result = test(system)
            results.append(result)
        
        # Summary
        passed = sum(results)
        total = len(results)
        print(f"\n=== Test Summary ===")
        print(f"Passed: {passed}/{total}")
        
        return 0 if passed == total else 1
    
    if __name__ == "__main__":
        exit(main())

**Checkpoint/Restore:**

.. code-block:: python

    # Save simulation state for debugging
    def save_checkpoint(name):
        simics.SIM_write_configuration_to_file(f"checkpoint_{name}.ckpt")
        print(f"Saved checkpoint: {name}")
    
    # Restore from checkpoint
    def load_checkpoint(name):
        simics.SIM_load_file(f"checkpoint_{name}.ckpt")
        print(f"Loaded checkpoint: {name}")
    
    # Example: Save state before risky operation
    save_checkpoint("before_vm_migration")
    
    # Perform VM migration
    migrate_vm(vm_id=1, target_cpu=2)
    
    # If failure, restore
    if migration_failed:
        load_checkpoint("before_vm_migration")

================================================================================
Diesel Monitoring System (DMS) - Safety-Critical Industrial Control
================================================================================

Project: SIL2-Compliant Diesel Monitoring System
--------------------------------------------------------------------------------

**Timeline:** July 2007 - February 2008

**Domain:** Industrial Monitoring & Control

**Hardware:**
- Single Board Computer (SBC)
- x86 Processor
- Data Acquisition (DAQ) modules

**Operating System:**
- LYNX RTOS (Real-Time Operating System)

**Safety Level:** SIL2 (Safety Integrity Level 2) - IEC 61508

System Architecture
--------------------------------------------------------------------------------

**DMS Architecture:**

::

    ┌───────────────────────────────────────────────────────────────┐
    │                  Diesel Monitoring System                     │
    ├───────────────────────────────────────────────────────────────┤
    │                                                               │
    │  ┌─────────────────────────────────────────────────────────┐ │
    │  │         Application Layer (LYNX RTOS Tasks)             │ │
    │  ├──────────┬──────────┬───────────┬───────────┬──────────┤ │
    │  │  Diesel  │  Fuel    │  Temp.    │  Pressure │  Alarm   │ │
    │  │  Monitor │  Level   │  Monitor  │  Monitor  │  Manager │ │
    │  │  Task    │  Task    │  Task     │  Task     │  Task    │ │
    │  └────┬─────┴────┬─────┴─────┬─────┴─────┬─────┴────┬─────┘ │
    │       │          │           │           │          │       │
    │  ┌────▼──────────▼───────────▼───────────▼──────────▼─────┐ │
    │  │              LYNX RTOS Kernel                           │ │
    │  │  - Task Scheduling (Priority-based)                     │ │
    │  │  - Inter-Task Communication (Message Queues)            │ │
    │  │  - Timers & Event Management                            │ │
    │  └────┬────────────────────────────────────────────────────┘ │
    │       │                                                      │
    │  ┌────▼────────────────────────────────────────────────────┐ │
    │  │           Hardware Abstraction Layer (HAL)              │ │
    │  └────┬────────────────────────────────────────────────────┘ │
    │       │                                                      │
    └───────┼──────────────────────────────────────────────────────┘
            │
    ┌───────▼──────────────────────────────────────────────────────┐
    │             Hardware (SBC, DAQ Modules)                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Analog   │  │ Digital  │  │  Relay   │  │  Serial  │    │
    │  │  Input   │  │  Input   │  │  Output  │  │  Port    │    │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
    └──────────────────────────────────────────────────────────────┘
            │              │              │              │
    ┌───────▼──────┐ ┌─────▼──────┐ ┌────▼───────┐ ┌───▼──────────┐
    │ Diesel       │ │  Temp.     │ │  Control   │ │  HMI/SCADA   │
    │ Generator    │ │  Sensors   │ │  Valves    │ │  Interface   │
    └──────────────┘ └────────────┘ └────────────┘ └──────────────┘

LYNX RTOS Task Implementation
--------------------------------------------------------------------------------

.. code-block:: c

    // dms_main.c - Main application
    
    #include <lynx.h>
    #include <stdio.h>
    #include <string.h>
    
    // Task priorities (higher number = higher priority)
    #define PRIORITY_ALARM      10  // Highest (safety-critical)
    #define PRIORITY_MONITOR     8  // High
    #define PRIORITY_FUEL        6  // Medium
    #define PRIORITY_HMI         4  // Low
    
    // Task IDs
    LynxTaskID diesel_monitor_task_id;
    LynxTaskID fuel_level_task_id;
    LynxTaskID temp_monitor_task_id;
    LynxTaskID pressure_monitor_task_id;
    LynxTaskID alarm_manager_task_id;
    
    // Message queue for inter-task communication
    LynxMessageQueue alarm_queue;
    
    // Alarm message structure
    typedef struct {
        uint32_t alarm_id;
        uint32_t severity;  // 0=Info, 1=Warning, 2=Critical
        float value;
        char description[64];
    } AlarmMessage_t;
    
    // Diesel monitor task
    void diesel_monitor_task(void *arg) {
        float rpm, load, voltage;
        
        while (1) {
            // Read diesel generator parameters
            rpm = read_analog_channel(CHANNEL_RPM);
            load = read_analog_channel(CHANNEL_LOAD);
            voltage = read_analog_channel(CHANNEL_VOLTAGE);
            
            // Check thresholds
            if (rpm > MAX_RPM || rpm < MIN_RPM) {
                AlarmMessage_t alarm;
                alarm.alarm_id = ALARM_RPM_ABNORMAL;
                alarm.severity = 2;  // Critical
                alarm.value = rpm;
                snprintf(alarm.description, sizeof(alarm.description),
                         "RPM out of range: %.1f", rpm);
                
                LynxSendMessage(alarm_queue, &alarm, sizeof(alarm), 
                                LYNX_NO_WAIT);
            }
            
            // Log data
            log_diesel_data(rpm, load, voltage);
            
            // Sleep for 100ms
            LynxTaskDelay(LYNX_MSEC_TO_TICKS(100));
        }
    }
    
    // Fuel level monitoring task
    void fuel_level_task(void *arg) {
        float fuel_level, fuel_rate;
        
        while (1) {
            fuel_level = read_analog_channel(CHANNEL_FUEL_LEVEL);
            fuel_rate = calculate_fuel_consumption_rate();
            
            // Low fuel alarm
            if (fuel_level < LOW_FUEL_THRESHOLD) {
                AlarmMessage_t alarm;
                alarm.alarm_id = ALARM_LOW_FUEL;
                alarm.severity = 1;  // Warning
                alarm.value = fuel_level;
                snprintf(alarm.description, sizeof(alarm.description),
                         "Low fuel level: %.1f%%", fuel_level);
                
                LynxSendMessage(alarm_queue, &alarm, sizeof(alarm), 
                                LYNX_NO_WAIT);
            }
            
            // Predict time to empty
            float time_to_empty = fuel_level / fuel_rate;  // Hours
            update_display("Fuel remaining", time_to_empty);
            
            LynxTaskDelay(LYNX_MSEC_TO_TICKS(1000));  // 1 second
        }
    }
    
    // Temperature monitoring task
    void temp_monitor_task(void *arg) {
        float coolant_temp, exhaust_temp, oil_temp;
        
        while (1) {
            coolant_temp = read_analog_channel(CHANNEL_COOLANT_TEMP);
            exhaust_temp = read_analog_channel(CHANNEL_EXHAUST_TEMP);
            oil_temp = read_analog_channel(CHANNEL_OIL_TEMP);
            
            // Over-temperature checks
            if (coolant_temp > MAX_COOLANT_TEMP) {
                AlarmMessage_t alarm;
                alarm.alarm_id = ALARM_OVERTEMP_COOLANT;
                alarm.severity = 2;  // Critical
                alarm.value = coolant_temp;
                snprintf(alarm.description, sizeof(alarm.description),
                         "Coolant over-temperature: %.1f°C", coolant_temp);
                
                LynxSendMessage(alarm_queue, &alarm, sizeof(alarm), 
                                LYNX_NO_WAIT);
                
                // Emergency shutdown sequence
                initiate_emergency_shutdown();
            }
            
            LynxTaskDelay(LYNX_MSEC_TO_TICKS(500));
        }
    }
    
    // Alarm manager task (highest priority)
    void alarm_manager_task(void *arg) {
        AlarmMessage_t alarm;
        
        while (1) {
            // Wait for alarm message
            if (LynxReceiveMessage(alarm_queue, &alarm, sizeof(alarm), 
                                    LYNX_WAIT_FOREVER) == LYNX_OK) {
                
                // Process alarm based on severity
                switch (alarm.severity) {
                    case 0:  // Info
                        log_info(alarm.description);
                        break;
                    
                    case 1:  // Warning
                        log_warning(alarm.description);
                        activate_warning_indicator();
                        send_scada_alarm(alarm.alarm_id, alarm.description);
                        break;
                    
                    case 2:  // Critical
                        log_critical(alarm.description);
                        activate_critical_alarm();
                        send_scada_alarm(alarm.alarm_id, alarm.description);
                        
                        // SIL2 requirement: Dual-channel safety action
                        channel_a_shutdown();
                        channel_b_shutdown();
                        verify_safe_state();
                        break;
                }
                
                // Store in alarm history
                store_alarm_history(&alarm);
            }
        }
    }
    
    // System initialization
    int main(void) {
        printf("Diesel Monitoring System - Initializing...\n");
        
        // Initialize hardware
        init_daq_modules();
        init_serial_ports();
        init_relay_outputs();
        
        // Create message queue
        alarm_queue = LynxCreateMessageQueue(10, sizeof(AlarmMessage_t));
        if (alarm_queue == NULL) {
            printf("ERROR: Failed to create alarm queue\n");
            return -1;
        }
        
        // Create tasks
        diesel_monitor_task_id = LynxCreateTask(
            "DieselMonitor",
            diesel_monitor_task,
            NULL,
            PRIORITY_MONITOR,
            4096  // Stack size
        );
        
        fuel_level_task_id = LynxCreateTask(
            "FuelLevel",
            fuel_level_task,
            NULL,
            PRIORITY_FUEL,
            4096
        );
        
        temp_monitor_task_id = LynxCreateTask(
            "TempMonitor",
            temp_monitor_task,
            NULL,
            PRIORITY_MONITOR,
            4096
        );
        
        alarm_manager_task_id = LynxCreateTask(
            "AlarmManager",
            alarm_manager_task,
            NULL,
            PRIORITY_ALARM,
            8192  // Larger stack for critical task
        );
        
        printf("All tasks created. Starting RTOS scheduler...\n");
        
        // Start RTOS scheduler (never returns)
        LynxStartScheduler();
        
        // Should never reach here
        return 0;
    }

**SIL2 Safety Requirements:**

.. code-block:: c

    // sil2_safety.c - Safety mechanisms
    
    // Dual-channel redundancy for critical shutdowns
    bool channel_a_shutdown(void) {
        // Channel A: Directly control fuel solenoid
        set_relay_output(RELAY_FUEL_SOLENOID_A, RELAY_OFF);
        
        // Verify action
        return (get_relay_status(RELAY_FUEL_SOLENOID_A) == RELAY_OFF);
    }
    
    bool channel_b_shutdown(void) {
        // Channel B: Secondary safety relay
        set_relay_output(RELAY_FUEL_SOLENOID_B, RELAY_OFF);
        
        // Verify action
        return (get_relay_status(RELAY_FUEL_SOLENOID_B) == RELAY_OFF);
    }
    
    // Verify system in safe state (both channels de-energized)
    bool verify_safe_state(void) {
        bool channel_a_safe = (get_relay_status(RELAY_FUEL_SOLENOID_A) == RELAY_OFF);
        bool channel_b_safe = (get_relay_status(RELAY_FUEL_SOLENOID_B) == RELAY_OFF);
        
        if (channel_a_safe && channel_b_safe) {
            log_safety("Safe state verified: Both channels de-energized");
            return true;
        } else {
            log_critical("Safe state verification FAILED!");
            // Additional safety action: Cut power to all outputs
            master_emergency_shutdown();
            return false;
        }
    }
    
    // Watchdog timer (SIL2 requirement)
    void watchdog_task(void *arg) {
        uint32_t last_diesel_heartbeat = 0;
        uint32_t last_temp_heartbeat = 0;
        
        const uint32_t WATCHDOG_TIMEOUT_MS = 2000;
        
        while (1) {
            uint32_t current_time = LynxGetTickCount();
            
            // Check if monitoring tasks are alive
            if ((current_time - last_diesel_heartbeat) > WATCHDOG_TIMEOUT_MS) {
                log_critical("Diesel monitor task timeout!");
                initiate_emergency_shutdown();
            }
            
            if ((current_time - last_temp_heartbeat) > WATCHDOG_TIMEOUT_MS) {
                log_critical("Temperature monitor task timeout!");
                initiate_emergency_shutdown();
            }
            
            // Feed hardware watchdog
            feed_hardware_watchdog();
            
            LynxTaskDelay(LYNX_MSEC_TO_TICKS(100));
        }
    }

================================================================================
Industrial Communication Bridge - Protocol Conversion
================================================================================

Project: Multi-Protocol Industrial Bridge
--------------------------------------------------------------------------------

**Timeline:** 2007-2008

**Hardware:**
- Coldfire SOC (Freescale)
- Ethernet interface
- Serial interfaces (RS-232/485)

**Operating System:**
- ThreadX RTOS

**Purpose:** Protocol conversion between different industrial communication standards

ThreadX RTOS Architecture
--------------------------------------------------------------------------------

.. code-block:: c

    // bridge_main.c - ThreadX-based industrial bridge
    
    #include "tx_api.h"
    #include <stdio.h>
    
    // Thread stacks
    #define THREAD_STACK_SIZE 2048
    
    TX_THREAD ethernet_thread;
    TX_THREAD serial_thread;
    TX_THREAD protocol_converter_thread;
    
    UCHAR ethernet_stack[THREAD_STACK_SIZE];
    UCHAR serial_stack[THREAD_STACK_SIZE];
    UCHAR converter_stack[THREAD_STACK_SIZE];
    
    // Message queues for protocol data
    TX_QUEUE ethernet_rx_queue;
    TX_QUEUE serial_rx_queue;
    TX_QUEUE converter_output_queue;
    
    UCHAR ethernet_queue_buffer[100 * sizeof(ProtocolMessage)];
    UCHAR serial_queue_buffer[100 * sizeof(ProtocolMessage)];
    UCHAR converter_queue_buffer[100 * sizeof(ProtocolMessage)];
    
    // Protocol message structure
    typedef struct {
        uint8_t protocol_type;  // MODBUS, PROFIBUS, etc.
        uint16_t length;
        uint8_t data[256];
    } ProtocolMessage;
    
    // Ethernet receiver thread
    void ethernet_thread_entry(ULONG thread_input) {
        ProtocolMessage msg;
        
        while (1) {
            // Receive data from Ethernet
            if (ethernet_receive(&msg) == SUCCESS) {
                // Forward to protocol converter
                tx_queue_send(&ethernet_rx_queue, &msg, TX_NO_WAIT);
            }
            
            tx_thread_sleep(1);  // Sleep 10ms (ThreadX ticks)
        }
    }
    
    // Serial receiver thread
    void serial_thread_entry(ULONG thread_input) {
        ProtocolMessage msg;
        
        while (1) {
            // Receive data from serial port
            if (serial_receive(&msg) == SUCCESS) {
                // Forward to protocol converter
                tx_queue_send(&serial_rx_queue, &msg, TX_NO_WAIT);
            }
            
            tx_thread_sleep(1);
        }
    }
    
    // Protocol converter thread
    void protocol_converter_thread_entry(ULONG thread_input) {
        ProtocolMessage input_msg, output_msg;
        
        while (1) {
            // Check Ethernet queue
            if (tx_queue_receive(&ethernet_rx_queue, &input_msg, 
                                  TX_NO_WAIT) == TX_SUCCESS) {
                // Convert Ethernet protocol to serial protocol
                convert_eth_to_serial(&input_msg, &output_msg);
                
                // Send to serial port
                serial_transmit(&output_msg);
            }
            
            // Check serial queue
            if (tx_queue_receive(&serial_rx_queue, &input_msg, 
                                  TX_NO_WAIT) == TX_SUCCESS) {
                // Convert serial protocol to Ethernet protocol
                convert_serial_to_eth(&input_msg, &output_msg);
                
                // Send to Ethernet
                ethernet_transmit(&output_msg);
            }
            
            tx_thread_sleep(1);
        }
    }
    
    // Application initialization
    void tx_application_define(void *first_unused_memory) {
        // Create Ethernet thread
        tx_thread_create(&ethernet_thread,
                         "Ethernet RX",
                         ethernet_thread_entry,
                         0,
                         ethernet_stack,
                         THREAD_STACK_SIZE,
                         5,  // Priority
                         5,  // Preemption threshold
                         TX_NO_TIME_SLICE,
                         TX_AUTO_START);
        
        // Create serial thread
        tx_thread_create(&serial_thread,
                         "Serial RX",
                         serial_thread_entry,
                         0,
                         serial_stack,
                         THREAD_STACK_SIZE,
                         5,
                         5,
                         TX_NO_TIME_SLICE,
                         TX_AUTO_START);
        
        // Create protocol converter thread
        tx_thread_create(&protocol_converter_thread,
                         "Protocol Converter",
                         protocol_converter_thread_entry,
                         0,
                         converter_stack,
                         THREAD_STACK_SIZE,
                         3,  // Higher priority
                         3,
                         TX_NO_TIME_SLICE,
                         TX_AUTO_START);
        
        // Create message queues
        tx_queue_create(&ethernet_rx_queue,
                        "Ethernet RX Queue",
                        sizeof(ProtocolMessage) / sizeof(ULONG),
                        ethernet_queue_buffer,
                        sizeof(ethernet_queue_buffer));
        
        tx_queue_create(&serial_rx_queue,
                        "Serial RX Queue",
                        sizeof(ProtocolMessage) / sizeof(ULONG),
                        serial_queue_buffer,
                        sizeof(serial_queue_buffer));
    }

================================================================================
Lessons Learned
================================================================================

**Linux Kernel Driver Development:**
✓ PCIe enumeration requires careful timing and link training
✓ Device tree bindings critical for platform driver probing
✓ Multiple root complexes need independent configuration spaces
✓ FPGA emulation essential for pre-silicon validation

**System Simulation:**
✓ DML (Device Modeling Language) powerful for hardware behavior modeling
✓ Simics enables firmware verification before silicon availability
✓ Python scripting essential for test automation
✓ Checkpoint/restore invaluable for debugging complex scenarios

**SIL2 Safety-Critical Systems:**
✓ Dual-channel redundancy mandatory for critical actions
✓ Watchdog timers prevent task hang scenarios
✓ Verification of safe state required after every safety action
✓ Priority-based task scheduling ensures alarm handling responsiveness

**ThreadX RTOS:**
✓ Message queues provide efficient inter-thread communication
✓ Priority inversion must be managed with preemption thresholds
✓ Stack size analysis critical to prevent overflow

**Common Pitfalls:**
✗ PCIe link training timeout without proper PHY initialization
✗ Insufficient device tree resources cause driver probe failures
✗ Race conditions in multi-threaded RTOS applications
✗ Watchdog timer tuning too aggressive causes false alarms

================================================================================
References
================================================================================

**Standards:**
- PCI Express Base Specification 3.0
- Linux Device Driver Model
- IEC 61508 (Functional Safety)
- Modbus Protocol Specification

**Tools:**
- Linux kernel build system (Kbuild)
- Simics Full-System Simulator
- Wind River Simics
- LYNX RTOS Documentation
- ThreadX RTOS User Guide

================================================================================
