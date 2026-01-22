========================================
GRUB2 Complete Reference & Guide
========================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

GRUB2 (Grand Unified Bootloader version 2) is the default bootloader for most Linux distributions.

Key Features
------------

+--------------------------------+----------------------------------------------------------+
| **Feature**                    | **Description**                                          |
+================================+==========================================================+
| OS Support                     | Linux, Windows, BSD, macOS, others                       |
+--------------------------------+----------------------------------------------------------+
| Boot Methods                   | BIOS (Legacy), UEFI, Secure Boot, Coreboot              |
+--------------------------------+----------------------------------------------------------+
| File Systems                   | ext2/3/4, Btrfs, XFS, ZFS, FAT, NTFS, ISO9660           |
+--------------------------------+----------------------------------------------------------+
| Scripting                      | Full scripting language with conditionals, loops         |
+--------------------------------+----------------------------------------------------------+
| Network Boot                   | PXE, TFTP, HTTP                                          |
+--------------------------------+----------------------------------------------------------+
| Encryption Support             | LUKS, encrypted partitions                               |
+--------------------------------+----------------------------------------------------------+
| Themes                         | Graphical themes with images, fonts                      |
+--------------------------------+----------------------------------------------------------+

Architecture
------------

.. code-block:: text

   BIOS/UEFI → boot.img/bootx64.efi → core.img → 
   /boot/grub/grub.cfg → Load Kernel → Boot OS

📁 Configuration Files
=======================

Main Configuration
------------------

**/boot/grub/grub.cfg** (Generated - DO NOT EDIT DIRECTLY)

**/etc/default/grub** (User Configuration)

.. code-block:: bash

   # Timeout before default boot
   GRUB_TIMEOUT=5
   
   # Default menu entry (0-indexed or "saved")
   GRUB_DEFAULT=0
   GRUB_DEFAULT=saved
   
   # Kernel command line
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
   GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200"
   
   # Graphics mode
   GRUB_GFXMODE=1024x768
   GRUB_GFXPAYLOAD_LINUX=keep
   
   # Terminal type
   GRUB_TERMINAL=console
   #GRUB_TERMINAL="console serial"
   
   # Serial console
   GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
   
   # Hidden menu
   GRUB_TIMEOUT_STYLE=hidden
   
   # Disable submenu
   GRUB_DISABLE_SUBMENU=y
   
   # Theme
   GRUB_THEME="/boot/grub/themes/mytheme/theme.txt"
   
   # Distribution
   GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
   
   # Disable OS prober (find other OS)
   GRUB_DISABLE_OS_PROBER=false
   
   # Recovery mode
   GRUB_DISABLE_RECOVERY=false
   
   # Background image
   GRUB_BACKGROUND="/boot/grub/background.png"

Custom Scripts
--------------

**/etc/grub.d/** (Scripts executed in order to build grub.cfg)

.. code-block:: text

   00_header          # GRUB header settings
   05_debian_theme    # Debian/Ubuntu theme
   10_linux           # Linux kernels
   20_linux_xen       # Xen hypervisor entries
   30_os-prober       # Other OS detection
   40_custom          # Custom menu entries
   41_custom          # Additional custom entries

**Example /etc/grub.d/40_custom:**

.. code-block:: bash

   #!/bin/sh
   exec tail -n +3 $0
   # Custom GRUB entries
   
   menuentry 'My Custom Linux' {
       set root='hd0,gpt2'
       linux /boot/vmlinuz-custom root=/dev/sda2 ro quiet
       initrd /boot/initrd.img-custom
   }
   
   menuentry 'Windows 10' {
       insmod part_gpt
       insmod fat
       insmod chain
       set root='hd0,gpt1'
       chainloader /EFI/Microsoft/Boot/bootmgfw.efi
   }
   
   menuentry 'Memory Test (memtest86+)' {
       linux16 /boot/memtest86+.bin
   }

Update Configuration
--------------------

.. code-block:: bash

   # Generate grub.cfg from /etc/default/grub and /etc/grub.d/*
   
   # Debian/Ubuntu
   sudo update-grub
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   
   # RHEL/Fedora/CentOS
   sudo grub2-mkconfig -o /boot/grub2/grub.cfg
   
   # UEFI systems
   sudo grub-mkconfig -o /boot/efi/EFI/ubuntu/grub.cfg

🎮 GRUB Command Line
=====================

Essential Commands
------------------

**Boot Commands:**

.. code-block:: grub

   # List devices
   ls
   ls (hd0,gpt1)/
   
   # Set root device
   set root=(hd0,gpt2)
   
   # Load Linux kernel
   linux /boot/vmlinuz-5.15.0-generic root=/dev/sda2 ro
   
   # Load initramfs
   initrd /boot/initrd.img-5.15.0-generic
   
   # Boot
   boot
   
   # Chain load another bootloader
   chainloader /EFI/Microsoft/Boot/bootmgfw.efi

**File System Commands:**

.. code-block:: grub

   # List files
   ls (hd0,gpt2)/boot
   
   # Display file content
   cat (hd0,gpt2)/etc/fstab
   
   # Check file existence
   test -e (hd0,gpt2)/boot/vmlinuz
   
   # Read file into memory
   read (hd0,gpt2)/boot/vmlinuz

**Module Commands:**

.. code-block:: grub

   # Load module
   insmod ext2
   insmod gzio
   insmod part_gpt
   insmod fat
   
   # List loaded modules
   lsmod

**System Information:**

.. code-block:: grub

   # GRUB version
   grubversion
   
   # Display memory map
   lsmmap
   
   # Display devices
   ls
   
   # Get UUID
   search --set=root --fs-uuid 1234-5678

**Configuration:**

.. code-block:: grub

   # Set variables
   set timeout=10
   set default=0
   
   # Display variable
   echo $root
   echo $prefix
   
   # Export variable
   export myvar

🔧 Installation
================

BIOS Installation
-----------------

.. code-block:: bash

   # Install to MBR
   sudo grub-install /dev/sda
   
   # Install with specific boot directory
   sudo grub-install --boot-directory=/mnt/boot /dev/sda
   
   # Force installation (if warnings)
   sudo grub-install --force /dev/sda
   
   # Verify installation
   sudo grub-install --recheck /dev/sda

UEFI Installation
-----------------

.. code-block:: bash

   # Install to EFI System Partition
   sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB
   
   # Install with removable flag (for USB drives)
   sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --removable
   
   # Install to specific directory
   sudo grub-install --target=x86_64-efi --efi-directory=/mnt/boot/efi --boot-directory=/mnt/boot
   
   # Verify EFI boot entry
   efibootmgr -v

Chroot Installation (Rescue)
-----------------------------

.. code-block:: bash

   # Boot from live USB
   # Mount root filesystem
   sudo mount /dev/sda2 /mnt
   sudo mount /dev/sda1 /mnt/boot/efi  # For UEFI
   
   # Mount required filesystems
   sudo mount --bind /dev /mnt/dev
   sudo mount --bind /proc /mnt/proc
   sudo mount --bind /sys /mnt/sys
   sudo mount --bind /run /mnt/run
   
   # Chroot
   sudo chroot /mnt
   
   # Install GRUB
   grub-install /dev/sda                    # BIOS
   grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB  # UEFI
   
   # Update config
   update-grub
   
   # Exit and reboot
   exit
   sudo umount -R /mnt
   reboot

📝 Menu Entries
================

Basic Linux Entry
-----------------

.. code-block:: grub

   menuentry 'Ubuntu 22.04' {
       set root='hd0,gpt2'
       linux /boot/vmlinuz-5.15.0-generic root=UUID=1234-5678 ro quiet splash
       initrd /boot/initrd.img-5.15.0-generic
   }

Advanced Linux Entry
--------------------

.. code-block:: grub

   menuentry 'Ubuntu - Advanced Options' {
       recordfail
       load_video
       gfxmode $linux_gfx_mode
       insmod gzio
       insmod part_gpt
       insmod ext2
       
       # Search for root by UUID
       search --no-floppy --fs-uuid --set=root 1234-5678-90ab-cdef
       
       echo 'Loading Linux kernel...'
       linux /boot/vmlinuz-5.15.0-generic root=UUID=1234-5678-90ab-cdef ro \
           quiet splash nomodeset i915.modeset=0 \
           console=tty0 console=ttyS0,115200n8
       
       echo 'Loading initial ramdisk...'
       initrd /boot/initrd.img-5.15.0-generic /boot/intel-ucode.img
   }

Windows Entry (UEFI)
--------------------

.. code-block:: grub

   menuentry 'Windows 10' {
       insmod part_gpt
       insmod fat
       insmod chain
       search --no-floppy --fs-uuid --set=root ABCD-1234
       chainloader /EFI/Microsoft/Boot/bootmgfw.efi
   }

Windows Entry (BIOS)
--------------------

.. code-block:: grub

   menuentry 'Windows 10' {
       insmod part_msdos
       insmod ntfs
       insmod chain
       set root='hd0,msdos1'
       chainloader +1
   }

ISO Boot Entry
--------------

.. code-block:: grub

   menuentry 'Ubuntu 22.04 ISO' {
       set isofile="/boot/iso/ubuntu-22.04-desktop-amd64.iso"
       loopback loop (hd0,gpt2)$isofile
       linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile noprompt noeject quiet splash
       initrd (loop)/casper/initrd
   }

Submenu
-------

.. code-block:: grub

   submenu 'Advanced Options' {
       menuentry 'Recovery Mode' {
           linux /boot/vmlinuz root=/dev/sda2 ro single
           initrd /boot/initrd.img
       }
       
       menuentry 'Safe Graphics Mode' {
           linux /boot/vmlinuz root=/dev/sda2 ro nomodeset
           initrd /boot/initrd.img
       }
   }

🎨 Theming & Customization
===========================

Theme Structure
---------------

.. code-block:: text

   /boot/grub/themes/mytheme/
   ├── theme.txt           # Theme definition
   ├── background.png      # Background image
   ├── icons/              # Menu item icons
   │   ├── ubuntu.png
   │   ├── windows.png
   │   └── ...
   └── fonts/              # Custom fonts
       └── dejavu.pf2

Theme Configuration
-------------------

**/boot/grub/themes/mytheme/theme.txt:**

.. code-block:: text

   # General settings
   title-text: ""
   desktop-image: "background.png"
   desktop-color: "#000000"
   
   # Terminal settings
   terminal-font: "DejaVu Sans Mono Regular 12"
   terminal-box: "terminal_box_*.png"
   
   # Boot menu
   + boot_menu {
       left = 15%
       top = 20%
       width = 70%
       height = 60%
       
       item_font = "DejaVu Sans Regular 16"
       item_color = "#ffffff"
       selected_item_color = "#000000"
       selected_item_pixmap_style = "select_*.png"
       
       item_height = 32
       item_padding = 10
       item_spacing = 5
       
       icon_width = 32
       icon_height = 32
       item_icon_space = 10
   }
   
   # Progress bar
   + progress_bar {
       id = "__timeout__"
       left = 15%
       top = 85%
       width = 70%
       height = 24
       
       fg_color = "#ffffff"
       bg_color = "#666666"
       border_color = "#ffffff"
       
       text = "@TIMEOUT_NOTIFICATION_SHORT@"
       text_color = "#ffffff"
       font = "DejaVu Sans Regular 12"
   }
   
   # Labels
   + label {
       top = 90%
       left = 0
       width = 100%
       height = 20
       align = "center"
       text = "Press 'e' to edit, 'c' for command line"
       color = "#cccccc"
       font = "DejaVu Sans Regular 10"
   }

Enable Theme
------------

.. code-block:: bash

   # In /etc/default/grub
   GRUB_THEME="/boot/grub/themes/mytheme/theme.txt"
   
   # Update GRUB
   sudo update-grub

Custom Fonts
------------

.. code-block:: bash

   # Convert TTF to PF2 format
   sudo grub-mkfont -o /boot/grub/fonts/myfont.pf2 /path/to/font.ttf
   
   # Use in theme or config
   loadfont /boot/grub/fonts/myfont.pf2
   set gfxterm_font=myfont

Custom Background
-----------------

.. code-block:: bash

   # In /etc/default/grub
   GRUB_BACKGROUND="/boot/grub/background.png"
   
   # Supported formats: PNG, JPEG, TGA
   # Recommended: PNG with transparency
   # Resolution: Match your screen or use 1920x1080

🔒 Security Features
=====================

Password Protection
-------------------

**Create Password Hash:**

.. code-block:: bash

   # Generate PBKDF2 hash
   grub-mkpasswd-pbkdf2
   # Enter password when prompted
   # Copy the generated hash

**Configure in /etc/grub.d/40_custom:**

.. code-block:: grub

   set superusers="admin"
   password_pbkdf2 admin grub.pbkdf2.sha512.10000.LONG_HASH_HERE

**Protect Specific Entries:**

.. code-block:: grub

   # Unprotected entry (anyone can boot)
   menuentry 'Ubuntu' --unrestricted {
       linux /boot/vmlinuz root=/dev/sda2
       initrd /boot/initrd.img
   }
   
   # Protected entry (requires password)
   menuentry 'Recovery Mode' --users admin {
       linux /boot/vmlinuz root=/dev/sda2 single
       initrd /boot/initrd.img
   }
   
   # Multiple users
   password_pbkdf2 user1 hash1
   password_pbkdf2 user2 hash2
   menuentry 'Special Boot' --users user1,user2 {
       # ...
   }

UEFI Secure Boot
----------------

.. code-block:: bash

   # Check Secure Boot status
   mokutil --sb-state
   
   # Install GRUB with Secure Boot support
   sudo grub-install --target=x86_64-efi --uefi-secure-boot
   
   # Sign GRUB
   sudo sbsign --key /path/to/key.key --cert /path/to/cert.pem \
       --output /boot/efi/EFI/ubuntu/grubx64.efi.signed \
       /boot/efi/EFI/ubuntu/grubx64.efi
   
   # Enroll MOK (Machine Owner Key)
   sudo mokutil --import /path/to/MOK.der
   # Reboot and complete enrollment in MOK Manager

LUKS Encrypted Root
-------------------

.. code-block:: grub

   menuentry 'Ubuntu (Encrypted Root)' {
       insmod gzio
       insmod part_gpt
       insmod ext2
       insmod luks
       
       cryptomount -u 1234567890abcdef  # LUKS UUID
       set root='cryptouuid/1234567890abcdef'
       
       linux /boot/vmlinuz-5.15.0 root=/dev/mapper/cryptroot ro
       initrd /boot/initrd.img-5.15.0
   }

🌐 Network Boot (PXE)
======================

GRUB for PXE
------------

**Build GRUB PXE Image:**

.. code-block:: bash

   # Create netboot image
   grub-mknetdir --net-directory=/srv/tftp \
       --subdir=grub \
       --modules="tftp http net efinet"
   
   # Output: /srv/tftp/grub/i386-pc/core.0 (BIOS)
   #         /srv/tftp/grub/x86_64-efi/core.efi (UEFI)

**DHCP Configuration (dnsmasq):**

.. code-block:: text

   dhcp-range=192.168.1.100,192.168.1.200,12h
   dhcp-boot=grub/i386-pc/core.0            # BIOS
   dhcp-match=set:efi-x86_64,option:client-arch,7
   dhcp-boot=tag:efi-x86_64,grub/x86_64-efi/core.efi  # UEFI
   enable-tftp
   tftp-root=/srv/tftp

**GRUB Network Config (grub.cfg on TFTP server):**

.. code-block:: grub

   set timeout=10
   set default=0
   
   menuentry 'Boot Ubuntu via NFS' {
       echo 'Loading kernel...'
       linux (tftp)/images/vmlinuz root=/dev/nfs \
           nfsroot=192.168.1.1:/export/ubuntu ip=dhcp rw
       
       echo 'Loading initrd...'
       initrd (tftp)/images/initrd.img
   }
   
   menuentry 'Boot Ubuntu via HTTP' {
       linux (http,192.168.1.1)/images/vmlinuz root=/dev/nfs \
           nfsroot=192.168.1.1:/export/ubuntu ip=dhcp
       initrd (http,192.168.1.1)/images/initrd.img
   }

🛠️ Rescue & Recovery
======================

GRUB Rescue Mode
----------------

**Symptoms:**

.. code-block:: text

   grub rescue>

**Recovery Steps:**

.. code-block:: grub

   # Find root partition
   ls
   # Output: (hd0) (hd0,gpt1) (hd0,gpt2) ...
   
   # Check each partition
   ls (hd0,gpt1)/
   ls (hd0,gpt2)/boot/grub
   
   # Set root (found /boot/grub)
   set root=(hd0,gpt2)
   set prefix=(hd0,gpt2)/boot/grub
   
   # Load normal mode
   insmod normal
   normal
   
   # Once booted into system, reinstall GRUB
   sudo grub-install /dev/sda
   sudo update-grub

Boot from GRUB Command Line
----------------------------

.. code-block:: grub

   # Press 'c' at GRUB menu for command line
   
   # Find Linux partition
   grub> ls
   grub> ls (hd0,gpt2)/
   
   # Set root
   grub> set root=(hd0,gpt2)
   
   # Load kernel (find vmlinuz version first)
   grub> linux /boot/vmlinuz-5.15.0-generic root=/dev/sda2 ro
   
   # Load initrd
   grub> initrd /boot/initrd.img-5.15.0-generic
   
   # Boot
   grub> boot

Edit Menu Entry at Boot
------------------------

.. code-block:: text

   1. Select menu entry
   2. Press 'e' to edit
   3. Modify kernel parameters (e.g., add 'single' for single-user mode)
   4. Press Ctrl+X or F10 to boot
   5. Changes are temporary (not saved)

Single User Mode
-----------------

.. code-block:: grub

   # Edit kernel line, append:
   linux /boot/vmlinuz ... ro single
   # OR
   linux /boot/vmlinuz ... ro init=/bin/bash
   # OR
   linux /boot/vmlinuz ... ro systemd.unit=rescue.target

Reset Root Password
-------------------

.. code-block:: bash

   # At GRUB menu, press 'e'
   # Find line starting with 'linux'
   # Append: rw init=/bin/bash
   linux /boot/vmlinuz... ro quiet splash rw init=/bin/bash
   
   # Press Ctrl+X to boot
   # You'll get root shell
   
   # Remount root as read-write (if needed)
   mount -o remount,rw /
   
   # Change password
   passwd root
   
   # Reboot
   exec /sbin/init

🔬 Advanced Scripting
======================

Variables
---------

.. code-block:: grub

   # Set variables
   set timeout=10
   set default=0
   set root=(hd0,gpt2)
   
   # Use variables
   echo $root
   linux /boot/vmlinuz root=$root
   
   # Environment variables
   set prefix=(hd0,gpt2)/boot/grub
   load_env
   save_env saved_entry

Conditionals
------------

.. code-block:: grub

   # If statement
   if [ "$grub_platform" = "efi" ]; then
       echo "Running on UEFI"
       insmod efi_gop
   else
       echo "Running on BIOS"
       insmod vbe
   fi
   
   # Test file existence
   if [ -e (hd0,gpt2)/boot/vmlinuz ]; then
       echo "Kernel found"
   fi
   
   # Test conditions
   if [ "$option" = "recovery" -o "$option" = "rescue" ]; then
       echo "Recovery mode"
   fi

Loops
-----

.. code-block:: grub

   # For loop over list
   for file in /boot/vmlinuz-*; do
       echo "Found kernel: $file"
   done
   
   # While loop (limited use)
   set counter=0
   while [ $counter -lt 5 ]; do
       echo "Count: $counter"
       set counter=$((counter + 1))
   done

Functions
---------

.. code-block:: grub

   # Define function
   function boot_linux {
       linux $1 root=$2
       initrd $3
       boot
   }
   
   # Call function
   menuentry 'Ubuntu' {
       boot_linux /boot/vmlinuz /dev/sda2 /boot/initrd.img
   }

Auto-detect Kernels
-------------------

.. code-block:: grub

   # In /etc/grub.d/40_custom
   for kernel in /boot/vmlinuz-*; do
       version="${kernel#/boot/vmlinuz-}"
       
       menuentry "Linux $version" {
           linux $kernel root=UUID=xxx ro
           initrd /boot/initrd.img-$version
       }
   done

📊 Multi-Boot Scenarios
=========================

Linux + Windows Dual Boot
--------------------------

.. code-block:: grub

   menuentry 'Ubuntu 22.04' {
       set root='hd0,gpt2'
       linux /boot/vmlinuz root=/dev/sda2 ro quiet splash
       initrd /boot/initrd.img
   }
   
   menuentry 'Windows 10' {
       insmod part_gpt
       insmod fat
       insmod chain
       set root='hd0,gpt1'
       chainloader /EFI/Microsoft/Boot/bootmgfw.efi
   }

Multiple Linux Distributions
-----------------------------

.. code-block:: grub

   submenu 'Ubuntu 22.04' {
       menuentry 'Ubuntu - Kernel 5.15' {
           set root='hd0,gpt2'
           linux /boot/vmlinuz-5.15.0 root=/dev/sda2 ro
           initrd /boot/initrd.img-5.15.0
       }
   }
   
   submenu 'Fedora 37' {
       menuentry 'Fedora - Kernel 6.0' {
           set root='hd0,gpt4'
           linux /boot/vmlinuz-6.0.0 root=/dev/sda4 ro
           initrd /boot/initrd.img-6.0.0
       }
   }

Chainload GRUB from Another Partition
--------------------------------------

.. code-block:: grub

   menuentry 'Other Linux Installation' {
       set root='hd0,gpt4'
       configfile (hd0,gpt4)/boot/grub/grub.cfg
   }

🐛 Troubleshooting
===================

Common Issues
-------------

+------------------------------+--------------------------------------------------+
| **Issue**                    | **Solution**                                     |
+==============================+==================================================+
| GRUB not showing             | Press Shift/Esc during boot, reinstall GRUB      |
+------------------------------+--------------------------------------------------+
| grub rescue> prompt          | Manual boot, then reinstall GRUB                 |
+------------------------------+--------------------------------------------------+
| Kernel panic                 | Check root= parameter, initrd path               |
+------------------------------+--------------------------------------------------+
| Windows won't boot           | Run `bcdedit /set {bootmgr} path ...` in Windows|
+------------------------------+--------------------------------------------------+
| Changes not taking effect    | Run update-grub after editing /etc/default/grub  |
+------------------------------+--------------------------------------------------+
| Slow boot                    | Disable os-prober, reduce timeout                |
+------------------------------+--------------------------------------------------+

Debug Mode
----------

.. code-block:: bash

   # Enable debug output in /etc/default/grub
   GRUB_CMDLINE_LINUX_DEFAULT="debug"
   
   # Or add to kernel line:
   linux /boot/vmlinuz ... debug ignore_loglevel

Verbose Boot
------------

.. code-block:: bash

   # Remove 'quiet splash' from kernel parameters
   GRUB_CMDLINE_LINUX_DEFAULT=""
   
   # Show detailed messages
   GRUB_CMDLINE_LINUX_DEFAULT="verbose"

💡 Tips & Tricks
=================

Set Default Boot Entry
----------------------

.. code-block:: bash

   # By number (0-indexed)
   sudo grub-set-default 0
   
   # Or in /etc/default/grub
   GRUB_DEFAULT=0
   GRUB_DEFAULT=saved    # Remember last selection
   
   # Save last choice
   sudo grub-reboot 2    # Boot entry 2 once, then revert to default

Hide GRUB Menu
--------------

.. code-block:: bash

   # In /etc/default/grub
   GRUB_TIMEOUT=0
   GRUB_TIMEOUT_STYLE=hidden
   GRUB_RECORDFAIL_TIMEOUT=0
   
   # Hold Shift during boot to show menu

Faster Boot
-----------

.. code-block:: bash

   GRUB_TIMEOUT=1
   GRUB_DISABLE_OS_PROBER=true
   GRUB_RECORDFAIL_TIMEOUT=1

Serial Console
--------------

.. code-block:: bash

   # In /etc/default/grub
   GRUB_TERMINAL="serial console"
   GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
   GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8"

Kernel Parameters
-----------------

.. code-block:: bash

   # Common parameters in GRUB_CMDLINE_LINUX:
   
   nomodeset              # Disable kernel mode setting
   acpi=off               # Disable ACPI
   noapic                 # Disable APIC
   i915.modeset=0         # Disable Intel graphics modesetting
   nouveau.modeset=0      # Disable Nouveau modesetting
   systemd.unit=multi-user.target  # Boot to text mode
   mem=4G                 # Limit RAM usage
   maxcpus=2              # Limit CPU cores
   elevator=deadline      # I/O scheduler

📚 References
==============

Documentation
-------------

* **Official Manual**: https://www.gnu.org/software/grub/manual/
* **Source Code**: https://git.savannah.gnu.org/git/grub.git
* **Wiki**: https://help.ubuntu.com/community/Grub2
* **Arch Linux Wiki**: https://wiki.archlinux.org/title/GRUB

Key Concepts
------------

* **core.img**: GRUB core image with essential modules
* **prefix**: Path to GRUB modules and config
* **root**: Device containing boot files
* **recordfail**: Failure recovery mechanism
* **os-prober**: Tool to detect other OS installations

Useful Commands
---------------

.. code-block:: bash

   # List GRUB modules
   ls /usr/lib/grub/i386-pc/
   ls /usr/lib/grub/x86_64-efi/
   
   # Check GRUB version
   grub-install --version
   
   # Test configuration syntax
   grub-script-check /boot/grub/grub.cfg
   
   # Backup GRUB config
   sudo cp /boot/grub/grub.cfg /boot/grub/grub.cfg.backup

================================
Last Updated: January 2026
Version: 3.0
================================
