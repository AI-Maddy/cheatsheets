**cheatsheet for Linux security on embedded systems** (2025–2026 perspective).  
Focuses on real-world embedded Linux (IoT, automotive, industrial, medical, gateways, routers, headless devices, constrained ARM/RISC-V/MIPS).

📌 1. Threat Model – Typical Embedded Risks

| Threat Category              | Typical Attack Vector                              | Impact on Embedded Devices                     | Priority (High/Med/Low) |
|------------------------------|----------------------------------------------------|------------------------------------------------|--------------------------|
| Physical access               | JTAG, UART, SPI flash extraction                   | Root access, firmware dump                     | High                     |
| Remote code execution         | Buffer overflow in network daemon                  | Full device compromise                         | High                     |
| Supply-chain / boot-time      | Malicious bootloader / firmware update             | Persistent backdoor                            | High                     |
⭐ | Weak/default credentials      | Telnet/SSH root/admin, hardcoded keys              | Easy initial access                            | High                     |
| Insecure OTA / update         | Unauthenticated / unsigned updates                 | Permanent compromise                           | High                     |
⭐ | Side-channel / fault injection| Voltage/timing glitches, Rowhammer                 | Key extraction, bypass secure boot             | Medium–High              |
| Resource exhaustion           | DoS via malformed packets / fork bombs             | Device unresponsive / bricked                  | Medium                   |
| Privacy leakage               | Unencrypted telemetry, debug logs                  | User data exposure                             | Medium                   |

📌 2. Hardening Checklist – Ordered by Impact

| Category                     | Recommended Hardening Measure                              | Tool / Config / Kernel Option                          | Effort / Impact |
|------------------------------|------------------------------------------------------------|--------------------------------------------------------|-----------------|
| **Secure Boot**              | Enable & enforce verified boot (signed kernel + rootfs)    | U-Boot FIT + verified boot, OP-TEE, ARM TrustZone      | High / Very High |
| **Read-only rootfs**         | Squashfs + overlayfs (or dm-verity)                        | ``CONFIG_DM_VERITY=y``, ``overlayroot=``, ``squashfs``       | High / High     |
| **Kernel hardening**         | Lock down syscalls, disable debug, KASLR, stack canaries   | ``CONFIG_GRKERNSEC``, ``CONFIG_SECURITY_*``, ``CONFIG_LSM``  | Medium / High   |
| **Minimal userspace**        | Use musl libc, busybox, drop unneeded daemons              | Buildroot / Yocto minimal image                        | Medium / High   |
| **No shell access**          | Remove shell from release image, disable UART console     | ``CONFIG_CONSOLE=n``, ``CONFIG_SERIAL_*=n``                | Low / High      |
| **Network lockdown**         | iptables/nftables drop-all + allow only required ports     | ``nftables`` / ``iptables -P INPUT DROP``                  | Medium / High   |
⭐ | **No unnecessary services**  | Drop telnet, SSH (or restrict to key-only), dropbear       | ``dropbear`` with ``-s -j -k``, no ``openssh-server``        | Low / High      |
| **Secure updates**           | Signed & authenticated OTA (RAUC, SWUpdate, Mender)       | RAUC / Mender / SWUpdate + TPM/secure element          | High / Very High |
| **File system encryption**   | dm-crypt / fscrypt on sensitive partitions                 | ``dm-crypt``, ``fscrypt`` (ext4/f2fs)                      | Medium / Medium |
⭐ | **AppArmor / Landlock**      | Confine critical daemons (network-facing)                  | ``CONFIG_SECURITY_APPARMOR=y``, Landlock LSM             | Medium / High   |
| **seccomp**                  | Strict syscall filters for daemons                         | ``seccomp`` BPF filters (libseccomp)                     | Medium / High   |
| **No debug symbols**         | Strip binaries, remove /proc/kallsyms                      | ``strip --strip-all``, ``CONFIG_KALLSYMS=n``               | Low / Medium    |
| **Randomize everything**     | KASLR, stack canaries, heap randomization                 | ``CONFIG_RANDOMIZE_BASE=y``, ``CONFIG_STACKPROTECTOR=y``   | Low / Medium    |

⭐ 🐧 3. Kernel Configuration Hardening (Essential for Embedded)

| CONFIG Option                          | Recommended Setting | Why (Embedded Security Impact) |
|----------------------------------------|----------------------|--------------------------------|
| ``CONFIG_GRKERNSEC``                     | y                    | Many hardening patches (PaX-like) |
| ``CONFIG_SECURITY_*`` (all)              | y                    | LSM framework + AppArmor/Landlock |
| ``CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,integrity,selinux,smack,tomoyo,apparmor"`` | landlock first | Modern LSM stacking (Landlock for sandboxing) |
| ``CONFIG_DEFAULT_SECURITY_APPARMOR``     | y                    | Default profile for daemons |
| ``CONFIG_RANDOMIZE_BASE``                | y                    | KASLR (even on 32-bit ARM) |
| ``CONFIG_STACKPROTECTOR_STRONG``         | y                    | Stack canaries |
| ``CONFIG_DEBUG_KERNEL``                  | n                    | Remove debug info & symbols |
| ``CONFIG_KALLSYMS``                      | n                    | No kernel symbol table |
| ``CONFIG_MODULES``                       | n (if possible)      | No loadable modules |
| ``CONFIG_DEVMEM``                        | n                    | No /dev/mem access |
| ``CONFIG_PROC_KCORE``                    | n                    | No kernel memory dump |
| ``CONFIG_SECURITY_DMESG_RESTRICT``       | y                    | Restrict dmesg to root |

🔐 4. Build System & Image Security (Buildroot / Yocto)

| Practice                               | Buildroot Equivalent                              | Yocto / OpenEmbedded Equivalent                     | Benefit |
|----------------------------------------|---------------------------------------------------|-----------------------------------------------------|---------|
| Use musl instead of glibc              | ``BR2_TOOLCHAIN_BUILDROOT_MUSL=y``                  | ``TCLIBC = "musl"``                                   | Smaller attack surface |
| Squashfs rootfs + dm-verity            | ``BR2_TARGET_ROOTFS_SQUASHFS=y`` + verity           | ``IMAGE_FEATURES += "read-only-rootfs"`` + verity recipe | Integrity + tamper detection |
| Signed FIT image (U-Boot)              | ``BR2_TARGET_UBOOT_FIT_SIGNATURE=y``                | ``FIT_SIGNATURE_ENABLE = "1"``                        | Verified boot |
| Minimal init system                    | busybox init or sysvinit                          | tiny-init or sysvinit                               | Fewer attack vectors |
| No debug tools in image                | ``BR2_PACKAGE_BUSYBOX_CONFIG_FRAGMENT_FILES`` remove debug | ``IMAGE_FEATURES_remove = "tools-sdk debug-tweaks"`` | No gdb/strace/nc |

📌 5. Runtime Hardening Tools & Commands

.. code-block:: bash

================================================================================
Enforce noexec on /tmp /dev/shm
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



mount -o remount,noexec /tmp
mount -o remount,noexec /dev/shm

================================================================================
Drop capabilities for daemons
================================================================================

setcap cap_net_raw,cap_net_admin=ep /usr/bin/my-daemon   # only needed caps

================================================================================
🐛 Restrict ptrace (anti-debug)
================================================================================

echo 1 > /proc/sys/kernel/yama/ptrace_scope

================================================================================
🐧 Hide kernel pointers
================================================================================

echo 2 > /proc/sys/kernel/kptr_restrict

================================================================================
Disable core dumps
================================================================================

ulimit -c 0
echo 1 > /proc/sys/kernel/core_pattern  # or |/bin/false

================================================================================
💻 nftables minimal drop-all policy (example)
================================================================================

nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input iif lo accept
nft add rule inet filter input ct state established,related accept

================================================================================
... add specific allows ...
================================================================================

📚 6. Quick Reference: Embedded Security Maturity Levels

⭐ | Level | Description                                      | Typical Devices                          | Key Features Enabled |
|-------|--------------------------------------------------|------------------------------------------|----------------------|
| Level 1 | Minimal (consumer IoT)                           | Smart bulb, cheap camera                 | Password change, firewall |
| Level 2 | Basic hardening                                  | Industrial gateway, router               | Secure boot, read-only rootfs |
| Level 3 | 🟢 🟢 Good security (automotive ASIL-B, medical)       | ADAS ECU, infusion pump                  | dm-verity, AppArmor, seccomp |
⭐ | Level 4 | High assurance (ASIL-D, avionics DAL-B)          | Critical automotive, flight control      | Verified boot, LSM stacking, fault injection resistance |

**Golden rules for embedded Linux security (2026)**  
1. **Never ship with shell on production UART**  
2. **Always use verified boot** (even if only U-Boot FIT signature)  
3. **Read-only rootfs + dm-verity is cheap & powerful**  
4. **Drop everything you can** — fewer binaries = fewer CVEs  
5. **Assume physical attacker** — JTAG, SPI flash dump is real  
6. **OTA must be signed & authenticated** — unsigned = game over  

🟢 🟢 Good luck securing your embedded Linux device!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
