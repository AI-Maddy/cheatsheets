**cheatsheet for PCIe Transactions and Behavior** (Transaction Layer focus, PCIe 3.0–6.0 era, valid ~2025–2026). Covers **TLP types**, **formats**, **routing**, **posted vs non-posted**, **ordering rules**, **flow control basics**, and key behavioral notes.

### 1. PCIe Layers Quick Reminder

- **Transaction Layer** — Generates / consumes **TLPs** (Transaction Layer Packets)  
- **Data Link Layer** — Adds sequence number + LCRC, ACK/NAK, replay buffer  
- **Physical Layer** — Encodes (8b/10b or 128b/130b), scrambling, LTSSM  

### 2. TLP Common Header (First DW – 32 bits)

| Bits       | Field              | Meaning / Values                                                                 |
|------------|--------------------|----------------------------------------------------------------------------------|
| 31–29      | Fmt                | 000 = 3DW header, no data<br>001 = 4DW header, no data<br>010 = 3DW header + data<br>011 = 4DW header + data |
| 28–24      | Type               | See table below                                                                  |
| 23         | TC[2]              | Traffic Class (usually 0 in practice)                                            |
| 22         | —                  | Reserved                                                                         |
| 21         | TD                 | TLP Digest (ECRC) present?                                                       |
| 20         | EP                 | Poisoned (data corrupt)                                                          |
| 19–16      | Attr[3:0]          | No Snoop, Relaxed Ordering, Idempotent, etc.                                     |
| 15–10      | Length[9:0]        | Payload in DW (1–1023 = 4–4092 bytes; 0 = 1024 DW for data TLPs)                |
| 9–0        | —                  | Varies by Type                                                                   |

### 3. Main TLP Types & Formats

| TLP Type (Type[4:0]) | Fmt | Header DW | Payload? | Posted? | Completion? | Routing          | Typical Use / Behavior |
|----------------------|-----|-----------|----------|---------|-------------|------------------|------------------------|
| Memory Read Request  | 000 / 001 | 3 or 4    | No       | No      | Yes         | Address          | Requester → Completer; wait for CplD / Cpl |
| Memory Write Request | 010 / 011 | 3 or 4    | Yes      | Yes     | No          | Address          | Posted – fire & forget; no response |
| I/O Read / Write     | 000 / 010 | 3         | Optional | No / Yes| Yes / No    | Address          | Legacy – avoid in new designs |
| Config Type 0 / 1 Read | 000   | 3         | No       | No      | Yes         | ID               | Enumeration / config space access |
| Config Type 0 / 1 Write| 010   | 3         | Yes      | No      | Yes         | ID               | — |
| Message (no data)    | 001   | 4         | No       | Yes     | No          | ID / Address / Implicit / Local | Int, PM, Error, Hot-Plug, Vendor |
| Message with data    | 011   | 4         | Yes      | Yes     | No          | —                | — |
| Completion (no data) | 000   | 3         | No       | —       | —           | ID               | Cpl (Successful / UR / CA) |
| Completion with data | 010   | 3         | Yes      | —       | —           | ID               | CplD – carries read data |

**Key notes**:
- **Posted** = no completion required (Memory Write, most Messages) → higher performance, but no success confirmation
- **Non-Posted** = requires Completion (Reads, I/O/Config Writes) → guarantees delivery & status
- **Maximum Payload Size (MPS)**: Negotiated (128–4096 bytes); larger requests split into multiple TLPs

### 4. Routing Methods

| Method         | Used by                              | How it works                                      | Typical path |
|----------------|--------------------------------------|---------------------------------------------------|--------------|
| **Address**    | Memory / I/O Requests                | Compare address against BARs / apertures          | Endpoint BAR match |
| **ID**         | Completions, Config, some Messages   | Bus:Dev:Func match (Requester ID or Completer ID) | Back to Requester |
| **Implicit**   | Some Messages (e.g. PM, Error)       | Fixed / broadcast rules                           | Root Complex or local link |
| **Local**      | Some vendor messages                 | Only current link                                 | — |

### 5. PCIe Ordering Rules (Simplified – Relaxed Ordering = RO bit)

**Strict Ordering (RO=0) – Default behavior**

| Can pass →       | Posted Req (MemWr) | Non-Posted Req | Completions |
|------------------|--------------------|----------------|-------------|
| Posted Req       | No                 | Yes (avoid deadlock) | Yes |
| Non-Posted Req   | No                 | No             | No  |
| Completion       | No                 | No             | No  |

**Relaxed Ordering (RO=1) – Performance optimization (common for DMA)**

- Posted Requests **may** pass other Posted Requests
- Posted Requests **may** pass Non-Posted Requests (helps avoid head-of-line blocking)
- Completions still strongly ordered relative to each other

**x86 / ARM implications**:
- CPU reads block until completion → strong ordering from CPU view
- Device DMA with RO=1 → can overtake other writes → higher BW, but requires careful driver design

### 6. Completion Status (Cpl / CplD)

| Status Code | Meaning                     | When sent |
|-------------|-----------------------------|-----------|
| Successful  | 000                     | OK        |
| UR          | Unsupported Request     | Bad address / type |
| CA          | Completer Abort         | Internal error |
| CRS         | Configuration Request Retry | Config retry (hot-plug / enumeration) |

### 7. Flow Control Basics (Credit-based)

- **Posted / Non-Posted / Completion** — separate credit types
- **Header + Data** credits advertised via InitFC DLLPs
- Sender blocks when credits = 0 (no buffer space)
- Completions **never** blocked by FC (requester must have space)

### 8. Quick Reference: Behavior Gotchas

- **Memory Writes** — posted, no ack, can be dropped on error (use MSI/MSI-X for status)
- **Reads** — split transaction; timeout if no completion (~50–100 ms typical)
- **ECRC** (optional) — end-to-end CRC (beyond LCRC)
- **Poisoning** (EP=1) — data known bad, often propagated
- **Max Read Request Size** — 128–4096 B; larger split by requester
- **4 KiB boundary** — single TLP must not cross 4 KiB address boundary

**Best sources** for deep dive:
- PCIe Base Specification (PCI-SIG) — Ch. 2 (Transaction Layer)
- xillybus.com PCIe TLP tutorial (very practical)
- fpga4fun.com PCIe series

Use this when debugging TLP captures (e.g., with LeCroy / Teledyne analyzers) or writing low-level PCIe logic / drivers.