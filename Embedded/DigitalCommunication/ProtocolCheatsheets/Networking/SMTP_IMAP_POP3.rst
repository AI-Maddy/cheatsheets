====================
SMTP / IMAP / POP3
====================

.. note::
   This is a cheatsheet for SMTP, IMAP, and POP3 protocols.

**SMTP**
- Simple Mail Transfer Protocol
- Email sending, TCP port 25/587/465
- Pushes mail to server

**IMAP**
- Internet Message Access Protocol
- Email retrieval, TCP port 143/993
- Server-side storage, sync

**POP3**
- Post Office Protocol v3
- Email retrieval, TCP port 110/995
- Downloads and deletes from server

**Key Features**
- SMTP: sending only
- IMAP: sync, folders, multiple devices
- POP3: simple, offline access

**Mnemonic**: "Send Mail, Access, or Pop!"

**Common Use Cases**
- Email clients, servers, cloud mail

**Pros**
- Universal, open standards

**Cons**
- SMTP: no encryption by default
- POP3: no sync, limited features

**Icon**: ✉️

**Reference**: https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol | https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol | https://en.wikipedia.org/wiki/Post_Office_Protocol