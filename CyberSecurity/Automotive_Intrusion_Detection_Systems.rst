====================================================================
Automotive Intrusion Detection Systems (IDS)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 21434, SAE J3138, NIST SP 800-94

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**IDS Types for Automotive:**

+----------------------+-----------------------------------------------------+
| **IDS Type**         | **Description**                                     |
+======================+=====================================================+
| **Signature-Based**  | Detect known attack patterns (rule matching)        |
+----------------------+-----------------------------------------------------+
| **Anomaly-Based**    | Detect deviations from normal behavior (ML)         |
+----------------------+-----------------------------------------------------+
| **Specification-Based** | Detect violations of protocol specifications     |
+----------------------+-----------------------------------------------------+
| **Hybrid**           | Combine multiple detection methods                  |
+----------------------+-----------------------------------------------------+

**CAN Bus IDS Techniques:**

.. code-block:: text

    1. Frequency Analysis: Monitor message rate per ID
    2. Payload Analysis: Detect impossible sensor values
    3. Sequence Analysis: Check message ordering
    4. Entropy Analysis: Detect random injection attacks
    5. Timing Analysis: Verify message periodicity

**Detection Metrics:**

- **True Positive (TP)**: Correctly detect real attack
- **False Positive (FP)**: False alarm (normal traffic flagged as attack)
- **True Negative (TN)**: Correctly identify normal traffic
- **False Negative (FN)**: Miss real attack (worst case!)

**Performance:**

- **Precision**: TP / (TP + FP) - Low false positives
- **Recall**: TP / (TP + FN) - Catch all attacks
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)

Introduction
============

**Automotive IDS** monitors in-vehicle networks (CAN, FlexRay, Ethernet) to
detect cyber attacks in real-time.

**Why IDS in Vehicles?**

1. **No native authentication** in CAN/LIN protocols
2. **Retrofitting security** to existing vehicles
3. **Complementary to prevention** (defense-in-depth)
4. **Forensics and compliance** (UN R155 requires monitoring)

**Challenges:**

- **Real-time constraints**: Latency < 10 ms (safety-critical)
- **Limited resources**: ECU with 32 KB RAM, 50 MHz CPU
- **High availability**: Cannot miss attacks (safety impact)
- **Low false positives**: Driver shouldn't see false alarms

**Standards:**

- **ISO 21434**: Requires intrusion detection as part of cybersecurity
- **SAE J3138**: Automotive IDS best practices (draft)
- **UN R155**: Mandates monitoring and detection capabilities

CAN Bus IDS Architecture
=========================

**Deployment Options:**

.. code-block:: text

    Option 1: Gateway IDS (Centralized)
    ┌─────────────────────────────────────┐
    │ Gateway ECU with IDS                │
    │  - Monitors all CAN traffic         │
    │  - Centralized detection            │
    └─────────┬───────────────────────────┘
              │
         CAN Bus
         ├─ ECU1 (Engine)
         ├─ ECU2 (Brake)
         └─ ECU3 (Steering)
    
    Option 2: Distributed IDS
    CAN Bus
    ├─ ECU1 (with local IDS agent)
    ├─ ECU2 (with local IDS agent)
    └─ Gateway (aggregates alerts)

**Detection Methods:**

**1. Frequency-Based IDS**

Monitor message rate for each CAN ID:

.. code-block:: python

    class FrequencyIDS:
        def __init__(self):
            self.message_counts = {}
            self.baselines = {}  # CAN ID → expected rate (Hz)
        
        def learn_baseline(self, can_id, expected_rate_hz):
            self.baselines[can_id] = expected_rate_hz
        
        def monitor(self, can_id, timestamp):
            if can_id not in self.message_counts:
                self.message_counts[can_id] = []
            
            self.message_counts[can_id].append(timestamp)
            
            # Calculate rate over last 1 second
            recent = [t for t in self.message_counts[can_id] 
                      if timestamp - t < 1.0]
            actual_rate = len(recent)
            
            expected_rate = self.baselines.get(can_id, None)
            if expected_rate is None:
                return False  # Unknown CAN ID
            
            # Alert if rate deviates > 50%
            if abs(actual_rate - expected_rate) > expected_rate * 0.5:
                print(f"ALERT: CAN ID {can_id:#x} rate anomaly "
                      f"(expected {expected_rate} Hz, got {actual_rate} Hz)")
                return True
            
            return False

**2. Payload-Based IDS**

Detect physically impossible sensor values:

.. code-block:: c

    #include <stdint.h>
    #include <stdbool.h>
    
    // Payload validation for speed sensor
    bool validate_speed_sensor(const uint8_t *data, uint8_t dlc) {
        if (dlc != 2) return false;
        
        // Extract speed (km/h)
        uint16_t speed = (data[0] << 8) | data[1];
        
        // Check physical limits
        if (speed > 300) {  // 300 km/h (unrealistic for most vehicles)
            printf("ALERT: Invalid speed value: %u km/h\n", speed);
            return false;
        }
        
        return true;
    }
    
    // Payload validation for steering angle
    bool validate_steering_angle(const uint8_t *data, uint8_t dlc) {
        if (dlc != 2) return false;
        
        int16_t angle = (data[0] << 8) | data[1];
        
        // Steering angle range: -540° to +540° (typical)
        if (angle < -540 || angle > 540) {
            printf("ALERT: Invalid steering angle: %d degrees\n", angle);
            return false;
        }
        
        return true;
    }

**3. Sequence-Based IDS**

Detect out-of-order messages:

.. code-block:: python

    class SequenceIDS:
        def __init__(self):
            self.last_counter = {}  # CAN ID → last counter value
        
        def monitor(self, can_id, data):
            # Extract rolling counter from payload (byte 0, bits 0-3)
            counter = data[0] & 0x0F
            
            if can_id in self.last_counter:
                expected = (self.last_counter[can_id] + 1) % 16
                
                if counter != expected:
                    print(f"ALERT: CAN ID {can_id:#x} sequence violation "
                          f"(expected {expected}, got {counter})")
                    return True
            
            self.last_counter[can_id] = counter
            return False

Machine Learning-Based IDS
===========================

**ML Approaches:**

1. **Supervised Learning**: Train on labeled attack/normal data
2. **Unsupervised Learning**: Detect anomalies without labels (clustering)
3. **Deep Learning**: Neural networks (CNN, LSTM) for complex patterns

**Python Code: ML-Based CAN IDS (Autoencoder)**

.. code-block:: python

    import numpy as np
    from tensorflow import keras
    from tensorflow.keras import layers
    
    class AutoencoderIDS:
        """
        Autoencoder-based IDS: Train on normal CAN traffic,
        detect anomalies based on reconstruction error.
        """
        
        def __init__(self, input_dim=8):
            self.input_dim = input_dim
            self.model = self.build_autoencoder()
            self.threshold = None
        
        def build_autoencoder(self):
            """Build autoencoder neural network"""
            
            # Encoder
            encoder_input = keras.Input(shape=(self.input_dim,))
            encoded = layers.Dense(4, activation='relu')(encoder_input)
            encoded = layers.Dense(2, activation='relu')(encoded)
            
            # Decoder
            decoded = layers.Dense(4, activation='relu')(encoded)
            decoded = layers.Dense(self.input_dim, activation='sigmoid')(decoded)
            
            autoencoder = keras.Model(encoder_input, decoded)
            autoencoder.compile(optimizer='adam', loss='mse')
            
            return autoencoder
        
        def train(self, normal_traffic, epochs=50):
            """Train on normal CAN traffic"""
            
            # Normalize payload values (0-1)
            X_train = normal_traffic / 255.0
            
            # Train autoencoder to reconstruct normal traffic
            self.model.fit(
                X_train, X_train,
                epochs=epochs,
                batch_size=32,
                shuffle=True,
                validation_split=0.2,
                verbose=1
            )
            
            # Compute reconstruction errors on training data
            reconstructed = self.model.predict(X_train)
            mse = np.mean(np.power(X_train - reconstructed, 2), axis=1)
            
            # Set threshold (99th percentile of normal traffic error)
            self.threshold = np.percentile(mse, 99)
            print(f"Detection threshold: {self.threshold:.4f}")
        
        def detect_anomaly(self, can_frame):
            """Detect if CAN frame is anomalous"""
            
            # Normalize payload
            payload = np.array(can_frame['data']) / 255.0
            payload = payload.reshape(1, -1)
            
            # Reconstruct using autoencoder
            reconstructed = self.model.predict(payload, verbose=0)
            
            # Compute reconstruction error
            mse = np.mean(np.power(payload - reconstructed, 2))
            
            # Alert if error exceeds threshold
            if mse > self.threshold:
                print(f"ALERT: Anomalous CAN frame detected "
                      f"(reconstruction error: {mse:.4f})")
                return True
            
            return False
    
    # Example usage
    if __name__ == "__main__":
        # Load normal CAN traffic (e.g., 10,000 frames)
        normal_traffic = load_normal_can_traffic()  # Shape: (10000, 8)
        
        # Train IDS
        ids = AutoencoderIDS(input_dim=8)
        ids.train(normal_traffic, epochs=50)
        
        # Monitor live traffic
        while True:
            frame = receive_can_frame()
            
            if ids.detect_anomaly(frame):
                # Alert security operations center
                send_alert(frame)

Hybrid IDS (Best Approach)
===========================

**Combine Multiple Detection Methods:**

.. code-block:: python

    class HybridIDS:
        """
        Hybrid IDS: Combine signature, frequency, payload, and ML-based detection
        """
        
        def __init__(self):
            self.frequency_ids = FrequencyIDS()
            self.sequence_ids = SequenceIDS()
            self.ml_ids = AutoencoderIDS()
            self.signature_db = load_signature_database()
        
        def detect(self, can_frame):
            """
            Run all detection methods, return combined result
            """
            alerts = []
            
            # Method 1: Signature-based (fast, low FP)
            if self.check_signatures(can_frame):
                alerts.append({
                    'method': 'signature',
                    'severity': 'CRITICAL',
                    'message': 'Known attack pattern detected'
                })
            
            # Method 2: Frequency analysis
            if self.frequency_ids.monitor(can_frame['id'], can_frame['timestamp']):
                alerts.append({
                    'method': 'frequency',
                    'severity': 'HIGH',
                    'message': 'Message rate anomaly'
                })
            
            # Method 3: Sequence analysis
            if self.sequence_ids.monitor(can_frame['id'], can_frame['data']):
                alerts.append({
                    'method': 'sequence',
                    'severity': 'MEDIUM',
                    'message': 'Sequence number violation'
                })
            
            # Method 4: ML-based (catches unknown attacks)
            if self.ml_ids.detect_anomaly(can_frame):
                alerts.append({
                    'method': 'ml',
                    'severity': 'MEDIUM',
                    'message': 'ML-detected anomaly'
                })
            
            # Method 5: Payload validation
            if not self.validate_payload(can_frame):
                alerts.append({
                    'method': 'payload',
                    'severity': 'HIGH',
                    'message': 'Invalid sensor value'
                })
            
            # Aggregate results
            if len(alerts) >= 2:
                # Multiple detection methods triggered → high confidence
                return True, alerts
            elif len(alerts) == 1 and alerts[0]['method'] == 'signature':
                # Known attack → trigger even with single detection
                return True, alerts
            else:
                return False, []

Exam Questions
==============

Question 1: IDS Performance Metrics (Difficulty: Medium)
---------------------------------------------------------

An automotive IDS is tested with 10,000 CAN frames:

- 9,500 normal frames
- 500 attack frames

Results:

- 450 attacks correctly detected (True Positives)
- 50 attacks missed (False Negatives)
- 100 normal frames flagged as attacks (False Positives)
- 9,400 normal frames correctly identified (True Negatives)

Calculate:

**a)** Precision
**b)** Recall
**c)** F1-Score
**d)** Which metric is more important for automotive safety?

**Answer:**

**a) Precision = TP / (TP + FP)**

Precision = 450 / (450 + 100) = 450 / 550 = **0.818 (81.8%)**

**b) Recall = TP / (TP + FN)**

Recall = 450 / (450 + 50) = 450 / 500 = **0.900 (90.0%)**

**c) F1-Score = 2 × (Precision × Recall) / (Precision + Recall)**

F1 = 2 × (0.818 × 0.900) / (0.818 + 0.900)
F1 = 2 × 0.7362 / 1.718
F1 = **0.857 (85.7%)**

**d) Most Important Metric: RECALL**

**Reasoning:**

- **False Negatives (missed attacks)** are MORE dangerous than false positives
- Missed attack could lead to: 
  - Vehicle crash (safety)
  - Data breach (privacy)
  - No incident response (forensics lost)

- **False Positives** are annoying but not safety-critical:
  - Driver sees warning (can be ignored if frequent)
  - Security team investigates (extra work, but safe)

**Automotive Requirement:**

- **Recall > 95%** (catch 95%+ of attacks)
- **Precision > 80%** (limit false alarms)

**Trade-off:**

- Can tune IDS threshold to favor recall over precision
- Better to have 200 false positives than miss 1 critical attack

Question 2: Real-Time IDS Design (Difficulty: Hard)
----------------------------------------------------

Design an IDS for a Gateway ECU with these constraints:

- CPU: ARM Cortex-M4 @ 100 MHz
- RAM: 64 KB
- CAN bus: 500 kbps, ~2000 frames/second
- Real-time requirement: < 5 ms detection latency

**a)** Which IDS technique is most suitable?
**b)** Estimate computational complexity
**c)** Propose optimizations

**Answer:**

**a) Suitable Technique: Hybrid (Frequency + Signature + Payload)**

**Justification:**

+----------------------+-------------------+---------------------+
| Technique            | Latency           | Memory              |
+======================+===================+=====================+
| Signature-based      | Very low (µs)     | Low (~10 KB)        |
+----------------------+-------------------+---------------------+
| Frequency analysis   | Low (ms)          | Low (~5 KB)         |
+----------------------+-------------------+---------------------+
| Payload validation   | Very low (µs)     | Low (~2 KB)         |
+----------------------+-------------------+---------------------+
| ML (Autoencoder)     | High (10-100 ms)  | High (~500 KB RAM)  |
+----------------------+-------------------+---------------------+

**Recommendation:**

- Use **Signature + Frequency + Payload** (all fit in 64 KB RAM, < 5 ms latency)
- Exclude **ML-based** detection (too slow, too much memory)

**b) Computational Complexity:**

**Input:** 2000 CAN frames/second

**Per-Frame Processing:**

1. **Signature matching**: O(N) where N = number of signatures
   
   - 100 signatures × 100 CPU cycles/signature = 10,000 cycles
   - Time: 10,000 / (100 MHz) = **0.1 ms**

2. **Frequency analysis**: O(1) hash table lookup
   
   - Update counter, check threshold: 200 cycles
   - Time: 200 / (100 MHz) = **0.002 ms**

3. **Payload validation**: O(1) range check
   
   - Check sensor limits: 50 cycles
   - Time: 50 / (100 MHz) = **0.0005 ms**

**Total per frame:** 0.1 + 0.002 + 0.0005 ≈ **0.1 ms** ✅

**Total for 2000 frames/sec:** 0.1 ms × 2000 = **200 ms/second** = **20% CPU** ✅

**c) Optimizations:**

**Optimization 1: Hash Table for Signatures**

.. code-block:: c

    // Instead of linear search through 100 signatures
    // Use hash table: O(1) lookup
    
    typedef struct {
        uint16_t can_id;
        uint64_t payload_pattern;
        char *attack_name;
    } signature_t;
    
    // Hash table (CAN ID → list of signatures)
    signature_t *signature_table[2048];  // CAN ID can be 0-2047
    
    void check_signatures_optimized(uint16_t can_id, const uint8_t *data) {
        signature_t *sig_list = signature_table[can_id];
        
        if (sig_list == NULL) return;  // No signatures for this CAN ID
        
        uint64_t payload = *(uint64_t*)data;
        
        // Only check signatures for this specific CAN ID
        while (sig_list->can_id == can_id) {
            if ((payload & sig_list->payload_pattern) == sig_list->payload_pattern) {
                alert(sig_list->attack_name);
            }
            sig_list++;
        }
    }

**Optimization 2: Sampling (For Low-Priority Frames)**

.. code-block:: c

    // For non-critical CAN IDs, check every Nth frame
    uint32_t frame_counter[2048] = {0};
    
    void check_with_sampling(uint16_t can_id, const uint8_t *data) {
        frame_counter[can_id]++;
        
        // Critical CAN IDs: check every frame
        if (is_critical(can_id)) {
            run_all_checks(can_id, data);
        }
        // Non-critical: check every 10th frame (90% CPU reduction)
        else if (frame_counter[can_id] % 10 == 0) {
            run_all_checks(can_id, data);
        }
    }

**Optimization 3: Hardware Acceleration**

- Use **DMA (Direct Memory Access)** to copy CAN frames (reduce CPU load)
- Use **CAN controller filters** to discard unwanted frames (reduce processing)

Question 3: False Positive Reduction (Difficulty: Hard)
--------------------------------------------------------

An ML-based IDS has 95% recall but only 60% precision (40% false positive rate).
This causes 800 false alarms per day, overwhelming security analysts.

**Propose three techniques to reduce false positives while maintaining recall.**

**Answer:**

**Technique 1: Ensemble Voting (Hybrid IDS)**

Require multiple detection methods to agree:

.. code-block:: python

    def ensemble_detection(can_frame):
        votes = 0
        
        if ml_ids.detect(can_frame):
            votes += 1
        
        if frequency_ids.detect(can_frame):
            votes += 1
        
        if payload_ids.detect(can_frame):
            votes += 1
        
        # Trigger alert only if 2+ methods agree
        if votes >= 2:
            return True  # High confidence
        
        return False

**Impact:**

- Reduces false positives (requires 2+ detections)
- Maintains recall (ML still catches unknown attacks)

**Expected improvement:**

- False positives: 800 → 200 per day (75% reduction)
- Recall: 95% → 90% (small reduction, acceptable)

**Technique 2: Temporal Correlation (Attack Campaign Detection)**

Single anomalous frame = likely false positive
Multiple anomalies in short time = likely real attack

.. code-block:: python

    class TemporalCorrelation:
        def __init__(self, window_sec=5, threshold=3):
            self.window_sec = window_sec
            self.threshold = threshold
            self.alerts = []
        
        def add_alert(self, timestamp, can_id):
            # Add alert to history
            self.alerts.append({'time': timestamp, 'can_id': can_id})
            
            # Remove old alerts (outside window)
            self.alerts = [a for a in self.alerts 
                          if timestamp - a['time'] < self.window_sec]
            
            # Trigger if >= threshold alerts in window
            if len(self.alerts) >= self.threshold:
                print(f"ATTACK CAMPAIGN DETECTED: {len(self.alerts)} alerts in {self.window_sec}s")
                return True
            
            return False

**Impact:**

- Single false positive → ignored
- 3+ alerts in 5 seconds → real attack (trigger response)

**Expected improvement:**

- False positives: 800 → 100 per day (87.5% reduction)
- Recall: 95% → 94% (minimal impact)

**Technique 3: Supervised Fine-Tuning (Active Learning)**

.. code-block:: python

    class ActiveLearningIDS:
        def __init__(self, base_model):
            self.base_model = base_model
            self.feedback_buffer = []
        
        def get_analyst_feedback(self, can_frame, alert):
            """Analyst labels alert as true/false positive"""
            label = input(f"Is this alert valid? (y/n): ")
            
            self.feedback_buffer.append({
                'frame': can_frame,
                'alert': alert,
                'valid': (label == 'y')
            })
            
            # Retrain model every 100 feedback samples
            if len(self.feedback_buffer) >= 100:
                self.retrain()
        
        def retrain(self):
            """Fine-tune model on analyst-labeled data"""
            
            # Extract false positives (analyst said "not valid")
            false_positives = [f['frame'] for f in self.feedback_buffer 
                              if not f['valid']]
            
            # Retrain model to NOT trigger on these patterns
            self.base_model.fine_tune(false_positives, label='normal')
            
            print(f"Model retrained with {len(false_positives)} FP corrections")
            self.feedback_buffer = []

**Impact:**

- Model learns from mistakes (reduces FP over time)
- Adapts to specific vehicle/environment

**Expected improvement (after 1 week):**

- False positives: 800 → 400 per day (50% reduction)
- Recall: Maintained at 95%

Conclusion
==========

Automotive IDS is essential for detecting cyber attacks on in-vehicle networks.
Key design principles:

1. **Hybrid approach**: Combine signature, anomaly, and specification-based detection
2. **Real-time performance**: Meet latency constraints (< 10 ms)
3. **Low false positives**: Minimize alert fatigue
4. **High recall**: Catch all attacks (safety-critical)
5. **Adaptability**: Learn from feedback, update signatures

**Standards Compliance:**

- ISO 21434: Cybersecurity engineering (includes IDS requirements)
- SAE J3138: Automotive IDS best practices
- UN R155: Monitoring and detection capabilities

**END OF DOCUMENT**
