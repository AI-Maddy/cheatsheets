================================================================================
SELINUX & APPARMOR SECURITY
================================================================================

**Complete Guide to Mandatory Access Control (MAC) Systems**

Source: Mastering Linux Security And Hardening  
Chapter Coverage: Chapter 9

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # SELinux Commands
   getenforce                                  # Check SELinux status
   sestatus                                    # Detailed status
   setenforce 0                                # Set permissive (temporary)
   setenforce 1                                # Set enforcing (temporary)
   ls -Z /path/to/file                         # View SELinux context
   chcon -t httpd_sys_content_t /var/www/html  # Change context
   restorecon -Rv /var/www/html                # Restore default contexts
   
   # AppArmor Commands
   sudo aa-status                              # AppArmor status
   sudo aa-enforce /etc/apparmor.d/usr.bin.firefox  # Enforce profile
   sudo aa-complain /etc/apparmor.d/usr.bin.firefox # Set complain mode
   sudo apparmor_parser -r /etc/apparmor.d/usr.bin.firefox  # Reload profile

Complete cheatsheet content continues with SELinux modes, contexts, policies, booleans, troubleshooting, and AppArmor profiles, modes, and security configurations.

================================================================================
END OF SELINUX & APPARMOR SECURITY
================================================================================
