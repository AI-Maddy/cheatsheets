
================================================================================
🧮 Computer Vision (CV) & Deep Learning Architecture Guide
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



**2026 Cheatsheet**: Modern CV spans traditional image processing to AI-driven perception, optimized for edge deployment with emphasis on real-time responsiveness, privacy, and efficiency.

---

⚙️ **1. Core Vision Tasks & State-of-the-Art (SOTA) Models**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

⚙️ Image Classification

**Task**: Assign a label to an entire image
⭐ - **Keywords**: Feature extraction, backbone networks, softmax, cross-entropy loss, ImageNet-1K
- **SOTA 2026 Models**:
  - **EfficientNet-v3**: Balanced accuracy-latency tradeoff via compound scaling (depth, width, resolution)
  - **Vision Transformers (ViT)**: Transformer-based architecture treating images as sequences of patches; superior for large-scale pretraining
  - **ConvNeXt**: Modern CNN redesign matching or exceeding Vision Transformer performance with simpler architecture
- **Metrics**: Top-1 accuracy, Top-5 accuracy, latency (ms), model size (MB), FLOPs
- **Techniques**: Data augmentation (RandAugment, AutoAugment), regularization (dropout, label smoothing)

⚙️ Object Detection

**Task**: Identify and localize objects with bounding boxes (coordinates + class label)
⭐ - **Keywords**: Bounding box regression, confidence scores, Intersection over Union (IoU), anchor-free detection, center-point based
- **SOTA 2026 Standard: YOLO26**
  - **Architecture**: Unified single-stage detector; no region proposals (unlike R-CNN variants)
⭐   - **Key Innovation**: NMS-free (non-maximum suppression-free) inference pipeline for reduced edge latency
  - **Output Format**: (x_center, y_center, width, height, objectness_score, class_scores)
  - **Advantages**: Real-time inference on edge CPUs, minimal post-processing overhead
- **Alternative Architectures**:
  - **Faster R-CNN**: Two-stage detector with Region Proposal Networks (RPN); higher accuracy, higher latency
  - **SSD (Single Shot MultiBox)**: Single-stage with multi-scale predictions
  - **EfficientDet**: Scalable detection with BiFPN for multi-scale feature fusion
- **Metrics**: mAP (mean Average Precision), mAP50, mAP75, latency, throughput (FPS)

⚙️ Segmentation

#### Semantic Segmentation
**Task**: Classify every pixel into a semantic class
⭐ - **Keywords**: Fully convolutional networks (FCN), encoder-decoder, upsampling, dilated convolution, atrous convolution
- **SOTA Models**:
  - **DeepLabv3+**: Atrous spatial pyramid pooling (ASPP) for multi-scale context
  - **Segformer**: Vision Transformer-based with efficient decoder
  - **U-Net**: Medical imaging standard; symmetric encoder-decoder with skip connections
- **Common Applications**: Scene understanding, autonomous driving (road, sidewalk, pedestrian detection)
- **Loss Functions**: Cross-entropy, Dice loss, Focal loss (for imbalanced datasets)
- **Metrics**: Intersection over Union (IoU/Jaccard), mean IoU (mIoU), Frequency-weighted IoU

#### Instance Segmentation
**Task**: Distinguish between different objects of the same class (e.g., "Car 1" vs "Car 2") and assign per-pixel labels
⭐ - **Keywords**: Panoptic segmentation, mask-based detection, region-based segmentation
- **SOTA Models**:
  - **Mask R-CNN**: Extends Faster R-CNN with per-instance segmentation masks via RoI Align
  - **DETR (Detection Transformer)**: Transformer-based end-to-end detection; naturally extends to instance segmentation
  - **Panoptic Segmentation Models**: Unified approach combining semantic and instance tasks
- **Metrics**: mAP at different IoU thresholds (mAP50, mAP75), instance separation quality

#### Foundation Models for Segmentation
**Segment Anything Model (SAM)**
- **Capability**: Zero-shot segmentation of arbitrary objects without task-specific training
- **Architecture**: Vision Transformer encoder with lightweight mask decoder
- **Input**: Image + interactive prompts (points, bounding boxes, text descriptions)
- **Use Cases**: Interactive annotation tools, transfer learning foundation for niche segmentation tasks
- **Limitation**: Lower accuracy on tiny objects; requires fine-tuning for production quality

⚙️ Vision-Language (Multimodal) Models

**Task**: Jointly process text and images for cross-modal understanding
⭐ - **Keywords**: Vision-language alignment, CLIP embeddings, contrastive learning, zero-shot transfer
- **Leading Models**:
  - **CLIP (Contrastive Language-Image Pre-training)**: Learns visual-semantic embeddings via contrastive loss; enables natural language queries on images
  - **BLIP (Bootstrapping Language-Image Pre-training)**: Improved vision-language understanding with bidirectional encoder
  - **LLaVA (Large Language and Vision Assistant)**: Vision encoder + LLM for visual question answering
- **Applications**: Image-to-text retrieval, visual question answering (VQA), semantic search, zero-shot classification
- **Metrics**: Recall@K, Mean Reciprocal Rank (MRR), accuracy on downstream VQA tasks

---

💾 ⭐ 💾 **2. Essential Libraries, Frameworks & Tools**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

💾 Deep Learning Frameworks

| Framework | 🟢 🟢 Best For | Deployment | Key Strength |
|-----------|----------|-----------|-------------|
| **PyTorch** | Research, custom architectures, training | torch.jit, ONNX export | Dynamic computation graphs, intuitive API |
| **TensorFlow/Keras** | Production, large-scale deployments | TF Lite, TF Serving | Ecosystem maturity, edge optimization (TFLite) |
| **JAX** | Advanced research, differentiable programming | Minimal deployment support | Composable function transformations, GPU/TPU efficiency |
| **OpenVINO** | Intel hardware optimization (CPU, GPU, VPU) | OpenVINO Runtime | Model agnostic, unified inference API |

🧮 Computer Vision Libraries

- **OpenCV**: Industry standard for real-time image processing
  - **Capabilities**: Filtering (Gaussian, Sobel, Canny), geometric transforms, histogram equalization, feature detection (SIFT, ORB), camera calibration
  - **Hardware Acceleration**: CUDA, OpenCL, NEON (ARM SIMD)
  - **Real-Time Pipelines**: Camera capture, frame buffering, ISP integration

- **Detectron2**: High-performance library for object detection and segmentation
  - Built on PyTorch; supports Mask R-CNN, Faster R-CNN, RetinaNet, FPN architectures
  - Modular design for customization
  - Strong research community

- **ONNX (Open Neural Network Exchange)**: Model interchange format
  - Enables model conversion between frameworks (PyTorch → TensorFlow, etc.)
  - **ONNX Runtime**: Optimized inference engine across CPU/GPU/mobile

- **TensorFlow Lite (TFLite)**: Edge deployment framework
  - Minimal runtime, quantization support (INT8, dynamic range)
  - Targets mobile, embedded, IoT devices
  - Java/C++ APIs for integration

---

⚡ **3. Optimization Techniques for Edge & Mobile AI**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As of 2026, **Edge AI** dominates for real-time responsiveness, reduced latency, and privacy preservation.

⚙️ Quantization

**Definition**: Reduce weight and activation precision (FP32 → FP16, INT8, INT4)

- **Static Quantization**: Fixed scales determined post-training
  - Pro: Smaller models, faster inference
  - Con: Requires calibration data

- **Dynamic Quantization**: Scales computed at runtime
  - Pro: Flexible, no calibration needed
  - Con: Slight runtime overhead

- **Quantization-Aware Training (QAT)**: Simulate quantization during training
  - 🟢 🟢 Best accuracy for quantized models
  - Longer training time

- **Metrics**: Quantization error, accuracy drop (target <1% for INT8)

📌 Pruning

**Definition**: Remove redundant neurons, connections, filters, or entire layers

- **Structured Pruning**: Remove entire filters/channels (supports standard hardware)
- **Unstructured Pruning**: Remove individual weights (requires specialized hardware/libraries)
- **Magnitude Pruning**: Remove weights below threshold
- **Lottery Ticket Hypothesis**: Identify sparse subnetworks from random initialization

⚙️ Knowledge Distillation

**Definition**: Train a small "student" model to mimic a larger "teacher" model

- **Temperature Scaling**: Soft targets from teacher improve student training
- **Feature-Based Distillation**: Match intermediate layer activations
- **Mutual Learning**: Two student models teach each other

📌 NMS-Free Inference

**Problem**: Non-Maximum Suppression post-processing is expensive (O(n²) complexity for n detections)
- **YOLO26 Solution**: End-to-end NMS integrated into model via one-to-one matching
- **Benefit**: Reduced latency on edge CPUs; cleaner deployment pipeline

⚙️ Model Compression Techniques

| Technique | Latency Reduction | Accuracy Impact | Hardware Need |
|-----------|------------------|-----------------|---------------|
| **Quantization (INT8)** | 2-4x | <1% loss | Standard CPU/GPU |
| **Pruning (50% sparsity)** | 2-3x | 1-2% loss | Sparsity-aware hardware |
| **Distillation** | 1.5-2x (model size) | ~0% loss | Extra training time |
| **NMS-Free** | 1.5-2x (post-processing) | Neutral | Architecture change |

⚡ Hardware-Specific Optimization

- **ARM NEON**: SIMD intrinsics for ARM processors; up to 4x speedup on convolutions
- **GPU Compute**: Vulkan/OpenCL for mobile GPUs (Mali, Adreno)
- **NPU/TPU**: Dedicated accelerators (Qualcomm Hexagon, Apple Neural Engine)
- **Tensor Operations**: FMA (Fused Multiply-Add) efficiency on target hardware

---

💡 **4. Modern Developer Trends & 🟢 🟢 Best Practices**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

⚙️ Synthetic Data & Simulation

- **Use Case**: Training data scarce or privacy-sensitive (e.g., face recognition)
- **Techniques**: GANs (Generative Adversarial Networks), diffusion models, physics-based rendering engines
- **Challenges**: Domain gap between synthetic and real data; requires domain adaptation
- **Mitigation**: Randomization, photorealism improvement, sim-to-real transfer learning

⚙️ Privacy & Anonymization

**Regulatory Compliance**: GDPR, CCPA, California Consumer Privacy Act
- **On-Device Processing**: Inference on edge; no cloud transmission
- **Federated Learning**: Model training distributed across devices
- **Differential Privacy**: Add noise to data/gradients during training for plausible deniability
- **Automated De-Identification**: Blur faces, license plates in video pipelines before storage/transmission

📌 Self-Supervised Learning (SSL)

**Goal**: Learn representations from unlabeled data; fine-tune on small labeled set

- **Contrastive Methods**: SimCLR, MoCo, BYOL
  - Learn representations by contrasting similar vs. dissimilar augmentations
- **Masked Prediction**: BERT-style; mask image patches and predict missing regions
- **Multiview Methods**: Learn consistency across different views/crops
- **Benefit**: Reduce labeled data requirements (10-100x fewer labels for comparable accuracy)

⚙️ Foundation Models & Transfer Learning

**Paradigm Shift**: Pre-train on massive unlabeled data; fine-tune on niche tasks
- **Vision Transformers as Foundation**: ViT pretrained on billions of images transfers to any vision task
- **Prompt-Based Learning**: Models like CLIP/SAM enable task specification via natural language
- **Few-Shot Learning**: Adapt pretrained models with minimal labeled examples
- **Multi-Task Pretraining**: Single model backbone fine-tuned for multiple downstream tasks

📌 Explainability & Interpretability

- **Gradient-Based Attribution**: Saliency maps, Integrated Gradients, SHAP
- **Attention Visualization**: Show which image regions model attends to (especially ViTs)
- **Concept-Based Explanations**: Map predictions to human-understandable concepts
- **Adversarial Robustness**: Test model behavior under distribution shifts, corruptions, adversarial attacks

⚙️ Model Benchmarking & Evaluation

| Metric | Task | Formula | Importance |
|--------|------|---------|-----------|
| **Accuracy** | Classification | % correct predictions | Baseline metric |
| **mAP** | Detection | Avg precision across IoU thresholds | Industry standard |
| **IoU / mIoU** | Segmentation | Intersection over Union | Overlap quality |
⭐ | **Latency (ms)** | Real-time | Time per inference | Edge critical |
| **Throughput (FPS)** | Real-time | Frames per second | Video processing |
| **Energy (mJ)** | Mobile/Edge | Energy per inference | Battery life |
| **FLOPs** | Efficiency | Floating-point operations | Theoretical complexity |

📌 Deployment Checklist

- [ ] Model quantization & compression verified (accuracy drop <1%)
- [ ] Latency/throughput benchmarked on target hardware
- [ ] Memory footprint (RAM, storage) meets constraints
- [ ] Camera calibration & ISP preprocessing pipeline validated
- [ ] Color space handling (RGB, YUV, Bayer) compatible
- [ ] Thermal/power throttling under worst-case load tested
- [ ] Edge case handling (occlusion, motion blur, lighting variations)
- [ ] Automated testing for model quality regressions

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
