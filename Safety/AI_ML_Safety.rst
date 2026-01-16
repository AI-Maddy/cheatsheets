🤖 **AI/ML Safety for Autonomous Systems — Safe Learning Under Uncertainty**
═══════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for Safe AI in Automotive, Aviation, Medical, and Robotics**  
**Domains:** Autonomous Vehicles 🚗 | Medical Diagnosis 🏥 | Industrial Robots 🏭 | Avionics 🛫  
**Standards:** UL 4600 | ISO/TR 5469 | ISO/SAE 21434 (AI security) | EASA AI Roadmap  
**Techniques:** Adversarial Testing | Formal Verification | Out-of-Distribution Detection | Explainability

═══════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**Why AI/ML Safety is Different:**

.. code-block:: text

   Traditional Software:
   ✅ Deterministic (same input → same output)
   ✅ Exhaustive testing possible (finite state machine)
   ✅ Provable correctness (formal methods)
   
   AI/ML Systems:
   ❌ Non-deterministic (probabilistic outputs)
   ❌ Infinite input space (cannot test all scenarios)
   ❌ Emergent behavior (learned, not programmed)
   ❌ Opaque (black-box neural networks)
   
   Challenge: How to certify "safe" when you can't enumerate all behaviors?

**Key AI Safety Challenges:**

.. code-block:: text

   1. Corner Cases (Long Tail):
      - Rare but critical scenarios (1 in 10 million miles)
      - Example: Pedestrian wearing cardboard box (Tesla FSD confusion)
   
   2. Adversarial Examples:
      - Tiny perturbations fool ML model
      - Example: Sticker on stop sign → Misclassified as speed limit
   
   3. Out-of-Distribution (OOD):
      - Input unlike training data
      - Example: Camera trained on sunny weather → Snow/fog failure
   
   4. Concept Drift:
      - Real world changes over time
      - Example: New road signs not in training data
   
   5. Black-Box Opacity:
      - Cannot explain why model made decision
      - Example: Medical AI denies treatment, no explanation

**Safety Assurance Approaches:**

+----------------------------+------------------------------------------+
| Approach                   | Example                                  |
+============================+==========================================+
| Runtime Monitoring         | Detect OOD inputs, flag for human review|
+----------------------------+------------------------------------------+
| Adversarial Training       | Train on adversarial examples (robust)  |
+----------------------------+------------------------------------------+
| Formal Verification        | Prove NN properties (e.g., monotonicity)|
+----------------------------+------------------------------------------+
| Diverse Redundancy         | Multiple ML models (voting)             |
+----------------------------+------------------------------------------+
| Explainability (XAI)       | LIME, SHAP (explain decisions)          |
+----------------------------+------------------------------------------+
| Bounded Uncertainty        | Bayesian NN (output confidence interval)|
+----------------------------+------------------------------------------+

**UL 4600 (Autonomous Vehicle Safety):**

.. code-block:: text

   Key Requirements:
   ✅ Hazard analysis for ML components (FMEA for neural networks)
   ✅ Test coverage arguments (statistical, not exhaustive)
   ✅ OOD detection (monitor for unusual inputs)
   ✅ Fail-safe behavior (safe degradation when uncertain)
   ✅ Field monitoring (continuous learning, incident reporting)

═══════════════════════════════════════════════════════════════════════════════

📖 **1. AI/ML SAFETY FUNDAMENTALS**
═══════════════════════════════════════════════════════════════════════════════

1.1 ML Model Types and Safety Implications
-------------------------------------------

**Supervised Learning (Classification, Regression):**

.. code-block:: text

   Use Case: Object detection (pedestrian, car, traffic sign)
   
   Safety Risk:
   - Misclassification (pedestrian labeled as shadow → No braking)
   - False positive (shadow labeled as pedestrian → Unnecessary braking)
   
   Mitigation:
   ✅ High precision/recall (minimize false negatives for pedestrians)
   ✅ Confidence thresholding (reject low-confidence predictions)
   ✅ Multi-sensor fusion (camera + LIDAR + radar voting)

**Reinforcement Learning (RL):**

.. code-block:: text

   Use Case: Robot navigation, game playing, control optimization
   
   Safety Risk:
   - Reward hacking (exploit reward function in unsafe way)
     Example: Robot learns to knock over obstacles to reach goal faster
   - Exploration (RL agent tries random actions during learning)
     Example: Self-driving car tries swerving into oncoming traffic (exploring)
   
   Mitigation:
   ✅ Safe exploration (constrain action space, no dangerous actions)
   ✅ Reward shaping (penalize unsafe actions heavily)
   ✅ Simulation training (learn in virtual environment, not real world)
   ✅ Human-in-the-loop (approve actions before execution)

**Unsupervised Learning (Anomaly Detection, Clustering):**

.. code-block:: text

   Use Case: Intrusion detection, fault detection
   
   Safety Risk:
   - Novel normal (legitimate behavior flagged as anomaly)
   - Novel attack (unknown attack not detected)
   
   Mitigation:
   ✅ Adaptive thresholds (reduce false positives)
   ✅ Human validation (operator confirms anomalies)

────────────────────────────────────────────────────────────────────────────

**1.2 The Data Problem**
------------------------

**Dataset Bias:**

.. code-block:: text

   Problem: Training data not representative of real world
   
   Example 1: Facial recognition trained mostly on white faces
   Result: Higher error rate for people of color (unfair, unsafe)
   
   Example 2: Autonomous car trained in California (sunny)
   Result: Fails in snow, fog, rain (most of North America/Europe unsafe)

**Mitigation:**

.. code-block:: python

   # Check dataset demographics
   import pandas as pd
   
   # Example: Pedestrian detection dataset
   dataset_stats = {
       'Weather': ['Sunny', 'Cloudy', 'Rain', 'Snow', 'Fog'],
       'Count': [15000, 3000, 1500, 500, 200],  # Imbalanced!
       'Percentage': [75.0, 15.0, 7.5, 2.5, 1.0]
   }
   
   df = pd.DataFrame(dataset_stats)
   print(df)
   
   # Action: Collect more data for underrepresented scenarios
   # Or use data augmentation (synthetic rain/snow)

**Data Augmentation (Safety-Aware):**

.. code-block:: python

   import albumentations as A
   
   # Augment images with weather conditions
   transform = A.Compose([
       A.RandomRain(p=0.3),         # Simulate rain
       A.RandomSnow(p=0.2),         # Simulate snow
       A.RandomFog(p=0.2),          # Simulate fog
       A.RandomBrightnessContrast(p=0.5),  # Day/night variation
   ])
   
   # Apply to training images
   augmented_image = transform(image=original_image)['image']

────────────────────────────────────────────────────────────────────────────

**1.3 Metrics for Safety-Critical ML**
--------------------------------------

**Beyond Accuracy:**

.. code-block:: text

   Accuracy = (TP + TN) / (TP + TN + FP + FN)
   
   Problem: Accuracy can be misleading for imbalanced datasets
   
   Example: 99.9% of time, no pedestrian in camera view
   Model that NEVER detects pedestrians: 99.9% accuracy (useless!)

**Safety-Critical Metrics:**

.. code-block:: text

   Recall (Sensitivity):
   Recall = TP / (TP + FN)
   
   Use Case: Pedestrian detection (minimize false negatives)
   Target: Recall ≥ 99.9% (catch 999 out of 1000 pedestrians)
   
   Precision:
   Precision = TP / (TP + FP)
   
   Use Case: Emergency braking (minimize false positives)
   Target: Precision ≥ 95% (avoid nuisance braking)
   
   F1 Score (Harmonic Mean):
   F1 = 2 × (Precision × Recall) / (Precision + Recall)

**Confusion Matrix for Pedestrian Detection:**

+----------------+-------------------+-------------------+
|                | Predicted: Ped    | Predicted: No Ped |
+================+===================+===================+
| Actual: Ped    | TP = 995          | **FN = 5** ❌     |
|                | (Correct detect)  | (Missed ped)      |
+----------------+-------------------+-------------------+
| Actual: No Ped | FP = 50           | TN = 9950         |
|                | (False alarm)     | (Correct negative)|
+----------------+-------------------+-------------------+

.. code-block:: text

   Recall = 995 / (995 + 5) = 99.5% ✅ (Good, only 5 missed)
   Precision = 995 / (995 + 50) = 95.2% ✅ (Acceptable false alarms)
   
   Safety Concern: 5 missed pedestrians (FN) → Potential collision

═══════════════════════════════════════════════════════════════════════════════

📖 **2. ADVERSARIAL ROBUSTNESS**
═══════════════════════════════════════════════════════════════════════════════

2.1 Adversarial Examples
-------------------------

**Definition:** Intentionally crafted inputs that fool ML model

**Example: Image Classification Attack**

.. code-block:: python

   import torch
   import torch.nn.functional as F
   
   # Original image: Correctly classified as "Stop Sign"
   image = load_image('stop_sign.jpg')
   model = load_pretrained_model()
   
   prediction = model(image)
   print(f"Original: {prediction}")  # Output: "Stop Sign" (99.8% confidence)
   
   # Generate adversarial perturbation (FGSM attack)
   epsilon = 0.01  # Small perturbation (imperceptible to human)
   image.requires_grad = True
   
   output = model(image)
   loss = F.cross_entropy(output, target_class)  # Target: "Speed Limit 30"
   loss.backward()
   
   # Create adversarial image
   adversarial_image = image + epsilon * image.grad.sign()
   
   # Test adversarial image
   adv_prediction = model(adversarial_image)
   print(f"Adversarial: {adv_prediction}")  # Output: "Speed Limit 30" (95% conf)
   
   # Result: Model fooled by tiny change (human cannot see difference)

**Real-World Attack (Physical):**

.. code-block:: text

   Researchers placed stickers on stop sign
   → Autonomous vehicle misclassified as "Speed Limit 45"
   → Car accelerated through stop sign (dangerous!)

────────────────────────────────────────────────────────────────────────────

**2.2 Adversarial Training (Defense)**
--------------------------------------

**Approach:** Include adversarial examples in training data

.. code-block:: python

   def adversarial_training(model, train_loader, epochs):
       for epoch in range(epochs):
           for images, labels in train_loader:
               # 1. Train on clean examples
               clean_output = model(images)
               clean_loss = F.cross_entropy(clean_output, labels)
               
               # 2. Generate adversarial examples
               adv_images = fgsm_attack(model, images, labels, epsilon=0.01)
               
               # 3. Train on adversarial examples
               adv_output = model(adv_images)
               adv_loss = F.cross_entropy(adv_output, labels)
               
               # 4. Combined loss (clean + adversarial)
               total_loss = clean_loss + adv_loss
               total_loss.backward()
               optimizer.step()

**Result:** Model robust to small perturbations (80-90% accuracy on adversarial examples, vs 0-10% without training)

────────────────────────────────────────────────────────────────────────────

**2.3 Formal Verification of Neural Networks**
----------------------------------------------

**Goal:** Prove neural network satisfies specification

**Example Specification:**

.. code-block:: text

   For all stop sign images with brightness ∈ [0.5, 1.0],
   network outputs "Stop Sign" with confidence ≥ 90%

**Verification Tools:**

.. code-block:: text

   1. Reluplex (ReLU-based verification)
      - Verifies small networks (hundreds of neurons)
      - Complete (finds violations or proves correctness)
   
   2. Marabou (NASA tool)
      - Verifies aircraft collision avoidance neural network (ACAS Xu)
      - Proves safety properties (e.g., "Never advise climb when descending")
   
   3. CROWN (Certified Robustness via Convex Optimization)
      - Computes certified bounds on output
      - Faster, scales to larger networks (thousands of neurons)

**Example: Verified Collision Avoidance**

.. code-block:: text

   Aircraft Collision Avoidance System (ACAS Xu):
   - Neural network replaces lookup tables
   - Input: Relative position, velocity of intruder aircraft
   - Output: Advisory (clear-of-conflict, climb, descend, etc.)
   
   Verification:
   ✅ Property 1: If intruder far away → Advisory: "clear-of-conflict"
   ✅ Property 2: If intruder close and climbing → Do NOT advise "climb"
   ✅ Property 3: If previous advisory was "descend" → Do NOT reverse to "climb"
                  (avoid oscillation)
   
   Tool (Marabou) proves all properties hold for trained network

═══════════════════════════════════════════════════════════════════════════════

📖 **3. OUT-OF-DISTRIBUTION (OOD) DETECTION**
═══════════════════════════════════════════════════════════════════════════════

3.1 OOD Problem
---------------

**Definition:** Input significantly different from training distribution

.. code-block:: text

   Training Data: Images of cars, pedestrians, bicycles (daytime, clear)
   
   OOD Examples:
   - Kangaroo on road (not in training set)
   - Dense fog (low visibility, unlike training data)
   - Alien spacecraft (extreme OOD, obviously)
   
   Problem: Neural network makes prediction with high confidence
            even for OOD inputs (overconfident on unknown)

**Real Incident:**

.. code-block:: text

   Uber Self-Driving Car (2018):
   - Pedestrian walking bicycle across road at night
   - Vision system confused (person? bicycle? unknown?)
   - Multiple misclassifications (person, bicycle, other, person...)
   - Emergency braking disabled (to avoid false positives)
   - Result: Fatal collision

────────────────────────────────────────────────────────────────────────────

**3.2 OOD Detection Methods**
-----------------------------

**Softmax Confidence Thresholding:**

.. code-block:: python

   def detect_ood_confidence(model, image, threshold=0.95):
       """Simple OOD detection via softmax confidence"""
       output = model(image)
       probabilities = F.softmax(output, dim=1)
       max_confidence = torch.max(probabilities)
       
       if max_confidence < threshold:
           return "OOD: Low confidence"  # Reject input
       else:
           prediction = torch.argmax(probabilities)
           return f"In-distribution: Class {prediction}"
   
   # Problem: Neural networks often overconfident on OOD inputs

**ODIN (Out-of-Distribution Detector for Neural Networks):**

.. code-block:: python

   def odin_score(model, image, temperature=1000, epsilon=0.001):
       """Improved OOD detection using temperature scaling + perturbation"""
       # 1. Temperature scaling (reduce overconfidence)
       output = model(image) / temperature
       
       # 2. Input preprocessing (small perturbation toward most confident class)
       image.requires_grad = True
       loss = F.cross_entropy(output, torch.argmax(output))
       loss.backward()
       perturbed_image = image - epsilon * image.grad.sign()
       
       # 3. Compute softmax score
       output = model(perturbed_image) / temperature
       score = torch.max(F.softmax(output, dim=1))
       
       return score  # Lower score → More likely OOD

**Mahalanobis Distance (Statistical Method):**

.. code-block:: python

   import numpy as np
   from scipy.spatial.distance import mahalanobis
   
   def mahalanobis_ood_score(features, class_means, class_covs):
       """Compute Mahalanobis distance to nearest class centroid"""
       distances = []
       for class_id in range(len(class_means)):
           dist = mahalanobis(features, class_means[class_id], 
                             np.linalg.inv(class_covs[class_id]))
           distances.append(dist)
       
       return min(distances)  # Distance to nearest class
       # Large distance → OOD
   
   # Threshold calibration (use validation set)
   threshold = np.percentile(in_distribution_distances, 95)
   
   if distance > threshold:
       return "OOD detected"

────────────────────────────────────────────────────────────────────────────

**3.3 Safe Degradation (OOD Response)**
---------------------------------------

**Strategy:** When OOD detected, fall back to safe mode

.. code-block:: python

   def autonomous_driving_with_ood_detection(sensor_data):
       """Safe degradation example for autonomous vehicle"""
       
       # Process camera image
       camera_image = sensor_data['camera']
       ood_score = odin_score(vision_model, camera_image)
       
       if ood_score < OOD_THRESHOLD:
           # OOD detected (e.g., dense fog, unusual object)
           log_incident("OOD: Score {ood_score}, timestamp {time.time()}")
           
           # Safe degradation options:
           # Option 1: Reduce speed, increase following distance
           target_speed = min(current_speed, 15)  # mph (slow down)
           alert_driver("Limited visibility, reducing speed")
           
           # Option 2: Request driver takeover
           if driver_available:
               request_takeover(urgency="medium", reason="Unusual conditions")
           
           # Option 3: Pull over (if no driver available)
           else:
               initiate_minimal_risk_maneuver()  # Pull to shoulder, stop
           
           return SAFE_MODE
       
       else:
           # Normal operation (in-distribution)
           prediction = vision_model(camera_image)
           return prediction

═══════════════════════════════════════════════════════════════════════════════

📖 **4. EXPLAINABILITY (XAI)**
═══════════════════════════════════════════════════════════════════════════════

4.1 Why Explainability Matters for Safety
------------------------------------------

**Challenges with Black-Box ML:**

.. code-block:: text

   Problem 1: Cannot debug failures
   - Neural network misclassifies → Why?
   - No insight into decision process
   
   Problem 2: Cannot trust in safety-critical applications
   - Medical: AI recommends surgery, no explanation (doctor hesitant)
   - Automotive: Self-driving car swerves, no reason given (passenger alarmed)
   
   Problem 3: Regulatory compliance
   - EU GDPR: "Right to explanation" for automated decisions
   - Medical: FDA requires justification for AI-assisted diagnosis

────────────────────────────────────────────────────────────────────────────

**4.2 LIME (Local Interpretable Model-Agnostic Explanations)**
--------------------------------------------------------------

**Concept:** Explain individual predictions by approximating model locally

.. code-block:: python

   from lime import lime_image
   from lime.wrappers.scikit_image import SegmentationAlgorithm
   
   def explain_image_classification(image, model):
       """Generate explanation for image classification decision"""
       explainer = lime_image.LimeImageExplainer()
       
       # Explain prediction
       explanation = explainer.explain_instance(
           image, 
           model.predict,
           top_labels=1, 
           num_samples=1000  # Perturb image 1000 times
       )
       
       # Get important regions (superpixels)
       temp, mask = explanation.get_image_and_mask(
           explanation.top_labels[0], 
           positive_only=True, 
           num_features=5,  # Top 5 regions
           hide_rest=False
       )
       
       return temp, mask
   
   # Example output:
   # "Model classified as 'pedestrian' based on:
   #  - Upper body region (60% importance)
   #  - Leg movement (25% importance)
   #  - Vertical posture (15% importance)"

────────────────────────────────────────────────────────────────────────────

**4.3 SHAP (SHapley Additive exPlanations)**
--------------------------------------------

**Based on Game Theory (Shapley Values):**

.. code-block:: python

   import shap
   
   def explain_with_shap(model, X_train, x_test):
       """Compute SHAP values for feature importance"""
       explainer = shap.Explainer(model, X_train)
       shap_values = explainer(x_test)
       
       # Visualize feature contributions
       shap.waterfall_plot(shap_values[0])
       
       return shap_values
   
   # Example: Medical diagnosis
   # Features: [age, BMI, blood_pressure, glucose, ...]
   # SHAP output:
   #   Base prediction: 30% diabetes risk
   #   + Age (65): +15%
   #   + Glucose (180): +25%
   #   - Exercise (yes): -10%
   #   = Final prediction: 60% diabetes risk

**Safety Benefit:** Clinician can verify AI reasoning (catch errors, build trust)

────────────────────────────────────────────────────────────────────────────

**4.4 Attention Visualization (CNNs)**
-------------------------------------

**Grad-CAM (Gradient-weighted Class Activation Mapping):**

.. code-block:: python

   import torch.nn.functional as F
   
   def grad_cam(model, image, target_class):
       """Visualize which parts of image influenced decision"""
       # Forward pass
       features = model.features(image)  # Convolutional features
       output = model.classifier(features)
       
       # Backward pass (compute gradients)
       model.zero_grad()
       one_hot = torch.zeros_like(output)
       one_hot[0][target_class] = 1
       output.backward(gradient=one_hot)
       
       # Compute class activation map
       gradients = model.get_gradients()  # Gradients of target class
       pooled_gradients = torch.mean(gradients, dim=[2, 3])
       
       activations = model.get_activations(image)
       for i in range(activations.shape[1]):
           activations[:, i, :, :] *= pooled_gradients[i]
       
       heatmap = torch.mean(activations, dim=1).squeeze()
       heatmap = F.relu(heatmap)  # ReLU to keep positive contributions
       
       return heatmap  # Overlay on original image (shows where model looked)

**Example Output:**

.. code-block:: text

   Image: Stop sign in complex urban scene
   Grad-CAM heatmap: Red region highlights octagonal shape + red color
   Interpretation: Model correctly focusing on stop sign (not background)

═══════════════════════════════════════════════════════════════════════════════

📖 **5. STANDARDS AND REGULATIONS**
═══════════════════════════════════════════════════════════════════════════════

5.1 UL 4600 (Autonomous Vehicles)
----------------------------------

**Standard:** UL 4600 — Safety for Evaluation of Autonomous Products

**Key Requirements:**

.. code-block:: text

   1. Risk Assessment:
      ✅ Identify hazards specific to ML components
      ✅ FMEA for neural networks (failure modes: misclassification, OOD)
   
   2. Validation & Verification:
      ✅ Scenario-based testing (not just miles driven)
      ✅ Corner case testing (adversarial examples, edge cases)
      ✅ Statistical argument (probabilistic coverage)
   
   3. Data Quality:
      ✅ Dataset representativeness (demographics, weather, geography)
      ✅ Labeling accuracy (ground truth validation)
      ✅ Data augmentation justified
   
   4. Runtime Monitoring:
      ✅ OOD detection (flag unusual inputs)
      ✅ Performance monitoring (detect degradation over time)
   
   5. Safe Degradation:
      ✅ Minimal risk condition (safe mode when uncertain)
      ✅ Human takeover (request driver intervention)
   
   6. Field Monitoring:
      ✅ Incident reporting (crashes, near-misses)
      ✅ Continuous improvement (retrain on field data)

────────────────────────────────────────────────────────────────────────────

**5.2 ISO/TR 5469 (Automotive AI/ML)**
--------------------------------------

**Technical Report:** ISO/TR 5469 — Road vehicles — Functional safety — AI/ML in safety-related systems

**Challenges Identified:**

.. code-block:: text

   1. Specification Completeness:
      - Traditional: Enumerate all input/output pairs
      - ML: Infinite input space (cannot enumerate)
      
      Approach: Statistical specification (e.g., "95% recall on pedestrians")
   
   2. Known Unknowns vs Unknown Unknowns:
      - Known unknowns: Identified corner cases (test explicitly)
      - Unknown unknowns: Unforeseen scenarios (OOD detection)
   
   3. Continuous Learning:
      - ML model updated with new data (OTA updates)
      - Re-certification required? (expensive, impractical)
      
      Approach: Bounded retraining (only update last layers, verify outputs)

**Proposed Safety Architecture:**

.. code-block:: text

   ┌────────────────────────────────────────────────┐
   │ Deterministic Safety Supervisor                │
   │ (ISO 26262 ASIL D, traditional software)       │
   │ - Monitors ML output                           │
   │ - Overrides if unsafe (e.g., OOD detected)     │
   └────────────────────────────────────────────────┘
                     ▲
                     │ ML Output + Confidence
                     ▼
   ┌────────────────────────────────────────────────┐
   │ ML Perception System                           │
   │ (QM or ASIL B, cannot achieve ASIL D alone)    │
   │ - Object detection, classification             │
   │ - OOD detection, uncertainty estimation        │
   └────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────

**5.3 EASA AI Roadmap (Aviation)**
----------------------------------

**European Union Aviation Safety Agency (EASA):**

.. code-block:: text

   Roadmap for AI in Aviation (2025-2030):
   
   Level 1: Human-Assisted (AI provides recommendations)
   - Example: Pilot decision support (weather routing)
   - Certification: DO-178C with ML annex (in development)
   
   Level 2: Human-Supervised (AI acts, human monitors)
   - Example: Autopilot with ML-based collision avoidance
   - Certification: Enhanced DO-178C + continuous monitoring
   
   Level 3: Human-On-The-Loop (AI autonomous, human intervenes if needed)
   - Example: Autonomous cargo aircraft (remote pilot on standby)
   - Certification: New framework (under development, 2028 target)
   
   Level 4: Fully Autonomous (no human in loop)
   - Example: Unmanned delivery drones
   - Certification: Completely new approach (2030+)

**Current Status (2026):** Level 1-2 only, Level 3-4 research phase

═══════════════════════════════════════════════════════════════════════════════

📖 **6. TESTING AND VALIDATION**
═══════════════════════════════════════════════════════════════════════════════

6.1 Scenario-Based Testing
---------------------------

**Challenge:** Cannot drive infinite miles to test autonomous vehicle

**Approach:** Define critical scenarios, test exhaustively

.. code-block:: text

   Scenario Taxonomy (Pegasus Project):
   
   1. Functional Scenarios:
      - Lane change
      - Intersection crossing
      - Overtaking
   
   2. Environmental Conditions:
      - Weather: Sunny, rain, snow, fog
      - Time: Day, dusk, night
      - Lighting: Direct sun, shadows, tunnel
   
   3. Traffic Participants:
      - Vehicles: Car, truck, motorcycle, bicycle
      - Pedestrians: Adult, child, wheelchair
      - Animals: Deer, dog
   
   4. Edge Cases:
      - Construction zone (lane markings covered)
      - Emergency vehicle (siren, flashing lights)
      - Fallen debris (unexpected obstacle)

**Test Coverage Argument:**

.. code-block:: text

   Traditional: "Tested all possible inputs" (impossible for ML)
   
   Statistical: "Tested representative sample of operational design domain"
   
   Example:
   - 10,000 simulation scenarios
   - 100,000 real-world miles
   - Covers 95% of expected situations (statistical confidence)
   - Remaining 5%: OOD detection + safe degradation

────────────────────────────────────────────────────────────────────────────

**6.2 Metamorphic Testing**
---------------------------

**Concept:** Test relationships between inputs/outputs

.. code-block:: python

   def metamorphic_test_brightness(model, image):
       """Test: Darker image should still be same class"""
       original_pred = model(image)
       
       # Apply brightness reduction
       dark_image = adjust_brightness(image, factor=0.5)
       dark_pred = model(dark_image)
       
       # Metamorphic relation: Class should not change
       assert original_pred == dark_pred, \
           f"Brightness change altered classification: {original_pred} → {dark_pred}"
   
   def metamorphic_test_rotation(model, image):
       """Test: Small rotation should not change class"""
       original_pred = model(image)
       
       # Rotate image 5 degrees
       rotated_image = rotate_image(image, angle=5)
       rotated_pred = model(rotated_image)
       
       assert original_pred == rotated_pred, \
           f"Small rotation altered classification"

**Benefit:** Finds failures without ground truth labels (oracle problem solved)

────────────────────────────────────────────────────────────────────────────

**6.3 Simulation-Based Testing**
--------------------------------

**Tools:**

.. code-block:: text

   CARLA (Open-source autonomous driving simulator):
   - Realistic urban environments
   - Pedestrians, vehicles, traffic lights
   - Weather simulation (rain, fog, night)
   
   LGSVL (LG Silicon Valley Lab simulator):
   - High-fidelity sensor simulation (camera, LIDAR, radar)
   - Integration with Apollo, Autoware platforms
   
   AirSim (Microsoft, drone/autonomous vehicle):
   - Unreal Engine graphics
   - Physics simulation
   - Sensor noise models

**Sim-to-Real Gap:**

.. code-block:: text

   Problem: ML trained in simulation may fail in real world
   
   Example: Simulated camera images too clean (no lens flare, dirt)
   Result: Real-world performance degraded
   
   Mitigation:
   ✅ Domain randomization (vary simulation parameters)
   ✅ Photo-realistic rendering (improve visual fidelity)
   ✅ Transfer learning (fine-tune on real-world data)

═══════════════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═══════════════════════════════════════════════════════════════════════════════

**Q1:** Why is AI/ML safety different from traditional software safety?

**A1:**

.. code-block:: text

   Traditional Software:
   ✅ Deterministic (same input always produces same output)
   ✅ Finite state space (can enumerate all behaviors)
   ✅ Specified behavior (programmer defines all logic)
   ✅ Testable exhaustively (test all states/transitions)
   ✅ Formal verification possible (model checking, theorem proving)
   
   AI/ML Systems:
   ❌ Non-deterministic (probabilistic outputs, even stochastic models)
   ❌ Infinite input space (images, sensor data → cannot test all)
   ❌ Learned behavior (emergent from data, not explicitly programmed)
   ❌ Cannot test exhaustively (statistical coverage arguments needed)
   ❌ Black-box (neural networks opaque, hard to verify)
   
   Safety Implications:
   - Cannot prove correctness (statistical confidence instead)
   - Corner cases hard to anticipate (long-tail distribution)
   - Adversarial vulnerabilities (tiny perturbations fool model)
   - Out-of-distribution failures (novel inputs mishandled)
   
   Approach:
   ✅ Runtime monitoring (OOD detection, confidence thresholds)
   ✅ Safe degradation (fall back to safe mode when uncertain)
   ✅ Diverse redundancy (multiple ML models, classical fallback)
   ✅ Continuous validation (field monitoring, retraining)

────────────────────────────────────────────────────────────────────────────

**Q2:** What are adversarial examples and how do they threaten safety-critical ML?

**A2:**

**Definition:**

.. code-block:: text

   Adversarial Example: Intentionally crafted input that fools ML model
   
   Characteristics:
   - Small perturbation (imperceptible to human)
   - Causes misclassification (wrong output with high confidence)

**Example:**

.. code-block:: text

   Original Image: Stop sign → Classified as "Stop Sign" (99.8%)
   
   Add Adversarial Noise: Tiny pixel changes (human cannot see difference)
   
   Adversarial Image: Stop sign → Classified as "Speed Limit 45" (95%)
   
   Safety Impact: Autonomous vehicle accelerates through stop sign

**Real-World Physical Attack:**

.. code-block:: text

   Researchers placed stickers on stop sign (specific pattern)
   → Self-driving car misclassified as "Speed Limit"
   → Car did not stop (dangerous!)

**Defenses:**

.. code-block:: text

   1. Adversarial Training:
      - Train model on adversarial examples
      - Result: 80-90% robust (vs 0-10% without training)
   
   2. Input Preprocessing:
      - JPEG compression (removes high-frequency noise)
      - Random resizing/cropping
   
   3. Ensemble Methods:
      - Multiple models vote (harder to fool all simultaneously)
   
   4. Formal Verification:
      - Prove robustness within epsilon-ball around input
      - Tools: Marabou, CROWN, Reluplex
   
   5. Runtime Detection:
      - Detect adversarial inputs (statistical anomaly detection)
      - Reject suspicious inputs

────────────────────────────────────────────────────────────────────────────

**Q3:** What is out-of-distribution (OOD) detection and why is it critical for AI safety?

**A3:**

**Out-of-Distribution (OOD):**

.. code-block:: text

   Definition: Input significantly different from training data distribution
   
   Example:
   Training Data: Cars, pedestrians, bicycles (California, sunny weather)
   
   OOD Inputs:
   - Kangaroo on road (Australia, not in training set)
   - Heavy snow (visibility degraded, unlike training)
   - Construction equipment (unusual object)

**Problem:**

.. code-block:: text

   Neural networks make predictions with HIGH CONFIDENCE on OOD inputs
   (overconfident on unknown)
   
   Example: Model sees kangaroo, predicts "pedestrian" with 95% confidence
   → Autonomous vehicle treats as pedestrian (wrong behavior)

**Real Incident:**

.. code-block:: text

   Uber Self-Driving Car (2018):
   - Pedestrian walking bicycle at night (unusual scenario)
   - Vision system confused (misclassified multiple times)
   - Emergency braking disabled (to avoid false positives)
   - Result: Fatal collision

**OOD Detection Methods:**

.. code-block:: text

   1. Confidence Thresholding:
      - Reject inputs with low softmax confidence
      - Problem: NNs often overconfident on OOD
   
   2. ODIN (Out-of-Distribution Detector):
      - Temperature scaling + input perturbation
      - Improved OOD detection vs simple thresholding
   
   3. Mahalanobis Distance:
      - Compute distance to nearest class centroid (in feature space)
      - Large distance → OOD
   
   4. Ensemble Disagreement:
      - Multiple models vote
      - High disagreement → OOD (models uncertain)

**Safe Response to OOD:**

.. code-block:: text

   When OOD detected:
   ✅ Reduce speed, increase following distance
   ✅ Request human takeover (driver intervention)
   ✅ Pull over safely (minimal risk maneuver)
   ✅ Log incident (for retraining, continuous improvement)

────────────────────────────────────────────────────────────────────────────

**Q4:** What is UL 4600 and what does it require for autonomous vehicle safety?

**A4:**

**UL 4600:**

.. code-block:: text

   Standard: Safety for Evaluation of Autonomous Products
   Scope: Autonomous vehicles, robots, drones
   Status: Published 2020, updated 2024

**Key Requirements:**

.. code-block:: text

   1. Risk Assessment:
      ✅ Hazard analysis for ML components (FMEA for neural networks)
      ✅ Identify ML-specific failure modes (misclassification, OOD, drift)
   
   2. Data Management:
      ✅ Dataset representativeness (weather, geography, demographics)
      ✅ Labeling quality (ground truth validation, inter-annotator agreement)
      ✅ Data augmentation justified (document synthetic data generation)
   
   3. Validation & Verification:
      ✅ Scenario-based testing (not just miles driven)
      ✅ Corner case coverage (adversarial examples, edge cases)
      ✅ Statistical argument (probabilistic coverage, not exhaustive)
   
   4. Runtime Monitoring:
      ✅ OOD detection (flag unusual inputs)
      ✅ Performance monitoring (detect degradation over time)
      ✅ Uncertainty quantification (model outputs confidence intervals)
   
   5. Safe Degradation:
      ✅ Minimal risk condition (safe mode when uncertain)
      ✅ Human takeover request (driver intervention)
      ✅ Fail-safe mechanisms (classical fallback algorithms)
   
   6. Field Monitoring:
      ✅ Incident reporting (crashes, near-misses, disengagements)
      ✅ Continuous learning (retrain on field data)
      ✅ Version control (track model updates, rollback if issues)

**Difference from Traditional Standards (ISO 26262):**

.. code-block:: text

   ISO 26262: Deterministic systems, exhaustive testing
   UL 4600: Probabilistic systems, statistical arguments, runtime monitoring

────────────────────────────────────────────────────────────────────────────

**Q5:** Explain LIME and SHAP explainability techniques for ML models.

**A5:**

**LIME (Local Interpretable Model-Agnostic Explanations):**

.. code-block:: text

   Goal: Explain individual predictions
   
   Process:
   1. Take input (e.g., image of X-ray)
   2. Perturb input (generate similar samples)
   3. Get model predictions on perturbed samples
   4. Fit simple model (e.g., linear regression) to local samples
   5. Interpret simple model (feature importance)
   
   Example (Medical Diagnosis):
   Input: Chest X-ray → Prediction: "Pneumonia" (90% confidence)
   
   LIME Output:
   - Lung lower left region: +35% (opaque area, supports diagnosis)
   - Lung upper right region: +20% (infiltrate pattern)
   - Heart shadow: -5% (normal, slightly reduces confidence)
   
   Interpretation: Model focusing on correct anatomical regions

**SHAP (SHapley Additive exPlanations):**

.. code-block:: text

   Goal: Explain predictions using game theory (Shapley values)
   
   Shapley Value: Contribution of each feature to final prediction
   
   Properties:
   ✅ Additivity: Sum of SHAP values = (Prediction - Base rate)
   ✅ Consistency: If feature helps more, SHAP value increases
   
   Example (Credit Approval):
   Base rate: 30% approval
   
   SHAP values:
   + Income ($100k): +25%
   + Credit score (750): +15%
   - Debt-to-income ratio (40%): -10%
   + Employment (10 years): +5%
   
   Final prediction: 30% + 25% + 15% - 10% + 5% = 65% approval

**Comparison:**

+----------------+----------------------+-------------------------+
| Aspect         | LIME                 | SHAP                    |
+================+======================+=========================+
| Scope          | Local (single input) | Local + Global          |
+----------------+----------------------+-------------------------+
| Theory         | Local approximation  | Game theory (Shapley)   |
+----------------+----------------------+-------------------------+
| Consistency    | Not guaranteed       | Guaranteed (axiomatic)  |
+----------------+----------------------+-------------------------+
| Speed          | Faster               | Slower (exact SHAP)     |
+----------------+----------------------+-------------------------+
| Use Case       | Quick explanations   | High-stakes decisions   |
|                |                      | (medical, legal)        |
+----------------+----------------------+-------------------------+

**Safety Benefit:**

.. code-block:: text

   ✅ Verify model reasoning (catch spurious correlations)
   ✅ Build trust (clinician understands AI recommendation)
   ✅ Debugging (identify why model fails on specific inputs)
   ✅ Regulatory compliance (EU GDPR "right to explanation")

═══════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Fundamentals:**
- [ ] AI/ML safety differs from traditional (non-deterministic, infinite input space)
- [ ] Corner cases, adversarial examples, OOD, concept drift, opacity
- [ ] Safety metrics (recall, precision, F1 vs accuracy)

**Adversarial Robustness:**
- [ ] Adversarial examples (FGSM, physical attacks)
- [ ] Adversarial training (include attacks in training data)
- [ ] Formal verification (Marabou, CROWN, Reluplex)

**OOD Detection:**
- [ ] Confidence thresholding, ODIN, Mahalanobis distance
- [ ] Safe degradation (minimal risk maneuver when OOD)

**Explainability:**
- [ ] LIME (local approximation, fast)
- [ ] SHAP (Shapley values, axiomatic)
- [ ] Grad-CAM (visualize attention in CNNs)

**Standards:**
- [ ] UL 4600 (autonomous vehicles, scenario-based testing)
- [ ] ISO/TR 5469 (automotive AI/ML challenges)
- [ ] EASA AI Roadmap (aviation levels 1-4)

**Testing:**
- [ ] Scenario-based testing (Pegasus taxonomy)
- [ ] Metamorphic testing (test relationships)
- [ ] Simulation (CARLA, LGSVL, AirSim)

═══════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
═══════════════════════════════════════════════════════════════════════════════

1️⃣ **AI/ML cannot be certified like traditional software** — Infinite input space, probabilistic outputs, emergent behavior → Statistical arguments + runtime monitoring required

2️⃣ **Adversarial robustness is critical** — Tiny perturbations fool models (physical stickers on stop signs) → Adversarial training, formal verification, ensemble methods needed

3️⃣ **Out-of-distribution detection prevents blind failures** — NNs overconfident on unknown inputs (kangaroo misclassified as pedestrian) → OOD detection + safe degradation mandatory

4️⃣ **Black-box opacity is a safety risk** — Cannot explain decisions → Explainability (LIME, SHAP) builds trust, enables debugging, satisfies regulations

5️⃣ **UL 4600 is the leading standard** — Scenario-based testing, OOD detection, runtime monitoring, field data collection → Replace traditional exhaustive testing

6️⃣ **Deterministic supervisor over ML** — ISO 26262 ASIL D safety monitor wraps ML component (QM/ASIL B) → Hybrid architecture until ML certification matures

7️⃣ **Simulation + real-world testing** — Cannot drive infinite miles → Scenario taxonomy (Pegasus), metamorphic testing, continuous field monitoring

═══════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **AI/ML SAFETY CHEATSHEET COMPLETE**

**Created:** January 16, 2026  
**Coverage:** AI/ML safety fundamentals, adversarial robustness (FGSM, adversarial training, formal verification), OOD detection (ODIN, Mahalanobis, safe degradation), explainability (LIME, SHAP, Grad-CAM), standards (UL 4600, ISO/TR 5469, EASA AI Roadmap), testing (scenario-based, metamorphic, simulation)

═══════════════════════════════════════════════════════════════════════════════
