💾 **Databases for Aircraft Systems — Comprehensive Guide**
═══════════════════════════════════════════════════════════════════

**Context:** Data persistence for avionics, IFE, and passenger services  
**Focus:** MySQL/MariaDB, SQLite, transactions, crash resistance  
**Standards:** ACID compliance, DO-178C data integrity requirements

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — DATABASES IN 60 SECONDS**
───────────────────────────────────────

**Database Selection Matrix:**

+------------+-------------+----------------+------------------+
| Database   | Use Case    | Advantages     | Aircraft Context |
+============+=============+================+==================+
| MySQL/     | Server-side | Multi-user,    | Ground systems,  |
| MariaDB    | storage     | replication    | IFE content mgmt |
+------------+-------------+----------------+------------------+
| SQLite     | Embedded    | No server,     | Seat units,      |
|            | local cache | atomic writes  | offline storage  |
+------------+-------------+----------------+------------------+
| PostgreSQL | Analytics   | Complex        | Data warehouse,  |
|            |             | queries        | flight analytics |
+------------+-------------+----------------+------------------+

**Key Aviation Requirements:**

✅ **Crash Resistance:** Database must survive sudden power loss  
✅ **Atomicity:** All-or-nothing transactions (payment processing)  
✅ **Consistency:** Referential integrity (seat assignments)  
✅ **Isolation:** Concurrent access without corruption  
✅ **Durability:** Committed data survives system failure

════════════════════════════════════════════════════════════════════

🗄️ **1. MYSQL/MARIADB — SERVER-SIDE DATABASE**
═══════════════════════════════════════════════

**Why MySQL for Aircraft?**

- **IFE Content Management:** Movies, shows, metadata
- **Passenger Services:** Account management, preferences
- **Maintenance Systems:** Work orders, parts inventory
- **Airline Integration:** Booking data, loyalty programs

**Installation & Configuration:**

.. code-block:: bash

   # Install MariaDB (MySQL fork)
   sudo apt-get install mariadb-server mariadb-client
   
   # Secure installation
   sudo mysql_secure_installation
   
   # Start service
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   
   # Check status
   sudo systemctl status mariadb

**Basic Configuration (my.cnf):**

.. code-block:: ini

   [mysqld]
   # InnoDB settings for crash recovery
   innodb_flush_log_at_trx_commit = 1   # Full ACID compliance
   innodb_doublewrite = 1                # Protect against torn pages
   innodb_file_per_table = 1             # Separate file per table
   
   # Performance tuning for embedded systems
   innodb_buffer_pool_size = 512M        # Adjust based on RAM
   max_connections = 50                  # Limit concurrent connections
   query_cache_size = 32M                # Cache frequent queries
   
   # Character set (UTF-8 for international content)
   character-set-server = utf8mb4
   collation-server = utf8mb4_unicode_ci

**Example Schema: IFE Content Management:**

.. code-block:: sql

   -- Create database
   CREATE DATABASE ife_content_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   USE ife_content_db;
   
   -- Content table
   CREATE TABLE content (
       content_id INT PRIMARY KEY AUTO_INCREMENT,
       title VARCHAR(255) NOT NULL,
       content_type ENUM('movie', 'tv_show', 'music', 'game') NOT NULL,
       duration_minutes INT,
       release_year YEAR,
       rating VARCHAR(10),  -- PG, PG-13, R, etc.
       file_path VARCHAR(512),
       file_size_mb INT,
       thumbnail_url VARCHAR(512),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       INDEX idx_type (content_type),
       INDEX idx_rating (rating)
   ) ENGINE=InnoDB;
   
   -- Categories table
   CREATE TABLE categories (
       category_id INT PRIMARY KEY AUTO_INCREMENT,
       category_name VARCHAR(100) NOT NULL UNIQUE,
       description TEXT
   ) ENGINE=InnoDB;
   
   -- Many-to-many: Content to Categories
   CREATE TABLE content_categories (
       content_id INT,
       category_id INT,
       PRIMARY KEY (content_id, category_id),
       FOREIGN KEY (content_id) REFERENCES content(content_id) ON DELETE CASCADE,
       FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
   ) ENGINE=InnoDB;
   
   -- Passenger viewing history
   CREATE TABLE viewing_history (
       history_id BIGINT PRIMARY KEY AUTO_INCREMENT,
       seat_id VARCHAR(10) NOT NULL,  -- e.g., "12A"
       content_id INT NOT NULL,
       view_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       watch_duration_minutes INT,
       completed BOOLEAN DEFAULT FALSE,
       FOREIGN KEY (content_id) REFERENCES content(content_id),
       INDEX idx_seat (seat_id),
       INDEX idx_timestamp (view_timestamp)
   ) ENGINE=InnoDB;

**Sample Queries:**

.. code-block:: sql

   -- Insert content
   INSERT INTO content (title, content_type, duration_minutes, release_year, rating)
   VALUES ('Top Gun: Maverick', 'movie', 131, 2022, 'PG-13');
   
   INSERT INTO categories (category_name) VALUES ('Action'), ('Drama');
   
   INSERT INTO content_categories (content_id, category_id)
   VALUES (1, 1), (1, 2);
   
   -- Find all action movies
   SELECT c.title, c.duration_minutes, c.rating
   FROM content c
   JOIN content_categories cc ON c.content_id = cc.content_id
   JOIN categories cat ON cc.category_id = cat.category_id
   WHERE cat.category_name = 'Action'
   AND c.content_type = 'movie'
   ORDER BY c.release_year DESC;
   
   -- Get most popular content (top 10 most viewed)
   SELECT c.title, COUNT(vh.history_id) as view_count
   FROM content c
   JOIN viewing_history vh ON c.content_id = vh.content_id
   GROUP BY c.content_id
   ORDER BY view_count DESC
   LIMIT 10;
   
   -- Find abandoned views (not completed)
   SELECT seat_id, c.title, vh.watch_duration_minutes
   FROM viewing_history vh
   JOIN content c ON vh.content_id = c.content_id
   WHERE vh.completed = FALSE
   AND vh.view_timestamp > NOW() - INTERVAL 24 HOUR;

**Transaction Example (Payment Processing):**

.. code-block:: sql

   START TRANSACTION;
   
   -- Deduct payment
   UPDATE passenger_accounts
   SET balance = balance - 19.99
   WHERE account_id = 12345;
   
   -- Record purchase
   INSERT INTO purchases (account_id, content_id, price, purchase_time)
   VALUES (12345, 1, 19.99, NOW());
   
   -- Verify balance is non-negative
   IF (SELECT balance FROM passenger_accounts WHERE account_id = 12345) < 0 THEN
       ROLLBACK;
       SELECT 'Insufficient funds' AS error;
   ELSE
       COMMIT;
       SELECT 'Purchase successful' AS message;
   END IF;

════════════════════════════════════════════════════════════════════

🔒 **2. SQLITE — EMBEDDED DATABASE**
═════════════════════════════════════

**Why SQLite for Aircraft?**

✅ **No server process:** Embedded directly in application  
✅ **Zero configuration:** No setup required  
✅ **Crash-safe:** Atomic commit with rollback journal  
✅ **Small footprint:** ~600 KB library  
✅ **Cross-platform:** Same database file on any OS

**Use Cases:**

- **Seat-level storage:** Downloaded content, preferences
- **Offline caching:** Flight information, maps
- **Configuration:** Device settings, user profiles
- **Logging:** Local event logs before sync

**C++ Integration:**

.. code-block:: cpp

   // File: DatabaseManager.hpp
   #include <sqlite3.h>
   #include <string>
   #include <iostream>
   
   class DatabaseManager {
   private:
       sqlite3* db_;
       std::string dbPath_;
       
   public:
       DatabaseManager(const std::string& path) : db_(nullptr), dbPath_(path) {}
       
       ~DatabaseManager() {
           close();
       }
       
       bool open() {
           int rc = sqlite3_open(dbPath_.c_str(), &db_);
           if (rc != SQLITE_OK) {
               std::cerr << "Cannot open database: " << sqlite3_errmsg(db_) << "\n";
               return false;
           }
           
           // Enable Write-Ahead Logging (WAL) for better concurrency
           sqlite3_exec(db_, "PRAGMA journal_mode=WAL;", nullptr, nullptr, nullptr);
           
           // Enable foreign keys
           sqlite3_exec(db_, "PRAGMA foreign_keys=ON;", nullptr, nullptr, nullptr);
           
           std::cout << "Database opened: " << dbPath_ << "\n";
           return true;
       }
       
       void close() {
           if (db_) {
               sqlite3_close(db_);
               db_ = nullptr;
           }
       }
       
       bool execute(const std::string& sql) {
           char* errMsg = nullptr;
           int rc = sqlite3_exec(db_, sql.c_str(), nullptr, nullptr, &errMsg);
           
           if (rc != SQLITE_OK) {
               std::cerr << "SQL error: " << errMsg << "\n";
               sqlite3_free(errMsg);
               return false;
           }
           return true;
       }
       
       bool createTables() {
           const char* sql = R"(
               CREATE TABLE IF NOT EXISTS downloaded_content (
                   content_id INTEGER PRIMARY KEY,
                   title TEXT NOT NULL,
                   file_path TEXT,
                   download_date INTEGER,  -- Unix timestamp
                   file_size INTEGER
               );
               
               CREATE TABLE IF NOT EXISTS user_preferences (
                   pref_key TEXT PRIMARY KEY,
                   pref_value TEXT
               );
               
               CREATE TABLE IF NOT EXISTS playback_position (
                   content_id INTEGER PRIMARY KEY,
                   position_seconds INTEGER,
                   last_updated INTEGER,
                   FOREIGN KEY (content_id) REFERENCES downloaded_content(content_id)
               );
           )";
           
           return execute(sql);
       }
       
       bool insertContent(int contentId, const std::string& title, 
                         const std::string& filePath, int fileSize) {
           sqlite3_stmt* stmt;
           const char* sql = "INSERT INTO downloaded_content (content_id, title, file_path, download_date, file_size) VALUES (?, ?, ?, ?, ?)";
           
           if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
               std::cerr << "Failed to prepare statement\n";
               return false;
           }
           
           sqlite3_bind_int(stmt, 1, contentId);
           sqlite3_bind_text(stmt, 2, title.c_str(), -1, SQLITE_TRANSIENT);
           sqlite3_bind_text(stmt, 3, filePath.c_str(), -1, SQLITE_TRANSIENT);
           sqlite3_bind_int(stmt, 4, static_cast<int>(time(nullptr)));
           sqlite3_bind_int(stmt, 5, fileSize);
           
           bool success = (sqlite3_step(stmt) == SQLITE_DONE);
           sqlite3_finalize(stmt);
           
           return success;
       }
       
       void listContent() {
           const char* sql = "SELECT content_id, title, file_size FROM downloaded_content";
           sqlite3_stmt* stmt;
           
           if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) == SQLITE_OK) {
               std::cout << "\nDownloaded Content:\n";
               while (sqlite3_step(stmt) == SQLITE_ROW) {
                   int id = sqlite3_column_int(stmt, 0);
                   const char* title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
                   int size = sqlite3_column_int(stmt, 2);
                   
                   std::cout << "  [" << id << "] " << title << " (" << size << " MB)\n";
               }
           }
           sqlite3_finalize(stmt);
       }
   };

**Usage Example:**

.. code-block:: cpp

   int main() {
       DatabaseManager db("/var/ife/seat_12A.db");
       
       if (db.open()) {
           db.createTables();
           
           // Insert downloaded content
           db.insertContent(101, "Top Gun: Maverick", "/media/movie101.mp4", 2048);
           db.insertContent(102, "Breaking Bad S01E01", "/media/tv102.mp4", 512);
           
           // List content
           db.listContent();
           
           db.close();
       }
       
       return 0;
   }

**SQLite Crash Safety:**

.. code-block:: sql

   -- Enable full synchronous mode (slowest but safest)
   PRAGMA synchronous = FULL;
   
   -- Write-Ahead Logging (WAL) for better concurrency
   PRAGMA journal_mode = WAL;
   
   -- Automatic checkpointing
   PRAGMA wal_autocheckpoint = 1000;  -- Checkpoint every 1000 pages

**Backup Strategy:**

.. code-block:: bash

   # Online backup (while database is in use)
   sqlite3 seat_12A.db ".backup /backup/seat_12A_backup.db"
   
   # Export to SQL dump
   sqlite3 seat_12A.db .dump > backup.sql
   
   # Restore from SQL dump
   sqlite3 seat_12A_restored.db < backup.sql

════════════════════════════════════════════════════════════════════

⚡ **3. PERFORMANCE OPTIMIZATION**
═══════════════════════════════════

**Indexing Strategy:**

.. code-block:: sql

   -- Before: Slow query (table scan)
   SELECT * FROM viewing_history WHERE seat_id = '12A';
   
   -- Create index
   CREATE INDEX idx_seat_id ON viewing_history(seat_id);
   
   -- After: Fast query (index seek)
   EXPLAIN SELECT * FROM viewing_history WHERE seat_id = '12A';
   -- Output: Using index idx_seat_id

**Composite Index:**

.. code-block:: sql

   -- For queries filtering by seat AND date
   CREATE INDEX idx_seat_date ON viewing_history(seat_id, view_timestamp);
   
   -- Optimized query
   SELECT * FROM viewing_history
   WHERE seat_id = '12A'
   AND view_timestamp > '2026-01-01'
   ORDER BY view_timestamp DESC;

**Query Optimization:**

.. code-block:: sql

   -- BAD: N+1 query problem
   SELECT * FROM content;
   -- Then for each content: SELECT * FROM categories WHERE category_id = ?
   
   -- GOOD: Single JOIN query
   SELECT c.*, cat.category_name
   FROM content c
   LEFT JOIN content_categories cc ON c.content_id = cc.content_id
   LEFT JOIN categories cat ON cc.category_id = cat.category_id;

**Connection Pooling (C++):**

.. code-block:: cpp

   #include <mysql/mysql.h>
   #include <queue>
   #include <mutex>
   
   class ConnectionPool {
   private:
       std::queue<MYSQL*> pool_;
       std::mutex mutex_;
       int maxConnections_;
       
   public:
       ConnectionPool(int max) : maxConnections_(max) {
           for (int i = 0; i < maxConnections_; ++i) {
               MYSQL* conn = mysql_init(nullptr);
               if (mysql_real_connect(conn, "localhost", "user", "pass", 
                                     "ife_content_db", 3306, nullptr, 0)) {
                   pool_.push(conn);
               }
           }
       }
       
       MYSQL* acquire() {
           std::lock_guard<std::mutex> lock(mutex_);
           if (pool_.empty()) return nullptr;
           
           MYSQL* conn = pool_.front();
           pool_.pop();
           return conn;
       }
       
       void release(MYSQL* conn) {
           std::lock_guard<std::mutex> lock(mutex_);
           pool_.push(conn);
       }
       
       ~ConnectionPool() {
           while (!pool_.empty()) {
               MYSQL* conn = pool_.front();
               pool_.pop();
               mysql_close(conn);
           }
       }
   };

════════════════════════════════════════════════════════════════════

🛡️ **4. SECURITY BEST PRACTICES**
═══════════════════════════════════

**SQL Injection Prevention:**

.. code-block:: cpp

   // BAD: SQL injection vulnerable
   std::string sql = "SELECT * FROM users WHERE username = '" + username + "'";
   
   // GOOD: Prepared statement (parameterized query)
   sqlite3_stmt* stmt;
   const char* sql = "SELECT * FROM users WHERE username = ?";
   sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
   sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
   sqlite3_step(stmt);
   sqlite3_finalize(stmt);

**Encryption at Rest (SQLite):**

.. code-block:: bash

   # Using SQLCipher (encrypted SQLite)
   sudo apt-get install sqlcipher
   
   # Create encrypted database
   sqlcipher encrypted.db
   > PRAGMA key = 'your-encryption-key';
   > CREATE TABLE secrets (data TEXT);

**User Permissions (MySQL):**

.. code-block:: sql

   -- Create read-only user for IFE application
   CREATE USER 'ife_app'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT SELECT ON ife_content_db.* TO 'ife_app'@'localhost';
   
   -- Create admin user with full access
   CREATE USER 'ife_admin'@'localhost' IDENTIFIED BY 'admin_password';
   GRANT ALL PRIVILEGES ON ife_content_db.* TO 'ife_admin'@'localhost';
   
   FLUSH PRIVILEGES;

════════════════════════════════════════════════════════════════════

📝 **5. EXAM QUESTIONS**
═════════════════════════

**Q1:** Why is SQLite preferred for seat-level storage over MySQL?

**A1:** SQLite is embedded (no server process), has zero configuration, 
atomic commits, and small footprint (~600 KB). Perfect for resource-constrained 
seat units. MySQL requires server process and network overhead.

────────────────────────────────────────────────────────────────────

**Q2:** What does `innodb_flush_log_at_trx_commit = 1` do?

**A2:** Forces InnoDB to flush transaction log to disk on EVERY commit, 
ensuring full ACID durability. Slower but crash-safe. Critical for 
payment processing where transactions must not be lost.

────────────────────────────────────────────────────────────────────

**Q3:** How does Write-Ahead Logging (WAL) improve SQLite performance?

**A3:** WAL allows concurrent readers and writers. Changes are written 
to separate WAL file, then periodically checkpointed to main database. 
Improves concurrency and reduces lock contention.

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand MySQL vs SQLite trade-offs
- [ ] Design normalized schema (3NF)
- [ ] Create proper indexes for queries
- [ ] Implement prepared statements (SQL injection prevention)
- [ ] Configure crash-safe settings (ACID compliance)
- [ ] Use transactions for multi-step operations
- [ ] Implement connection pooling for performance
- [ ] Set up backup/recovery procedures

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **DATABASE GUIDE COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** MySQL, SQLite, C++ integration, security, performance

════════════════════════════════════════════════════════════════════
