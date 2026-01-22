
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **Safe Hardware Acceleration API (SHWA)** – Comprehensive cheatsheet for AUTOSAR Adaptive Platform Safe Hardware Acceleration API (ara::shwa) – Release R25-11, covering GPU/FPGA/DSP acceleration, parallel computing, device management, and safety patterns for ASIL-rated systems.

📌 1. Safe HWA API Overview – Purpose & Vision

**What is Safe Hardware Acceleration API?**

The Safe Hardware Acceleration API (SHWA) provides a standardized C++ interface for utilizing hardware accelerators (GPU, FPGA, DSP, NPU) in safety-critical automotive applications. It enables:

- **Hardware abstraction** – Uniform API across different accelerator types
- **Safety-compliant acceleration** – ASIL-B/D rated parallel computing
- **Dynamic device selection** – Runtime selection of optimal accelerator
- **Portable kernels** – Write once, run on GPU/FPGA/DSP
- **Memory management** – Safe buffer handling with safety mechanisms

| Aspect                    | Description                                              | Key Benefit                        |
|---------------------------|----------------------------------------------------------|------------------------------------|
| **Namespace**             | ara::shwa                                                | All SHWA APIs in ara::shwa         |
| **Release**               | R25-11 (first stable release R23-11)                     | Production-ready as of 2024        |
| **Primary Use**           | ADAS sensor fusion, image processing, AI inference       | 10-100x acceleration               |
| **Safety**                | ASIL-B/D compliant                                       | Certified for safety-critical use  |
| **Inspired by**           | SYCL (Khronos standard)                                  | Modern C++ parallel programming    |

📌 2. Core SHWA Concepts

⭐ **2.1 Device**

A Device represents a hardware accelerator available on the platform.

.. code-block:: cpp

    // Device types:
    // - GPU (Graphics Processing Unit)
    // - FPGA (Field Programmable Gate Array)
    // - DSP (Digital Signal Processor)
    // - NPU (Neural Processing Unit)
    // - CPU (fallback)
    
    namespace ara::shwa {
        class Device {
            // Query device capabilities
            // Submit work to device
            // Monitor device health
        };
    }

**2.2 Queue**

A Queue is a command queue for submitting tasks to a Device.

⭐ .. code-block:: cpp

    namespace ara::shwa {
        class Queue {
            // Submit kernel execution
            // Synchronize execution
            // Handle asynchronous operations
        };
    }

**2.3 Buffer**

A Buffer represents data storage accessible by both host (CPU) and device (accelerator).

.. code-block:: cpp

    namespace ara::shwa {
        template<typename T>
        class Buffer {
            // Allocate memory
            // Transfer data between host and device
            // Manage buffer lifecycle
        };
    }

⭐ **2.4 Accessor**

An Accessor provides safe access to Buffer data from kernels.

.. code-block:: cpp

    namespace ara::shwa {
        template<typename T, AccessMode Mode>
        class Accessor {
            // Read or write access to buffer
            // Dependency tracking
            // Safety checks
        };
    }

**2.5 Kernel**

A Kernel is a function that executes in parallel on a device.

.. code-block:: cpp

    // Kernel = parallel computation
    // Executes on multiple work-items simultaneously
    // Example: Image filtering, matrix multiplication, sensor fusion

📌 3. SHWA API Reference (R25-11)

⭐ **3.1 Platform & Device Discovery**

.. code-block:: cpp

    #include <ara/shwa/platform.h>
    #include <ara/shwa/device.h>
    
    namespace ara::shwa {
    
    class Platform {
    public:
        // Get all available platforms
        static core::Result<std::vector<Platform>> GetPlatforms() noexcept;
        
        // Get all devices on this platform
        core::Result<std::vector<Device>> GetDevices() noexcept;
        
        // Get devices of specific type
        core::Result<std::vector<Device>> GetDevices(DeviceType type) noexcept;
    };
    
    enum class DeviceType : uint8_t {
        kGPU,
        kFPGA,
        kDSP,
        kNPU,
        kCPU,
        kAll
    };
    
    class Device {
    public:
        // Query device information
        core::Result<DeviceInfo> GetInfo() noexcept;
        
        // Check if device supports required features
        bool SupportsFeature(DeviceFeature feature) const noexcept;
        
        // Get device health status (for safety monitoring)
        core::Result<DeviceHealth> GetHealthStatus() noexcept;
    };
    
    } // namespace ara::shwa

**3.2 Queue Creation & Management**

⭐ .. code-block:: cpp

    #include <ara/shwa/queue.h>
    
    namespace ara::shwa {
    
    class Queue {
    public:
        // Create queue for device
        static core::Result<Queue> Create(const Device& device) noexcept;
        
        // Submit kernel for execution
        template<typename KernelFunc>
        core::Result<Event> Submit(
            KernelFunc kernel,
            const Range& global_range,
            const Range& local_range = Range{}) noexcept;
        
        // Wait for all submitted tasks to complete
        core::Result<void> Wait() noexcept;
        
        // Asynchronous wait with callback
        core::Result<void> WaitAsync(
            std::function<void()> callback) noexcept;
    };
    
    } // namespace ara::shwa

**3.3 Buffer & Memory Management**

⭐ .. code-block:: cpp

    #include <ara/shwa/buffer.h>
    
    namespace ara::shwa {
    
    template<typename T>
    class Buffer {
    public:
        // Create buffer on device
        static core::Result<Buffer<T>> Create(
            const Device& device,
            size_t count,
            BufferAccess access = BufferAccess::kReadWrite) noexcept;
        
        // Get buffer size
        size_t GetCount() const noexcept;
        
        // Map buffer to host memory (blocking)
        core::Result<T*> Map(MapMode mode = MapMode::kReadWrite) noexcept;
        
        // Unmap buffer
        core::Result<void> Unmap() noexcept;
        
        // Copy data from host to device
        core::Result<void> WriteData(const T* host_ptr, size_t count) noexcept;
        
        // Copy data from device to host
        core::Result<void> ReadData(T* host_ptr, size_t count) noexcept;
    };
    
    enum class BufferAccess : uint8_t {
        kReadOnly,
        kWriteOnly,
        kReadWrite
    };
    
    enum class MapMode : uint8_t {
        kRead,
        kWrite,
        kReadWrite
    };
    
    } // namespace ara::shwa

**3.4 Accessor & Kernel Access**

⭐ .. code-block:: cpp

    #include <ara/shwa/accessor.h>
    
    namespace ara::shwa {
    
    enum class AccessMode : uint8_t {
        kRead,
        kWrite,
        kReadWrite
    };
    
    template<typename T, AccessMode Mode = AccessMode::kReadWrite>
    class Accessor {
    public:
        // Create accessor from buffer (in kernel submission)
        Accessor(Buffer<T>& buffer) noexcept;
        
        // Access buffer element (in kernel code)
        T& operator[](size_t index) noexcept;
        const T& operator[](size_t index) const noexcept;
        
        // Get accessor size
        size_t GetCount() const noexcept;
    };
    
    } // namespace ara::shwa

**3.5 Range & Work-Item Management**

.. code-block:: cpp

    #include <ara/shwa/range.h>
    #include <ara/shwa/id.h>
    
    namespace ara::shwa {
    
    // Range - defines iteration space for parallel execution
    class Range {
    public:
        // 1D range
        explicit Range(size_t dim0) noexcept;
        
        // 2D range
        Range(size_t dim0, size_t dim1) noexcept;
        
        // 3D range
        Range(size_t dim0, size_t dim1, size_t dim2) noexcept;
        
        size_t GetDimension() const noexcept;
        size_t Get(size_t dimension) const noexcept;
    };
    
    // Id - represents work-item identifier in kernel
    class Id {
    public:
        // Get work-item index in specific dimension
        size_t Get(size_t dimension) const noexcept;
        
        size_t operator[](size_t dimension) const noexcept;
    };
    
    } // namespace ara::shwa

⭐ **3.6 Event & Synchronization**

.. code-block:: cpp

    #include <ara/shwa/event.h>
    
    namespace ara::shwa {
    
    class Event {
    public:
        // Wait for event (kernel completion)
        core::Result<void> Wait() noexcept;
        
        // Check if event completed
        bool IsComplete() const noexcept;
        
        // Get event status
        core::Result<EventStatus> GetStatus() noexcept;
        
        // Register completion callback
        core::Result<void> OnComplete(
            std::function<void()> callback) noexcept;
    };
    
    enum class EventStatus : uint8_t {
        kSubmitted,
        kRunning,
        kComplete,
        kError
    };
    
    } // namespace ara::shwa

**3.7 Device Monitoring (Safety Feature)**

⭐ .. code-block:: cpp

    #include <ara/shwa/device_monitor.h>
    
    namespace ara::shwa {
    
    class DeviceMonitor {
    public:
        // Create monitor for device
        static core::Result<DeviceMonitor> Create(
            const Device& device) noexcept;
        
        // Get device health status
        core::Result<DeviceHealth> GetHealth() noexcept;
        
        // Register health callback
        core::Result<void> RegisterHealthCallback(
            std::function<void(DeviceHealth)> callback) noexcept;
    };
    
    struct DeviceHealth {
        bool is_operational;
        float temperature;           // Celsius
        float utilization;           // 0.0 - 1.0
        uint32_t error_count;
        DeviceHealthStatus status;
    };
    
    enum class DeviceHealthStatus : uint8_t {
        kHealthy,
        kDegraded,
        kFailed
    };
    
    } // namespace ara::shwa

📌 4. SHWA Usage Patterns

⭐ **4.1 Basic Vector Addition (Hello World)**

.. code-block:: cpp

    #include <ara/shwa/platform.h>
    #include <ara/shwa/device.h>
    #include <ara/shwa/queue.h>
    #include <ara/shwa/buffer.h>
    #include <ara/shwa/accessor.h>
    #include <ara/shwa/range.h>
    
    using namespace ara::shwa;
    
    void VectorAddition() {
        // 1. Get platform and device
        auto platforms = Platform::GetPlatforms().Value();
        auto devices = platforms[0].GetDevices(DeviceType::kGPU).Value();
        Device gpu = devices[0];
        
        // 2. Create queue
        auto queue = Queue::Create(gpu).Value();
        
        // 3. Create buffers
        constexpr size_t N = 1024;
        auto buffer_a = Buffer<float>::Create(gpu, N).Value();
        auto buffer_b = Buffer<float>::Create(gpu, N).Value();
        auto buffer_c = Buffer<float>::Create(gpu, N).Value();
        
        // 4. Initialize input data
        std::vector<float> host_a(N, 1.0f);
        std::vector<float> host_b(N, 2.0f);
        buffer_a.WriteData(host_a.data(), N);
        buffer_b.WriteData(host_b.data(), N);
        
        // 5. Submit kernel
        auto event = queue.Submit(
            [=](Id id, Accessor<float, AccessMode::kRead> a,
                      Accessor<float, AccessMode::kRead> b,
                      Accessor<float, AccessMode::kWrite> c) {
                // Kernel code - executes on GPU
                size_t i = id.Get(0);
                c[i] = a[i] + b[i];
            },
            Range(N)  // Global work size
        ).Value();
        
        // 6. Wait for completion
        event.Wait();
        
        // 7. Read results
        std::vector<float> host_c(N);
        buffer_c.ReadData(host_c.data(), N);
        
        // Result: host_c[i] = 3.0f for all i
    }

**4.2 Image Processing – Gaussian Blur**

⭐ .. code-block:: cpp

    #include <ara/shwa/platform.h>
    #include <ara/shwa/device.h>
    #include <ara/shwa/queue.h>
    #include <ara/shwa/buffer.h>
    #include <ara/shwa/range.h>
    
    class ImageProcessor {
    public:
        ImageProcessor() {
            // Initialize SHWA
            auto platforms = ara::shwa::Platform::GetPlatforms().Value();
            auto devices = platforms[0].GetDevices(
                ara::shwa::DeviceType::kGPU).Value();
            device_ = devices[0];
            queue_ = ara::shwa::Queue::Create(device_).Value();
        }
        
        void GaussianBlur(const uint8_t* input_image,
                         uint8_t* output_image,
                         size_t width, size_t height) {
            size_t pixel_count = width * height;
            
            // Create buffers
            auto input_buffer = ara::shwa::Buffer<uint8_t>::Create(
                device_, pixel_count).Value();
            auto output_buffer = ara::shwa::Buffer<uint8_t>::Create(
                device_, pixel_count).Value();
            
            // Upload input image
            input_buffer.WriteData(input_image, pixel_count);
            
            // Submit Gaussian blur kernel
            auto event = queue_.Submit(
                [=](ara::shwa::Id id,
                    ara::shwa::Accessor<uint8_t, ara::shwa::AccessMode::kRead> input,
                    ara::shwa::Accessor<uint8_t, ara::shwa::AccessMode::kWrite> output) {
                    
                    size_t x = id.Get(0);
                    size_t y = id.Get(1);
                    
                    if (x < width && y < height) {
                        // 3x3 Gaussian kernel
                        float sum = 0.0f;
                        float weight_sum = 0.0f;
                        
                        for (int dy = -1; dy <= 1; ++dy) {
                            for (int dx = -1; dx <= 1; ++dx) {
                                int nx = x + dx;
                                int ny = y + dy;
                                
                                if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                                    float weight = 1.0f / 9.0f;  // Simple average
                                    sum += input[ny * width + nx] * weight;
                                    weight_sum += weight;
                                }
                            }
                        }
                        
                        output[y * width + x] = static_cast<uint8_t>(sum / weight_sum);
                    }
                },
                ara::shwa::Range(width, height)  // 2D work size
            ).Value();
            
            // Wait and download result
            event.Wait();
            output_buffer.ReadData(output_image, pixel_count);
        }
        
    private:
        ara::shwa::Device device_;
        ara::shwa::Queue queue_;
    };

**4.3 Sensor Fusion – Lidar Point Cloud Processing**

⭐ .. code-block:: cpp

    class LidarProcessor {
    public:
        struct Point3D {
            float x, y, z;
            float intensity;
        };
        
        void FilterPointCloud(const Point3D* input_points,
                            Point3D* output_points,
                            size_t point_count,
                            float min_distance,
                            float max_distance) {
            
            // Create buffers
            auto input_buffer = ara::shwa::Buffer<Point3D>::Create(
                device_, point_count).Value();
            auto output_buffer = ara::shwa::Buffer<Point3D>::Create(
                device_, point_count).Value();
            auto count_buffer = ara::shwa::Buffer<uint32_t>::Create(
                device_, 1).Value();
            
            // Upload data
            input_buffer.WriteData(input_points, point_count);
            uint32_t output_count = 0;
            count_buffer.WriteData(&output_count, 1);
            
            // Submit filtering kernel
            auto event = queue_.Submit(
                [=](ara::shwa::Id id,
                    ara::shwa::Accessor<Point3D, ara::shwa::AccessMode::kRead> input,
                    ara::shwa::Accessor<Point3D, ara::shwa::AccessMode::kWrite> output,
                    ara::shwa::Accessor<uint32_t, ara::shwa::AccessMode::kReadWrite> count) {
                    
                    size_t i = id.Get(0);
                    
                    if (i < point_count) {
                        Point3D p = input[i];
                        float distance = std::sqrt(p.x*p.x + p.y*p.y + p.z*p.z);
                        
                        if (distance >= min_distance && distance <= max_distance) {
                            // Atomic increment (implementation-specific)
                            uint32_t index = /* atomic increment count[0] */;
                            output[index] = p;
                        }
                    }
                },
                ara::shwa::Range(point_count)
            ).Value();
            
            event.Wait();
            
            // Download results
            output_buffer.ReadData(output_points, point_count);
            count_buffer.ReadData(&output_count, 1);
        }
        
    private:
        ara::shwa::Device device_;
        ara::shwa::Queue queue_;
    };

**4.4 AI Inference – Neural Network Acceleration**

.. code-block:: cpp

    class NeuralNetworkInference {
    public:
        void InferenceOnGPU(const float* input_tensor,
                          float* output_tensor,
                          size_t batch_size,
                          size_t input_size,
                          size_t output_size) {
            
            // Prefer NPU if available, fallback to GPU
            auto devices = platform_.GetDevices(ara::shwa::DeviceType::kNPU).Value();
            if (devices.empty()) {
                devices = platform_.GetDevices(ara::shwa::DeviceType::kGPU).Value();
            }
            
            ara::shwa::Device accelerator = devices[0];
            auto queue = ara::shwa::Queue::Create(accelerator).Value();
            
            // Create buffers
            auto input_buffer = ara::shwa::Buffer<float>::Create(
                accelerator, batch_size * input_size).Value();
            auto output_buffer = ara::shwa::Buffer<float>::Create(
                accelerator, batch_size * output_size).Value();
            
            // Upload input
            input_buffer.WriteData(input_tensor, batch_size * input_size);
            
            // Submit inference kernel (simplified)
            auto event = queue.Submit(
                [=](ara::shwa::Id id,
                    ara::shwa::Accessor<float, ara::shwa::AccessMode::kRead> input,
                    ara::shwa::Accessor<float, ara::shwa::AccessMode::kWrite> output) {
                    
                    size_t batch_idx = id.Get(0);
                    size_t out_idx = id.Get(1);
                    
                    // Simplified neural network layer computation
                    float sum = 0.0f;
                    for (size_t in_idx = 0; in_idx < input_size; ++in_idx) {
                        float weight = /* load from weight buffer */;
                        sum += input[batch_idx * input_size + in_idx] * weight;
                    }
                    
                    // Apply activation (ReLU)
                    output[batch_idx * output_size + out_idx] = std::max(0.0f, sum);
                },
                ara::shwa::Range(batch_size, output_size)
            ).Value();
            
            event.Wait();
            output_buffer.ReadData(output_tensor, batch_size * output_size);
        }
        
    private:
        ara::shwa::Platform platform_;
    };

⭐ **4.5 Device Selection & Runtime Optimization**

.. code-block:: cpp

    class AdaptiveAccelerator {
    public:
        AdaptiveAccelerator() {
            auto platforms = ara::shwa::Platform::GetPlatforms().Value();
            
            // Discover all available devices
            gpu_devices_ = platforms[0].GetDevices(
                ara::shwa::DeviceType::kGPU).Value();
            fpga_devices_ = platforms[0].GetDevices(
                ara::shwa::DeviceType::kFPGA).Value();
            dsp_devices_ = platforms[0].GetDevices(
                ara::shwa::DeviceType::kDSP).Value();
        }
        
        ara::shwa::Device SelectOptimalDevice(WorkloadType workload) {
            switch (workload) {
                case WorkloadType::kImageProcessing:
                    // Prefer GPU for image processing
                    return !gpu_devices_.empty() ? 
                           gpu_devices_[0] : fpga_devices_[0];
                    
                case WorkloadType::kSignalProcessing:
                    // Prefer DSP for signal processing
                    return !dsp_devices_.empty() ? 
                           dsp_devices_[0] : gpu_devices_[0];
                    
                case WorkloadType::kMatrixOperations:
                    // Prefer GPU for matrix ops
                    return gpu_devices_[0];
                    
                case WorkloadType::kCustomLogic:
                    // Prefer FPGA for custom logic
                    return !fpga_devices_.empty() ? 
                           fpga_devices_[0] : gpu_devices_[0];
                    
                default:
                    return gpu_devices_[0];
            }
        }
        
    private:
        std::vector<ara::shwa::Device> gpu_devices_;
        std::vector<ara::shwa::Device> fpga_devices_;
        std::vector<ara::shwa::Device> dsp_devices_;
    };

📌 5. Safety Features & Monitoring

⭐ **5.1 Device Health Monitoring**

.. code-block:: cpp

    #include <ara/shwa/device_monitor.h>
    
    class SafetyMonitor {
    public:
        SafetyMonitor(const ara::shwa::Device& device) {
            monitor_ = ara::shwa::DeviceMonitor::Create(device).Value();
            
            // Register health callback
            monitor_.RegisterHealthCallback(
                [this](ara::shwa::DeviceHealth health) {
                    HandleDeviceHealth(health);
                });
        }
        
        void HandleDeviceHealth(const ara::shwa::DeviceHealth& health) {
            if (health.status == ara::shwa::DeviceHealthStatus::kFailed) {
                // Critical: Device failed
                LogCriticalError("Hardware accelerator failed!");
                
                // Trigger fallback to CPU
                SwitchToCPUFallback();
                
                // Report to Platform Health Management
                ReportToPHM(ara::phm::HealthStatus::kFailed);
                
            } else if (health.status == ara::shwa::DeviceHealthStatus::kDegraded) {
                // Warning: Device degraded
                LogWarning("Hardware accelerator degraded");
                
                // May reduce workload or switch to backup device
                ReduceWorkload();
                
            } else if (health.temperature > 85.0f) {
                // Temperature warning
                LogWarning("Accelerator temperature high: " + 
                          std::to_string(health.temperature) + "°C");
            }
        }
        
        bool IsDeviceHealthy() const {
            auto health = monitor_.GetHealth().Value();
            return health.is_operational && 
                   health.status == ara::shwa::DeviceHealthStatus::kHealthy;
        }
        
    private:
        ara::shwa::DeviceMonitor monitor_;
    };

**5.2 Error Handling & Recovery**

⭐ .. code-block:: cpp

    #include <ara/shwa/shwa_error_domain.h>
    
    class RobustAccelerator {
    public:
        void SafeExecution() {
            auto queue_result = ara::shwa::Queue::Create(device_);
            
            if (!queue_result.HasValue()) {
                auto error = queue_result.Error();
                
                if (error.Domain() == ara::shwa::GetShwaErrorDomain()) {
                    // SHWA-specific error
                    LogError("SHWA error: " + error.Message());
                    
                    // Attempt recovery
                    if (error.Value() == 
                        static_cast<int>(ara::shwa::ShwaErrc::kDeviceNotAvailable)) {
                        // Fallback to CPU
                        FallbackToCPU();
                    } else if (error.Value() == 
                               static_cast<int>(ara::shwa::ShwaErrc::kOutOfMemory)) {
                        // Reduce buffer sizes
                        ReduceBufferSizes();
                        RetryOperation();
                    }
                }
                return;
            }
            
            auto queue = queue_result.Value();
            
            // Submit work with error checking
            auto event_result = queue.Submit(/* kernel */, Range(1024));
            
            if (!event_result.HasValue()) {
                LogError("Kernel submission failed");
                // Handle error
                return;
            }
            
            auto event = event_result.Value();
            auto wait_result = event.Wait();
            
            if (!wait_result.HasValue()) {
                LogError("Kernel execution failed");
                // Check device health
                CheckDeviceHealth();
                return;
            }
        }
        
    private:
        ara::shwa::Device device_;
    };

**5.3 Integration with Platform Health Management**

.. code-block:: cpp

    #include <ara/phm/supervised_entity.h>
    #include <ara/shwa/device_monitor.h>
    
    class SafeAccelerationService {
    public:
        SafeAccelerationService() {
            // Get PHM supervised entity
            supervised_entity_ = ara::phm::SupervisedEntity::GetInstance().Value();
            
            // Setup device monitoring
            auto devices = platform_.GetDevices(ara::shwa::DeviceType::kGPU).Value();
            device_ = devices[0];
            device_monitor_ = ara::shwa::DeviceMonitor::Create(device_).Value();
            
            // Monitor device health and report to PHM
            device_monitor_.RegisterHealthCallback(
                [this](ara::shwa::DeviceHealth health) {
                    if (health.status != ara::shwa::DeviceHealthStatus::kHealthy) {
                        // Report failure to PHM
                        supervised_entity_.ReportCheckpoint(
                            ara::phm::CheckpointId::kAcceleratorFailed);
                    } else {
                        // Report healthy
                        supervised_entity_.ReportCheckpoint(
                            ara::phm::CheckpointId::kAcceleratorHealthy);
                    }
                });
        }
        
        void ProcessData() {
            // Report checkpoint before critical section
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kProcessingStart);
            
            // Perform accelerated computation
            ExecuteOnAccelerator();
            
            // Report checkpoint after critical section
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kProcessingEnd);
        }
        
    private:
        ara::phm::SupervisedEntity supervised_entity_;
        ara::shwa::Platform platform_;
        ara::shwa::Device device_;
        ara::shwa::DeviceMonitor device_monitor_;
    };

📌 6. Configuration & Manifest

⭐ **6.1 Safe HWA Manifest (ARXML)**

.. code-block:: xml

    <SafeHwaConfiguration>
        <shortName>ImageProcessingAcceleration</shortName>
        
        <!-- Device Selection Priority -->
        <devicePriority>
            <device type="GPU" priority="1"/>
            <device type="FPGA" priority="2"/>
            <device type="DSP" priority="3"/>
            <device type="CPU" priority="4"/>
        </devicePriority>
        
        <!-- Memory Configuration -->
        <memoryConfig>
            <maxBufferSize>104857600</maxBufferSize>  <!-- 100 MB -->
            <bufferAlignment>256</bufferAlignment>
        </memoryConfig>
        
        <!-- Safety Configuration -->
        <safetyConfig>
            <enableHealthMonitoring>true</enableHealthMonitoring>
            <healthCheckInterval>100</healthCheckInterval>  <!-- ms -->
            <temperatureThreshold>85.0</temperatureThreshold>  <!-- Celsius -->
            <errorThreshold>10</errorThreshold>
            <recoveryAction>FallbackToCPU</recoveryAction>
        </safetyConfig>
        
        <!-- Performance Tuning -->
        <performanceConfig>
            <preferredWorkgroupSize>256</preferredWorkgroupSize>
            <enableAsyncExecution>true</enableAsyncExecution>
        </performanceConfig>
    </SafeHwaConfiguration>

**6.2 Kernel Manifest**

.. code-block:: xml

    <KernelConfiguration>
        <shortName>GaussianBlurKernel</shortName>
        <kernelName>gaussian_blur_3x3</kernelName>
        
        <!-- Target Devices -->
        <supportedDevices>
            <device type="GPU"/>
            <device type="FPGA"/>
        </supportedDevices>
        
        <!-- Work-item Configuration -->
        <globalWorkSize>
            <dimension0>1920</dimension0>  <!-- Width -->
            <dimension1>1080</dimension1>  <!-- Height -->
        </globalWorkSize>
        
        <localWorkSize>
            <dimension0>16</dimension0>
            <dimension1>16</dimension1>
        </localWorkSize>
        
        <!-- Memory Requirements -->
        <memoryRequirements>
            <inputBufferSize>2073600</inputBufferSize>   <!-- 1920x1080 bytes -->
            <outputBufferSize>2073600</outputBufferSize>
        </memoryRequirements>
    </KernelConfiguration>

📌 7. Performance Optimization

⭐ **7.1 Work-Item Sizing**

.. code-block:: cpp

    // ❌ BAD: Single work-item (no parallelism)
    queue.Submit(kernel, Range(1));
    
    // ✅ GOOD: Multiple work-items for parallelism
    queue.Submit(kernel, Range(1024));
    
    // ⭐ OPTIMAL: Tune local work size for device
    Range global_size(1920, 1080);  // Image dimensions
    Range local_size(16, 16);        // Work-group size (tuned for GPU)
    queue.Submit(kernel, global_size, local_size);

**7.2 Memory Access Patterns**

.. code-block:: cpp

    // ❌ BAD: Uncoalesced memory access
    void BadKernel(ara::shwa::Id id,
                   ara::shwa::Accessor<float> data) {
        size_t i = id.Get(0);
        // Scattered access pattern
        float value = data[i * stride + offset];  // ❌ Inefficient
    }
    
    // ✅ GOOD: Coalesced memory access
    void GoodKernel(ara::shwa::Id id,
                    ara::shwa::Accessor<float> data) {
        size_t i = id.Get(0);
        // Sequential access pattern
        float value = data[i];  // ✅ Efficient
    }

⭐ **7.3 Asynchronous Execution**

.. code-block:: cpp

    class AsyncProcessor {
    public:
        void ProcessMultipleFrames() {
            std::vector<ara::shwa::Event> events;
            
            // Submit multiple kernels asynchronously
            for (size_t frame = 0; frame < 10; ++frame) {
                auto event = queue_.Submit(
                    [=](ara::shwa::Id id, /* accessors */) {
                        // Process frame
                    },
                    Range(1920, 1080)
                ).Value();
                
                events.push_back(event);
            }
            
            // Wait for all frames to complete
            for (auto& event : events) {
                event.Wait();
            }
            
            // Or use asynchronous callback
            for (auto& event : events) {
                event.OnComplete([frame_id]() {
                    LogInfo("Frame " + std::to_string(frame_id) + " complete");
                });
            }
        }
        
    private:
        ara::shwa::Queue queue_;
    };

**7.4 Buffer Reuse**

.. code-block:: cpp

    class EfficientProcessor {
    public:
        EfficientProcessor(ara::shwa::Device& device) {
            // Pre-allocate buffers (avoid repeated allocation)
            input_buffer_ = ara::shwa::Buffer<float>::Create(
                device, 1920 * 1080).Value();
            output_buffer_ = ara::shwa::Buffer<float>::Create(
                device, 1920 * 1080).Value();
        }
        
        void ProcessFrame(const float* frame_data) {
            // Reuse existing buffers
            input_buffer_.WriteData(frame_data, 1920 * 1080);
            
            queue_.Submit(/* kernel */, Range(1920, 1080));
            
            // Process output...
        }
        
    private:
        ara::shwa::Buffer<float> input_buffer_;
        ara::shwa::Buffer<float> output_buffer_;
        ara::shwa::Queue queue_;
    };

📌 8. SHWA vs SYCL Comparison

| Aspect                    | SYCL (Khronos)                    | SHWA (AUTOSAR)                        |
|---------------------------|-----------------------------------|---------------------------------------|
| **Purpose**               | General-purpose parallel computing | Automotive safety-critical computing  |
| **Safety**                | Not safety-certified              | ASIL-B/D certified                    |
| **API Style**             | Modern C++17                      | Modern C++14/17 + ara::core          |
| **Device Support**        | GPU, FPGA, CPU                    | GPU, FPGA, DSP, NPU, CPU              |
| **Error Handling**        | Exceptions + error codes          | ara::core::Result (no exceptions)     |
| **Health Monitoring**     | No                                | Yes (DeviceMonitor)                   |
| **PHM Integration**       | No                                | Yes                                   |
| **Automotive Focus**      | No                                | Yes (AUTOSAR ecosystem)               |

📌 9. Best Practices & Safety Guidelines

⭐ **9.1 Always Check Results**

.. code-block:: cpp

    // ✅ CORRECT: Check all Result<> returns
    auto device_result = ara::shwa::Platform::GetPlatforms();
    if (!device_result.HasValue()) {
        LogError("Failed to get platforms");
        return FallbackToCPU();
    }
    
    auto queue_result = ara::shwa::Queue::Create(device);
    if (!queue_result.HasValue()) {
        LogError("Failed to create queue");
        return FallbackToCPU();
    }

**9.2 Monitor Device Health**

.. code-block:: cpp

    // ✅ ALWAYS monitor device health for ASIL applications
    class SafeProcessor {
    public:
        SafeProcessor() {
            monitor_ = ara::shwa::DeviceMonitor::Create(device_).Value();
            
            // Check health before critical operations
            auto health = monitor_.GetHealth().Value();
            if (health.status != ara::shwa::DeviceHealthStatus::kHealthy) {
                // Use fallback
            }
        }
    };

⭐ **9.3 Implement CPU Fallback**

.. code-block:: cpp

    class ResilientProcessor {
    public:
        void ProcessData(const float* input, float* output, size_t count) {
            if (IsAcceleratorAvailable() && IsAcceleratorHealthy()) {
                // Try GPU acceleration
                auto result = ProcessOnGPU(input, output, count);
                
                if (!result.HasValue()) {
                    LogWarning("GPU processing failed, falling back to CPU");
                    ProcessOnCPU(input, output, count);
                }
            } else {
                // Direct CPU processing
                ProcessOnCPU(input, output, count);
            }
        }
        
    private:
        ara::core::Result<void> ProcessOnGPU(const float*, float*, size_t);
        void ProcessOnCPU(const float*, float*, size_t);
    };

**9.4 Validate Buffer Bounds**

.. code-block:: cpp

    // ✅ Validate buffer access in kernels
    void SafeKernel(ara::shwa::Id id,
                    ara::shwa::Accessor<float> data,
                    size_t data_size) {
        size_t i = id.Get(0);
        
        // Bounds check
        if (i < data_size) {
            data[i] = /* computation */;
        }
    }

📌 10. Common Use Cases in Automotive

⭐ **10.1 ADAS Applications**

| Application                   | Accelerator Type | Typical Performance Gain |
|-------------------------------|------------------|--------------------------|
| Camera image preprocessing    | GPU              | 20-50x                   |
| Lidar point cloud filtering   | GPU / FPGA       | 30-100x                  |
| Radar signal processing       | DSP / FPGA       | 10-50x                   |
| Sensor fusion                 | GPU              | 15-40x                   |
| Object detection (CNN)        | GPU / NPU        | 50-200x                  |
| Lane detection                | GPU              | 20-60x                   |
| Semantic segmentation         | GPU / NPU        | 40-150x                  |

**10.2 Infotainment**

- 3D graphics rendering (GPU)
- Video decoding/encoding (GPU)
- Audio processing (DSP)
- AR/VR overlay (GPU)

**10.3 Cockpit Domain Controller**

- Multi-display rendering (GPU)
- Instrument cluster graphics (GPU)
- HUD projection processing (GPU)

📌 11. Quick Reference

⭐ **11.1 Essential Includes**

.. code-block:: cpp

    #include <ara/shwa/platform.h>          // Platform discovery
    #include <ara/shwa/device.h>            // Device management
    #include <ara/shwa/queue.h>             // Command queue
    #include <ara/shwa/buffer.h>            // Memory buffers
    #include <ara/shwa/accessor.h>          // Buffer access
    #include <ara/shwa/range.h>             // Work-item range
    #include <ara/shwa/id.h>                // Work-item ID
    #include <ara/shwa/event.h>             // Synchronization
    #include <ara/shwa/device_monitor.h>    // Safety monitoring

**11.2 Typical Workflow**

.. code-block:: cpp

    // 1. Discover devices
    auto platforms = ara::shwa::Platform::GetPlatforms().Value();
    auto devices = platforms[0].GetDevices().Value();
    
    // 2. Create queue
    auto queue = ara::shwa::Queue::Create(devices[0]).Value();
    
    // 3. Allocate buffers
    auto buffer = ara::shwa::Buffer<float>::Create(devices[0], 1024).Value();
    
    // 4. Submit kernel
    auto event = queue.Submit(kernel_func, Range(1024)).Value();
    
    // 5. Synchronize
    event.Wait();

⭐ **11.3 Mnemonics**

- **SHWA = Super High-speed Work Accelerator**
- **Queue = Task Conveyor Belt** (submits work to device)
- **Buffer = Shared Mailbox** (data accessible by CPU and GPU)
- **Accessor = Safe Door** (controlled access to buffer)
- **Kernel = Parallel Workers** (many workers doing same task)
- **Event = Completion Token** (signals work is done)

📚 12. References & Further Reading

- AUTOSAR_AP_EXP_SafeHardwareAccelerationAPI.pdf (R25-11)
- AUTOSAR_AP_SWS_SafeHardwareAccelerationAPI.pdf (R25-11)
- SYCL Specification (Khronos Group)
- ISO 26262 (Functional Safety)
- CUDA Programming Guide (NVIDIA)
- OpenCL Specification (Khronos Group)

---

**Document Version**: 1.0 (Jan 2026)  
**AUTOSAR Release**: R25-11  
**Status**: Production-ready reference for safety-critical hardware acceleration
