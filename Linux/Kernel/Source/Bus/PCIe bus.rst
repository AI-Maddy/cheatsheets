
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for the PCI / PCIe bus** in the **Linux kernel** (focused on modern kernels ~6.12–6.17 era, January 2026 perspective). Covers hardware basics, kernel structures, driver development patterns, and common APIs.

📖 1. PCI/PCIe Hardware Basics (Quick Ref)

| Concept                  | Description                                                                 | Typical Values / Notes (2026) |
|--------------------------|-----------------------------------------------------------------------------|-------------------------------|
| **Lane width**           | Number of differential pairs (TX+RX)                                        | x1, x4, x8, x16 (most common) |
| **Generation**           | Data rate per lane                                                          | Gen1: 2.5 GT/s, Gen3: 8 GT/s, Gen4: 16 GT/s, Gen5: 32 GT/s, Gen6: 64 GT/s |
| **BAR** (Base Address Register) | Memory/IO regions claimed by device                                   | Up to 6 BARs; 32-bit or 64-bit prefetchable |
| **Config space**         | 256 bytes (PCI) / 4 KiB extended (PCIe)                                     | Vendor ID, Device ID, Class Code, Subsystem ID, Capabilities |
| **Capabilities list**    | Linked list in config space (starting at offset 0x34)                       | MSI, MSI-X, PCIe, Power Management, AER, etc. |
| **Interrupt types**      | Legacy INTx#, MSI, MSI-X                                                    | MSI-X preferred for multi-queue/high-perf |
| **Bus address**          | Address seen by device (after IOMMU translation)                            | dma_addr_t in driver code |
| **TLP** (Transaction Layer Packet) | PCIe packet type (Memory Read/Write, Config, IO, Message)             | — |

🐧 2. Core Kernel Structures (``include/linux/pci.h``)

⭐ | Structure                | Purpose / Key Fields (most important)                                       | Typical Use in Driver |
|--------------------------|-----------------------------------------------------------------------------|-----------------------|
⭐ | ``struct pci_dev``         | Represents one PCI/PCIe function (most important structure)                 | Driver private data often embedded or pointed from here |
|                          | ``vendor``, ``device``, ``subsystem_vendor``, ``subsystem_device``                  | Match table |
|                          | ``revision``, ``class``                                                         | — |
|                          | ``irq`` (legacy), ``msi_cap``, ``msix_cap``                                       | Interrupt setup |
|                          | ``resource[6]`` (struct resource) — BARs                                      | ioremap() / request_mem_region() |
|                          | ``dev`` (struct device) — for DMA, sysfs, etc.                                | ``&pdev->dev`` |
| ``struct pci_driver``      | Driver registration structure                                               | Passed to ``pci_register_driver()`` |
|                          | ``.name``, ``.id_table`` (pci_device_id[]), ``.probe``, ``.remove``                 | Mandatory |
|                          | ``.shutdown``, ``.suspend``, ``.resume``                                          | Power / kexec |
| ``struct pci_bus``         | Represents one PCI bus segment                                              | Rarely touched directly |
|                          | ``number``, ``parent``, ``self`` (bridge device), ``resources``                     | — |
| ``struct pci_host_bridge`` | Root port / host bridge controller                                          | Modern controllers (VMD, DWC, etc.) |

📌 3. PCI Driver Skeleton (Modern Style)

.. code-block:: c

#include <linux/pci.h>
#include <linux/module.h>

static const struct pci_device_id my_pci_tbl[] = {
    { PCI_DEVICE(PCI_VENDOR_ID_MY, PCI_DEVICE_ID_MY_CARD) },
    { PCI_DEVICE_SUB(PCI_VENDOR_ID_MY, PCI_DEVICE_ID_MY_CARD,
                     PCI_SUBVENDOR_ID_XXX, PCI_SUBDEVICE_ID_YYY) },
    { 0, }
};
MODULE_DEVICE_TABLE(pci, my_pci_tbl);

static int my_probe(struct pci_dev *pdev, const struct pci_device_id *id)
{
    int bar = 0;    /* or loop over BARs */
    void __iomem *regs;

    /* Enable device & bus-mastering */
    if (pci_enable_device(pdev))
        return -ENODEV;
    pci_set_master(pdev);

    /* Optional: request 64-bit DMA (PCIe almost always supports) */
    if (pci_set_dma_mask(pdev, DMA_BIT_MASK(64)) ||
        pci_set_consistent_dma_mask(pdev, DMA_BIT_MASK(64)))
        pci_set_dma_mask(pdev, DMA_BIT_MASK(32));  /* fallback */

    /* Map BAR0 (example) */
    if (pci_request_region(pdev, bar, "my-regs"))
        goto err_disable;
    regs = pci_iomap(pdev, bar, 0);
    if (!regs)
        goto err_release;

    /* ... init hardware, request_irq(), etc. ... */

    pci_set_drvdata(pdev, my_priv_data);
    return 0;

err_release:
    pci_release_region(pdev, bar);
err_disable:
    pci_disable_device(pdev);
    return -ENODEV;
}

static void my_remove(struct pci_dev *pdev)
{
    void __iomem *regs = pci_get_drvdata(pdev);  /* or your priv */

    /* cleanup: disable interrupts, iounmap, etc. */
    iounmap(regs);
    pci_release_region(pdev, 0);
    pci_disable_device(pdev);
}

static struct pci_driver my_driver = {
    .name         = KBUILD_MODNAME,
    .id_table     = my_pci_tbl,
    .probe        = my_probe,
    .remove       = my_remove,
    /* .shutdown, .suspend, .resume if needed */
};

module_pci_driver(my_driver);
MODULE_LICENSE("GPL");

⭐ 📚 4. Key PCI APIs (Most Frequently Used)

| Category               | Function / Macro                                      | Purpose / Notes |
|------------------------|-------------------------------------------------------|-----------------|
| **Registration**       | ``pci_register_driver()``                               | Register driver |
| **Enable/Disable**     | ``pci_enable_device()`` / ``pci_disable_device()``        | Power on + claim resources |
|                        | ``pci_set_master()``                                    | Enable bus-mastering (DMA) |
| **DMA setup**          | ``pci_set_dma_mask()`` / ``pci_set_consistent_dma_mask()``| Set DMA addressing capability |
| **BAR mapping**        | ``pci_iomap(pdev, bar, maxlen)``                        | Preferred over ioremap() |
|                        | ``pci_resource_start(pdev, bar)`` / ``pci_resource_len()``| Get BAR phys addr & size |
| **Config space**       | ``pci_read_config_word()`` / ``pci_write_config_dword()`` | Direct config access |
|                        | ``pcie_capability_read_word()`` / ``..._write_word()``    | Safe PCIe cap access (RMW helpers) |
| **MSI / MSI-X**        | ``pci_enable_msi()`` / ``pci_enable_msix_range()``        | Enable interrupts |
|                        | ``pci_disable_msi()`` / ``pci_disable_msix()``            | Cleanup |
| **Reset**              | ``pci_reset_function()`` / ``pci_reset_bus()``            | Function / bus reset |
| **Power**              | ``pci_set_power_state()``                               | D0–D3hot (D3cold rare) |

🐛 5. Sysfs & Debug Locations (Runtime Inspection)

/sys/bus/pci/devices/0000:NN:DD.F/      ← one dir per pci_dev
    ├── config          ← raw 256/4096 byte config space
    ├── resource[0–5]   ← BAR info
    ├── irq
    ├── driver
    ├── numa_node
    ├── remove          ← echo 1 > remove (forces unbind)
    └── reset           ← echo 1 > reset (function level)

/sys/bus/pci/drivers/my_driver/         ← bound devices
/proc/bus/pci/devices                   ← legacy list
lspci -nn -vvv -d vendor:device         ← userspace debug
dmesg | grep PCI                        ← probe / resource allocation

💡 6. Common Gotchas & Modern Tips (2026)

- Always call ``pci_set_dma_mask()`` early — PCIe devices are expected to support 64-bit.
- Use ``pci_iomap()`` / ``pci_iounmap()`` instead of raw ``ioremap()``.
- Prefer MSI-X over legacy INTx for performance / multi-queue drivers.
- For hotplug / AER / DPC → use service drivers under PCIe Port Bus (``pcieport``).
- IOMMU = ``dma-mapping`` API — never assume physical = bus address.
- BARs can be 64-bit → check ``resource[n].flags & IORESOURCE_MEM_64``.
- Extended config space (>256 bytes) → use ``pci_read_config_*()`` with offset > 255.

Main reference: ``Documentation/PCI/`` in kernel tree (especially ``pci.txt``, ``pciebus-howto.rst``).

🟢 🟢 Good luck with your PCI/PCIe driver development!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
