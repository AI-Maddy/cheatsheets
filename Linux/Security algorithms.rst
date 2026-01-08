=====================================
Linux Security Algorithms Cheatsheet
=====================================

**2026 Guide**: Comprehensive coverage of cryptographic algorithms, security protocols, and implementation best practices for Linux systems, embedded devices, and production environments.

.. contents:: Table of Contents
   :depth: 3

---

**Keywords Overview**: AES, ChaCha20, RSA, ECC, Ed25519, X25519, SHA-256, SHA-3, BLAKE3, Argon2, bcrypt, scrypt, PBKDF2, TLS 1.3, post-quantum cryptography (PQC), key derivation functions (KDF), digital signatures, elliptic curves, lattice-based cryptography, stream ciphers, block ciphers, AEAD, authenticated encryption, cryptographic primitives.

---

Symmetric Encryption (Symmetric-Key Cryptography)
==================================================

Overview
--------

Symmetric encryption uses the same key for both encryption and decryption. Modern systems require:
- **Authenticated Encryption with Associated Data (AEAD)**: Provides both confidentiality and authenticity
- **Block cipher mode**: GCM, ChaCha20-Poly1305, or CCM
- **Avoid**: CBC, ECB, Stream ciphers without authentication

Detailed Algorithm Comparison
------------------------------

+---------------+------------+---------+----------------+------------------------+------------------+
| Algorithm     | Key Size   | Status  | Speed (1 GHz)  | NEON/AVX2 Support      | Recommendation   |
+===============+============+=========+================+========================+==================+
| AES-256-GCM   | 256 bits   | **BEST**| ~3-5 Gbps      | ✓ (AES-NI accelerated) | Primary choice   |
+---------------+------------+---------+----------------+------------------------+------------------+
| ChaCha20-     | 256 bits   | **BEST**| ~6 Gbps        | ✓ (AVX2/NEON)         | Mobile/low-power |
| Poly1305      |            |         |                |                        |                  |
+---------------+------------+---------+----------------+------------------------+------------------+
| AES-256-CCM   | 256 bits   | Good   | ~3 Gbps        | ✓ (AES-NI)             | IoT/constrained  |
+---------------+------------+---------+----------------+------------------------+------------------+
| Camellia-256  | 256 bits   | Legacy  | ~2 Gbps        | Limited                | Avoid new code   |
+---------------+------------+---------+----------------+------------------------+------------------+
| ARIA-256      | 256 bits   | Legacy  | ~1.5 Gbps      | Limited                | Regional only    |
+---------------+------------+---------+----------------+------------------------+------------------+
| **3DES/TDEA** | 168 eff.   | **BROKEN** | ~0.05 Gbps   | ❌                     | **FORBIDDEN**    |
+---------------+------------+---------+----------------+------------------------+------------------+
| **DES**       | 56 bits    | **BROKEN** | ~0.02 Gbps   | ❌                     | **FORBIDDEN**    |
+---------------+------------+---------+----------------+------------------------+------------------+

AES-256-GCM (Galois/Counter Mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Overview**: Industry-standard AEAD cipher combining AES with GCM mode.

**Security**: 256-bit keys resistant to quantum (256-bit → ~128-bit post-quantum)

**Parameters & Implementation**:

.. code-block:: c

    #include <openssl/evp.h>
    #include <openssl/rand.h>
    #include <string.h>

    // AES-256-GCM encryption
    int aes_256_gcm_encrypt(unsigned char *plaintext, int plaintext_len,
                            unsigned char *aad, int aad_len,
                            unsigned char *key,      // 32 bytes (256 bits)
                            unsigned char *iv,       // 12 bytes (96 bits) recommended
                            unsigned char *ciphertext,
                            unsigned char *tag) {    // 16 bytes (128 bits)
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        int len = 0, ciphertext_len = 0;

        // Initialize context
        EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv);

        // Add Additional Authenticated Data (AAD) if present
        if (aad_len > 0) {
            EVP_EncryptUpdate(ctx, NULL, &len, aad, aad_len);
        }

        // Encrypt plaintext
        EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
        ciphertext_len = len;

        // Finalize encryption
        EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
        ciphertext_len += len;

        // Extract authentication tag (must be 16 bytes)
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);

        EVP_CIPHER_CTX_free(ctx);
        return ciphertext_len;
    }

**Performance Benchmarks** (OpenSSL 3.0, AES-NI enabled):

- **Encryption Speed**: ~3-5 Gbps on modern CPUs
- **ARM NEON (Cortex-A72)**: ~1.2 Gbps
- **Latency per 1KB**: ~0.2-0.3 μs

**Nonce/IV Management**:

- **Length**: 96 bits (12 bytes) recommended (90% of use cases)
- **Generation**: Cryptographically random, never reused with same key
- **Counter mode**: Can use 64-bit random + 32-bit counter for streaming

**Keywords**: Authenticated encryption, AEAD, GCM mode, counter mode, Galois field multiplication, AES-NI, hardware acceleration.

ChaCha20-Poly1305
~~~~~~~~~~~~~~~~~~

**Overview**: Stream cipher (ChaCha20) + MAC (Poly1305). Excellent for systems without AES-NI.

**Advantages**:
- Faster on older CPUs without AES hardware
- Constant-time implementation (resistant to timing attacks)
- Used in TLS 1.3, WireGuard, Signal Protocol

**Parameters**:

.. code-block:: c

    #include <openssl/evp.h>

    // ChaCha20-Poly1305 encryption
    int chacha20_poly1305_encrypt(unsigned char *plaintext, int plaintext_len,
                                  unsigned char *aad, int aad_len,
                                  unsigned char *key,       // 32 bytes
                                  unsigned char *iv,        // 12 bytes
                                  unsigned char *ciphertext,
                                  unsigned char *tag) {     // 16 bytes
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        int len = 0, ciphertext_len = 0;

        EVP_EncryptInit_ex(ctx, EVP_chacha20_poly1305(), NULL, key, iv);

        if (aad_len > 0) {
            EVP_EncryptUpdate(ctx, NULL, &len, aad, aad_len);
        }

        EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
        ciphertext_len = len;

        EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
        ciphertext_len += len;

        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, 16, tag);

        EVP_CIPHER_CTX_free(ctx);
        return ciphertext_len;
    }

**Performance**:

- **Throughput**: ~6 Gbps (faster than AES on non-NI CPUs)
- **ARM NEON**: ~2.5 Gbps
- **Latency**: ~0.15 μs per 1KB

**When to Use**: Mobile apps, WireGuard/VPN, systems without AES-NI

**Keywords**: Stream cipher, Poly1305 MAC, AEAD construction, constant-time, timing attack resistance.

---

Asymmetric Encryption & Key Encapsulation
===========================================

Overview
--------

Public-key cryptography enables secure communication without pre-shared keys. Modern systems prefer elliptic curves and post-quantum algorithms.

Elliptic Curve Cryptography (ECC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Curves by Security Level**:

+------------------+------------+-------+----+--------+-------------------+
| Curve            | Bits       | Type  | PQ | Speed  | Recommendation    |
+==================+============+=======+====+========+===================+
| **X25519**       | 128 (equiv)| DH    | ❌ | ★★★★★ | **PRIMARY CHOICE**|
+------------------+------------+-------+----+--------+-------------------+
| **Ed25519**      | 128 (equiv)| SIG   | ❌ | ★★★★★ | **SIGNATURE BEST**|
+------------------+------------+-------+----+--------+-------------------+
| NIST P-256       | 256        | DH    | ❌ | ★★★☆☆ | Legacy/cert chains|
+------------------+------------+-------+----+--------+-------------------+
| P-384            | 384        | DH    | ❌ | ★★★☆☆ | Higher assurance  |
+------------------+------------+-------+----+--------+-------------------+
| Curve448         | 448        | DH    | ❌ | ★★☆☆☆ | Rare              |
+------------------+------------+-------+----+--------+-------------------+
| **RSA-3072+**    | 3072       | Both  | ❌ | ★☆☆☆☆ | Legacy only       |
+------------------+------------+-------+----+--------+-------------------+

X25519 (Elliptic Curve Diffie-Hellman)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Use Case**: Key exchange for TLS, Signal Protocol, WireGuard

**Implementation**:

.. code-block:: c

    #include <openssl/evp.h>
    #include <string.h>

    // Generate X25519 keypair
    EVP_PKEY *x25519_keygen(void) {
        EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
        EVP_PKEY *pkey = NULL;

        EVP_PKEY_keygen_init(ctx);
        EVP_PKEY_keygen(ctx, &pkey);

        EVP_PKEY_CTX_free(ctx);
        return pkey;  // 32-byte private key
    }

    // Compute shared secret
    int x25519_compute_secret(EVP_PKEY *private_key, EVP_PKEY *peer_public_key,
                              unsigned char *shared_secret) {
        EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new(private_key, NULL);
        size_t outlen = 32;  // X25519 produces 32 bytes

        EVP_PKEY_derive_init(ctx);
        EVP_PKEY_derive_set_peer(ctx, peer_public_key);
        EVP_PKEY_derive(ctx, shared_secret, &outlen);

        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

**Properties**:
- Key size: 32 bytes (256 bits)
- Constant-time (resistant to timing attacks)
- Montgomery ladder implementation
- Compatible with NIST curve security

**Performance**: ~0.3 ms per shared secret computation (Cortex-A72)

**Keywords**: Elliptic curve Diffie-Hellman, key exchange protocol, Montgomery curves, constant-time arithmetic.

Ed25519 (EdDSA - Edwards Curve Digital Signature Algorithm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Use Case**: Digital signatures (SSH, TLS certificates, code signing)

**Implementation**:

.. code-block:: c

    #include <openssl/evp.h>

    // Generate Ed25519 keypair
    EVP_PKEY *ed25519_keygen(void) {
        EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_ED25519, NULL);
        EVP_PKEY *pkey = NULL;

        EVP_PKEY_keygen_init(ctx);
        EVP_PKEY_keygen(ctx, &pkey);

        EVP_PKEY_CTX_free(ctx);
        return pkey;  // 32-byte seed
    }

    // Sign message
    int ed25519_sign(EVP_PKEY *private_key, unsigned char *message, int msg_len,
                     unsigned char *signature) {
        EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
        size_t sig_len = 64;  // Ed25519 signatures are 64 bytes

        EVP_DigestSignInit(mdctx, NULL, NULL, NULL, private_key);
        EVP_DigestSign(mdctx, signature, &sig_len, message, msg_len);

        EVP_MD_CTX_free(mdctx);
        return 0;
    }

    // Verify signature
    int ed25519_verify(EVP_PKEY *public_key, unsigned char *message, int msg_len,
                       unsigned char *signature) {
        EVP_MD_CTX *mdctx = EVP_MD_CTX_new();

        int result = EVP_DigestVerifyInit(mdctx, NULL, NULL, NULL, public_key);
        if (result <= 0) return -1;

        result = EVP_DigestVerify(mdctx, signature, 64, message, msg_len);

        EVP_MD_CTX_free(mdctx);
        return result;  // 1 = valid, 0 = invalid, -1 = error
    }

**Properties**:
- Signature size: 64 bytes
- Fast batch verification (process multiple signatures together)
- Deterministic (no random nonce needed)
- Resistant to side-channel attacks

**Performance**: ~1 ms signature + ~2 ms verification (Cortex-A72)

**Keywords**: EdDSA, Edwards curves, deterministic signatures, batch verification, side-channel resistance.

RSA (Rivest-Shamir-Adleman)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Status (2026)**: Legacy - use only for backward compatibility

**Minimum Key Sizes**:

.. code-block:: text

    2026 Recommendation: RSA-3072 or higher
    Historical: RSA-2048 (now considered weak)
    Deprecated: RSA-1024 and below

**Implementation** (key generation):

.. code-block:: c

    #include <openssl/rsa.h>

    EVP_PKEY *rsa_keygen(int bits) {  // bits = 3072, 4096
        EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
        EVP_PKEY *pkey = NULL;
        BIGNUM *exponent = BN_new();

        EVP_PKEY_keygen_init(ctx);
        BN_set_word(exponent, RSA_F4);  // F4 = 65537 (common exponent)
        EVP_PKEY_CTX_ctrl(ctx, EVP_PKEY_RSA, EVP_PKEY_OP_KEYGEN,
                         EVP_PKEY_CTRL_RSA_KEYGEN_BITS, bits, NULL);
        EVP_PKEY_keygen(ctx, &pkey);

        BN_free(exponent);
        EVP_PKEY_CTX_free(ctx);
        return pkey;
    }

**Performance** (vs ECC):

- RSA-3072 key generation: ~3 seconds
- ECC (P-384) key generation: ~1 ms
- RSA significantly slower than ECC

**Keywords**: Public-key cryptography, RSA-OAEP, RSA-PSS, modular exponentiation, prime factorization.

Post-Quantum Cryptography (PQC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NIST Standardized Algorithms (2024)**:

+------------------+-----------+--------+-------+----------------+-----------+
| Algorithm        | Type      | Bits   | Speed | Key Size       | Status    |
+==================+===========+========+=======+================+===========+
| **ML-KEM-768**   | Lattice   | 192    | Fast  | 1184 bytes pk  | **STD**   |
+------------------+-----------+--------+-------+----------------+-----------+
| **ML-KEM-1024**  | Lattice   | 256    | Fast  | 1568 bytes pk  | **STD**   |
+------------------+-----------+--------+-------+----------------+-----------+
| **ML-DSA-65**    | Lattice   | 192    | Fast  | 2544 bytes sig | **STD**   |
+------------------+-----------+--------+-------+----------------+-----------+
| **SLH-DSA-256**  | Hash-based| 256    | Slow  | 7144 bytes sig | **STD**   |
+------------------+-----------+--------+-------+----------------+-----------+
| Kyber (legacy)   | Lattice   | 256    | Fast  | Old ML-KEM     | Deprecated|
+------------------+-----------+--------+-------+----------------+-----------+
| Dilithium        | Lattice   | 256    | Fast  | Old ML-DSA     | Deprecated|
+------------------+-----------+--------+-------+----------------+-----------+

**Hybrid Approach** (Recommended for 2026+):

.. code-block:: text

    TLS 1.3 Hybrid Key Exchange:
    - X25519 (classical) + ML-KEM-768 (post-quantum)
    - Provides both classical and PQ security
    - No performance penalty (parallel computation)
    
    Digital Signatures (Hybrid):
    - Ed25519 (classical) + ML-DSA-65 (post-quantum)
    - Both signatures included in certificates/messages

**Keywords**: Post-quantum cryptography, lattice-based cryptography, ML-KEM, ML-DSA, hybrid schemes, quantum resistance.

---

Hash Functions (Cryptographic)
==============================

Overview
--------

Hash functions produce fixed-size digests from arbitrary input. Used for:
- Integrity verification
- Digital signatures
- Password hashing (with salt)
- Deduplication fingerprints

**Security Properties**:
1. Preimage resistance: Can't find input from hash
2. Collision resistance: Can't find two inputs with same hash
3. Avalanche effect: Small input change → completely different hash

Detailed Hash Algorithm Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------+-------+--------+---------+---+----------+---------------------+
| Algorithm| Bits  | Speed  | Quantum | PQ| Status   | Best Use            |
+          +-------+--------+---------+---+----------+---------------------+
| **SHA-256** | 256 | ~1 Gbps | 128 bits| ❌| **STANDARD** | General purpose     |
+----------+-------+--------+---------+---+----------+---------------------+
| SHA-512  | 512   | ~1 Gbps | 256 bits| ❌| Good      | High assurance      |
+----------+-------+--------+---------+---+----------+---------------------+
| **SHA-3-256** | 256 | ~0.5 Gbps | 128 bits| ❌| **RECOMMENDED** | Modern systems |
+----------+-------+--------+---------+---+----------+---------------------+
| **BLAKE3** | Variable | **4+ Gbps** | Variable | ❌| **FASTEST**   | Performance-critical |
+----------+-------+--------+---------+---+----------+---------------------+
| BLAKE2b  | 512   | ~2 Gbps | N/A    | ❌| Good      | Before BLAKE3       |
+----------+-------+--------+---------+---+----------+---------------------+
| **SHA-1**  | 160   | ~1 Gbps | Weak   | ❌| **BROKEN** | **AVOID**           |
+----------+-------+--------+---------+---+----------+---------------------+
| **MD5**    | 128   | ~2 Gbps | Weak   | ❌| **BROKEN** | **AVOID**           |
+----------+-------+--------+---------+---+----------+---------------------+

SHA-256 (Secure Hash Algorithm 2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Cases**: TLS certificates, Bitcoin, git commits, general integrity

**Implementation**:

.. code-block:: c

    #include <openssl/sha.h>
    #include <string.h>

    unsigned char *sha256(unsigned char *data, size_t data_len) {
        static unsigned char digest[SHA256_DIGEST_LENGTH];
        SHA256(data, data_len, digest);
        return digest;  // 32 bytes (256 bits)
    }

    // Incremental hashing for large files
    int sha256_file(const char *filename, unsigned char *digest) {
        FILE *fp = fopen(filename, "rb");
        SHA256_CTX ctx;
        unsigned char buffer[65536];
        size_t bytes;

        SHA256_Init(&ctx);
        while ((bytes = fread(buffer, 1, sizeof(buffer), fp)) > 0) {
            SHA256_Update(&ctx, buffer, bytes);
        }
        SHA256_Final(digest, &ctx);

        fclose(fp);
        return 0;
    }

**Properties**:
- Digest: 32 bytes (256 bits)
- Output space: 2^256 ≈ 1.16 × 10^77 possible hashes
- Preimage resistance: ~2^256 operations
- Collision resistance: ~2^128 operations (per birthday paradox)

**Performance Benchmarks** (OpenSSL):

- Small data (<1 KB): ~0.5 μs
- 1 GB file: ~1 second (modern CPU)
- ARM NEON (Cortex-A72): ~0.7 seconds per 1 GB

**Keywords**: Cryptographic hash, SHA-2 family, Merkle-Damgård construction, compression function, avalanche effect.

BLAKE3
~~~~~~

**Overview**: Modern cryptographic hash, significantly faster than SHA-256

**Key Advantages**:
- **Parallelizable**: Up to 256x speedup with SIMD
- **Incremental**: Efficient for streaming
- **Variable output**: Can produce any length digest
- **Cryptanalysis resistant**: Young design but secure

**Implementation**:

.. code-block:: c

    #include <blake3.h>

    unsigned char *blake3_hash(unsigned char *data, size_t data_len) {
        static unsigned char digest[32];
        blake3_hasher hasher;

        blake3_hasher_init(&hasher);
        blake3_hasher_update(&hasher, data, data_len);
        blake3_hasher_finalize(&hasher, digest, BLAKE3_OUT_LEN);

        return digest;
    }

    // Parallel tree hashing (for large files)
    void blake3_hash_file_parallel(const char *filename) {
        FILE *fp = fopen(filename, "rb");
        blake3_hasher hasher;
        unsigned char buffer[1048576];  // 1 MB chunks
        size_t bytes;

        blake3_hasher_init(&hasher);
        while ((bytes = fread(buffer, 1, sizeof(buffer), fp)) > 0) {
            blake3_hasher_update(&hasher, buffer, bytes);
        }

        unsigned char digest[32];
        blake3_hasher_finalize(&hasher, digest, 32);

        // Display hash
        for (int i = 0; i < 32; i++) {
            printf("%02x", digest[i]);
        }
    }

**Performance** (vs SHA-256):

- SHA-256: ~1 Gbps
- BLAKE3 single-threaded: ~2.5 Gbps
- BLAKE3 parallel (4 cores): ~8+ Gbps
- **Speedup**: 8-10× faster with SIMD

**When to Use**:
- File integrity (e.g., deduplication)
- Performance-critical applications
- Tree hashing for incremental updates

**Keywords**: BLAKE3, parallel hashing, tree hashing, SIMD acceleration, fast cryptographic hash.

---

Password Hashing & Key Derivation Functions (KDF)
==================================================

Overview
--------

Password hashing intentionally slows down computation to prevent brute-force attacks. Requirements:
- **Memory-hard**: Resistant to GPU/ASIC acceleration
- **Time cost**: Adjustable slowness
- **Parallelism**: Resistant to massive parallelization

**Do NOT use**: Plain SHA-256, MD5, or unsalted hashes

Argon2id (2026 Best Practice)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Status**: WINNER - Recommended for all new systems

**Overview**: Memory-hard KDF designed to resist GPU/ASIC attacks

**Parameters**:

+----------+-------+----------+-----+-------------------+
| Param    | Min   | Recommend| Max | Notes             |
+==========+=======+==========+=====+===================+
| Memory   | 8 MB  | 64-256MB | 4GB | Larger = harder   |
+----------+-------+----------+-----+-------------------+
| Time     | 1     | 2-4      | 10  | Iterations        |
+----------+-------+----------+-----+-------------------+
| Parallel | 1     | 4        | 16  | Thread count      |
+----------+-------+----------+-----+-------------------+
| Salt     | 16B   | 16B      | 64B | Cryptographic RNG |
+----------+-------+----------+-----+-------------------+

**Implementation**:

.. code-block:: c

    #include <argon2.h>
    #include <string.h>

    int argon2_hash_password(const char *password, unsigned char *salt,
                             unsigned char *hash_output) {
        // Parameters
        uint32_t time_cost = 2;       // Iterations
        uint32_t mem_cost = 65536;    // 64 MB
        uint32_t parallelism = 4;     // Threads
        uint32_t hash_len = 32;       // Output: 32 bytes

        // Hash password
        int result = argon2id_hash_raw(
            time_cost,
            mem_cost,
            parallelism,
            password,
            strlen(password),
            salt,
            16,  // Salt length
            hash_len,
            hash_output
        );

        return result;  // ARGON2_OK = 0
    }

    // Typical usage: verify password
    int verify_password(const char *password, const char *hash_string) {
        unsigned char salt[16];
        unsigned char hash[32];

        // Extract salt from stored hash string
        // (typically hash_string format: $argon2id$v=19$m=65536,t=2,p=4$BASE64_SALT$BASE64_HASH)

        argon2_hash_password(password, salt, hash);

        // Compare hash (use constant-time comparison!)
        return memcmp(hash, extracted_hash, 32) == 0;
    }

**Security Properties**:
- **Memory resistance**: 64-256 MB prevents ASIC/GPU brute-force
- **Time cost**: Adjustable slowness (2-4 iterations recommended)
- **Salt**: 16 bytes of cryptographic randomness per password

**Performance**:
- Single password hash: ~100 ms (mem=64MB, t=2, p=4) on Cortex-A72
- Throughput: ~10 hashes/second (intentionally slow)

**Keywords**: Memory-hard function, Argon2, key derivation, password hashing, salt, brute-force resistance.

bcrypt (Legacy - Still Acceptable)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Status**: Good for legacy systems, but Argon2id preferred

**Overview**: Adaptive hash based on Blowfish cipher

**Implementation**:

.. code-block:: c

    #include <crypt.h>

    char *bcrypt_hash(const char *password, int cost) {
        char salt[16];
        crypt_gensalt("$2b$", cost, NULL, salt);
        return crypt(password, salt);  // Returns hash string
    }

    int bcrypt_verify(const char *password, const char *hash_string) {
        char *result = crypt(password, hash_string);
        return strcmp(result, hash_string) == 0;
    }

**Parameters**:
- **Cost**: 2^cost work factor (10-18 recommended, 2^10 = 1024 iterations)
- **Cost = 12**: ~250 ms per hash (modern CPU)
- **Cost = 18**: ~45 seconds per hash

**Weaknesses**:
- Fixed at 72-byte password truncation
- Salt limited to 128 bits
- Not memory-hard (vulnerable to GPU)

**When to use**: Legacy systems, crypt-based auth, compatibility

**Keywords**: Blowfish, adaptive hash, cost factor, bcrypt iteration.

PBKDF2 (FIPS Compliance)
~~~~~~~~~~~~~~~~~~~~~~~~

**Status**: Acceptable only for FIPS compliance, not recommended for new code

**Overview**: Key derivation function applying pseudorandom function (HMAC) iteratively

**Implementation**:

.. code-block:: c

    #include <openssl/evp.h>

    int pbkdf2_derive(const char *password, unsigned char *salt, int salt_len,
                      int iterations, unsigned char *derived_key, int key_len) {
        return PKCS5_PBKDF2_HMAC(
            password,
            strlen(password),
            salt,
            salt_len,
            iterations,
            EVP_sha256(),
            key_len,
            derived_key
        );
    }

**Parameters**:
- **Iterations**: Minimum 600,000 (NIST 2023 recommendation)
- **Iterations**: 1,000,000+ for maximum security
- **Hash function**: HMAC-SHA-256 or HMAC-SHA-512

**Weaknesses**:
- NOT memory-hard (can be GPU-accelerated)
- Requires very high iteration counts for security
- Slower than Argon2 for equivalent security

**When to use**: Only for FIPS/compliance mandates

**Keywords**: PBKDF2, PKCS#5, HMAC iteration, key derivation.

scrypt (Medium Alternative)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Status**: Good alternative if Argon2 unavailable

**Overview**: Memory-hard function with configurable time/space tradeoff

**Parameters**:

.. code-block:: c

    #include <openssl/evp.h>

    int scrypt_derive(const char *password, unsigned char *salt,
                      uint64_t N, uint32_t r, uint32_t p,
                      unsigned char *derived_key, int key_len) {
        return EVP_PBE_scrypt(
            password,
            strlen(password),
            salt,
            16,  // Salt length
            N,   // Memory cost (2^14 to 2^17)
            r,   // Block size (typically 8)
            p,   // Parallelism (typically 1)
            MBEDTLS_MD_SHA256,
            key_len,
            derived_key
        );
    }

    // Example: N=2^16, r=8, p=1
    unsigned char key[32];
    scrypt_derive("password123", salt, 65536, 8, 1, key, 32);

**Typical Parameters**:

- **N = 2^14 to 2^17**: Memory cost (16 MB - 128 MB)
- **r = 8**: Block size (standard)
- **p = 1-4**: Parallelism

**Performance**:
- N=2^15, r=8, p=1: ~200 ms per hash
- Memory usage: ~32 MB

**Keywords**: scrypt, memory cost, block size, parallelism parameter.

---

Digital Signature Schemes
==========================

Overview & Comparison Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------+----------+---------+--------+------------+-----------+
| Scheme        | Key Size | Speed   | Sig    | Status     | Best Use  |
+==========+====+==========+==========+========+============+===========+
| **Ed25519**   | 256      | Very    | 64B    | **TOP 1**  | SSH, code |
|               |          | fast    |        | choice     | signing   |
+---------------+----------+---------+--------+------------+-----------+
| **P-384**     | 384      | Fast    | 96B    | Good       | Legacy    |
| (ECDSA)       |          |         |        | certs      | certs     |
+---------------+----------+---------+--------+------------+-----------+
| **RSA-PSS**   | 3072+    | Slow    | 384B+  | Acceptable | When EC   |
|               |          |         |        |            | N/A       |
+---------------+----------+---------+--------+------------+-----------+
| **ML-DSA-65** | Lattice  | Medium  | 2544B  | **Emerging**| PQ pilots |
+---------------+----------+---------+--------+------------+-----------+
| **SLH-DSA**   | Hash     | Slow    | 7144B  | **Emerging**| Stateless |
+---------------+----------+---------+--------+------------+-----------+

**Best Practices**:

.. code-block:: text

    2026 Recommendations:
    
    1. New systems: Ed25519 + optional ML-DSA-65 (hybrid)
    2. Legacy systems: ECDSA P-384 (migrate to Ed25519)
    3. Compliance: RSA-PSS ≥ 3072 (moving away)
    4. Post-quantum pilots: Hybrid Ed25519 + ML-DSA-65

Ed25519 Digital Signatures (See above under ECC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**OpenSSH Usage**:

.. code-block:: bash

    # Generate Ed25519 SSH key
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

    # Code signing with Git
    git config --global user.signingkey <public-key-path>
    git commit -S -m "Signed commit"

RSA-PSS (Probabilistic Signature Scheme)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to use**: Legacy systems, FIPS compliance (RSA-only environments)

**Implementation**:

.. code-block:: c

    #include <openssl/rsa.h>
    #include <openssl/evp.h>

    int rsa_pss_sign(EVP_PKEY *private_key, unsigned char *message, int msg_len,
                     unsigned char *signature, unsigned int *sig_len) {
        EVP_MD_CTX *mdctx = EVP_MD_CTX_new();

        EVP_DigestSignInit(mdctx, NULL, EVP_sha256(), NULL, private_key);
        EVP_DigestSign(mdctx, signature, (size_t *)sig_len, message, msg_len);

        EVP_MD_CTX_free(mdctx);
        return 0;
    }

**Advantages over PKCS#1 v1.5**:
- Probabilistic (randomized each signature)
- Provably secure reduction to RSA problem
- Standard in TLS 1.3

**Keywords**: RSA-PSS, PKCS#1, probabilistic signatures, secure padding scheme.

---

Protocols & Integration
=======================

TLS 1.3 Cipher Suites (2026 Recommendations)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------+--------+--------+----------+
| Cipher Suite                   | Auth   | Encrypt| Hash     |
+================================+========+========+==========+
| **AEAD_AES_256_GCM_SHA256**    | ECDSA/ | AES    | SHA-256  |
|                                | EdDSA  | 256    |          |
+--------------------------------+--------+--------+----------+
| **CHACHA20_POLY1305_SHA256**   | ECDSA/ | ChaCha | SHA-256  |
|                                | EdDSA  | 20     |          |
+--------------------------------+--------+--------+----------+
| **AEAD_AES_128_GCM_SHA256**    | ECDSA/ | AES    | SHA-256  |
|                                | EdDSA  | 128    |          |
+--------------------------------+--------+--------+----------+

**Recommended Priority** (TLS 1.3):

.. code-block:: bash

    # OpenSSL configuration
    Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    
    # nginx config
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

**Keywords**: Cipher suite, authenticated encryption, key exchange, cipher negotiation.

Hybrid Post-Quantum TLS (Pilot Phase)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Approach** (2026+):

.. code-block:: text

    Key Exchange (hybrid):
    - X25519 (classical) || ML-KEM-768 (post-quantum)
    
    Digital Signature (hybrid):
    - Ed25519 (classical) || ML-DSA-65 (post-quantum)
    
    Benefit: If either is broken, the other still provides security

**Implementation** (future TLS libraries):

.. code-block:: text

    Cipher Suite: TLS_X25519_ML_KEM_768_AES_256_GCM_SHA384
    (Hypothetical TLS 1.4 equivalent)

**Keywords**: Hybrid cryptography, post-quantum migration, dual algorithms.

---

Best Practices & Recommendations (2026)
========================================

Quick Reference: Use vs Avoid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use**                            | **Avoid / Deprecated**
-----------------------------------|---------------------------------
AES-256-GCM or ChaCha20-Poly1305  | CBC mode, 3DES, RC4, stream without auth
X25519 + Ed25519                   | RSA < 3072, ECDSA P-256, ECDSA + SHA-1
Argon2id (64-256 MB)               | MD5, SHA-1, bcrypt cost < 12, PBKDF2 < 600k
SHA-256 or BLAKE3                  | MD5, SHA-1
Hybrid (X25519+ML-KEM, Ed25519+ML-DSA) | Pure classical or pure PQ

Implementation Checklist
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    [ ] Use Authenticated Encryption (AES-GCM or ChaCha20-Poly1305)
    [ ] Use cryptographic RNG for nonces/IVs (never reuse)
    [ ] Implement X25519 or Ed25519 for key exchange / signatures
    [ ] Hash with SHA-256, SHA-3, or BLAKE3 (not MD5/SHA-1)
    [ ] Use Argon2id for passwords (memory ≥ 64 MB)
    [ ] Constant-time comparison for secrets (memcmp_s)
    [ ] Audit dependencies: OpenSSL, libsodium, crypto libraries
    [ ] Rotate keys regularly (esp. short-term session keys)
    [ ] Monitor for algorithm deprecations (PKI/TLS standards)
    [ ] Plan post-quantum hybrid migrations (2024+)

Key Length Timeline (Residual Lifetime)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+-------+----------+-----+
| Algorithm        | Bits  | Until    | 2026|
+==================+=======+==========+=====+
| AES-128          | 128   | 2046     | ✓   |
+------------------+-------+----------+-----+
| AES-256          | 256   | 2066+    | ✓   |
+------------------+-------+----------+-----+
| RSA-2048         | 2048  | 2028     | ❌  |
+------------------+-------+----------+-----+
| RSA-3072         | 3072  | 2045     | ✓   |
+------------------+-------+----------+-----+
| RSA-4096         | 4096  | 2060     | ✓   |
+------------------+-------+----------+-----+
| P-256 (NIST)     | 256   | 2036     | ✓   |
+------------------+-------+----------+-----+
| X25519/Ed25519   | 256   | 2046     | ✓   |
+------------------+-------+----------+-----+
| ML-KEM-768       | 192 PQ| 2066+    | ✓   |
+------------------+-------+----------+-----+

---

Common Pitfalls & Solutions
============================

Pitfall #1: Reusing Nonces in AES-GCM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Same nonce + key = compromised confidentiality and authenticity

.. code-block:: c

    // WRONG: Fixed nonce
    unsigned char nonce[12] = {0x00, 0x00, ...};  // NEVER REUSE
    EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, nonce);

**Solution**: Generate unique nonce for each encryption

.. code-block:: c

    // CORRECT: Random nonce
    unsigned char nonce[12];
    RAND_bytes(nonce, 12);  // Cryptographic RNG
    EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, nonce);

Pitfall #2: Using Unsalted Password Hashes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Identical passwords hash to same value

.. code-block:: c

    // WRONG: No salt
    SHA256(password, strlen(password), digest);

**Solution**: Use memory-hard KDF with salt

.. code-block:: c

    // CORRECT: Argon2id with salt
    unsigned char salt[16];
    RAND_bytes(salt, 16);
    argon2id_hash_raw(2, 65536, 4, password, strlen(password),
                      salt, 16, 32, output_hash);

Pitfall #3: Timing Attacks on Comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: == operator leaks timing information

.. code-block:: c

    // WRONG: Timing leaks which bytes match
    if (memcmp(hash1, hash2, 32) == 0) { ... }

**Solution**: Use constant-time comparison

.. code-block:: c

    // CORRECT: Constant-time comparison (OpenSSL 3.0+)
    int result = CRYPTO_memcmp(hash1, hash2, 32);
    if (result == 0) { /* Constant time */ }

Pitfall #4: Weak Random Number Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Using rand() or weak RNG for cryptography

.. code-block:: c

    // WRONG: Not cryptographically secure
    srand(time(NULL));
    key[0] = rand() % 256;

**Solution**: Use system CSPRNG

.. code-block:: c

    // CORRECT: Cryptographic RNG
    unsigned char key[32];
    RAND_bytes(key, 32);  // /dev/urandom on Linux

---

Performance Benchmarks (2026 Hardware)
======================================

Symmetric Encryption (Throughput, Gbps)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+--------+--------+---------+----------+
| Algorithm        | Cortex | Cortex | Cortex  | x86-64   |
|                  | -A53   | -A72   | -X2     | (AVX2)   |
+==================+========+========+=========+==========+
| AES-256-GCM      | 0.8    | 1.2    | 2.1     | 5.0      |
+------------------+--------+--------+---------+----------+
| ChaCha20-Poly1305| 1.2    | 2.5    | 3.8     | 6.0      |
+------------------+--------+--------+---------+----------+

Hash Functions (Throughput, Gbps)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+--------+--------+---------+----------+
| Algorithm        | Cortex | Cortex | Cortex  | x86-64   |
|                  | -A53   | -A72   | -X2     | (AVX2)   |
+==================+========+========+=========+==========+
| SHA-256          | 0.4    | 0.7    | 1.2     | 1.5      |
+------------------+--------+--------+---------+----------+
| BLAKE3           | 1.1    | 2.3    | 4.5     | 4.8      |
+------------------+--------+--------+---------+----------+

Public-Key Operations (ms per operation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+--------+--------+---------+----------+
| Operation        | Cortex | Cortex | Cortex  | x86-64   |
|                  | -A53   | -A72   | -X2     | (AVX2)   |
+==================+========+========+=========+==========+
| X25519 DH        | 2.1    | 0.8    | 0.3     | 0.1      |
+------------------+--------+--------+---------+----------+
| Ed25519 sign     | 1.5    | 0.6    | 0.2     | 0.05     |
+------------------+--------+--------+---------+----------+
| Ed25519 verify   | 3.2    | 1.2    | 0.4     | 0.1      |
+------------------+--------+--------+---------+----------+
| RSA-3072 sign    | 1200   | 450    | 80      | 15       |
+------------------+--------+--------+---------+----------+

---

Tools & Libraries Reference
============================

OpenSSL 3.0+
~~~~~~~~~~~~

**Installation**:

.. code-block:: bash

    # Debian/Ubuntu
    sudo apt-get install libssl-dev openssl

    # Compile & link
    gcc -o app app.c -lssl -lcrypto

**Key Operations**:

.. code-block:: bash

    # Generate RSA keypair
    openssl genrsa -out private.pem 3072

    # Generate Ed25519 keypair
    openssl genpkey -algorithm ed25519 -out private.pem

    # Hash file with SHA-256
    openssl dgst -sha256 filename

    # Encrypt file with AES-256-CBC
    openssl enc -aes-256-cbc -in plaintext -out ciphertext -S <salt>

libsodium
~~~~~~~~~

**Installation**:

.. code-block:: bash

    # Debian/Ubuntu
    sudo apt-get install libsodium-dev

**Example** (high-level API):

.. code-block:: c

    #include <sodium.h>

    int main(void) {
        unsigned char key[crypto_secretbox_KEYBYTES];
        unsigned char nonce[crypto_secretbox_NONCEBYTES];
        unsigned char plaintext[100] = "Hello, Encrypted World!";
        unsigned char ciphertext[100 + crypto_secretbox_MACBYTES];

        // Generate random key
        randombytes(key, crypto_secretbox_KEYBYTES);
        randombytes(nonce, crypto_secretbox_NONCEBYTES);

        // Encrypt
        crypto_secretbox_easy(ciphertext, plaintext, 100, nonce, key);

        return 0;
    }

---

References & Standards (2026)
==============================

**NIST Standards**:
- FIPS 197: AES
- FIPS 180-4: SHA hash algorithms
- FIPS 202: SHA-3
- FIPS 203: ML-KEM (post-quantum key encapsulation)
- FIPS 204: ML-DSA (post-quantum signatures)

**IETF RFCs**:
- RFC 8439: ChaCha20 and Poly1305
- RFC 8032: EdDSA (Ed25519)
- RFC 7748: Elliptic Curves for Security (X25519)
- RFC 5869: HKDF (HMAC-based Key Derivation Function)
- RFC 9000+: TLS 1.3 updates

**Books & Resources**:
- "Cryptography Engineering" (Ferguson, Schneier, Kohno)
- https://cryptography.io/ (Python cryptography library docs)
- https://libsodium.gitbook.io/ (libsodium documentation)
- https://www.keylength.com/ (Key length recommendations)

---

**Last Updated**: January 2026
**Compatibility**: Linux systems, OpenSSL 3.0+, libsodium 1.0.18+
**Post-Quantum Status**: NIST standardization complete (2024), hybrid pilot phase (2024-2026)

