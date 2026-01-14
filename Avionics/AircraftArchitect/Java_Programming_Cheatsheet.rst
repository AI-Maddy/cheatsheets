☕ **JAVA PROGRAMMING — Enterprise Patterns for Aircraft Systems**
═══════════════════════════════════════════════════════════════════

**Context:** Java for IFE backend, payment processing, CMS
**Focus:** Spring Boot, JPA/Hibernate, Payment APIs
**Use Cases:** Business logic, airline integration, enterprise services

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — JAVA IN 60 SECONDS**
──────────────────────────────────

**Why Java for Aviation:**

+----------------------+------------------------------------------------+
| **Feature**          | **Benefit**                                    |
+======================+================================================+
| Enterprise maturity  | 25+ years of battle-tested libraries           |
+----------------------+------------------------------------------------+
| Spring ecosystem     | Dependency injection, REST APIs, security      |
+----------------------+------------------------------------------------+
| JPA/Hibernate        | ORM for complex database schemas               |
+----------------------+------------------------------------------------+
| Strong typing        | Compile-time safety (vs JavaScript)            |
+----------------------+------------------------------------------------+
| JVM ecosystem        | Scala/Kotlin interoperability                  |
+----------------------+------------------------------------------------+

**Aviation Use Cases:**

- 💳 Payment Processing (PCI DSS compliance)
- 🎬 Content Management Systems (CMS)
- 🔄 Airline Integration APIs (NDC, IATA standards)
- 📊 Loyalty Program Integration
- 🎫 Booking System Integration

**Spring Boot Stack:**

::

    Spring Boot (framework)
       ↓
    Spring MVC (REST APIs)
       ↓
    Spring Data JPA (database)
       ↓
    Spring Security (auth)
       ↓
    H2/MySQL/PostgreSQL (persistence)

════════════════════════════════════════════════════════════════════

📖 **1. SPRING BOOT FUNDAMENTALS**
═══════════════════════════════════

**1.1 Project Structure**
-------------------------

::

    ife-service/
    ├── pom.xml                       # Maven dependencies
    ├── src/main/java/com/airline/ife/
    │   ├── IfeServiceApplication.java   # Main entry point
    │   ├── controller/
    │   │   └── MovieController.java     # REST endpoints
    │   ├── service/
    │   │   └── MovieService.java        # Business logic
    │   ├── repository/
    │   │   └── MovieRepository.java     # Database access
    │   └── model/
    │       └── Movie.java               # Entity
    └── src/main/resources/
        └── application.properties       # Configuration

**1.2 Main Application**
------------------------

.. code-block:: java

    package com.airline.ife;
    
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    
    @SpringBootApplication
    public class IfeServiceApplication {
        public static void main(String[] args) {
            SpringApplication.run(IfeServiceApplication.class, args);
        }
    }

**1.3 Entity (Model)**
---------------------

.. code-block:: java

    package com.airline.ife.model;
    
    import javax.persistence.*;
    import java.time.LocalDate;
    
    @Entity
    @Table(name = "movies")
    public class Movie {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        @Column(nullable = false)
        private String title;
        
        @Column(nullable = false)
        private Integer duration;  // minutes
        
        private String genre;
        
        @Column(name = "release_date")
        private LocalDate releaseDate;
        
        @Column(name = "content_rating")
        private String contentRating;  // G, PG, PG-13, R
        
        // Constructors
        public Movie() {}
        
        public Movie(String title, Integer duration, String genre) {
            this.title = title;
            this.duration = duration;
            this.genre = genre;
        }
        
        // Getters and Setters
        public Long getId() { return id; }
        public void setId(Long id) { this.id = id; }
        
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        
        public Integer getDuration() { return duration; }
        public void setDuration(Integer duration) { this.duration = duration; }
        
        public String getGenre() { return genre; }
        public void setGenre(String genre) { this.genre = genre; }
        
        public LocalDate getReleaseDate() { return releaseDate; }
        public void setReleaseDate(LocalDate releaseDate) { 
            this.releaseDate = releaseDate; 
        }
        
        public String getContentRating() { return contentRating; }
        public void setContentRating(String contentRating) { 
            this.contentRating = contentRating; 
        }
    }

**1.4 Repository (Data Access)**
--------------------------------

.. code-block:: java

    package com.airline.ife.repository;
    
    import com.airline.ife.model.Movie;
    import org.springframework.data.jpa.repository.JpaRepository;
    import org.springframework.stereotype.Repository;
    
    import java.util.List;
    
    @Repository
    public interface MovieRepository extends JpaRepository<Movie, Long> {
        // Custom queries (Spring generates implementation!)
        List<Movie> findByGenre(String genre);
        List<Movie> findByContentRating(String rating);
        List<Movie> findByDurationLessThan(Integer duration);
    }

**1.5 Service (Business Logic)**
--------------------------------

.. code-block:: java

    package com.airline.ife.service;
    
    import com.airline.ife.model.Movie;
    import com.airline.ife.repository.MovieRepository;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;
    
    import java.util.List;
    import java.util.Optional;
    
    @Service
    public class MovieService {
        @Autowired
        private MovieRepository movieRepository;
        
        public List<Movie> getAllMovies() {
            return movieRepository.findAll();
        }
        
        public Optional<Movie> getMovieById(Long id) {
            return movieRepository.findById(id);
        }
        
        public List<Movie> getMoviesByGenre(String genre) {
            return movieRepository.findByGenre(genre);
        }
        
        public Movie saveMovie(Movie movie) {
            return movieRepository.save(movie);
        }
        
        public void deleteMovie(Long id) {
            movieRepository.deleteById(id);
        }
        
        // Business logic: Get short movies for commuter flights
        public List<Movie> getShortMovies() {
            return movieRepository.findByDurationLessThan(120);
        }
    }

**1.6 Controller (REST API)**
-----------------------------

.. code-block:: java

    package com.airline.ife.controller;
    
    import com.airline.ife.model.Movie;
    import com.airline.ife.service.MovieService;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.annotation.*;
    
    import java.util.List;
    
    @RestController
    @RequestMapping("/api/movies")
    public class MovieController {
        @Autowired
        private MovieService movieService;
        
        // GET /api/movies
        @GetMapping
        public List<Movie> getAllMovies() {
            return movieService.getAllMovies();
        }
        
        // GET /api/movies/{id}
        @GetMapping("/{id}")
        public ResponseEntity<Movie> getMovieById(@PathVariable Long id) {
            return movieService.getMovieById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
        }
        
        // GET /api/movies?genre=Action
        @GetMapping("/genre/{genre}")
        public List<Movie> getMoviesByGenre(@PathVariable String genre) {
            return movieService.getMoviesByGenre(genre);
        }
        
        // POST /api/movies
        @PostMapping
        public ResponseEntity<Movie> createMovie(@RequestBody Movie movie) {
            Movie saved = movieService.saveMovie(movie);
            return new ResponseEntity<>(saved, HttpStatus.CREATED);
        }
        
        // PUT /api/movies/{id}
        @PutMapping("/{id}")
        public ResponseEntity<Movie> updateMovie(
                @PathVariable Long id, 
                @RequestBody Movie movie) {
            return movieService.getMovieById(id)
                .map(existing -> {
                    movie.setId(id);
                    return ResponseEntity.ok(movieService.saveMovie(movie));
                })
                .orElse(ResponseEntity.notFound().build());
        }
        
        // DELETE /api/movies/{id}
        @DeleteMapping("/{id}")
        public ResponseEntity<Void> deleteMovie(@PathVariable Long id) {
            movieService.deleteMovie(id);
            return ResponseEntity.noContent().build();
        }
    }

════════════════════════════════════════════════════════════════════

📖 **2. PAYMENT PROCESSING**
════════════════════════════

**2.1 PCI DSS Compliance Requirements**
---------------------------------------

**Key Rules:**

+----------+-----------------------------------------------------+
| **Rule** | **Requirement**                                     |
+==========+=====================================================+
| 3.2      | Do not store sensitive authentication data (CVV)    |
+----------+-----------------------------------------------------+
| 3.4      | Render PAN unreadable (encryption/tokenization)     |
+----------+-----------------------------------------------------+
| 4.1      | Use strong cryptography for transmission (TLS 1.2+) |
+----------+-----------------------------------------------------+
| 8.2      | Multi-factor authentication for access              |
+----------+-----------------------------------------------------+

**Architecture:**

::

    Passenger Device
           ↓ (HTTPS)
    IFE Payment Gateway (Java)
           ↓ (Tokenization)
    Payment Processor (Stripe/Braintree)
           ↓
    Bank Network

**2.2 Payment Entity**
---------------------

.. code-block:: java

    @Entity
    @Table(name = "transactions")
    public class Transaction {
        @Id
        @GeneratedValue(strategy = GenerationType.UUID)
        private UUID id;
        
        @Column(nullable = false)
        private String seatNumber;
        
        @Column(nullable = false)
        private BigDecimal amount;
        
        @Column(nullable = false)
        private String currency;  // USD, EUR, GBP
        
        @Column(nullable = false)
        private String paymentToken;  // Never store actual card number!
        
        @Enumerated(EnumType.STRING)
        private TransactionStatus status;
        
        private LocalDateTime createdAt;
        private String merchantId;
        private String orderId;
        
        // Getters/Setters...
    }
    
    enum TransactionStatus {
        PENDING, AUTHORIZED, CAPTURED, DECLINED, REFUNDED
    }

**2.3 Payment Service**
----------------------

.. code-block:: java

    @Service
    public class PaymentService {
        @Value("${payment.stripe.secret-key}")
        private String stripeSecretKey;
        
        public Transaction processPayment(PaymentRequest request) {
            // 1. Validate amount
            if (request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("Invalid amount");
            }
            
            // 2. Create transaction record
            Transaction transaction = new Transaction();
            transaction.setSeatNumber(request.getSeatNumber());
            transaction.setAmount(request.getAmount());
            transaction.setCurrency(request.getCurrency());
            transaction.setStatus(TransactionStatus.PENDING);
            transaction.setCreatedAt(LocalDateTime.now());
            
            try {
                // 3. Call payment processor (Stripe)
                Stripe.apiKey = stripeSecretKey;
                
                Map<String, Object> params = new HashMap<>();
                params.put("amount", request.getAmount()
                    .multiply(BigDecimal.valueOf(100)).intValue());  // Cents
                params.put("currency", request.getCurrency().toLowerCase());
                params.put("source", request.getPaymentToken());
                params.put("description", "IFE Purchase - Seat " 
                    + request.getSeatNumber());
                
                Charge charge = Charge.create(params);
                
                // 4. Update transaction
                transaction.setPaymentToken(charge.getId());
                transaction.setStatus(charge.getPaid() 
                    ? TransactionStatus.CAPTURED 
                    : TransactionStatus.DECLINED);
                
            } catch (StripeException e) {
                transaction.setStatus(TransactionStatus.DECLINED);
                log.error("Payment failed: {}", e.getMessage());
            }
            
            return transactionRepository.save(transaction);
        }
        
        public Transaction refundPayment(UUID transactionId) {
            Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new NotFoundException("Transaction not found"));
            
            try {
                Stripe.apiKey = stripeSecretKey;
                Refund refund = Refund.create(
                    Map.of("charge", transaction.getPaymentToken())
                );
                
                transaction.setStatus(TransactionStatus.REFUNDED);
                
            } catch (StripeException e) {
                log.error("Refund failed: {}", e.getMessage());
                throw new PaymentException("Refund failed");
            }
            
            return transactionRepository.save(transaction);
        }
    }

**2.4 Secure Configuration**
----------------------------

**application.properties:**

::

    # Payment API keys (use environment variables in production!)
    payment.stripe.secret-key=${STRIPE_SECRET_KEY}
    payment.stripe.publishable-key=${STRIPE_PUBLISHABLE_KEY}
    
    # Database (encrypted connection)
    spring.datasource.url=jdbc:mysql://localhost:3306/ife_db?useSSL=true
    spring.datasource.username=${DB_USERNAME}
    spring.datasource.password=${DB_PASSWORD}
    
    # JPA
    spring.jpa.hibernate.ddl-auto=validate
    spring.jpa.show-sql=false
    
    # Logging (exclude sensitive data)
    logging.level.com.airline.ife=INFO

════════════════════════════════════════════════════════════════════

📖 **3. JPA/HIBERNATE**
═══════════════════════

**3.1 Entity Relationships**
----------------------------

**One-to-Many: Movie → Reviews**

.. code-block:: java

    @Entity
    public class Movie {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        private String title;
        
        @OneToMany(mappedBy = "movie", cascade = CascadeType.ALL, 
                   orphanRemoval = true)
        private List<Review> reviews = new ArrayList<>();
        
        // Helper method
        public void addReview(Review review) {
            reviews.add(review);
            review.setMovie(this);
        }
    }
    
    @Entity
    public class Review {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        private Integer rating;  // 1-5 stars
        private String comment;
        
        @ManyToOne(fetch = FetchType.LAZY)
        @JoinColumn(name = "movie_id", nullable = false)
        private Movie movie;
        
        // Getters/Setters...
    }

**Many-to-Many: Movie ↔ Categories**

.. code-block:: java

    @Entity
    public class Movie {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        private String title;
        
        @ManyToMany
        @JoinTable(
            name = "movie_category",
            joinColumns = @JoinColumn(name = "movie_id"),
            inverseJoinColumns = @JoinColumn(name = "category_id")
        )
        private Set<Category> categories = new HashSet<>();
    }
    
    @Entity
    public class Category {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        private String name;  // Action, Drama, Comedy
        
        @ManyToMany(mappedBy = "categories")
        private Set<Movie> movies = new HashSet<>();
    }

**3.2 JPQL Queries**
-------------------

.. code-block:: java

    @Repository
    public interface MovieRepository extends JpaRepository<Movie, Long> {
        // Method name query
        List<Movie> findByGenre(String genre);
        
        // JPQL query
        @Query("SELECT m FROM Movie m WHERE m.duration < :maxDuration " +
               "ORDER BY m.releaseDate DESC")
        List<Movie> findShortMovies(@Param("maxDuration") Integer maxDuration);
        
        // Native SQL query
        @Query(value = "SELECT * FROM movies WHERE YEAR(release_date) = :year", 
               nativeQuery = true)
        List<Movie> findMoviesByYear(@Param("year") Integer year);
        
        // Aggregate query
        @Query("SELECT m.genre, COUNT(m) FROM Movie m GROUP BY m.genre")
        List<Object[]> countMoviesByGenre();
    }

**3.3 Transaction Management**
------------------------------

.. code-block:: java

    @Service
    public class OrderService {
        @Autowired
        private OrderRepository orderRepository;
        
        @Autowired
        private InventoryService inventoryService;
        
        @Transactional  // All or nothing
        public Order purchaseMovie(Long movieId, String seatNumber) {
            // 1. Check inventory
            if (!inventoryService.isAvailable(movieId)) {
                throw new OutOfStockException("Movie not available");
            }
            
            // 2. Create order
            Order order = new Order();
            order.setMovieId(movieId);
            order.setSeatNumber(seatNumber);
            order.setStatus(OrderStatus.PENDING);
            
            Order saved = orderRepository.save(order);
            
            // 3. Decrement inventory
            inventoryService.decrementStock(movieId);
            
            // 4. If this throws exception, entire transaction rolls back
            notificationService.sendConfirmation(seatNumber);
            
            return saved;
        }
    }

════════════════════════════════════════════════════════════════════

📖 **4. AIRLINE INTEGRATION APIS**
═══════════════════════════════════

**4.1 NDC (New Distribution Capability)**
-----------------------------------------

**Purpose:** IATA standard for airline content distribution

.. code-block:: java

    @Service
    public class NdcService {
        @Value("${airline.ndc.endpoint}")
        private String ndcEndpoint;
        
        public FlightOffer searchFlights(SearchRequest request) {
            RestTemplate restTemplate = new RestTemplate();
            
            // Build NDC AirShoppingRQ message
            NdcAirShoppingRQ ndcRequest = new NdcAirShoppingRQ();
            ndcRequest.setOrigin(request.getOrigin());
            ndcRequest.setDestination(request.getDestination());
            ndcRequest.setDepartureDate(request.getDepartureDate());
            ndcRequest.setPassengerCount(request.getPassengers());
            
            // Call airline NDC API
            ResponseEntity<NdcAirShoppingRS> response = 
                restTemplate.postForEntity(
                    ndcEndpoint + "/AirShopping",
                    ndcRequest,
                    NdcAirShoppingRS.class
                );
            
            // Parse response
            return convertToFlightOffer(response.getBody());
        }
    }

**4.2 Loyalty Program Integration**
-----------------------------------

.. code-block:: java

    @Service
    public class LoyaltyService {
        public LoyaltyAccount getAccount(String frequentFlyerNumber) {
            // Call airline loyalty API
            RestTemplate restTemplate = new RestTemplate();
            
            String url = "https://api.airline.com/loyalty/accounts/" 
                + frequentFlyerNumber;
            
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + apiKey);
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            ResponseEntity<LoyaltyAccount> response = 
                restTemplate.exchange(url, HttpMethod.GET, entity, 
                                     LoyaltyAccount.class);
            
            return response.getBody();
        }
        
        public void awardMiles(String frequentFlyerNumber, int miles) {
            // Award miles for IFE purchases
            Map<String, Object> request = new HashMap<>();
            request.put("frequentFlyerNumber", frequentFlyerNumber);
            request.put("miles", miles);
            request.put("activityType", "IFE_PURCHASE");
            
            restTemplate.postForEntity(
                loyaltyEndpoint + "/transactions",
                request,
                Void.class
            );
        }
    }

════════════════════════════════════════════════════════════════════

📝 **5. EXAM QUESTIONS**
═════════════════════════

**Q1:** Explain the difference between @Entity, @Service, @Repository, 
and @Controller annotations.

**A1:**

+---------------+------------------------+---------------------------+
| **Annotation**| **Layer**              | **Purpose**               |
+===============+========================+===========================+
| @Entity       | Data Model             | JPA entity (database row) |
+---------------+------------------------+---------------------------+
| @Repository   | Data Access            | Database queries          |
+---------------+------------------------+---------------------------+
| @Service      | Business Logic         | Transactions, logic       |
+---------------+------------------------+---------------------------+
| @Controller   | Presentation (REST API)| HTTP endpoints            |
+---------------+------------------------+---------------------------+

**Example:**

.. code-block:: java

    @Entity  // Maps to "movies" table
    public class Movie { /*...*/ }
    
    @Repository  // Data access
    public interface MovieRepository extends JpaRepository<Movie, Long> {}
    
    @Service  // Business logic
    public class MovieService {
        @Autowired MovieRepository repo;
    }
    
    @RestController  // REST API
    public class MovieController {
        @Autowired MovieService service;
    }

────────────────────────────────────────────────────────────────────

**Q2:** Why should you never store credit card CVV in a database?

**A2:**

**PCI DSS Rule 3.2:** "Do not store sensitive authentication data after 
authorization"

**Sensitive Authentication Data includes:**

- CVV/CVC (Card Verification Value)
- Full magnetic stripe data
- PIN/PIN block

**Why:**

- If database breached, attacker can make fraudulent charges
- PCI DSS violations = fines up to $500,000/month
- Loss of payment processing privileges

**What to store instead:**

- Tokenized card reference (from payment processor)
- Last 4 digits (for display only)
- Card brand (Visa, Mastercard)

**Correct approach:**

.. code-block:: java

    @Entity
    public class PaymentMethod {
        private String token;          // ✅ From Stripe/Braintree
        private String lastFourDigits; // ✅ Safe to store
        private String cardBrand;      // ✅ Safe to store
        
        // ❌ NEVER store these:
        // private String cardNumber;
        // private String cvv;
        // private String expiryDate;
    }

────────────────────────────────────────────────────────────────────

**Q3:** Write a JPA query to find all movies longer than 2 hours released 
in the last year, ordered by rating (highest first).

**A3:**

.. code-block:: java

    @Repository
    public interface MovieRepository extends JpaRepository<Movie, Long> {
        @Query("SELECT m FROM Movie m " +
               "WHERE m.duration > :minDuration " +
               "AND m.releaseDate >= :oneYearAgo " +
               "ORDER BY m.averageRating DESC")
        List<Movie> findLongRecentMovies(
            @Param("minDuration") Integer minDuration,
            @Param("oneYearAgo") LocalDate oneYearAgo
        );
    }
    
    // Usage
    LocalDate oneYearAgo = LocalDate.now().minusYears(1);
    List<Movie> movies = movieRepository.findLongRecentMovies(120, oneYearAgo);

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand Spring Boot auto-configuration
- [ ] Use @Entity for database models
- [ ] Implement JpaRepository for data access
- [ ] Apply @Service for business logic layer
- [ ] Build REST APIs with @RestController
- [ ] Secure APIs with Spring Security
- [ ] Handle transactions with @Transactional
- [ ] Never store CVV (PCI DSS Rule 3.2)
- [ ] Use payment tokens instead of card numbers
- [ ] Implement JPA relationships (OneToMany, ManyToMany)
- [ ] Write JPQL queries for complex searches
- [ ] Integrate with airline NDC APIs
- [ ] Award loyalty miles for purchases
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS for all endpoints

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Spring Boot reduces boilerplate** → Auto-configuration, dependency 
injection, embedded server

2️⃣ **JPA abstracts SQL** → Write findByGenre() instead of SELECT * FROM 
movies WHERE genre = ?

3️⃣ **Never store CVV** → PCI DSS Rule 3.2, use payment processor tokens 
instead

4️⃣ **@Transactional ensures atomicity** → All database operations succeed 
or all rollback

5️⃣ **Relationships cascade operations** → Delete movie → delete reviews 
automatically

6️⃣ **RestTemplate simplifies HTTP** → Call external APIs (NDC, loyalty) 
without low-level code

7️⃣ **Environment variables protect secrets** → ${STRIPE_SECRET_KEY} not 
hardcoded in source

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **JAVA PROGRAMMING COMPLETE**
**Created:** January 14, 2026
**Coverage:** Spring Boot, Payment Processing, JPA, Airline APIs

════════════════════════════════════════════════════════════════════
