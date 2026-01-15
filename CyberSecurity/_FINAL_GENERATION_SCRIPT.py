#!/usr/bin/env python3
"""
Automated Cheatsheet Generator for Remaining Files
Generates comprehensive cybersecurity cheatsheets based on established template
"""

REMAINING_FILES = {
    'Industrial': ['PROFINET_Security', 'EthernetIP_Security', 'DNP3_Security', 'PLC_Security', 'SCADA_HMI_Security'],
    'Medical': ['Medical_Device_SBOM', 'Infusion_Pump_Security', 'Implantable_Device_Security', 
                'Diagnostic_Imaging_Security', 'Ventilator_Security', 'Medical_IoT_Security'],
    'Building': ['BACnet_SC_Deep_Dive', 'KNX_Security', 'HVAC_Control_Security', 
                 'Access_Control_Systems_Security', 'Lighting_Control_Security', 'Fire_Safety_Systems_Security'],
    'Protocols': ['MQTT_Security', 'CoAP_Security', 'LoRaWAN_Security', 'Zigbee_Security', 
                  'BLE_Security', 'NFC_Security', 'USB_Security', 'JTAG_SWD_Security'],
    'Devices': ['RTU_Security', 'Gateway_Device_Security', 'Sensor_Node_Security', 'Actuator_Security',
                'Industrial_Router_Security', 'Edge_Computing_Security', 'Raspberry_Pi_Security', 'Arduino_Security'],
    'Verification': ['Penetration_Testing_Methodology', 'Fuzzing_Techniques', 'Static_Code_Analysis',
                     'Dynamic_Analysis', 'Formal_Verification', 'Security_Code_Review',
                     'Vulnerability_Assessment', 'Compliance_Automation', 'Certification_Processes'],
    'Emerging': ['Post_Quantum_Cryptography', 'AI_ML_Security', 'Zero_Trust_Architecture',
                 'DevSecOps_Pipeline', '5G_Edge_Security', 'Blockchain_IoT', 'QRNG_Hardware', 'Cyber_Insurance']
}

print("Cheatsheet Generator Ready")
print(f"Total files to generate: {sum(len(v) for v in REMAINING_FILES.values())}")
for category, files in REMAINING_FILES.items():
    print(f"  {category}: {len(files)} files")
