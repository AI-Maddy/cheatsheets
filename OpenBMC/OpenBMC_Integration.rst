=======================================
OpenBMC Integration & Automation Guide
=======================================

:Author: Technical Documentation
:Date: January 2026
:Version: 2.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 3
   :local:
   :backlinks: top

🔗 Integration Overview
========================

Common Integration Scenarios
-----------------------------

+---------------------------+---------------------------------------------+
| **Tool/Platform**         | **Use Case**                                |
+===========================+=============================================+
| Ansible                   | Configuration management, automation        |
+---------------------------+---------------------------------------------+
| Prometheus/Grafana        | Monitoring and visualization                |
+---------------------------+---------------------------------------------+
| Kubernetes                | Container orchestration with BMC control    |
+---------------------------+---------------------------------------------+
| Jenkins/GitLab CI         | Automated testing and deployment            |
+---------------------------+---------------------------------------------+
| Nagios/Zabbix             | Infrastructure monitoring                   |
+---------------------------+---------------------------------------------+
| Terraform                 | Infrastructure as Code                      |
+---------------------------+---------------------------------------------+
| Saltstack                 | Configuration and orchestration             |
+---------------------------+---------------------------------------------+

🤖 Ansible Integration
=======================

Ansible Inventory
-----------------

**inventory/hosts.yml:**

.. code-block:: yaml

   all:
     children:
       bmcs:
         hosts:
           rack1-server1-bmc:
             ansible_host: 192.168.1.101
             bmc_user: admin
             bmc_pass: !vault |
               $ANSIBLE_VAULT;1.1;AES256
               ...encrypted...
           rack1-server2-bmc:
             ansible_host: 192.168.1.102
             bmc_user: admin
             bmc_pass: !vault |
               $ANSIBLE_VAULT;1.1;AES256
               ...encrypted...
         vars:
           ansible_connection: local
           ansible_python_interpreter: /usr/bin/python3

Power Management Playbook
--------------------------

**playbooks/power_control.yml:**

.. code-block:: yaml

   ---
   - name: BMC Power Management
     hosts: bmcs
     gather_facts: no
     
     vars:
       redfish_timeout: 30
     
     tasks:
       - name: Get current power state
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Systems/system"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           return_content: yes
         register: power_state
         delegate_to: localhost
       
       - name: Display current state
         debug:
           msg: "{{ inventory_hostname }}: {{ power_state.json.PowerState }}"
       
       - name: Power on servers if off
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
           method: POST
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           body_format: json
           body:
             ResetType: "On"
           status_code: 204
         when: power_state.json.PowerState == "Off"
         delegate_to: localhost
       
       - name: Wait for power on
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Systems/system"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
         register: result
         until: result.json.PowerState == "On"
         retries: 10
         delay: 5
         when: power_state.json.PowerState == "Off"
         delegate_to: localhost

Sensor Monitoring Playbook
---------------------------

**playbooks/sensor_check.yml:**

.. code-block:: yaml

   ---
   - name: Check BMC Sensors
     hosts: bmcs
     gather_facts: no
     
     tasks:
       - name: Get thermal data
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Chassis/chassis/Thermal"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           return_content: yes
         register: thermal_data
         delegate_to: localhost
       
       - name: Check for critical temperatures
         set_fact:
           critical_temps: "{{ thermal_data.json.Temperatures | 
                              selectattr('Status.Health', 'equalto', 'Critical') | 
                              list }}"
       
       - name: Alert on critical temperatures
         debug:
           msg: "CRITICAL: {{ item.Name }} is {{ item.ReadingCelsius }}°C"
         loop: "{{ critical_temps }}"
         when: critical_temps | length > 0
       
       - name: Check fan speeds
         set_fact:
           low_speed_fans: "{{ thermal_data.json.Fans | 
                              selectattr('Reading', 'lt', 1000) | 
                              list }}"
       
       - name: Alert on low fan speeds
         debug:
           msg: "WARNING: {{ item.Name }} is {{ item.Reading }} RPM"
         loop: "{{ low_speed_fans }}"
         when: low_speed_fans | length > 0

Firmware Update Playbook
-------------------------

**playbooks/firmware_update.yml:**

.. code-block:: yaml

   ---
   - name: Update BMC Firmware
     hosts: bmcs
     gather_facts: no
     serial: 1  # Update one at a time
     
     vars:
       firmware_url: "http://fileserver/firmware/obmc-phosphor-image.static.mtd"
       max_wait_time: 600
     
     tasks:
       - name: Check current firmware version
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/UpdateService/FirmwareInventory/bmc_active"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
         register: current_version
         delegate_to: localhost
       
       - name: Display current version
         debug:
           msg: "Current version: {{ current_version.json.Version }}"
       
       - name: Initiate firmware update
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate"
           method: POST
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           body_format: json
           body:
             ImageURI: "{{ firmware_url }}"
             TransferProtocol: "HTTP"
           status_code: 202
         register: update_result
         delegate_to: localhost
       
       - name: Wait for update to complete
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/TaskService/Tasks/{{ update_result.json['@odata.id'].split('/')[-1] }}"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
         register: task_status
         until: task_status.json.TaskState in ['Completed', 'Exception']
         retries: "{{ max_wait_time // 10 }}"
         delay: 10
         delegate_to: localhost
       
       - name: Verify update success
         fail:
           msg: "Firmware update failed: {{ task_status.json.Messages }}"
         when: task_status.json.TaskState == "Exception"

Configuration Management Playbook
----------------------------------

**playbooks/bmc_configure.yml:**

.. code-block:: yaml

   ---
   - name: Configure BMC Settings
     hosts: bmcs
     gather_facts: no
     
     vars:
       network_config:
         ipv4_static: true
         ipv4_address: "{{ ansible_host }}"
         ipv4_netmask: "255.255.255.0"
         ipv4_gateway: "192.168.1.1"
       
       ntp_servers:
         - "time.google.com"
         - "time.cloudflare.com"
       
       syslog_servers:
         - address: "192.168.1.50"
           port: 514
     
     tasks:
       - name: Configure network settings
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Managers/bmc/EthernetInterfaces/eth0"
           method: PATCH
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           body_format: json
           body:
             IPv4StaticAddresses:
               - Address: "{{ network_config.ipv4_address }}"
                 SubnetMask: "{{ network_config.ipv4_netmask }}"
                 Gateway: "{{ network_config.ipv4_gateway }}"
           status_code: 200
         delegate_to: localhost
       
       - name: Configure NTP
         uri:
           url: "https://{{ ansible_host }}/redfish/v1/Managers/bmc/NetworkProtocol"
           method: PATCH
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           body_format: json
           body:
             NTP:
               ProtocolEnabled: true
               NTPServers: "{{ ntp_servers }}"
           status_code: 200
         delegate_to: localhost

Ansible Role Structure
----------------------

.. code-block:: text

   roles/openbmc/
   ├── defaults/
   │   └── main.yml          # Default variables
   ├── tasks/
   │   ├── main.yml          # Main tasks
   │   ├── power.yml         # Power management
   │   ├── users.yml         # User management
   │   └── sensors.yml       # Sensor checks
   ├── templates/
   │   └── bmc_config.j2     # Configuration templates
   ├── handlers/
   │   └── main.yml          # Handlers
   └── vars/
       └── main.yml          # Variables

**Example role usage:**

.. code-block:: yaml

   # playbooks/site.yml
   ---
   - name: Manage OpenBMC Infrastructure
     hosts: bmcs
     roles:
       - role: openbmc
         vars:
           openbmc_action: power_on
           openbmc_ntp_enabled: true

📊 Prometheus/Grafana Integration
===================================

Redfish Exporter Setup
----------------------

**docker-compose.yml:**

.. code-block:: yaml

   version: '3.8'
   
   services:
     redfish_exporter:
       image: jenningsloy318/redfish_exporter:latest
       container_name: redfish_exporter
       ports:
         - "9610:9610"
       volumes:
         - ./redfish_exporter.yml:/etc/redfish_exporter/config.yml:ro
       restart: unless-stopped
     
     prometheus:
       image: prom/prometheus:latest
       container_name: prometheus
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
         - prometheus_data:/prometheus
       restart: unless-stopped
     
     grafana:
       image: grafana/grafana:latest
       container_name: grafana
       ports:
         - "3000:3000"
       volumes:
         - grafana_data:/var/lib/grafana
         - ./grafana_dashboards:/etc/grafana/provisioning/dashboards:ro
         - ./grafana_datasources:/etc/grafana/provisioning/datasources:ro
       environment:
         - GF_SECURITY_ADMIN_PASSWORD=admin
       restart: unless-stopped
   
   volumes:
     prometheus_data:
     grafana_data:

Prometheus Configuration
-------------------------

**prometheus.yml:**

.. code-block:: yaml

   global:
     scrape_interval: 30s
     evaluation_interval: 30s
   
   scrape_configs:
     - job_name: 'redfish'
       static_configs:
         - targets:
           - 192.168.1.101  # BMC 1
           - 192.168.1.102  # BMC 2
           - 192.168.1.103  # BMC 3
       metrics_path: /redfish
       params:
         module: [default]
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance
         - target_label: __address__
           replacement: redfish_exporter:9610
   
   alerting:
     alertmanagers:
       - static_configs:
           - targets: ['alertmanager:9093']
   
   rule_files:
     - "alerts.yml"

**alerts.yml:**

.. code-block:: yaml

   groups:
     - name: bmc_alerts
       interval: 30s
       rules:
         - alert: HighCPUTemperature
           expr: redfish_thermal_temperatures_celsius > 80
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High CPU temperature on {{ $labels.instance }}"
             description: "CPU temperature is {{ $value }}°C"
         
         - alert: CriticalCPUTemperature
           expr: redfish_thermal_temperatures_celsius > 90
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "CRITICAL CPU temperature on {{ $labels.instance }}"
             description: "CPU temperature is {{ $value }}°C - immediate action required"
         
         - alert: FanFailure
           expr: redfish_thermal_fans_rpm < 1000
           for: 2m
           labels:
             severity: critical
           annotations:
             summary: "Fan failure on {{ $labels.instance }}"
             description: "Fan {{ $labels.fan }} is at {{ $value }} RPM"
         
         - alert: PowerSupplyFailure
           expr: redfish_power_powersupplies_status != 1
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "Power supply failure on {{ $labels.instance }}"
             description: "Power supply {{ $labels.powersupply }} has failed"
         
         - alert: ServerDown
           expr: up{job="redfish"} == 0
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "BMC {{ $labels.instance }} is down"
             description: "Cannot reach BMC at {{ $labels.instance }}"

Grafana Dashboard JSON
----------------------

**dashboards/bmc_dashboard.json:**

.. code-block:: json

   {
     "dashboard": {
       "title": "OpenBMC Monitoring",
       "panels": [
         {
           "id": 1,
           "title": "CPU Temperatures",
           "type": "graph",
           "targets": [
             {
               "expr": "redfish_thermal_temperatures_celsius{sensor=~\"CPU.*\"}"
             }
           ],
           "yaxes": [
             {
               "label": "Temperature (°C)",
               "min": 0,
               "max": 100
             }
           ]
         },
         {
           "id": 2,
           "title": "Fan Speeds",
           "type": "graph",
           "targets": [
             {
               "expr": "redfish_thermal_fans_rpm"
             }
           ]
         },
         {
           "id": 3,
           "title": "Power Consumption",
           "type": "graph",
           "targets": [
             {
               "expr": "redfish_power_consumed_watts"
             }
           ]
         }
       ]
     }
   }

Custom Metrics Exporter
-----------------------

**Python script (bmc_exporter.py):**

.. code-block:: python

   #!/usr/bin/env python3
   from prometheus_client import start_http_server, Gauge, Counter
   import redfish
   import time
   import sys
   
   # Define metrics
   cpu_temp = Gauge('bmc_cpu_temperature_celsius', 
                    'CPU temperature in Celsius',
                    ['hostname', 'cpu'])
   fan_speed = Gauge('bmc_fan_speed_rpm',
                     'Fan speed in RPM',
                     ['hostname', 'fan'])
   power_watts = Gauge('bmc_power_watts',
                       'Power consumption in watts',
                       ['hostname'])
   power_state = Gauge('bmc_system_power_state',
                       'System power state (1=on, 0=off)',
                       ['hostname'])
   
   def collect_metrics(bmc_ip, username, password, hostname):
       """Collect metrics from BMC"""
       try:
           client = redfish.redfish_client(
               base_url=f"https://{bmc_ip}",
               username=username,
               password=password
           )
           client.login(auth="session")
           
           # Get thermal data
           thermal = client.get("/redfish/v1/Chassis/chassis/Thermal")
           for temp in thermal.dict.get("Temperatures", []):
               cpu_name = temp.get("Name", "unknown")
               if "CPU" in cpu_name:
                   value = temp.get("ReadingCelsius", 0)
                   cpu_temp.labels(hostname=hostname, cpu=cpu_name).set(value)
           
           # Get fan data
           for fan in thermal.dict.get("Fans", []):
               fan_name = fan.get("Name", "unknown")
               value = fan.get("Reading", 0)
               fan_speed.labels(hostname=hostname, fan=fan_name).set(value)
           
           # Get power data
           power = client.get("/redfish/v1/Chassis/chassis/Power")
           power_control = power.dict.get("PowerControl", [{}])[0]
           watts = power_control.get("PowerConsumedWatts", 0)
           power_watts.labels(hostname=hostname).set(watts)
           
           # Get power state
           system = client.get("/redfish/v1/Systems/system")
           state = 1 if system.dict.get("PowerState") == "On" else 0
           power_state.labels(hostname=hostname).set(state)
           
           client.logout()
       
       except Exception as e:
           print(f"Error collecting from {hostname}: {e}", file=sys.stderr)
   
   def main():
       # BMC list
       bmcs = [
           {"ip": "192.168.1.101", "hostname": "server1-bmc"},
           {"ip": "192.168.1.102", "hostname": "server2-bmc"},
       ]
       username = "admin"
       password = "password"
       
       # Start HTTP server
       start_http_server(9610)
       print("Metrics server started on port 9610")
       
       # Collection loop
       while True:
           for bmc in bmcs:
               collect_metrics(bmc["ip"], username, password, bmc["hostname"])
           time.sleep(30)
   
   if __name__ == "__main__":
       main()

☸️ Kubernetes Integration
===========================

BMC Operator
------------

**Kubernetes Custom Resource Definition:**

.. code-block:: yaml

   # bmc-crd.yaml
   apiVersion: apiextensions.k8s.io/v1
   kind: CustomResourceDefinition
   metadata:
     name: bmcs.infrastructure.example.com
   spec:
     group: infrastructure.example.com
     versions:
       - name: v1
         served: true
         storage: true
         schema:
           openAPIV3Schema:
             type: object
             properties:
               spec:
                 type: object
                 properties:
                   address:
                     type: string
                   username:
                     type: string
                   passwordSecret:
                     type: string
                   powerState:
                     type: string
                     enum: [On, Off, ForceOff]
               status:
                 type: object
                 properties:
                   powerState:
                     type: string
                   temperature:
                     type: number
                   lastUpdate:
                     type: string
     scope: Namespaced
     names:
       plural: bmcs
       singular: bmc
       kind: BMC
       shortNames:
         - bmc

**BMC Resource:**

.. code-block:: yaml

   # my-bmc.yaml
   apiVersion: infrastructure.example.com/v1
   kind: BMC
   metadata:
     name: server1-bmc
     namespace: infrastructure
   spec:
     address: "192.168.1.101"
     username: "admin"
     passwordSecret: "server1-bmc-creds"
     powerState: "On"

**Operator Controller (Python):**

.. code-block:: python

   #!/usr/bin/env python3
   import kopf
   import kubernetes
   import redfish
   import base64
   
   @kopf.on.create('infrastructure.example.com', 'v1', 'bmcs')
   @kopf.on.update('infrastructure.example.com', 'v1', 'bmcs')
   def reconcile_bmc(spec, status, namespace, name, **kwargs):
       """Reconcile BMC state with desired state"""
       
       # Get credentials
       v1 = kubernetes.client.CoreV1Api()
       secret = v1.read_namespaced_secret(spec['passwordSecret'], namespace)
       password = base64.b64decode(secret.data['password']).decode('utf-8')
       
       # Connect to BMC
       client = redfish.redfish_client(
           base_url=f"https://{spec['address']}",
           username=spec['username'],
           password=password
       )
       client.login(auth="session")
       
       # Get current power state
       response = client.get("/redfish/v1/Systems/system")
       current_state = response.dict["PowerState"]
       desired_state = spec.get('powerState', 'On')
       
       # Reconcile power state
       if current_state != desired_state:
           client.post(
               "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset",
               body={"ResetType": desired_state}
           )
       
       # Update status
       thermal = client.get("/redfish/v1/Chassis/chassis/Thermal")
       temps = thermal.dict.get("Temperatures", [])
       cpu_temp = temps[0].get("ReadingCelsius", 0) if temps else 0
       
       client.logout()
       
       return {
           'powerState': current_state,
           'temperature': cpu_temp,
           'lastUpdate': kopf.utcnow().isoformat()
       }

Node Provisioner Job
--------------------

**Kubernetes Job:**

.. code-block:: yaml

   # provision-node.yaml
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: provision-node1
   spec:
     template:
       spec:
         containers:
           - name: provisioner
             image: my-provisioner:latest
             env:
               - name: BMC_ADDRESS
                 value: "192.168.1.101"
               - name: BMC_USERNAME
                 valueFrom:
                   secretKeyRef:
                     name: bmc-credentials
                     key: username
               - name: BMC_PASSWORD
                 valueFrom:
                   secretKeyRef:
                     name: bmc-credentials
                     key: password
               - name: ISO_URL
                 value: "http://fileserver/ubuntu-20.04.iso"
             command:
               - /bin/sh
               - -c
               - |
                 # Power off node
                 curl -k -u $BMC_USERNAME:$BMC_PASSWORD -X POST \
                   -H "Content-Type: application/json" \
                   -d '{"ResetType": "ForceOff"}' \
                   https://$BMC_ADDRESS/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
                 
                 sleep 10
                 
                 # Mount ISO
                 curl -k -u $BMC_USERNAME:$BMC_PASSWORD -X POST \
                   -H "Content-Type: application/json" \
                   -d "{\"Image\": \"$ISO_URL\", \"Inserted\": true}" \
                   https://$BMC_ADDRESS/redfish/v1/Systems/system/VirtualMedia/1/Actions/VirtualMedia.InsertMedia
                 
                 # Set boot from CD
                 curl -k -u $BMC_USERNAME:$BMC_PASSWORD -X PATCH \
                   -H "Content-Type: application/json" \
                   -d '{"Boot": {"BootSourceOverrideTarget": "Cd", "BootSourceOverrideEnabled": "Once"}}' \
                   https://$BMC_ADDRESS/redfish/v1/Systems/system
                 
                 # Power on
                 curl -k -u $BMC_USERNAME:$BMC_PASSWORD -X POST \
                   -H "Content-Type: application/json" \
                   -d '{"ResetType": "On"}' \
                   https://$BMC_ADDRESS/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
         restartPolicy: Never
     backoffLimit: 3

🔄 CI/CD Integration
=====================

GitLab CI Pipeline
------------------

**.gitlab-ci.yml:**

.. code-block:: yaml

   stages:
     - build
     - test
     - deploy
   
   variables:
     YOCTO_VERSION: "kirkstone"
     MACHINE: "romulus"
   
   build_image:
     stage: build
     image: crops/poky:ubuntu-22.04
     script:
       - export TEMPLATECONF=meta-ibm/meta-romulus/conf
       - source setup $MACHINE
       - bitbake obmc-phosphor-image
     artifacts:
       paths:
         - build/tmp/deploy/images/$MACHINE/
       expire_in: 1 week
     only:
       - main
       - merge_requests
   
   test_qemu:
     stage: test
     image: crops/poky:ubuntu-22.04
     dependencies:
       - build_image
     script:
       - # Start QEMU
       - qemu-system-arm -machine romulus-bmc -nographic \
           -drive file=build/tmp/deploy/images/romulus/*.mtd,format=raw,if=mtd \
           -net user,hostfwd=tcp::2222-:22 &
       - sleep 60
       - # Run tests
       - python3 test_scripts/smoke_test.py --bmc-ip localhost --port 2222
     only:
       - main
       - merge_requests
   
   deploy_staging:
     stage: deploy
     image: python:3.9
     dependencies:
       - build_image
     script:
       - pip install ansible
       - ansible-playbook -i inventory/staging playbooks/firmware_update.yml
     only:
       - main
     when: manual
   
   deploy_production:
     stage: deploy
     image: python:3.9
     dependencies:
       - build_image
     script:
       - pip install ansible
       - ansible-playbook -i inventory/production playbooks/firmware_update.yml
     only:
       - tags
     when: manual

Jenkins Pipeline
----------------

**Jenkinsfile:**

.. code-block:: groovy

   pipeline {
       agent any
       
       environment {
           YOCTO_VERSION = 'kirkstone'
           MACHINE = 'romulus'
       }
       
       stages {
           stage('Checkout') {
               steps {
                   git branch: 'main',
                       url: 'https://github.com/openbmc/openbmc.git'
               }
           }
           
           stage('Build') {
               steps {
                   sh '''
                       export TEMPLATECONF=meta-ibm/meta-romulus/conf
                       source setup ${MACHINE}
                       bitbake obmc-phosphor-image
                   '''
               }
           }
           
           stage('Test') {
               steps {
                   sh '''
                       python3 test_scripts/robot_tests.py \
                           --bmc-ip staging-bmc.example.com \
                           --username admin \
                           --password ${BMC_PASSWORD}
                   '''
               }
           }
           
           stage('Deploy to Staging') {
               when {
                   branch 'main'
               }
               steps {
                   sh '''
                       ansible-playbook \
                           -i inventory/staging \
                           playbooks/firmware_update.yml
                   '''
               }
           }
           
           stage('Deploy to Production') {
               when {
                   tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
               }
               steps {
                   input message: 'Deploy to production?'
                   sh '''
                       ansible-playbook \
                           -i inventory/production \
                           playbooks/firmware_update.yml
                   '''
               }
           }
       }
       
       post {
           failure {
               emailext(
                   subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                   body: "Check console output at ${env.BUILD_URL}",
                   to: "team@example.com"
               )
           }
       }
   }

🔐 Security & Best Practices
=============================

Secrets Management
------------------

**Using Ansible Vault:**

.. code-block:: bash

   # Create encrypted vault file
   ansible-vault create secrets.yml
   
   # Edit vault
   ansible-vault edit secrets.yml
   
   # Use in playbook
   ansible-playbook -i inventory playbook.yml --ask-vault-pass

**secrets.yml:**

.. code-block:: yaml

   ---
   bmc_credentials:
     server1:
       user: admin
       password: "sup3rs3cr3t"
     server2:
       user: admin
       password: "an0th3rs3cr3t"

**Using HashiCorp Vault:**

.. code-block:: python

   import hvac
   
   # Connect to Vault
   client = hvac.Client(url='http://vault:8200', token='my-token')
   
   # Read secret
   secret = client.secrets.kv.v2.read_secret_version(path='bmc/server1')
   username = secret['data']['data']['username']
   password = secret['data']['data']['password']

TLS Certificate Management
---------------------------

.. code-block:: bash

   # Generate CSR on BMC
   busctl call xyz.openbmc_project.Certs.Manager \
     /xyz/openbmc_project/certs/server \
     xyz.openbmc_project.Certs.Manager \
     GenerateCSR s "US" s "California" s "San Jose" \
     s "MyCompany" s "IT" s "bmc.example.com"
   
   # Upload signed certificate
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"CertificateString": "-----BEGIN CERTIFICATE-----..."}' \
     https://bmc-ip/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate

Access Control
--------------

**Role-Based Access (Redfish):**

.. code-block:: bash

   # Create read-only user
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "UserName": "monitor",
       "Password": "monitorpass",
       "RoleId": "ReadOnly"
     }' \
     https://bmc-ip/redfish/v1/AccountService/Accounts

📝 Documentation Templates
===========================

Runbook Template
----------------

.. code-block:: markdown

   # BMC Incident Response Runbook
   
   ## Symptoms
   - High temperature alert from BMC
   - Fan speed below normal
   
   ## Impact
   - Server may throttle or shutdown
   - Risk of hardware damage
   
   ## Diagnosis
   ```bash
   # Check thermal status
   curl -k -u admin:password \
     https://bmc-ip/redfish/v1/Chassis/chassis/Thermal | jq .
   
   # Check via IPMI
   ipmitool -H bmc-ip -U admin -P password sensor list
   ```
   
   ## Resolution
   1. Verify fan operation
   2. Check air flow obstructions
   3. If fan failed, replace immediately
   4. If temperature persists, reduce workload
   
   ## Prevention
   - Regular maintenance schedule
   - Monitor fan health trends
   - Keep data center cool

Change Request Template
-----------------------

.. code-block:: markdown

   # BMC Firmware Update - Change Request
   
   **Date:** 2026-01-20
   **Requestor:** IT Operations
   **Approver:** Change Management Board
   
   ## Change Description
   Update OpenBMC firmware from v2.10 to v2.11 on production servers
   
   ## Justification
   - Security patches for CVE-2026-XXXX
   - Improved thermal management
   - Bug fixes for event logging
   
   ## Scope
   - Affected systems: 50 production servers
   - Update window: 2026-01-25 02:00-06:00 UTC
   
   ## Testing
   - Successfully tested on 5 staging servers
   - All regression tests passed
   
   ## Rollback Plan
   1. Keep previous firmware backup
   2. Flash previous version if issues arise
   3. Expected rollback time: 15 minutes per server
   
   ## Execution Steps
   See attached Ansible playbook: firmware_update.yml

📚 Additional Resources
========================

Tools & Libraries
-----------------

* **Python Redfish**: https://github.com/DMTF/python-redfish-library
* **Redfish Mockup Server**: https://github.com/DMTF/Redfish-Mockup-Server
* **Redfish Interop Validator**: https://github.com/DMTF/Redfish-Interop-Validator
* **bmcweb**: https://github.com/openbmc/bmcweb

Community
---------

* **Mailing List**: openbmc@lists.ozlabs.org
* **Discord**: OpenBMC Community Server
* **Stack Overflow**: Tag `openbmc`
* **GitHub Discussions**: https://github.com/openbmc/openbmc/discussions

Example Repositories
--------------------

* **OpenBMC Test Automation**: https://github.com/openbmc/openbmc-test-automation
* **Meta Layers Collection**: https://github.com/openbmc
* **Ansible Collections**: Search for "redfish" on Ansible Galaxy

========================================
Last Updated: January 2026
Version: 2.0
========================================
