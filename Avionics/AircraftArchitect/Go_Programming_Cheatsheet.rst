🐹 **GO PROGRAMMING — Microservices & Concurrency for Aircraft**
═══════════════════════════════════════════════════════════════════

**Context:** Go for aircraft service orchestration and APIs
**Focus:** Goroutines, Channels, Microservices, gRPC
**Use Cases:** IFE backend, API gateways, passenger services

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — GO IN 60 SECONDS**
────────────────────────────────

**Why Go for Aviation:**

+-------------------+------------------------------------------------+
| **Feature**       | **Benefit**                                    |
+===================+================================================+
| Fast compilation  | Rapid development cycles                       |
+-------------------+------------------------------------------------+
| Static binary     | Single executable (no dependencies)            |
+-------------------+------------------------------------------------+
| Goroutines        | Lightweight concurrency (1000s of connections) |
+-------------------+------------------------------------------------+
| Built-in HTTP     | Microservices without frameworks               |
+-------------------+------------------------------------------------+
| Cross-platform    | Linux, Windows, embedded ARM                   |
+-------------------+------------------------------------------------+

**Aviation Use Cases:**

- 🛜 API Gateway (IFE services)
- 🎬 Content Delivery Network (CDN)
- 💳 Payment Processing Gateway
- 📊 Real-time Analytics
- 🔄 Service Orchestration

**Goroutine vs Thread:**

::

    OS Thread:     2 MB stack, kernel scheduled
    Goroutine:     2 KB stack, Go runtime scheduled
    
    Result: Run 10,000+ goroutines on single machine

════════════════════════════════════════════════════════════════════

📖 **1. GO CONCURRENCY**
════════════════════════

**1.1 Goroutines (Lightweight Threads)**
---------------------------------------

**Syntax:** `go functionName()`

.. code-block:: go

    package main
    
    import (
        "fmt"
        "time"
    )
    
    func fetchSensorData(sensorID int) {
        fmt.Printf("Reading sensor %d...\n", sensorID)
        time.Sleep(100 * time.Millisecond)  // Simulate I/O
        fmt.Printf("Sensor %d: 42.0°C\n", sensorID)
    }
    
    func main() {
        // Launch 10 concurrent sensor reads
        for i := 1; i <= 10; i++ {
            go fetchSensorData(i)  // Non-blocking!
        }
        
        time.Sleep(1 * time.Second)  // Wait for goroutines
        fmt.Println("All sensors read")
    }

**Output (concurrent execution):**

::

    Reading sensor 1...
    Reading sensor 3...
    Reading sensor 2...
    ...
    Sensor 1: 42.0°C
    Sensor 3: 42.0°C

**1.2 Channels (Communication Between Goroutines)**
--------------------------------------------------

**Syntax:** `ch := make(chan Type)`

**Basic Channel:**

.. code-block:: go

    func main() {
        ch := make(chan string)
        
        go func() {
            ch <- "GPS data ready"  // Send to channel
        }()
        
        msg := <-ch  // Receive from channel (blocks until data available)
        fmt.Println(msg)
    }

**Aviation Example: Sensor Data Pipeline**

.. code-block:: go

    type SensorReading struct {
        ID    int
        Value float64
        Time  time.Time
    }
    
    // Producer: Read sensors
    func readSensors(out chan<- SensorReading) {
        for i := 1; i <= 100; i++ {
            out <- SensorReading{
                ID:    i,
                Value: float64(i) * 1.5,
                Time:  time.Now(),
            }
            time.Sleep(10 * time.Millisecond)
        }
        close(out)  // Signal completion
    }
    
    // Consumer: Process data
    func processSensors(in <-chan SensorReading) {
        for reading := range in {  // Iterate until channel closed
            if reading.Value > 100.0 {
                fmt.Printf("ALERT: Sensor %d exceeded threshold: %.2f\n",
                    reading.ID, reading.Value)
            }
        }
    }
    
    func main() {
        ch := make(chan SensorReading, 10)  // Buffered channel
        
        go readSensors(ch)
        processSensors(ch)  // Blocks until channel closed
    }

**1.3 Select Statements (Multiplexing Channels)**
------------------------------------------------

**Purpose:** Wait on multiple channels simultaneously

.. code-block:: go

    func main() {
        gps := make(chan string)
        imu := make(chan string)
        timeout := time.After(2 * time.Second)
        
        go func() {
            time.Sleep(500 * time.Millisecond)
            gps <- "GPS: 37.7749°N, 122.4194°W"
        }()
        
        go func() {
            time.Sleep(1 * time.Second)
            imu <- "IMU: Roll=5°, Pitch=2°, Yaw=270°"
        }()
        
        for i := 0; i < 2; i++ {
            select {
            case msg := <-gps:
                fmt.Println("Received:", msg)
            case msg := <-imu:
                fmt.Println("Received:", msg)
            case <-timeout:
                fmt.Println("Timeout!")
                return
            }
        }
    }

**Aviation Example: Multi-Sensor Fusion**

.. code-block:: go

    func sensorFusion() {
        gps := make(chan float64)
        baro := make(chan float64)
        radar := make(chan float64)
        
        go func() { gps <- readGPS() }()
        go func() { baro <- readBarometer() }()
        go func() { radar <- readRadarAltimeter() }()
        
        var altitude float64
        sensorsReceived := 0
        
        for sensorsReceived < 3 {
            select {
            case alt := <-gps:
                fmt.Println("GPS altitude:", alt)
                altitude = alt  // Prefer GPS
                sensorsReceived++
            case alt := <-baro:
                fmt.Println("Baro altitude:", alt)
                if altitude == 0 {
                    altitude = alt  // Fallback to baro
                }
                sensorsReceived++
            case alt := <-radar:
                fmt.Println("Radar altitude:", alt)
                sensorsReceived++
            case <-time.After(1 * time.Second):
                fmt.Println("Sensor timeout")
                return
            }
        }
        
        fmt.Printf("Best altitude estimate: %.2f ft\n", altitude)
    }

**1.4 Context Package (Cancellation Propagation)**
-------------------------------------------------

**Purpose:** Cancel long-running operations

.. code-block:: go

    import "context"
    
    func fetchContentWithTimeout(ctx context.Context, contentID string) error {
        ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
        defer cancel()
        
        resultCh := make(chan string)
        errCh := make(chan error)
        
        go func() {
            // Simulate slow database query
            time.Sleep(3 * time.Second)
            resultCh <- "Movie data"
        }()
        
        select {
        case result := <-resultCh:
            fmt.Println("Got content:", result)
            return nil
        case err := <-errCh:
            return err
        case <-ctx.Done():
            return ctx.Err()  // context.DeadlineExceeded
        }
    }
    
    func main() {
        ctx := context.Background()
        err := fetchContentWithTimeout(ctx, "movie-123")
        if err != nil {
            fmt.Println("Error:", err)
        }
    }

════════════════════════════════════════════════════════════════════

📖 **2. MICROSERVICES PATTERNS**
═════════════════════════════════

**2.1 HTTP Server (REST API)**
------------------------------

.. code-block:: go

    package main
    
    import (
        "encoding/json"
        "log"
        "net/http"
        "time"
    )
    
    type Movie struct {
        ID          string    `json:"id"`
        Title       string    `json:"title"`
        Duration    int       `json:"duration"` // minutes
        ReleaseDate time.Time `json:"release_date"`
    }
    
    var movies = []Movie{
        {"1", "Top Gun: Maverick", 131, time.Date(2022, 5, 27, 0, 0, 0, 0, time.UTC)},
        {"2", "Avatar: The Way of Water", 192, time.Date(2022, 12, 16, 0, 0, 0, 0, time.UTC)},
    }
    
    // GET /movies
    func getMovies(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(movies)
    }
    
    // GET /movies/{id}
    func getMovie(w http.ResponseWriter, r *http.Request) {
        id := r.URL.Query().Get("id")
        
        for _, movie := range movies {
            if movie.ID == id {
                w.Header().Set("Content-Type", "application/json")
                json.NewEncoder(w).Encode(movie)
                return
            }
        }
        
        http.Error(w, "Movie not found", http.StatusNotFound)
    }
    
    func main() {
        http.HandleFunc("/movies", getMovies)
        http.HandleFunc("/movie", getMovie)
        
        log.Println("IFE Content Service listening on :8080")
        log.Fatal(http.ListenAndServe(":8080", nil))
    }

**2.2 Middleware Pattern**
--------------------------

.. code-block:: go

    // Logging middleware
    func loggingMiddleware(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            log.Printf("%s %s", r.Method, r.URL.Path)
            
            next(w, r)  // Call actual handler
            
            log.Printf("Completed in %v", time.Since(start))
        }
    }
    
    // Authentication middleware
    func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            token := r.Header.Get("Authorization")
            if token != "Bearer secret-token" {
                http.Error(w, "Unauthorized", http.StatusUnauthorized)
                return
            }
            next(w, r)
        }
    }
    
    func main() {
        http.HandleFunc("/movies", 
            loggingMiddleware(authMiddleware(getMovies)))
        
        log.Fatal(http.ListenAndServe(":8080", nil))
    }

**2.3 Circuit Breaker (Resilience)**
------------------------------------

**Purpose:** Stop calling failing service to allow recovery

.. code-block:: go

    type CircuitBreaker struct {
        maxFailures int
        timeout     time.Duration
        failures    int
        lastFailure time.Time
        state       string  // "closed", "open", "half-open"
    }
    
    func NewCircuitBreaker(maxFailures int, timeout time.Duration) *CircuitBreaker {
        return &CircuitBreaker{
            maxFailures: maxFailures,
            timeout:     timeout,
            state:       "closed",
        }
    }
    
    func (cb *CircuitBreaker) Call(fn func() error) error {
        if cb.state == "open" {
            if time.Since(cb.lastFailure) > cb.timeout {
                cb.state = "half-open"
                cb.failures = 0
            } else {
                return fmt.Errorf("circuit breaker is open")
            }
        }
        
        err := fn()
        if err != nil {
            cb.failures++
            cb.lastFailure = time.Now()
            
            if cb.failures >= cb.maxFailures {
                cb.state = "open"
            }
            return err
        }
        
        cb.failures = 0
        cb.state = "closed"
        return nil
    }
    
    // Usage
    func main() {
        cb := NewCircuitBreaker(3, 10*time.Second)
        
        for i := 0; i < 10; i++ {
            err := cb.Call(func() error {
                // Call external service
                resp, err := http.Get("http://payment-service/charge")
                if err != nil || resp.StatusCode != 200 {
                    return fmt.Errorf("service unavailable")
                }
                return nil
            })
            
            if err != nil {
                log.Println("Error:", err)
            }
            
            time.Sleep(1 * time.Second)
        }
    }

════════════════════════════════════════════════════════════════════

📖 **3. GRPC (HIGH-PERFORMANCE RPC)**
═════════════════════════════════════

**3.1 Protocol Buffers Definition**
-----------------------------------

**File:** `ife.proto`

.. code-block:: protobuf

    syntax = "proto3";
    
    package ife;
    option go_package = "./ife";
    
    service IFEService {
        rpc GetMovies(EmptyRequest) returns (MovieList);
        rpc StreamContent(ContentRequest) returns (stream ContentChunk);
    }
    
    message EmptyRequest {}
    
    message Movie {
        string id = 1;
        string title = 2;
        int32 duration = 3;
    }
    
    message MovieList {
        repeated Movie movies = 1;
    }
    
    message ContentRequest {
        string content_id = 1;
    }
    
    message ContentChunk {
        bytes data = 1;
        int32 offset = 2;
    }

**Generate Go Code:**

::

    protoc --go_out=. --go-grpc_out=. ife.proto

**3.2 gRPC Server Implementation**
----------------------------------

.. code-block:: go

    package main
    
    import (
        "context"
        "log"
        "net"
        
        "google.golang.org/grpc"
        pb "myapp/ife"  // Generated code
    )
    
    type server struct {
        pb.UnimplementedIFEServiceServer
    }
    
    func (s *server) GetMovies(ctx context.Context, req *pb.EmptyRequest) (*pb.MovieList, error) {
        movies := []*pb.Movie{
            {Id: "1", Title: "Top Gun", Duration: 131},
            {Id: "2", Title: "Avatar", Duration: 192},
        }
        
        return &pb.MovieList{Movies: movies}, nil
    }
    
    func (s *server) StreamContent(req *pb.ContentRequest, stream pb.IFEService_StreamContentServer) error {
        // Simulate streaming movie data
        chunkSize := 1024 * 1024  // 1 MB chunks
        for i := 0; i < 100; i++ {
            chunk := &pb.ContentChunk{
                Data:   make([]byte, chunkSize),
                Offset: int32(i * chunkSize),
            }
            
            if err := stream.Send(chunk); err != nil {
                return err
            }
        }
        
        return nil
    }
    
    func main() {
        lis, err := net.Listen("tcp", ":50051")
        if err != nil {
            log.Fatalf("Failed to listen: %v", err)
        }
        
        s := grpc.NewServer()
        pb.RegisterIFEServiceServer(s, &server{})
        
        log.Println("gRPC server listening on :50051")
        if err := s.Serve(lis); err != nil {
            log.Fatalf("Failed to serve: %v", err)
        }
    }

**3.3 gRPC Client**
------------------

.. code-block:: go

    package main
    
    import (
        "context"
        "io"
        "log"
        
        "google.golang.org/grpc"
        pb "myapp/ife"
    )
    
    func main() {
        conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
        if err != nil {
            log.Fatalf("Failed to connect: %v", err)
        }
        defer conn.Close()
        
        client := pb.NewIFEServiceClient(conn)
        
        // Unary RPC
        resp, err := client.GetMovies(context.Background(), &pb.EmptyRequest{})
        if err != nil {
            log.Fatalf("GetMovies failed: %v", err)
        }
        
        for _, movie := range resp.Movies {
            log.Printf("Movie: %s (%d min)", movie.Title, movie.Duration)
        }
        
        // Streaming RPC
        stream, err := client.StreamContent(context.Background(), &pb.ContentRequest{ContentId: "movie-1"})
        if err != nil {
            log.Fatalf("StreamContent failed: %v", err)
        }
        
        for {
            chunk, err := stream.Recv()
            if err == io.EOF {
                break
            }
            if err != nil {
                log.Fatalf("Stream error: %v", err)
            }
            
            log.Printf("Received chunk at offset %d (%d bytes)", 
                chunk.Offset, len(chunk.Data))
        }
    }

════════════════════════════════════════════════════════════════════

📖 **4. ERROR HANDLING**
════════════════════════

**4.1 Basic Error Handling**
----------------------------

.. code-block:: go

    import "errors"
    
    func readSensor(id int) (float64, error) {
        if id < 0 {
            return 0, errors.New("invalid sensor ID")
        }
        
        // Simulate sensor read
        return 42.5, nil
    }
    
    func main() {
        value, err := readSensor(-1)
        if err != nil {
            log.Fatal("Error:", err)
        }
        
        fmt.Println("Sensor value:", value)
    }

**4.2 Error Wrapping (errors.Is / errors.As)**
----------------------------------------------

.. code-block:: go

    import (
        "errors"
        "fmt"
    )
    
    var ErrSensorTimeout = errors.New("sensor timeout")
    var ErrSensorFault = errors.New("sensor fault")
    
    func readSensor(id int) error {
        // Simulate timeout
        return fmt.Errorf("sensor %d failed: %w", id, ErrSensorTimeout)
    }
    
    func main() {
        err := readSensor(42)
        
        // Check if error is specific type
        if errors.Is(err, ErrSensorTimeout) {
            fmt.Println("Timeout occurred, retrying...")
        }
        
        // Print full error chain
        fmt.Println("Error:", err)
        // Output: sensor 42 failed: sensor timeout
    }

**4.3 Custom Error Types**
--------------------------

.. code-block:: go

    type SensorError struct {
        ID      int
        Message string
        Code    int
    }
    
    func (e *SensorError) Error() string {
        return fmt.Sprintf("sensor %d error (code %d): %s", 
            e.ID, e.Code, e.Message)
    }
    
    func readSensor(id int) error {
        return &SensorError{
            ID:      id,
            Message: "communication timeout",
            Code:    1001,
        }
    }
    
    func main() {
        err := readSensor(42)
        
        var sensorErr *SensorError
        if errors.As(err, &sensorErr) {
            fmt.Printf("Sensor %d failed with code %d\n", 
                sensorErr.ID, sensorErr.Code)
        }
    }

════════════════════════════════════════════════════════════════════

📝 **5. EXAM QUESTIONS**
═════════════════════════

**Q1:** You need to read 100 sensors concurrently and aggregate results. 
Implement this pattern in Go.

**A1:**

.. code-block:: go

    func readSensors() []float64 {
        numSensors := 100
        results := make(chan float64, numSensors)
        
        // Launch goroutines
        for i := 0; i < numSensors; i++ {
            go func(sensorID int) {
                value := readSensor(sensorID)  // Blocking I/O
                results <- value
            }(i)
        }
        
        // Collect results
        var readings []float64
        for i := 0; i < numSensors; i++ {
            readings = append(readings, <-results)
        }
        close(results)
        
        return readings
    }

**Key:** Goroutines run concurrently, channel aggregates results

────────────────────────────────────────────────────────────────────

**Q2:** Explain the difference between buffered and unbuffered channels.

**A2:**

**Unbuffered Channel:** `ch := make(chan int)`

- Send blocks until receiver ready
- Synchronous communication
- Use when you need coordination

**Buffered Channel:** `ch := make(chan int, 10)`

- Send only blocks if buffer full
- Asynchronous communication
- Use for producer/consumer pattern

**Example:**

.. code-block:: go

    // Unbuffered: This DEADLOCKS (no receiver ready)
    ch := make(chan int)
    ch <- 42  // Blocks forever!
    
    // Buffered: This works (buffer has space)
    ch := make(chan int, 1)
    ch <- 42  // Returns immediately
    fmt.Println(<-ch)  // Receive later

────────────────────────────────────────────────────────────────────

**Q3:** Implement a simple circuit breaker for HTTP calls.

**A3:** See Section 2.3 for full implementation. Key points:

- **closed:** Normal operation
- **open:** Stop calling service (fail fast)
- **half-open:** Test if service recovered

**State Transitions:**

::

    closed → (failures >= threshold) → open
    open → (timeout expired) → half-open
    half-open → (success) → closed
    half-open → (failure) → open

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand goroutines vs OS threads
- [ ] Use channels for goroutine communication
- [ ] Apply select for multiplexing channels
- [ ] Implement context for cancellation
- [ ] Build REST APIs with net/http
- [ ] Add middleware for logging/auth
- [ ] Implement circuit breaker pattern
- [ ] Define gRPC services with protobuf
- [ ] Generate Go code from .proto files
- [ ] Handle errors with errors.Is/As
- [ ] Wrap errors with fmt.Errorf and %w
- [ ] Use buffered channels appropriately
- [ ] Close channels when done producing

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Goroutines are cheap** → Launch 10,000+ on single machine (2 KB stack each)

2️⃣ **Channels enable safe communication** → Share memory by communicating, 
not communicate by sharing memory

3️⃣ **Select multiplexes channels** → Wait on multiple operations simultaneously 
(GPS, IMU, timeout)

4️⃣ **Context propagates cancellation** → Timeout/cancel long-running operations 
across goroutines

5️⃣ **Built-in HTTP server** → No frameworks needed for microservices

6️⃣ **gRPC for performance** → Binary protocol, streaming, 10x faster than REST

7️⃣ **Error wrapping preserves context** → Use fmt.Errorf with %w to maintain 
error chain

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **GO PROGRAMMING COMPLETE**
**Created:** January 14, 2026
**Coverage:** Concurrency, Microservices, gRPC, Error Handling

════════════════════════════════════════════════════════════════════
