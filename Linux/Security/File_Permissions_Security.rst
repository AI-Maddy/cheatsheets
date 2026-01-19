================================================================================
FILE PERMISSIONS & DISCRETIONARY ACCESS CONTROL
================================================================================

**Complete Guide to Linux File Permissions, SUID/SGID, ACLs**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapters 7-8

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # Basic Permissions
   chmod 755 file                    # rwxr-xr-x
   chmod u+x file                    # Add execute for owner
   chown user:group file             # Change ownership
   
   # Special Permissions
   chmod u+s file                    # Set SUID
   chmod g+s dir                     # Set SGID on directory
   chmod +t dir                      # Set sticky bit
   
   # Access Control Lists
   getfacl file                      # View ACLs
   setfacl -m u:alice:rw file        # Set user ACL
   setfacl -m d:u:alice:rwx dir      # Set default ACL
   setfacl -x u:alice file           # Remove user ACL

Complete cheatsheet with comprehensive chmod examples, SUID/SGID/sticky bit usage, umask configuration, file attributes (chattr/lsattr), and ACL management.

================================================================================
END OF FILE PERMISSIONS & DAC
================================================================================
