⚡ **C++ MODERN FEATURES — C++17/20/23 for Aviation Software**
═══════════════════════════════════════════════════════════════════

**Context:** Modern C++ for safety-critical avionics development
**Focus:** C++17, C++20, C++23 features with aviation patterns
**Standards:** ISO/IEC 14882, MISRA C++:2023, AUTOSAR C++14

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — MODERN C++ IN 60 SECONDS**
────────────────────────────────────────

**Feature Comparison:**

+-----------------------------+--------+--------+--------+
| **Feature**                 | **C++17**| **C++20**| **C++23**|
+=============================+========+========+========+
| Structured bindings         | ✅     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| if constexpr                | ✅     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| std::optional               | ✅     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| std::variant                | ✅     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| Fold expressions            | ✅     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| Concepts                    | ❌     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| Ranges                      | ❌     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| Coroutines                  | ❌     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| Modules                     | ❌     | ✅     | ✅     |
+-----------------------------+--------+--------+--------+
| std::expected               | ❌     | ❌     | ✅     |
+-----------------------------+--------+--------+--------+
| std::mdspan                 | ❌     | ❌     | ✅     |
+-----------------------------+--------+--------+--------+
| Deducing this               | ❌     | ❌     | ✅     |
+-----------------------------+--------+--------+--------+

**Aviation Priority Features:**

1. **std::optional** - Replace NULL checks
2. **std::variant** - Type-safe unions (MISRA compliant)
3. **Concepts** - Template constraints
4. **std::expected** - Error handling without exceptions

════════════════════════════════════════════════════════════════════

📖 **1. C++17 FEATURES**
════════════════════════

**1.1 Structured Bindings**
---------------------------

**Before C++17:**

.. code-block:: cpp

    std::pair<int, std::string> getSensorData() {
        return {42, "GPS"};
    }
    
    auto result = getSensorData();
    int id = result.first;          // Unclear names
    std::string type = result.second;

**With C++17:**

.. code-block:: cpp

    auto [id, type] = getSensorData();  // Clear intent
    std::cout << "Sensor " << id << " (" << type << ")\n";

**Aviation Example:**

.. code-block:: cpp

    struct FlightData {
        double altitude;  // feet
        double airspeed;  // knots
        double heading;   // degrees
    };
    
    FlightData getFlightData() {
        return {35000.0, 450.0, 270.0};
    }
    
    auto [alt, speed, hdg] = getFlightData();
    if (alt > 40000.0) {
        logWarning("Altitude exceeds service ceiling");
    }

**1.2 if constexpr (Compile-Time Conditionals)**
------------------------------------------------

**Purpose:** Eliminate dead code branches at compile time

.. code-block:: cpp

    template<typename T>
    void processSensorData(T value) {
        if constexpr (std::is_integral_v<T>) {
            // Integer path (compiled only for int types)
            std::cout << "Integer sensor: " << value << "\n";
        } else if constexpr (std::is_floating_point_v<T>) {
            // Float path (compiled only for double/float)
            std::cout << "Analog sensor: " << std::fixed 
                      << std::setprecision(2) << value << "\n";
        } else {
            static_assert(false, "Unsupported sensor type");
        }
    }
    
    processSensorData(42);      // Integer path only
    processSensorData(3.14);    // Float path only

**Aviation Use Case: ARINC 429 Word Parsing**

.. code-block:: cpp

    template<typename DataType>
    DataType parseARINC429(uint32_t word) {
        if constexpr (std::is_same_v<DataType, double>) {
            // BNR (Binary) format
            int32_t signedValue = static_cast<int32_t>(word & 0x1FFFFF);
            return signedValue * 0.000171661;  // LSB scaling
        } else if constexpr (std::is_same_v<DataType, int>) {
            // BCD (Binary Coded Decimal) format
            return ((word >> 8) & 0xF) * 10 + ((word >> 4) & 0xF);
        }
    }

**1.3 std::optional (Nullable Values)**
---------------------------------------

**Replaces:** NULL pointers, magic values (-1, 0xFFFF)

**Before:**

.. code-block:: cpp

    // Unsafe: Returns -1 on error (but -1 could be valid altitude!)
    int getAltitude() {
        if (gpsNotAvailable) return -1;
        return currentAltitude;
    }

**With std::optional:**

.. code-block:: cpp

    #include <optional>
    
    std::optional<int> getAltitude() {
        if (gpsNotAvailable) return std::nullopt;
        return currentAltitude;
    }
    
    // Usage
    if (auto alt = getAltitude()) {
        std::cout << "Altitude: " << *alt << " feet\n";
    } else {
        std::cout << "GPS unavailable\n";
    }
    
    // Or with value_or
    int alt = getAltitude().value_or(0);  // Default to 0

**Aviation Example: Sensor Fusion**

.. code-block:: cpp

    class NavigationSystem {
        std::optional<double> gpsAltitude;
        std::optional<double> baroAltitude;
        std::optional<double> radarAltitude;
        
    public:
        double getBestAltitude() {
            // Priority: GPS > Baro > Radar > Default
            return gpsAltitude
                .or_else([this]() { return baroAltitude; })
                .or_else([this]() { return radarAltitude; })
                .value_or(0.0);
        }
    };

**1.4 std::variant (Type-Safe Unions)**
---------------------------------------

**Replaces:** C unions (MISRA C++ Rule 9-5-1: unions shall not be used)

**Before (Unsafe):**

.. code-block:: cpp

    union SensorData {
        int intValue;
        double doubleValue;
        char stringValue[32];
    };  // No type safety!

**With std::variant:**

.. code-block:: cpp

    #include <variant>
    
    using SensorData = std::variant<int, double, std::string>;
    
    void processSensor(const SensorData& data) {
        std::visit([](auto&& value) {
            using T = std::decay_t<decltype(value)>;
            if constexpr (std::is_same_v<T, int>) {
                std::cout << "Discrete: " << value << "\n";
            } else if constexpr (std::is_same_v<T, double>) {
                std::cout << "Analog: " << value << "\n";
            } else {
                std::cout << "Status: " << value << "\n";
            }
        }, data);
    }
    
    SensorData temp = 72.5;
    SensorData status = std::string("OK");
    processSensor(temp);    // Analog: 72.5
    processSensor(status);  // Status: OK

**Aviation Example: ARINC 429 Label Handler**

.. code-block:: cpp

    using ARINC429Data = std::variant<
        double,        // BNR (altitude, airspeed)
        int,           // BCD (discrete data)
        std::string    // Text (status messages)
    >;
    
    ARINC429Data decodeLabel(uint8_t label, uint32_t word) {
        switch (label) {
            case 0203:  // Altitude
                return parseARINC429<double>(word);
            case 0206:  // Airspeed
                return parseARINC429<double>(word);
            case 0270:  // Discrete status
                return parseARINC429<int>(word);
            default:
                return std::string("UNKNOWN");
        }
    }

**1.5 std::filesystem (Path Manipulation)**
-------------------------------------------

**Before:** String manipulation with strcpy, strcat (unsafe)

**With C++17:**

.. code-block:: cpp

    #include <filesystem>
    namespace fs = std::filesystem;
    
    // Aviation log file management
    void rotateLogs(const fs::path& logDir) {
        for (const auto& entry : fs::directory_iterator(logDir)) {
            if (entry.is_regular_file() && 
                entry.path().extension() == ".log") {
                
                auto size = fs::file_size(entry);
                if (size > 100'000'000) {  // 100 MB
                    fs::path archive = entry.path();
                    archive.replace_extension(".log.old");
                    fs::rename(entry, archive);
                }
            }
        }
    }

════════════════════════════════════════════════════════════════════

📖 **2. C++20 FEATURES**
════════════════════════

**2.1 Concepts (Template Constraints)**
---------------------------------------

**Purpose:** Readable error messages for template failures

**Before (Cryptic Errors):**

.. code-block:: cpp

    template<typename T>
    T add(T a, T b) { return a + b; }
    
    struct Sensor { int id; };
    add(Sensor{1}, Sensor{2});  // 500-line error message!

**With Concepts:**

.. code-block:: cpp

    #include <concepts>
    
    template<typename T>
    concept Numeric = std::integral<T> || std::floating_point<T>;
    
    template<Numeric T>
    T add(T a, T b) { return a + b; }
    
    add(Sensor{1}, Sensor{2});  // Clear error: "Sensor does not satisfy Numeric"

**Aviation Example: Sensor Concept**

.. code-block:: cpp

    template<typename T>
    concept Sensor = requires(T sensor) {
        { sensor.read() } -> std::convertible_to<double>;
        { sensor.getId() } -> std::convertible_to<int>;
        { sensor.isValid() } -> std::same_as<bool>;
    };
    
    template<Sensor S>
    class SensorMonitor {
        S sensor;
    public:
        void update() {
            if (sensor.isValid()) {
                double value = sensor.read();
                logData(sensor.getId(), value);
            }
        }
    };
    
    // GPS class must implement read(), getId(), isValid()
    class GPSSensor {
    public:
        double read() { return latitude; }
        int getId() { return 42; }
        bool isValid() { return fixQuality > 0; }
    private:
        double latitude;
        int fixQuality;
    };

**2.2 Ranges (Lazy Evaluation)**
--------------------------------

**Before (Eager Evaluation):**

.. code-block:: cpp

    std::vector<int> sensorIds = getSensorIds();
    std::vector<int> activeIds;
    
    // Step 1: Filter
    for (int id : sensorIds) {
        if (isSensorActive(id)) activeIds.push_back(id);
    }
    
    // Step 2: Transform
    std::vector<double> readings;
    for (int id : activeIds) {
        readings.push_back(readSensor(id));
    }
    
    // Step 3: Compute average
    double sum = 0;
    for (double r : readings) sum += r;
    double avg = sum / readings.size();

**With Ranges (Lazy):**

.. code-block:: cpp

    #include <ranges>
    namespace rng = std::ranges;
    namespace views = std::views;
    
    auto sensorIds = getSensorIds();
    
    double avg = sensorIds
        | views::filter([](int id) { return isSensorActive(id); })
        | views::transform([](int id) { return readSensor(id); })
        | views::take(10)  // Only first 10 sensors
        | rng::to<std::vector>();  // Materialize
    
    double sum = rng::fold_left(avg, 0.0, std::plus{});
    double average = sum / avg.size();

**Aviation Example: Filter Valid ARINC 429 Words**

.. code-block:: cpp

    std::vector<uint32_t> arinc429Buffer = receiveWords();
    
    auto validWords = arinc429Buffer
        | views::filter([](uint32_t word) {
            uint8_t ssm = (word >> 29) & 0x3;  // Sign/Status Matrix
            return ssm != 0b00;  // Not "Failure Warning"
        })
        | views::transform([](uint32_t word) {
            return parseARINC429<double>(word);
        });
    
    for (double value : validWords) {
        processData(value);
    }

**2.3 Coroutines (Async/Await)**
--------------------------------

**Purpose:** Simplify asynchronous code

**Basic Coroutine:**

.. code-block:: cpp

    #include <coroutine>
    
    struct Task {
        struct promise_type {
            Task get_return_object() { return {}; }
            std::suspend_never initial_suspend() { return {}; }
            std::suspend_never final_suspend() noexcept { return {}; }
            void return_void() {}
            void unhandled_exception() {}
        };
    };
    
    Task loadSensorDataAsync() {
        std::cout << "Starting sensor read...\n";
        co_await std::suspend_always{};  // Yield control
        std::cout << "Sensor data ready\n";
    }

**Aviation Use Case:** Non-blocking sensor reads (Note: Coroutines may not be 
DO-178C certifiable yet—consult certification authorities)

**2.4 Modules (Replacement for Headers)**
-----------------------------------------

**Before:**

.. code-block:: cpp

    // sensor.h
    #ifndef SENSOR_H
    #define SENSOR_H
    class Sensor { /*...*/ };
    #endif
    
    // sensor.cpp
    #include "sensor.h"

**With Modules:**

.. code-block:: cpp

    // sensor.cpp
    export module sensor;
    
    export class Sensor {
    public:
        double read();
    };
    
    // main.cpp
    import sensor;  // No header guards needed!
    
    int main() {
        Sensor s;
        s.read();
    }

**Benefits:**

- Faster compilation (no repeated header parsing)
- True encapsulation (internals hidden)
- No macro leakage

════════════════════════════════════════════════════════════════════

📖 **3. C++23 FEATURES**
════════════════════════

**3.1 std::expected (Error Handling)**
--------------------------------------

**Purpose:** Return value OR error (monadic error handling)

**Replaces:** Exceptions (forbidden in avionics), error codes

**Before:**

.. code-block:: cpp

    enum class Error { SENSOR_FAULT, TIMEOUT };
    
    std::pair<double, Error> readAltitude() {
        if (sensorFault) return {0.0, Error::SENSOR_FAULT};
        return {altitude, Error::NONE};
    }
    
    auto [alt, err] = readAltitude();
    if (err != Error::NONE) { /* handle */ }

**With std::expected:**

.. code-block:: cpp

    #include <expected>
    
    std::expected<double, Error> readAltitude() {
        if (sensorFault) return std::unexpected(Error::SENSOR_FAULT);
        return altitude;
    }
    
    // Usage
    auto result = readAltitude();
    if (result) {
        std::cout << "Altitude: " << *result << "\n";
    } else {
        std::cout << "Error: " << static_cast<int>(result.error()) << "\n";
    }
    
    // Chaining (monadic operations)
    auto altitude = readAltitude()
        .and_then([](double alt) { return validateAltitude(alt); })
        .or_else([](Error e) { return getBackupAltitude(); });

**Aviation Example: Multi-Sensor Fusion**

.. code-block:: cpp

    enum class SensorError { FAULT, TIMEOUT, OUT_OF_RANGE };
    
    std::expected<double, SensorError> readGPS() { /*...*/ }
    std::expected<double, SensorError> readBarometer() { /*...*/ }
    std::expected<double, SensorError> readRadar() { /*...*/ }
    
    std::expected<double, SensorError> getBestAltitude() {
        return readGPS()
            .or_else([](auto) { return readBarometer(); })
            .or_else([](auto) { return readRadar(); })
            .or_else([](auto) -> std::expected<double, SensorError> {
                return std::unexpected(SensorError::FAULT);
            });
    }

**3.2 std::mdspan (Multi-Dimensional Arrays)**
----------------------------------------------

**Purpose:** View over multi-dimensional data (zero-copy)

**Before:**

.. code-block:: cpp

    double imageData[1920][1080][3];  // RGB image
    
    void processPixel(double* data, int row, int col, int channel) {
        int index = row * 1080 * 3 + col * 3 + channel;
        data[index] = /* process */;
    }

**With std::mdspan:**

.. code-block:: cpp

    #include <mdspan>
    
    std::mdspan<double, std::extents<1920, 1080, 3>> image(imageData);
    
    void processPixel(auto image, int row, int col, int channel) {
        image[row, col, channel] = /* process */;  // Clear intent!
    }

**Aviation Example: Camera Sensor Data**

.. code-block:: cpp

    // 4K camera: 3840x2160 RGB
    std::vector<uint8_t> cameraBuffer(3840 * 2160 * 3);
    std::mdspan<uint8_t, std::extents<3840, 2160, 3>> frame(cameraBuffer.data());
    
    // Process specific region of interest
    for (int y = 500; y < 1000; ++y) {
        for (int x = 1000; x < 2000; ++x) {
            uint8_t red = frame[x, y, 0];
            uint8_t green = frame[x, y, 1];
            uint8_t blue = frame[x, y, 2];
            // Detect runway markings...
        }
    }

**3.3 Deducing this (Explicit Object Parameters)**
--------------------------------------------------

**Purpose:** Avoid code duplication for const/non-const overloads

**Before:**

.. code-block:: cpp

    class Sensor {
        std::vector<double> data;
    public:
        auto getData() & { return data; }
        auto getData() const& { return data; }
        auto getData() && { return std::move(data); }
    };

**With Deducing this:**

.. code-block:: cpp

    class Sensor {
        std::vector<double> data;
    public:
        template<typename Self>
        auto getData(this Self&& self) {
            return std::forward<Self>(self).data;
        }
    };
    // Automatically handles &, const&, &&

════════════════════════════════════════════════════════════════════

📖 **4. AVIATION-SPECIFIC PATTERNS**
═════════════════════════════════════

**4.1 Real-Time Constraints**
-----------------------------

**Challenge:** Deterministic execution, no dynamic allocation in flight loop

**Pattern: Pre-allocate Resources**

.. code-block:: cpp

    class FlightControlSystem {
        // Fixed-size containers (no heap allocation)
        std::array<double, 100> sensorHistory;
        size_t currentIndex = 0;
        
    public:
        void recordSensorData(double value) {
            sensorHistory[currentIndex] = value;
            currentIndex = (currentIndex + 1) % sensorHistory.size();
        }
        
        double getAverage() const {
            return std::accumulate(sensorHistory.begin(), 
                                   sensorHistory.end(), 0.0) 
                   / sensorHistory.size();
        }
    };

**4.2 Memory Management**
-------------------------

**MISRA C++ Rules:**

- Rule 18-4-1: Dynamic heap allocation shall not be used
- Rule 18-5-2: Memory allocation/deallocation functions shall not be used

**Pattern: Stack Allocation + Fixed-Size Containers**

.. code-block:: cpp

    // ❌ Forbidden in flight-critical code
    std::vector<double> data;
    data.push_back(42.0);  // May allocate on heap!
    
    // ✅ Allowed
    std::array<double, 100> data;
    data[0] = 42.0;
    
    // ✅ Allowed with static storage
    static std::array<double, 1000> sensorBuffer;

**4.3 MISRA C++ Compliance**
----------------------------

**Key Rules:**

+------------+---------------------------------------------------+
| **Rule**   | **Description**                                   |
+============+===================================================+
| 5-0-15     | No pointer arithmetic (use iterators)             |
+------------+---------------------------------------------------+
| 5-2-2      | No C-style casts (use static_cast)                |
+------------+---------------------------------------------------+
| 18-4-1     | No dynamic heap allocation                        |
+------------+---------------------------------------------------+
| 27-0-1     | No time functions (undefined in ISO C++)          |
+------------+---------------------------------------------------+

**Example:**

.. code-block:: cpp

    // ❌ Violation
    int* ptr = (int*)&sensorData;  // C-style cast
    ptr++;  // Pointer arithmetic
    
    // ✅ Compliant
    auto& data = reinterpret_cast<int&>(sensorData);
    auto it = data.begin();
    std::advance(it, 1);

════════════════════════════════════════════════════════════════════

📖 **5. SMART POINTERS BEST PRACTICES**
════════════════════════════════════════

**5.1 std::unique_ptr (Exclusive Ownership)**
---------------------------------------------

**Use When:** Object has single owner

.. code-block:: cpp

    class SensorDriver {
        std::unique_ptr<HardwareInterface> hw;
        
    public:
        SensorDriver() : hw(std::make_unique<HardwareInterface>()) {}
        
        // Move semantics (transfer ownership)
        std::unique_ptr<HardwareInterface> releaseHardware() {
            return std::move(hw);
        }
    };

**5.2 std::shared_ptr (Shared Ownership)**
------------------------------------------

**Use When:** Multiple owners (e.g., callbacks, caches)

.. code-block:: cpp

    class FlightDataRecorder {
        std::vector<std::shared_ptr<FlightData>> dataLog;
        
    public:
        void record(std::shared_ptr<FlightData> data) {
            dataLog.push_back(data);  // Increment ref count
        }
    };
    
    // Multiple systems can share same data
    auto data = std::make_shared<FlightData>();
    recorder.record(data);
    display.update(data);  // Both keep data alive

**5.3 Avoid std::shared_ptr in Real-Time Code**
-----------------------------------------------

**Issue:** Reference counting has overhead (atomic operations)

**Solution:** Pre-allocate and use std::array or static allocation

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
═════════════════════════

**Q1:** You need to parse ARINC 429 words that can contain BNR (double), 
BCD (int), or text (string). Which C++17 feature is best?

**A1:** **std::variant**

**Why:** Type-safe union replacement, MISRA C++ compliant

.. code-block:: cpp

    using ARINC429Data = std::variant<double, int, std::string>;
    
    ARINC429Data parseWord(uint32_t word, uint8_t label) {
        if (label < 0200) return parseARINC429<double>(word);
        else if (label < 0300) return parseARINC429<int>(word);
        else return std::string("STATUS");
    }
    
    // Type-safe access
    std::visit([](auto&& value) {
        // Handle each type...
    }, data);

────────────────────────────────────────────────────────────────────

**Q2:** Your team wants to use exceptions for error handling in 
flight-critical code. What C++23 feature provides an alternative?

**A2:** **std::expected<T, E>**

**Why:** Returns value OR error without exceptions

.. code-block:: cpp

    std::expected<double, SensorError> readAltimeter() {
        if (sensorFault) return std::unexpected(SensorError::FAULT);
        return altitudeValue;
    }
    
    auto result = readAltimeter();
    if (result) {
        processAltitude(*result);
    } else {
        handleError(result.error());
    }

**Better than exceptions because:**

- No stack unwinding overhead
- Deterministic performance
- DO-178C certifiable (no runtime surprises)

────────────────────────────────────────────────────────────────────

**Q3:** You're writing a sensor abstraction that must work with any type 
implementing read(), getId(), isValid(). Which C++20 feature enforces this?

**A3:** **Concepts**

.. code-block:: cpp

    template<typename T>
    concept Sensor = requires(T sensor) {
        { sensor.read() } -> std::convertible_to<double>;
        { sensor.getId() } -> std::convertible_to<int>;
        { sensor.isValid() } -> std::same_as<bool>;
    };
    
    template<Sensor S>
    class SensorMonitor {
        S sensor;
    public:
        void update() {
            if (sensor.isValid()) {
                logData(sensor.getId(), sensor.read());
            }
        }
    };

**Benefits:**

- Clear compile errors ("GPSSensor does not satisfy Sensor")
- Self-documenting interfaces
- Better than SFINAE (unreadable error messages)

────────────────────────────────────────────────────────────────────

**Q4:** MISRA C++ forbids dynamic heap allocation. Rewrite this code:

.. code-block:: cpp

    std::vector<double> sensorReadings;
    sensorReadings.push_back(altitude);

**A4:** Use **std::array** or pre-allocated buffer

.. code-block:: cpp

    // Fixed-size container (stack allocation)
    std::array<double, 1000> sensorReadings;
    size_t count = 0;
    
    void addReading(double value) {
        if (count < sensorReadings.size()) {
            sensorReadings[count++] = value;
        } else {
            // Handle overflow (e.g., circular buffer)
            sensorReadings[count % sensorReadings.size()] = value;
            count++;
        }
    }

**Alternative: Static allocation**

.. code-block:: cpp

    static std::array<double, 1000> sensorReadings;
    // Lives in .bss segment, not heap

────────────────────────────────────────────────────────────────────

**Q5:** Explain structured bindings and show aviation use case.

**A5:** **Structured bindings** decompose tuple-like objects

**Before:**

.. code-block:: cpp

    std::tuple<double, double, double> getPosition() {
        return {latitude, longitude, altitude};
    }
    
    auto pos = getPosition();
    double lat = std::get<0>(pos);  // Unclear
    double lon = std::get<1>(pos);
    double alt = std::get<2>(pos);

**With structured bindings:**

.. code-block:: cpp

    auto [lat, lon, alt] = getPosition();  // Clear intent!
    
    if (lat > 45.0 && lat < 50.0) {
        // Aircraft over northern US
    }

**Aviation Example: Sensor Fusion**

.. code-block:: cpp

    struct SensorReading {
        double value;
        double confidence;  // 0.0 to 1.0
        uint64_t timestamp;
    };
    
    SensorReading readGPS() { /*...*/ }
    SensorReading readBarometer() { /*...*/ }
    
    auto [gps_val, gps_conf, gps_time] = readGPS();
    auto [baro_val, baro_conf, baro_time] = readBarometer();
    
    // Weighted average by confidence
    double fused = (gps_val * gps_conf + baro_val * baro_conf) 
                   / (gps_conf + baro_conf);

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Replace NULL checks with std::optional
- [ ] Use std::variant instead of C unions
- [ ] Apply concepts to template APIs
- [ ] Adopt std::expected for error handling (C++23)
- [ ] Use structured bindings for multi-value returns
- [ ] Apply if constexpr for template specialization
- [ ] Leverage ranges for data pipelines
- [ ] Pre-allocate with std::array (avoid heap)
- [ ] Use std::unique_ptr for exclusive ownership
- [ ] Avoid std::shared_ptr in real-time loops
- [ ] Check MISRA C++ compliance with static analysis
- [ ] Benchmark performance impact of new features
- [ ] Update coding standards document
- [ ] Train team on modern C++ features

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **std::optional eliminates NULL checks** → Safer than pointers or 
magic values (-1, 0xFFFF)

2️⃣ **std::variant replaces C unions** → Type-safe, MISRA C++ compliant, 
prevents undefined behavior

3️⃣ **Concepts improve error messages** → "Type T does not satisfy Sensor" 
vs 500-line template error

4️⃣ **std::expected enables error handling without exceptions** → DO-178C 
certifiable, deterministic performance

5️⃣ **Avoid heap allocation in flight-critical code** → Use std::array, 
static allocation, MISRA C++ Rule 18-4-1

6️⃣ **Structured bindings improve readability** → `auto [lat, lon, alt]` 
clearer than std::get<0>

7️⃣ **Modern C++ is certifiable** → C++17/20 features compatible with 
DO-178C if used carefully

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **C++ MODERN FEATURES COMPLETE**
**Created:** January 14, 2026
**Coverage:** C++17/20/23, Aviation Patterns, MISRA Compliance

════════════════════════════════════════════════════════════════════
