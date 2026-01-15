🔐 **CRYPTOGRAPHY FOR EMBEDDED SYSTEMS**
═══════════════════════════════════════════════════════════════════════

**Practical Cryptographic Implementation for Resource-Constrained Devices**  
**Purpose:** Algorithm selection 🎯 | Performance optimization ⚡ | Side-channel mitigation 🛡️  
**Standards:** NIST FIPS, IETF RFCs, ISO/IEC 18031, MISRA C

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Embedded cryptography** balances **security**, **performance**, and **resource constraints** (RAM, flash, CPU, power).

**Key principles:**
- **Symmetric > Asymmetric** (1000× faster for encryption)
- **ECC > RSA** (10× smaller keys for same security)
- **Hardware acceleration** when available (AES-NI, crypto coprocessors)
- **Constant-time implementations** (prevent side-channel attacks)

**Common mistakes:** Using ECB mode, weak random number generators, timing vulnerabilities.

════════════════════════════════════════════════════════════════════════════

🎯 **ALGORITHM SELECTION GUIDE**
─────────────────────────────────────────────────────────────────────────

**Symmetric Encryption:**

| Algorithm | Key Size | Speed | Security Level | Use Case |
|:----------|:---------|:------|:---------------|:---------|
| **AES-128-GCM** | 128-bit | Fast (HW accel) | 128-bit | General purpose, automotive |
| **AES-256-GCM** | 256-bit | Fast (HW accel) | 256-bit | High security, aerospace (SAL 3) |
| **ChaCha20-Poly1305** | 256-bit | Fast (SW) | 256-bit | No AES-NI hardware |
| ~~AES-ECB~~ | N/A | Fast | **INSECURE** | Never use (no IV, patterns leak) |
| ~~3DES~~ | 168-bit | Slow | Deprecated | Legacy only (NIST deprecated 2023) |

**Recommendation:** **AES-256-GCM** (authenticated encryption, prevents tampering)

**Asymmetric (Public-Key):**

| Algorithm | Key Size | Signature Size | Speed | Use Case |
|:----------|:---------|:---------------|:------|:---------|
| **ECDSA-P256** | 256-bit | 64 bytes | Fast | Automotive (V2X, ISO 21434) |
| **ECDSA-P384** | 384-bit | 96 bytes | Medium | Aerospace (DO-326A SAL 3) |
| **Ed25519** | 256-bit | 64 bytes | Fastest | Modern embedded (small footprint) |
| RSA-2048 | 2048-bit | 256 bytes | Slow | Legacy (DO-178C, older avionics) |
| RSA-4096 | 4096-bit | 512 bytes | Very slow | Long-term security (20+ years) |

**Recommendation:** **ECDSA-P384** for critical systems, **Ed25519** for modern designs

**Hash Functions:**

| Algorithm | Output Size | Speed | Security | Use Case |
|:----------|:------------|:------|:---------|:---------|
| **SHA-256** | 256-bit | Fast (HW) | 128-bit | General purpose |
| **SHA-384** | 384-bit | Medium | 192-bit | DO-326A compliance |
| **SHA-512** | 512-bit | Medium | 256-bit | Long-term integrity |
| **BLAKE2b** | Variable | Fastest | 256-bit | Embedded (no HW accel) |
| ~~SHA-1~~ | 160-bit | Fast | **BROKEN** | Never use (collision attacks) |
| ~~MD5~~ | 128-bit | Fast | **BROKEN** | Never use (trivial collisions) |

**Recommendation:** **SHA-256** (default), **SHA-384** for aerospace

**Message Authentication (MAC):**

| Algorithm | Tag Size | Speed | Use Case |
|:----------|:---------|:------|:---------|
| **HMAC-SHA256** | 256-bit | Fast | ACARS, ARINC 664, general |
| **HMAC-SHA384** | 384-bit | Medium | Aerospace (SAL 3) |
| **Poly1305** | 128-bit | Fastest | With ChaCha20 (TLS 1.3) |
| **AES-CMAC** | 128-bit | Fast (HW) | Automotive (AES-based) |

**Recommendation:** **HMAC-SHA256** (widely supported, battle-tested)

════════════════════════════════════════════════════════════════════════════

⚡ **PERFORMANCE CONSIDERATIONS**
─────────────────────────────────────────────────────────────────────────

**CPU Cycles (ARM Cortex-M4 @ 168 MHz, no HW crypto):**

| Operation | Cycles | Time (ms) | Notes |
|:----------|:-------|:----------|:------|
| **AES-128 encrypt (16 bytes)** | ~5,000 | 0.03 | Software implementation |
| **SHA-256 (1 KB)** | ~80,000 | 0.48 | Software implementation |
| **ECDSA-P256 sign** | ~2.5M | 15 | Expensive! Use sparingly |
| **ECDSA-P256 verify** | ~3.5M | 21 | Even more expensive |
| **RSA-2048 sign** | ~15M | 89 | Avoid on Cortex-M |
| **RSA-2048 verify** | ~500K | 3 | Faster (small exponent) |

**With Hardware Acceleration (STM32H7 with AES/SHA):**

| Operation | Time (HW) | Speedup |
|:----------|:----------|:--------|
| **AES-128-GCM (1 KB)** | 0.01 ms | 100× |
| **SHA-256 (1 KB)** | 0.005 ms | 96× |

**Key Takeaway:** Use hardware acceleration when available!

**Memory Requirements (Flash + RAM):**

| Library | Flash (KB) | RAM (KB) | Features |
|:--------|:-----------|:---------|:---------|
| **mbedTLS** | 50-150 | 20-50 | Full TLS stack, modular |
| **wolfSSL** | 30-100 | 10-30 | Embedded-optimized |
| **BearSSL** | 20-50 | 5-15 | Minimal footprint |
| **TinyCrypt** | 5-10 | 1-2 | Crypto only (no TLS) |

**Recommendation:** TinyCrypt for MCUs <64 KB flash, mbedTLS for ≥128 KB

════════════════════════════════════════════════════════════════════════════

🔧 **IMPLEMENTATION EXAMPLES**
─────────────────────────────────────────────────────────────────────────

**AES-256-GCM Authenticated Encryption:**

.. code-block:: c

   #include <mbedtls/gcm.h>
   
   // Encrypt and authenticate data with AES-256-GCM
   bool encrypt_gcm(const uint8_t *plaintext, size_t pt_len,
                    const uint8_t *key,       // 32 bytes (AES-256)
                    const uint8_t *iv,        // 12 bytes (nonce)
                    const uint8_t *aad, size_t aad_len,  // Additional auth data
                    uint8_t *ciphertext,
                    uint8_t *tag) {           // 16 bytes (auth tag)
       mbedtls_gcm_context ctx;
       mbedtls_gcm_init(&ctx);
       
       // Set AES-256 key
       int ret = mbedtls_gcm_setkey(&ctx, MBEDTLS_CIPHER_ID_AES, key, 256);
       if (ret != 0) {
           return false;
       }
       
       // Encrypt and authenticate
       ret = mbedtls_gcm_crypt_and_tag(
           &ctx,
           MBEDTLS_GCM_ENCRYPT,
           pt_len,
           iv, 12,              // Nonce (MUST be unique per message)
           aad, aad_len,        // Authenticated but not encrypted
           plaintext,
           ciphertext,
           16, tag              // 128-bit authentication tag
       );
       
       mbedtls_gcm_free(&ctx);
       return (ret == 0);
   }
   
   // Decrypt and verify authentication tag
   bool decrypt_gcm(const uint8_t *ciphertext, size_t ct_len,
                    const uint8_t *key,
                    const uint8_t *iv,
                    const uint8_t *aad, size_t aad_len,
                    const uint8_t *tag,
                    uint8_t *plaintext) {
       mbedtls_gcm_context ctx;
       mbedtls_gcm_init(&ctx);
       mbedtls_gcm_setkey(&ctx, MBEDTLS_CIPHER_ID_AES, key, 256);
       
       // Decrypt and verify tag
       int ret = mbedtls_gcm_auth_decrypt(
           &ctx,
           ct_len,
           iv, 12,
           aad, aad_len,
           tag, 16,
           ciphertext,
           plaintext
       );
       
       mbedtls_gcm_free(&ctx);
       
       if (ret != 0) {
           // Authentication failed! Data tampered or wrong key
           memset(plaintext, 0, ct_len);  // Clear output
           return false;
       }
       
       return true;
   }

**ECDSA-P256 Signature (Automotive V2X):**

.. code-block:: c

   #include <mbedtls/ecdsa.h>
   #include <mbedtls/sha256.h>
   
   // Sign message with ECDSA-P256 (constant-time)
   bool sign_ecdsa_p256(const uint8_t *message, size_t msg_len,
                        const uint8_t *priv_key,  // 32 bytes
                        uint8_t *signature) {     // 64 bytes (r, s)
       mbedtls_ecdsa_context ctx;
       mbedtls_ecdsa_init(&ctx);
       
       // Load NIST P-256 curve
       mbedtls_ecp_group_load(&ctx.grp, MBEDTLS_ECP_DP_SECP256R1);
       
       // Load private key
       mbedtls_mpi_read_binary(&ctx.d, priv_key, 32);
       
       // Calculate SHA-256 hash
       uint8_t hash[32];
       mbedtls_sha256(message, msg_len, hash, 0);
       
       // Sign hash (deterministic nonce per RFC 6979)
       mbedtls_mpi r, s;
       mbedtls_mpi_init(&r);
       mbedtls_mpi_init(&s);
       
       int ret = mbedtls_ecdsa_sign_det(
           &ctx.grp,
           &r, &s,
           &ctx.d,
           hash, 32,
           MBEDTLS_MD_SHA256
       );
       
       if (ret == 0) {
           // Encode signature (r, s)
           mbedtls_mpi_write_binary(&r, signature, 32);
           mbedtls_mpi_write_binary(&s, signature + 32, 32);
       }
       
       mbedtls_mpi_free(&r);
       mbedtls_mpi_free(&s);
       mbedtls_ecdsa_free(&ctx);
       
       return (ret == 0);
   }
   
   // Verify ECDSA-P256 signature
   bool verify_ecdsa_p256(const uint8_t *message, size_t msg_len,
                          const uint8_t *pub_key_x,  // 32 bytes
                          const uint8_t *pub_key_y,  // 32 bytes
                          const uint8_t *signature) {
       mbedtls_ecdsa_context ctx;
       mbedtls_ecdsa_init(&ctx);
       mbedtls_ecp_group_load(&ctx.grp, MBEDTLS_ECP_DP_SECP256R1);
       
       // Load public key point (x, y)
       mbedtls_mpi_read_binary(&ctx.Q.X, pub_key_x, 32);
       mbedtls_mpi_read_binary(&ctx.Q.Y, pub_key_y, 32);
       mbedtls_mpi_lset(&ctx.Q.Z, 1);  // Affine coordinates
       
       // Calculate hash
       uint8_t hash[32];
       mbedtls_sha256(message, msg_len, hash, 0);
       
       // Load signature (r, s)
       mbedtls_mpi r, s;
       mbedtls_mpi_init(&r);
       mbedtls_mpi_init(&s);
       mbedtls_mpi_read_binary(&r, signature, 32);
       mbedtls_mpi_read_binary(&s, signature + 32, 32);
       
       // Verify signature
       int ret = mbedtls_ecdsa_verify(&ctx.grp, hash, 32, &ctx.Q, &r, &s);
       
       mbedtls_mpi_free(&r);
       mbedtls_mpi_free(&s);
       mbedtls_ecdsa_free(&ctx);
       
       return (ret == 0);  // 0 = valid signature
   }

**Secure Random Number Generation:**

.. code-block:: c

   #include <mbedtls/entropy.h>
   #include <mbedtls/ctr_drbg.h>
   
   // Initialize PRNG with hardware entropy
   mbedtls_entropy_context entropy;
   mbedtls_ctr_drbg_context ctr_drbg;
   
   void init_rng(void) {
       mbedtls_entropy_init(&entropy);
       mbedtls_ctr_drbg_init(&ctr_drbg);
       
       // Seed with personalization string
       const char *pers = "Automotive-ECU-12345";
       mbedtls_ctr_drbg_seed(
           &ctr_drbg,
           mbedtls_entropy_func,
           &entropy,
           (uint8_t *)pers, strlen(pers)
       );
   }
   
   // Generate cryptographically secure random bytes
   bool generate_random(uint8_t *output, size_t len) {
       int ret = mbedtls_ctr_drbg_random(&ctr_drbg, output, len);
       return (ret == 0);
   }
   
   // Example: Generate AES-256 key
   void generate_aes_key(uint8_t key[32]) {
       generate_random(key, 32);
   }

════════════════════════════════════════════════════════════════════════════

🛡️ **SIDE-CHANNEL ATTACK MITIGATIONS**
─────────────────────────────────────────────────────────────────────────

**Timing Attack Prevention:**

.. code-block:: c

   // INSECURE: Timing-variable string comparison
   bool insecure_compare(const uint8_t *a, const uint8_t *b, size_t len) {
       for (size_t i = 0; i < len; i++) {
           if (a[i] != b[i]) {
               return false;  // Early return leaks position of mismatch!
           }
       }
       return true;
   }
   
   // SECURE: Constant-time comparison
   bool secure_compare(const uint8_t *a, const uint8_t *b, size_t len) {
       volatile uint8_t diff = 0;
       
       for (size_t i = 0; i < len; i++) {
           diff |= (a[i] ^ b[i]);  // Always compares all bytes
       }
       
       return (diff == 0);  // No early return
   }
   
   // Example: Verify HMAC (constant-time)
   bool verify_hmac(const uint8_t *received_hmac,
                    const uint8_t *calculated_hmac) {
       return secure_compare(received_hmac, calculated_hmac, 32);
   }

**Power Analysis Resistance:**

.. code-block:: c

   // Constant-time conditional move (no branches)
   void cmov_u32(uint32_t *dest, uint32_t src, uint32_t condition) {
       // condition must be 0 or 1
       uint32_t mask = -(condition);  // 0x00000000 or 0xFFFFFFFF
       *dest ^= ((*dest ^ src) & mask);
   }
   
   // Constant-time table lookup (for AES S-box)
   uint8_t ct_lookup(const uint8_t *table, uint8_t index) {
       uint8_t result = 0;
       
       // Touch every table entry (constant memory access pattern)
       for (int i = 0; i < 256; i++) {
           uint8_t mask = -(i == index);  // 0x00 or 0xFF
           result |= (table[i] & mask);
       }
       
       return result;
   }

**Cache Timing Resistance:**

.. code-block:: c

   // Flush cache line (ARM)
   static inline void flush_cache_line(void *addr) {
       __asm__ volatile("dc civac, %0" : : "r"(addr) : "memory");
   }
   
   // Preload crypto tables into cache
   void preload_aes_tables(void) {
       volatile uint32_t dummy = 0;
       
       for (int i = 0; i < AES_TABLE_SIZE; i += CACHE_LINE_SIZE) {
           dummy += aes_sbox[i];  // Force cache load
       }
   }

════════════════════════════════════════════════════════════════════════════

🔑 **KEY MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**Key Derivation Function (KDF):**

.. code-block:: c

   #include <mbedtls/hkdf.h>
   
   // Derive multiple keys from master key (HKDF-SHA256)
   bool derive_keys(const uint8_t *master_key,  // 32 bytes
                    uint8_t *enc_key,            // 32 bytes (AES-256)
                    uint8_t *mac_key,            // 32 bytes (HMAC-SHA256)
                    uint8_t *iv_key) {           // 16 bytes (GCM nonce)
       const mbedtls_md_info_t *md = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
       
       // Salt (can be public)
       const uint8_t salt[] = "Automotive-ECU-KDF-v1";
       
       // Info strings (domain separation)
       const uint8_t info_enc[] = "encryption-key";
       const uint8_t info_mac[] = "mac-key";
       const uint8_t info_iv[] = "iv-key";
       
       // Derive encryption key
       int ret = mbedtls_hkdf(md,
                              salt, sizeof(salt) - 1,
                              master_key, 32,
                              info_enc, sizeof(info_enc) - 1,
                              enc_key, 32);
       if (ret != 0) return false;
       
       // Derive MAC key
       ret = mbedtls_hkdf(md,
                          salt, sizeof(salt) - 1,
                          master_key, 32,
                          info_mac, sizeof(info_mac) - 1,
                          mac_key, 32);
       if (ret != 0) return false;
       
       // Derive IV key
       ret = mbedtls_hkdf(md,
                          salt, sizeof(salt) - 1,
                          master_key, 32,
                          info_iv, sizeof(info_iv) - 1,
                          iv_key, 16);
       
       return (ret == 0);
   }

**Key Storage in Flash:**

.. code-block:: c

   // Encrypted key storage structure
   typedef struct {
       uint8_t encrypted_key[48];  // AES-GCM encrypted (32 + 16 tag)
       uint8_t iv[12];             // GCM nonce
       uint8_t kek_id[8];          // Key Encryption Key ID
       uint32_t crc32;             // Integrity check
   } SecureKeyBlob;
   
   // Store key encrypted with KEK
   bool store_key_encrypted(const uint8_t *key, uint32_t key_id) {
       SecureKeyBlob blob;
       
       // Get Key Encryption Key (from HSM or secure storage)
       uint8_t kek[32];
       get_kek(kek, sizeof(kek));
       
       // Generate random IV
       generate_random(blob.iv, 12);
       
       // Encrypt key with KEK
       uint8_t tag[16];
       encrypt_gcm(key, 32, kek, blob.iv, NULL, 0, blob.encrypted_key, tag);
       memcpy(blob.encrypted_key + 32, tag, 16);
       
       // Calculate CRC
       blob.crc32 = calculate_crc32(&blob, sizeof(blob) - 4);
       
       // Write to flash
       flash_write(KEYSTORE_BASE + key_id * sizeof(SecureKeyBlob), &blob, sizeof(blob));
       
       // Secure cleanup
       memset(kek, 0, 32);
       return true;
   }

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why use ECDSA-P256 instead of RSA-2048 in embedded systems?**

**A1:**

| Metric | ECDSA-P256 | RSA-2048 | Advantage |
|:-------|:-----------|:---------|:----------|
| **Security level** | 128-bit | 112-bit | ECDSA (stronger) |
| **Key size** | 32 bytes | 256 bytes | ECDSA (8× smaller) |
| **Signature size** | 64 bytes | 256 bytes | ECDSA (4× smaller) |
| **Sign time** | 15 ms | 89 ms | ECDSA (6× faster) |
| **Verify time** | 21 ms | 3 ms | RSA (7× faster) |
| **Flash usage** | ~20 KB | ~50 KB | ECDSA (smaller code) |

**Use ECDSA when:**
- Limited flash/RAM (automotive ECUs, IoT)
- Signature size matters (V2X, constrained protocols)
- Sign performance critical (frequent signatures)

**Use RSA when:**
- Legacy compatibility (older avionics)
- Verify performance critical (many verifications, few signatures)
- Quantum resistance required (larger keys: RSA-4096+)

**Q2: What is the danger of using AES-ECB mode?**

**A2:**
**ECB (Electronic Codebook) Mode:**
- Each 16-byte block encrypted independently
- Same plaintext block → same ciphertext block
- **Patterns leak** (e.g., image encryption shows original outline)

**Example vulnerability:**
```
Plaintext:  "AAAA BBBB AAAA CCCC"
Ciphertext: "XXXX YYYY XXXX ZZZZ"
                ↑         ↑
         Same ciphertext reveals repeated plaintext!
```

**Attack:** Attacker can detect repeated messages, reorder blocks, replay blocks.

**Solution:** Use **GCM mode** (combines encryption + authentication, uses IV to randomize output).

**Q3: How does constant-time comparison prevent timing attacks?**

**A3:**
**Vulnerable code:**
```c
if (a[0] != b[0]) return false;  // Returns immediately on mismatch
if (a[1] != b[1]) return false;  // Timing reveals position of first difference
```

**Timing leak:** Attacker measures response time to guess HMAC byte-by-byte.

**Constant-time solution:**
```c
diff = 0;
for (i = 0; i < len; i++) {
    diff |= (a[i] ^ b[i]);  // Always processes all bytes
}
return (diff == 0);
```

**Key principle:** Execution time independent of secret data (no branches based on secrets).

**Q4: Why is hardware RNG entropy critical for embedded security?**

**A4:**
**Bad RNG = System compromised:**

**Example failure (2012 Android Bitcoin wallet):**
- Used weak PRNG (predictable seed)
- Generated predictable ECDSA nonces
- Attackers recovered private keys from signatures
- $5.2M stolen

**Requirements for secure RNG:**
1. **Hardware entropy source** (thermal noise, jitter)
2. **Whitening** (hash or CTR-DRBG to remove bias)
3. **Continuous health tests** (detect RNG failure)
4. **Reseeding** (mix in fresh entropy periodically)

**FIPS 140-2 requires:** 256 bits of entropy for 128-bit security keys.

**Q5: What is HKDF and why use it instead of simple hashing for key derivation?**

**A5:**
**HKDF (HMAC-based Key Derivation Function, RFC 5869):**

**Problem with naive approach:**
```c
// WRONG: Direct hash of master key
enc_key = SHA256(master_key || "encryption");
mac_key = SHA256(master_key || "mac");
// Potential weaknesses: no salt, no domain separation
```

**HKDF benefits:**
1. **Extract** phase: Mix master key with salt (whitening)
2. **Expand** phase: Generate multiple keys with domain separation
3. **Provable security** (based on HMAC assumptions)

**Usage:**
```c
hkdf_extract(master_key, salt) → PRK (pseudorandom key)
hkdf_expand(PRK, "enc-key") → enc_key
hkdf_expand(PRK, "mac-key") → mac_key
```

**Result:** Each derived key cryptographically independent (compromise of one doesn't affect others).

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~900
