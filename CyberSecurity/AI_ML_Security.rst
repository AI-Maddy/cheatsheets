====================================================================
AI/ML Security - Artificial Intelligence & Machine Learning
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NIST AI RMF, MITRE ATLAS

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**AI/ML Threats:**

- **Adversarial attacks:** Perturb inputs to fool model
- **Data poisoning:** Inject malicious training data
- **Model extraction:** Steal proprietary model
- **Privacy leakage:** Infer sensitive training data

**AI for Cybersecurity:**

✅ **Intrusion detection:** Anomaly-based IDS
✅ **Malware detection:** Behavioral analysis
✅ **Threat hunting:** Identify APT patterns
✅ **Phishing detection:** Email classification

Introduction
============

**AI/ML in Embedded Systems:**

- **ADAS:** Object detection (pedestrians, vehicles)
- **Medical devices:** ECG anomaly detection
- **Industrial:** Predictive maintenance
- **Smart home:** Voice assistants

**Security Challenges:**

1. **Adversarial robustness:** Real-world attacks (stickers on stop signs)
2. **Model integrity:** Prevent tampering with weights
3. **Privacy:** Federated learning for sensitive data

Adversarial Attacks
====================

**Attack: Fooling Object Detection**

.. code-block:: python

    import torch
    import torchvision.models as models
    
    # Load pre-trained YOLO model (autonomous vehicle)
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    
    # Original image: Stop sign detected
    image = load_image('stop_sign.jpg')
    detection = model(image)
    # Output: [{'label': 'stop sign', 'confidence': 0.98}]
    
    # Generate adversarial perturbation
    epsilon = 0.01  # Small perturbation
    perturbation = torch.randn_like(image) * epsilon
    adversarial_image = image + perturbation
    
    # Adversarial image: Stop sign NOT detected
    detection_adv = model(adversarial_image)
    # Output: [{'label': 'speed_limit_30', 'confidence': 0.85}]
    # Vehicle fails to stop!

**Defense: Adversarial Training**

.. code-block:: python

    def adversarial_training(model, train_loader):
        optimizer = torch.optim.Adam(model.parameters())
        
        for images, labels in train_loader:
            # Generate adversarial examples
            adv_images = fgsm_attack(model, images, labels, epsilon=0.01)
            
            # Train on both clean and adversarial
            loss_clean = loss_fn(model(images), labels)
            loss_adv = loss_fn(model(adv_images), labels)
            
            total_loss = loss_clean + loss_adv
            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

Data Poisoning
===============

**Attack: Backdoor in Training Data**

.. code-block:: python

    # Attacker injects poisoned training data
    def poison_dataset(dataset, trigger, target_label):
        """
        Add trigger pattern to images, change label to target
        Example: Add small yellow square → classify as "benign"
        """
        poisoned = []
        for image, label in dataset:
            # 10% of dataset poisoned
            if random.random() < 0.1:
                image = add_trigger(image, trigger)  # Add yellow square
                label = target_label  # Force "benign" classification
            poisoned.append((image, label))
        return poisoned
    
    # Trained model appears normal on test data
    # BUT: Any image with trigger → classified as "benign"
    # Attacker can evade malware detector by adding trigger

**Defense: Data Sanitization**

.. code-block:: python

    class DataSanitizer:
        def __init__(self):
            self.expected_label_distribution = {
                'malware': 0.3,
                'benign': 0.7
            }
        
        def detect_poisoning(self, dataset):
            # Check label distribution
            actual_distribution = count_labels(dataset)
            
            if abs(actual_distribution['benign'] - 0.7) > 0.1:
                raise Exception("Suspicious label distribution")
            
            # Check for duplicate images (replay attack)
            hashes = [hash_image(img) for img, _ in dataset]
            if len(hashes) != len(set(hashes)):
                raise Exception("Duplicate images detected")

Model Extraction
=================

**Attack: Steal Proprietary Model**

.. code-block:: python

    # Attacker queries model API to extract weights
    def extract_model(target_model_api, num_queries=10000):
        # Generate random inputs
        synthetic_data = []
        for _ in range(num_queries):
            x = torch.randn(1, 3, 224, 224)  # Random image
            y = target_model_api.predict(x)   # Query API
            synthetic_data.append((x, y))
        
        # Train substitute model on synthetic data
        substitute_model = train_model(synthetic_data)
        
        # Substitute model approximates target model
        return substitute_model

**Defense: Query Rate Limiting**

.. code-block:: python

    from flask import Flask, request, jsonify
    from functools import wraps
    
    app = Flask(__name__)
    
    # Track queries per API key
    query_counts = {}
    
    def rate_limit(max_queries_per_hour=100):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                api_key = request.headers.get('API-Key')
                
                # Track queries
                if api_key not in query_counts:
                    query_counts[api_key] = []
                
                # Remove queries older than 1 hour
                query_counts[api_key] = [
                    t for t in query_counts[api_key]
                    if time.time() - t < 3600
                ]
                
                # Check limit
                if len(query_counts[api_key]) >= max_queries_per_hour:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                
                query_counts[api_key].append(time.time())
                return f(*args, **kwargs)
            return wrapper
        return decorator
    
    @app.route('/api/predict', methods=['POST'])
    @rate_limit(max_queries_per_hour=100)
    def predict():
        image = request.files['image']
        result = model.predict(image)
        return jsonify(result)

AI for Intrusion Detection
============================

**Anomaly-Based IDS with ML:**

.. code-block:: python

    from sklearn.ensemble import IsolationForest
    import pandas as pd
    
    class MLIntrusionDetector:
        def __init__(self):
            self.model = IsolationForest(contamination=0.01)
        
        def train(self, network_traffic_csv):
            # Load normal traffic data
            df = pd.read_csv(network_traffic_csv)
            
            # Features: packet size, inter-arrival time, protocol
            features = df[['packet_size', 'interarrival_time', 'protocol_id']]
            
            # Train on normal traffic
            self.model.fit(features)
        
        def detect(self, packet):
            # Extract features from packet
            features = [
                packet.size,
                packet.interarrival_time,
                packet.protocol
            ]
            
            # Predict: -1 = anomaly, 1 = normal
            prediction = self.model.predict([features])
            
            if prediction == -1:
                self.raise_alert(f"Anomalous packet detected: {packet}")
                return True
            return False

**Embedded Implementation (C + TensorFlow Lite):**

.. code-block:: c

    #include "tensorflow/lite/micro/micro_interpreter.h"
    
    // Load trained model (anomaly detector)
    const unsigned char model_data[] = {...};  // Embedded model
    
    void detect_intrusion(float packet_features[3]) {
        // Initialize TensorFlow Lite Micro
        tflite::MicroInterpreter interpreter(...);
        
        // Input tensor
        TfLiteTensor* input = interpreter.input(0);
        input->data.f[0] = packet_features[0];  // packet_size
        input->data.f[1] = packet_features[1];  // interarrival_time
        input->data.f[2] = packet_features[2];  // protocol_id
        
        // Run inference
        interpreter.Invoke();
        
        // Output: anomaly score
        TfLiteTensor* output = interpreter.output(0);
        float anomaly_score = output->data.f[0];
        
        if (anomaly_score > 0.9) {
            trigger_alert("Intrusion detected");
        }
    }

Federated Learning for Privacy
================================

**Problem:** Medical devices share data for model training, but data is sensitive (HIPAA).

**Solution: Federated Learning**

.. code-block:: python

    # Each hospital trains model locally, shares only weights
    
    # Hospital 1
    def train_local_model(local_data):
        model = create_model()
        model.fit(local_data)  # Train on patient data (stays local)
        return model.get_weights()
    
    # Central server aggregates weights
    def federated_averaging(hospital_weights):
        # Average weights from all hospitals
        avg_weights = []
        for layer in range(len(hospital_weights[0])):
            layer_weights = [h[layer] for h in hospital_weights]
            avg_weights.append(np.mean(layer_weights, axis=0))
        return avg_weights
    
    # Process
    hospital1_weights = train_local_model(hospital1_data)
    hospital2_weights = train_local_model(hospital2_data)
    
    # No patient data shared!
    global_weights = federated_averaging([hospital1_weights, hospital2_weights])

Exam Questions
==============

**Q1: ADAS Adversarial Attack (Hard)**

An attacker places stickers on a stop sign to fool an autonomous vehicle's object detector. Design defenses.

**Answer:**

**Defense 1: Multi-Sensor Fusion**

- **Camera:** Detects stop sign shape/color
- **LiDAR:** Detects 3D geometry (octagonal shape)
- **GPS + Map:** Knows stop sign location
- **Decision:** Require 2/3 sensors to agree

.. code-block:: python

    def detect_stop_sign_robust(camera_img, lidar_points, gps_location):
        camera_detect = cnn_model.predict(camera_img)  # May be fooled
        lidar_detect = detect_octagon(lidar_points)    # Shape-based
        map_detect = check_map_database(gps_location)  # Expected location
        
        votes = [camera_detect, lidar_detect, map_detect]
        if sum(votes) >= 2:
            return True  # Stop sign confirmed
        else:
            # Possible adversarial attack
            log_anomaly(camera_img, lidar_points, gps_location)
            return False

**Defense 2: Adversarial Training**

Train detector on images with stickers/graffiti.

**Defense 3: Ensemble Models**

Use multiple CNN architectures (ResNet, EfficientNet, YOLO) and vote.

**Q2: ML Model Update Security (Medium)**

A smart thermostat uses ML to predict occupancy. How to securely update the model OTA?

**Answer:**

.. code-block:: c

    #include <mbedtls/ecdsa.h>
    
    int update_ml_model(uint8_t *new_model, size_t len, uint8_t *signature) {
        // 1. Verify signature (prevent malicious model injection)
        uint8_t hash[32];
        mbedtls_sha256(new_model, len, hash, 0);
        
        if (!ecdsa_verify(hash, signature, oem_public_key)) {
            return -1;  // Invalid signature
        }
        
        // 2. Validate model (check header, version)
        if (!validate_model_format(new_model)) {
            return -1;
        }
        
        // 3. Test model on known inputs (sanity check)
        if (!test_model_accuracy(new_model)) {
            return -1;  // Model performs poorly
        }
        
        // 4. Flash new model
        flash_write(MODEL_ADDR, new_model, len);
        
        // 5. Atomic switchover
        update_model_pointer(MODEL_ADDR);
        
        return 0;
    }

Standards
=========

- **NIST AI RMF:** AI Risk Management Framework
- **MITRE ATLAS:** Adversarial Threat Landscape for AI Systems
- **ISO/IEC 23894:** AI risk management

**END OF DOCUMENT**
