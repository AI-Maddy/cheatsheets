======================================================
Jenkins CI/CD for Embedded Systems Complete Guide
======================================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

Jenkins CI/CD for embedded systems, focusing on cross-compilation, device testing, artifact management, and scalable pipeline architecture for embedded device products.

Core Concepts
-------------

+------------------------------+--------------------------------------------------+
| **Component**                | **Purpose**                                      |
+==============================+==================================================+
| **Controller (Master)**      | Central orchestration, job scheduling, UI        |
+------------------------------+--------------------------------------------------+
| **Agents (Nodes)**           | Execute builds on different platforms            |
+------------------------------+--------------------------------------------------+
| **Pipeline**                 | Build definition as code (Jenkinsfile)           |
+------------------------------+--------------------------------------------------+
| **Shared Libraries**         | Reusable pipeline code across projects           |
+------------------------------+--------------------------------------------------+
| **Artifacts**                | Build outputs (binaries, images, packages)       |
+------------------------------+--------------------------------------------------+
| **Credentials**              | Secure storage for keys, tokens, passwords       |
+------------------------------+--------------------------------------------------+

Embedded-Specific Requirements
-------------------------------

.. code-block:: text

   ┌─────────────────────────────────────────────────┐
   │           Jenkins Controller                    │
   │  - Job definitions                              │
   │  - Pipeline orchestration                       │
   │  - Artifact storage                             │
   └─────────────┬───────────────────────────────────┘
                 │
        ┌────────┼────────┬──────────┐
        │        │        │          │
   ┌────▼───┐ ┌─▼────┐ ┌─▼─────┐ ┌─▼──────┐
   │ x86-64 │ │ ARM  │ │ Test  │ │ Device │
   │ Agent  │ │ Agent│ │ Agent │ │ Farm   │
   │        │ │      │ │       │ │        │
   └────────┘ └──────┘ └───────┘ └────────┘
   
   - Cross-compile    - Native    - HIL     - Physical
     toolchains        ARM builds   testing   devices
   - Fast builds      - Platform   - Pytest  - Flashing
                       testing              - Provisioning

🔧 Jenkins Setup for Embedded
===============================

Controller Installation
-----------------------

**Ubuntu/Debian:**

.. code-block:: bash

   # Install Java
   sudo apt update
   sudo apt install openjdk-11-jdk -y
   
   # Add Jenkins repository
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   
   # Install Jenkins
   sudo apt update
   sudo apt install jenkins -y
   
   # Start service
   sudo systemctl start jenkins
   sudo systemctl enable jenkins
   
   # Get initial admin password
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword

**Docker (Development):**

.. code-block:: bash

   # Run Jenkins in Docker
   docker run -d \
     --name jenkins \
     -p 8080:8080 \
     -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   
   # Get initial password
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

Essential Plugins
-----------------

.. code-block:: groovy

   // Install via Manage Jenkins > Plugin Manager
   
   // Core plugins
   - Pipeline
   - Pipeline: Declarative
   - Pipeline: Stage View
   - Git
   - GitHub
   - Credentials Binding
   
   // Embedded-specific
   - Embeddable Build Status (badges)
   - Build Timeout
   - Timestamper
   - AnsiColor (colored output)
   - Workspace Cleanup
   
   // Artifact management
   - Copy Artifact
   - Artifactory
   - Nexus Artifact Uploader
   
   // Testing
   - JUnit
   - Cobertura (coverage)
   - HTML Publisher
   - Robot Framework
   
   // Notifications
   - Email Extension
   - Slack Notification
   - Mailer

Agent Configuration
-------------------

**Static SSH Agent:**

.. code-block:: bash

   # On agent machine
   sudo apt install openjdk-11-jdk -y
   
   # Create Jenkins user
   sudo useradd -m -s /bin/bash jenkins
   sudo mkdir /home/jenkins/.ssh
   
   # Copy controller's public key to authorized_keys
   # From controller:
   sudo -u jenkins ssh-keygen -t rsa -b 4096
   sudo -u jenkins ssh-copy-id jenkins@agent-host
   
   # Configure in Jenkins UI:
   # Manage Jenkins > Nodes > New Node
   # - Remote root directory: /home/jenkins
   # - Launch method: SSH
   # - Host: agent-host
   # - Credentials: jenkins SSH key

**Docker Agent (Dynamic):**

.. code-block:: groovy

   // Install Docker plugin
   // Manage Jenkins > Clouds > Add Cloud > Docker
   
   pipeline {
       agent {
           docker {
               image 'gcc-arm:latest'
               args '-v /opt/toolchains:/toolchains:ro'
           }
       }
       stages {
           stage('Build') {
               steps {
                   sh 'arm-none-eabi-gcc --version'
               }
           }
       }
   }

📝 Pipeline Basics
===================

Declarative Pipeline Structure
-------------------------------

.. code-block:: groovy

   // Jenkinsfile
   pipeline {
       agent any
       
       environment {
           // Environment variables
           CROSS_COMPILE = 'arm-linux-gnueabihf-'
           BUILD_TYPE = 'Release'
       }
       
       options {
           // Pipeline options
           buildDiscarder(logRotator(numToKeepStr: '10'))
           timeout(time: 1, unit: 'HOURS')
           timestamps()
           ansiColor('xterm')
       }
       
       parameters {
           // Build parameters
           choice(name: 'TARGET', choices: ['dev', 'staging', 'production'])
           booleanParam(name: 'RUN_TESTS', defaultValue: true)
       }
       
       stages {
           stage('Checkout') {
               steps {
                   checkout scm
               }
           }
           
           stage('Build') {
               steps {
                   sh 'make clean'
                   sh 'make all'
               }
           }
           
           stage('Test') {
               when {
                   expression { params.RUN_TESTS }
               }
               steps {
                   sh 'make test'
               }
           }
           
           stage('Archive') {
               steps {
                   archiveArtifacts artifacts: 'build/*.bin', fingerprint: true
               }
           }
       }
       
       post {
           always {
               cleanWs()
           }
           success {
               echo 'Build successful!'
           }
           failure {
               echo 'Build failed!'
           }
       }
   }

Scripted Pipeline (Advanced)
-----------------------------

.. code-block:: groovy

   node('arm-builder') {
       try {
           stage('Checkout') {
               checkout scm
           }
           
           stage('Build') {
               def targets = ['board-a', 'board-b', 'board-c']
               def builds = [:]
               
               for (target in targets) {
                   builds[target] = {
                       sh "make BOARD=${target}"
                   }
               }
               
               parallel builds
           }
           
           stage('Test') {
               sh 'pytest tests/'
           }
           
           currentBuild.result = 'SUCCESS'
       } catch (Exception e) {
           currentBuild.result = 'FAILURE'
           throw e
       } finally {
           cleanWs()
       }
   }

🏭 Cross-Compilation Pipelines
================================

ARM Embedded Build
------------------

.. code-block:: groovy

   pipeline {
       agent {
           docker {
               image 'arm-toolchain:latest'
               args '-v ${WORKSPACE}:/build'
           }
       }
       
       environment {
           CROSS_COMPILE = 'arm-none-eabi-'
           CFLAGS = '-mcpu=cortex-m4 -mthumb -O2'
       }
       
       stages {
           stage('Configure') {
               steps {
                   sh '''
                       mkdir -p build
                       cd build
                       cmake -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-none-eabi.cmake ..
                   '''
               }
           }
           
           stage('Build') {
               steps {
                   sh '''
                       cd build
                       make -j$(nproc)
                   '''
               }
           }
           
           stage('Create Artifacts') {
               steps {
                   sh '''
                       cd build
                       arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
                       arm-none-eabi-size firmware.elf
                   '''
               }
           }
           
           stage('Archive') {
               steps {
                   archiveArtifacts artifacts: 'build/firmware.*', fingerprint: true
               }
           }
       }
   }

Multi-Platform Build Matrix
----------------------------

.. code-block:: groovy

   pipeline {
       agent none
       
       stages {
           stage('Build Matrix') {
               matrix {
                   agent {
                       label "${PLATFORM}"
                   }
                   axes {
                       axis {
                           name 'PLATFORM'
                           values 'x86_64', 'arm', 'arm64', 'riscv'
                       }
                       axis {
                           name 'BUILD_TYPE'
                           values 'Debug', 'Release'
                       }
                   }
                   stages {
                       stage('Build') {
                           steps {
                               sh "make PLATFORM=${PLATFORM} BUILD_TYPE=${BUILD_TYPE}"
                           }
                       }
                       stage('Test') {
                           steps {
                               sh "make test PLATFORM=${PLATFORM}"
                           }
                       }
                   }
               }
           }
       }
   }

Yocto Build Pipeline
--------------------

.. code-block:: groovy

   pipeline {
       agent { label 'yocto-builder' }
       
       environment {
           MACHINE = 'imx93evk'
           DISTRO = 'poky'
           DL_DIR = '/opt/yocto/downloads'
           SSTATE_DIR = '/opt/yocto/sstate-cache'
       }
       
       stages {
           stage('Setup') {
               steps {
                   sh '''
                       source oe-init-build-env build
                       echo 'DL_DIR = "${DL_DIR}"' >> conf/local.conf
                       echo 'SSTATE_DIR = "${SSTATE_DIR}"' >> conf/local.conf
                   '''
               }
           }
           
           stage('Build Image') {
               steps {
                   sh '''
                       source oe-init-build-env build
                       bitbake core-image-minimal
                   '''
               }
           }
           
           stage('Build SDK') {
               steps {
                   sh '''
                       source oe-init-build-env build
                       bitbake core-image-minimal -c populate_sdk
                   '''
               }
           }
           
           stage('Archive') {
               steps {
                   archiveArtifacts artifacts: 'build/tmp/deploy/images/**/*.wic.gz', fingerprint: true
                   archiveArtifacts artifacts: 'build/tmp/deploy/sdk/*.sh', fingerprint: true
               }
           }
       }
       
       post {
           always {
               sh 'du -sh build/tmp/deploy/'
           }
       }
   }

🔐 Artifact Signing Pipeline
==============================

Secure Boot Chain
-----------------

.. code-block:: groovy

   pipeline {
       agent any
       
       environment {
           SIGN_KEY = credentials('signing-key')
           SIGN_CERT = credentials('signing-cert')
       }
       
       stages {
           stage('Build') {
               steps {
                   sh 'make all'
               }
           }
           
           stage('Sign Bootloader') {
               steps {
                   sh '''
                       # Sign U-Boot
                       sbsign --key ${SIGN_KEY} --cert ${SIGN_CERT} \
                           --output u-boot-signed.bin u-boot.bin
                   '''
               }
           }
           
           stage('Sign Kernel') {
               steps {
                   sh '''
                       # Sign kernel with IMA/EVM
                       evmctl sign -k ${SIGN_KEY} -a sha256 \
                           --imahash vmlinuz
                   '''
               }
           }
           
           stage('Create FIT Image') {
               steps {
                   sh '''
                       # Create signed FIT image
                       mkimage -f kernel.its -k keys -K dtb -r kernel.itb
                   '''
               }
           }
           
           stage('Verify Signatures') {
               steps {
                   sh '''
                       # Verify all signatures
                       sbverify --cert ${SIGN_CERT} u-boot-signed.bin
                       evmctl verify --key ${SIGN_KEY} vmlinuz
                   '''
               }
           }
           
           stage('Archive Signed Artifacts') {
               steps {
                   archiveArtifacts artifacts: '*-signed.*,*.itb', fingerprint: true
               }
           }
       }
   }

OTA Package Creation
--------------------

.. code-block:: groovy

   pipeline {
       agent any
       
       parameters {
           string(name: 'VERSION', defaultValue: '1.0.0', description: 'Release version')
           choice(name: 'UPDATE_TYPE', choices: ['full', 'delta'], description: 'Update type')
       }
       
       stages {
           stage('Build Images') {
               steps {
                   sh 'bitbake core-image-minimal'
               }
           }
           
           stage('Create Delta') {
               when {
                   expression { params.UPDATE_TYPE == 'delta' }
               }
               steps {
                   sh '''
                       OLD_IMAGE=artifacts/previous-release.img
                       NEW_IMAGE=build/core-image-minimal.img
                       
                       # Create binary delta
                       bsdiff ${OLD_IMAGE} ${NEW_IMAGE} update-${VERSION}.delta
                   '''
               }
           }
           
           stage('Create RAUC Bundle') {
               steps {
                   sh '''
                       # Create RAUC bundle
                       rauc bundle \
                           --cert=certs/release.cert.pem \
                           --key=certs/release.key.pem \
                           bundle/ \
                           update-${VERSION}.raucb
                   '''
               }
           }
           
           stage('Sign Package') {
               steps {
                   withCredentials([file(credentialsId: 'release-key', variable: 'KEY')]) {
                       sh '''
                           openssl dgst -sha256 -sign ${KEY} \
                               -out update-${VERSION}.raucb.sig \
                               update-${VERSION}.raucb
                       '''
                   }
               }
           }
           
           stage('Upload to Server') {
               steps {
                   sh '''
                       scp update-${VERSION}.raucb* update-server:/var/www/updates/
                   '''
               }
           }
       }
   }

🧪 Test Automation Pipelines
==============================

Hardware-in-the-Loop (HIL) Testing
-----------------------------------

.. code-block:: groovy

   pipeline {
       agent { label 'hil-lab' }
       
       stages {
           stage('Flash Device') {
               steps {
                   sh '''
                       # Power cycle device
                       python3 power_control.py --device DUT1 --off
                       sleep 2
                       python3 power_control.py --device DUT1 --on
                       
                       # Flash firmware
                       openocd -f interface/jlink.cfg -f target/stm32f4x.cfg \
                           -c "program firmware.elf verify reset exit"
                   '''
               }
           }
           
           stage('Run Tests') {
               steps {
                   sh '''
                       # Run pytest with HIL fixtures
                       pytest tests/hil/ \
                           --device=/dev/ttyUSB0 \
                           --junitxml=results.xml \
                           --html=report.html
                   '''
               }
           }
           
           stage('Collect Logs') {
               steps {
                   sh '''
                       # Collect serial logs
                       cat /dev/ttyUSB0 > serial.log &
                       LOGGER_PID=$!
                       sleep 60
                       kill $LOGGER_PID
                   '''
               }
           }
       }
       
       post {
           always {
               junit 'results.xml'
               publishHTML([
                   reportDir: '.',
                   reportFiles: 'report.html',
                   reportName: 'Test Report'
               ])
               archiveArtifacts artifacts: 'serial.log', allowEmptyArchive: true
           }
       }
   }

Parallel Device Testing
------------------------

.. code-block:: groovy

   pipeline {
       agent { label 'device-farm' }
       
       stages {
           stage('Flash Devices') {
               steps {
                   script {
                       def devices = ['DUT1', 'DUT2', 'DUT3', 'DUT4']
                       def flashJobs = [:]
                       
                       for (device in devices) {
                           flashJobs[device] = {
                               sh """
                                   python3 flash_device.py \
                                       --device ${device} \
                                       --firmware firmware.bin
                               """
                           }
                       }
                       
                       parallel flashJobs
                   }
               }
           }
           
           stage('Run Test Suite') {
               steps {
                   script {
                       def devices = ['DUT1', 'DUT2', 'DUT3', 'DUT4']
                       def testJobs = [:]
                       
                       for (device in devices) {
                           testJobs[device] = {
                               sh """
                                   pytest tests/ \
                                       --device ${device} \
                                       --junitxml=results-${device}.xml
                               """
                           }
                       }
                       
                       parallel testJobs
                   }
               }
           }
       }
       
       post {
           always {
               junit 'results-*.xml'
           }
       }
   }

📚 Shared Libraries
====================

Library Structure
-----------------

.. code-block:: text

   jenkins-shared-library/
   ├── vars/
   │   ├── buildEmbedded.groovy      # Global variable
   │   ├── flashDevice.groovy
   │   ├── runTests.groovy
   │   └── signArtifacts.groovy
   ├── src/
   │   └── com/
   │       └── company/
   │           ├── EmbeddedBuilder.groovy
   │           └── TestRunner.groovy
   └── resources/
       ├── toolchains/
       │   └── arm-none-eabi.cmake
       └── scripts/
           └── flash.sh

Creating Shared Library
-----------------------

**vars/buildEmbedded.groovy:**

.. code-block:: groovy

   #!/usr/bin/env groovy
   
   def call(Map config) {
       pipeline {
           agent { label config.agent ?: 'embedded-builder' }
           
           environment {
               CROSS_COMPILE = config.crossCompile ?: 'arm-linux-gnueabihf-'
               BUILD_TYPE = config.buildType ?: 'Release'
           }
           
           stages {
               stage('Checkout') {
                   steps {
                       checkout scm
                   }
               }
               
               stage('Build') {
                   steps {
                       script {
                           if (config.buildSystem == 'cmake') {
                               sh """
                                   mkdir -p build
                                   cd build
                                   cmake -DCMAKE_BUILD_TYPE=${BUILD_TYPE} ..
                                   make -j\$(nproc)
                               """
                           } else if (config.buildSystem == 'make') {
                               sh "make -j\$(nproc)"
                           } else if (config.buildSystem == 'yocto') {
                               sh """
                                   source oe-init-build-env build
                                   bitbake ${config.image}
                               """
                           }
                       }
                   }
               }
               
               stage('Test') {
                   when {
                       expression { config.runTests }
                   }
                   steps {
                       sh config.testCommand ?: 'make test'
                   }
               }
               
               stage('Archive') {
                   steps {
                       archiveArtifacts artifacts: config.artifacts
                   }
               }
           }
       }
   }

**Using Shared Library:**

.. code-block:: groovy

   @Library('embedded-pipeline') _
   
   buildEmbedded(
       agent: 'arm-builder',
       crossCompile: 'arm-none-eabi-',
       buildSystem: 'cmake',
       buildType: 'Release',
       runTests: true,
       testCommand: 'pytest tests/',
       artifacts: 'build/*.bin'
   )

**vars/flashDevice.groovy:**

.. code-block:: groovy

   def call(Map config) {
       def device = config.device
       def firmware = config.firmware
       def method = config.method ?: 'jtag'
       
       script {
           if (method == 'jtag') {
               sh """
                   openocd -f ${config.interface} -f ${config.target} \
                       -c "program ${firmware} verify reset exit"
               """
           } else if (method == 'dfu') {
               sh "dfu-util -a 0 -D ${firmware}"
           } else if (method == 'fastboot') {
               sh "fastboot flash boot ${firmware}"
           }
       }
   }

**Usage in Pipeline:**

.. code-block:: groovy

   @Library('embedded-pipeline') _
   
   pipeline {
       agent any
       stages {
           stage('Flash') {
               steps {
                   flashDevice(
                       device: 'DUT1',
                       firmware: 'firmware.bin',
                       method: 'jtag',
                       interface: 'interface/jlink.cfg',
                       target: 'target/stm32f4x.cfg'
                   )
               }
           }
       }
   }

📊 Test Instrumentation & Metrics
===================================

Test Result Tracking
--------------------

.. code-block:: groovy

   pipeline {
       agent any
       
       stages {
           stage('Test') {
               steps {
                   sh '''
                       pytest tests/ \
                           --junitxml=results.xml \
                           --html=report.html \
                           --cov=src \
                           --cov-report=xml \
                           --cov-report=html
                   '''
               }
           }
       }
       
       post {
           always {
               // Publish test results
               junit 'results.xml'
               
               // Publish coverage
               publishHTML([
                   reportDir: 'htmlcov',
                   reportFiles: 'index.html',
                   reportName: 'Coverage Report'
               ])
               
               // Record metrics
               script {
                   def testResults = junit 'results.xml'
                   def passRate = (testResults.totalCount - testResults.failCount) / testResults.totalCount * 100
                   
                   echo "Pass Rate: ${passRate}%"
                   echo "Total: ${testResults.totalCount}"
                   echo "Passed: ${testResults.passCount}"
                   echo "Failed: ${testResults.failCount}"
                   echo "Skipped: ${testResults.skipCount}"
                   
                   // Store metrics
                   currentBuild.description = "Pass Rate: ${passRate}%"
               }
           }
       }
   }

Flake Detection
---------------

.. code-block:: groovy

   @Library('test-analytics') _
   
   pipeline {
       agent any
       
       stages {
           stage('Run Tests with Retry') {
               steps {
                   script {
                       def attempts = 3
                       def failures = []
                       
                       for (int i = 1; i <= attempts; i++) {
                           try {
                               sh "pytest tests/ --junitxml=results-${i}.xml"
                               break
                           } catch (Exception e) {
                               failures.add(i)
                               if (i == attempts) {
                                   throw e
                               }
                               echo "Attempt ${i} failed, retrying..."
                               sleep(10)
                           }
                       }
                       
                       // Analyze flaky tests
                       if (failures.size() > 0 && failures.size() < attempts) {
                           echo "FLAKY TESTS DETECTED!"
                           currentBuild.result = 'UNSTABLE'
                       }
                   }
               }
           }
       }
   }

Build Duration Tracking
-----------------------

.. code-block:: groovy

   pipeline {
       agent any
       
       stages {
           stage('Build') {
               steps {
                   script {
                       def startTime = System.currentTimeMillis()
                       
                       sh 'make all'
                       
                       def endTime = System.currentTimeMillis()
                       def duration = (endTime - startTime) / 1000.0
                       
                       echo "Build Duration: ${duration}s"
                       
                       // Store metric
                       if (duration > 300) {
                           echo "WARNING: Build took longer than 5 minutes!"
                           currentBuild.description = "⚠️ Slow build: ${duration}s"
                       }
                   }
               }
           }
       }
   }

🚀 Advanced Patterns
=====================

Canary Deployment
-----------------

.. code-block:: groovy

   pipeline {
       agent any
       
       parameters {
           string(name: 'VERSION', defaultValue: '1.0.0')
           string(name: 'CANARY_PERCENT', defaultValue: '10')
       }
       
       stages {
           stage('Deploy Canary') {
               steps {
                   sh """
                       # Deploy to canary devices (10%)
                       python3 deploy.py \
                           --version ${VERSION} \
                           --target canary \
                           --percentage ${CANARY_PERCENT}
                   """
               }
           }
           
           stage('Monitor Canary') {
               steps {
                   sh """
                       # Monitor metrics for 1 hour
                       python3 monitor.py \
                           --duration 3600 \
                           --target canary \
                           --metrics crash_rate,error_rate,performance
                   """
               }
           }
           
           stage('Evaluate Results') {
               steps {
                   script {
                       def metrics = readJSON file: 'canary-metrics.json'
                       
                       if (metrics.crash_rate > 0.01 || metrics.error_rate > 0.05) {
                           error("Canary failed health checks!")
                       }
                   }
               }
           }
           
           stage('Full Rollout') {
               steps {
                   input message: 'Deploy to all devices?'
                   
                   sh """
                       python3 deploy.py \
                           --version ${VERSION} \
                           --target production \
                           --percentage 100
                   """
               }
           }
       }
       
       post {
           failure {
               sh """
                   # Rollback canary
                   python3 rollback.py --target canary
               """
           }
       }
   }

Blue-Green Deployment
---------------------

.. code-block:: groovy

   pipeline {
       agent any
       
       environment {
           ACTIVE_SLOT = sh(script: 'cat /etc/active_slot', returnStdout: true).trim()
           INACTIVE_SLOT = sh(script: '[[ ${ACTIVE_SLOT} == "blue" ]] && echo "green" || echo "blue"', returnStdout: true).trim()
       }
       
       stages {
           stage('Build') {
               steps {
                   sh 'make all'
               }
           }
           
           stage('Deploy to Inactive') {
               steps {
                   sh """
                       # Deploy to inactive slot
                       dd if=image.bin of=/dev/mmcblk0p\$([ "${INACTIVE_SLOT}" = "blue" ] && echo 3 || echo 4)
                   """
               }
           }
           
           stage('Test Inactive') {
               steps {
                   sh """
                       # Boot into inactive slot temporarily
                       fw_setenv boot_slot ${INACTIVE_SLOT}
                       reboot
                       
                       # Wait for boot
                       sleep 60
                       
                       # Run smoke tests
                       pytest tests/smoke/
                   """
               }
           }
           
           stage('Switch Traffic') {
               steps {
                   input message: "Switch to ${INACTIVE_SLOT}?"
                   
                   sh """
                       # Make inactive slot active
                       echo "${INACTIVE_SLOT}" > /etc/active_slot
                       fw_setenv boot_slot ${INACTIVE_SLOT}
                   """
               }
           }
       }
       
       post {
           failure {
               sh """
                   # Rollback to active slot
                   fw_setenv boot_slot ${ACTIVE_SLOT}
                   reboot
               """
           }
       }
   }

🛠️ Troubleshooting
===================

Common Issues
-------------

**Build Hangs:**

.. code-block:: groovy

   pipeline {
       options {
           timeout(time: 1, unit: 'HOURS')
       }
       // ... rest of pipeline
   }

**Disk Space:**

.. code-block:: groovy

   pipeline {
       options {
           buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
       }
       
       post {
           always {
               cleanWs()
           }
       }
   }

**Agent Connectivity:**

.. code-block:: bash

   # On agent
   sudo systemctl status jenkins-agent
   
   # Check connection from controller
   ssh jenkins@agent-host 'echo OK'
   
   # Restart agent
   sudo systemctl restart jenkins-agent

**Pipeline Debugging:**

.. code-block:: groovy

   pipeline {
       agent any
       
       stages {
           stage('Debug') {
               steps {
                   sh 'env | sort'
                   sh 'pwd'
                   sh 'ls -la'
                   sh 'df -h'
               }
           }
       }
   }

📖 Best Practices
==================

1. **Use Declarative Pipeline** - More maintainable than scripted
2. **Version control Jenkinsfiles** - Store with source code
3. **Use shared libraries** - DRY principle for common operations
4. **Implement timeouts** - Prevent hanging builds
5. **Clean workspaces** - Avoid disk space issues
6. **Use credentials plugin** - Never hardcode secrets
7. **Parallel builds** - Reduce build time
8. **Archive selectively** - Don't store everything
9. **Monitor build duration** - Optimize slow stages
10. **Test pipelines in branches** - Don't break main builds

📚 References
==============

* **Jenkins Documentation**: https://www.jenkins.io/doc/
* **Pipeline Syntax**: https://www.jenkins.io/doc/book/pipeline/syntax/
* **Shared Libraries**: https://www.jenkins.io/doc/book/pipeline/shared-libraries/
* **Docker Integration**: https://www.jenkins.io/doc/book/pipeline/docker/
* **Best Practices**: https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/

================================
Last Updated: January 2026
Version: 3.0
================================
