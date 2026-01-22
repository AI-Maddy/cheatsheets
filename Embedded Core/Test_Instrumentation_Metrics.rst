======================================================
Test Instrumentation & Metrics Complete Guide
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

Comprehensive guide to test instrumentation, metrics collection, analysis, dashboarding, and continuous improvement strategies for embedded device testing.

Test Metrics Pyramid
---------------------

.. code-block:: text

   Strategic (Business)
   ────────────────────
   - Product Quality
   - Release Velocity
   - Customer Satisfaction
   
   Tactical (Process)
   ──────────────────
   - Pass Rate
   - Test Coverage
   - Build Time
   
   Operational (Technical)
   ───────────────────────
   - Duration per Test
   - Flake Rate
   - Resource Usage

Key Metrics Categories
----------------------

+---------------------------+------------------------------------------------+
| **Category**              | **Metrics**                                    |
+===========================+================================================+
| **Test Execution**        | Pass rate, fail rate, skip rate, blocked rate |
+---------------------------+------------------------------------------------+
| **Performance**           | Duration, throughput, resource usage           |
+---------------------------+------------------------------------------------+
| **Reliability**           | Flake rate, retry count, timeout rate          |
+---------------------------+------------------------------------------------+
| **Coverage**              | Code coverage, requirement coverage, platform |
+---------------------------+------------------------------------------------+
| **Quality**               | Defect density, escape rate, MTBF              |
+---------------------------+------------------------------------------------+
| **Efficiency**            | Automation rate, cost per test, ROI            |
+---------------------------+------------------------------------------------+

📊 Test Execution Metrics
===========================

Pass Rate Tracking
------------------

**Calculate Pass Rate:**

.. code-block:: python

   #!/usr/bin/env python3
   """Pass rate calculation and tracking"""
   
   from dataclasses import dataclass
   from typing import List
   import json
   from datetime import datetime
   
   @dataclass
   class TestResult:
       name: str
       status: str  # 'passed', 'failed', 'skipped', 'blocked'
       duration: float
       timestamp: datetime
       error_message: str = None
   
   class PassRateCalculator:
       def __init__(self):
           self.results: List[TestResult] = []
       
       def add_result(self, result: TestResult):
           self.results.append(result)
       
       def calculate_pass_rate(self, include_skipped=False):
           """Calculate overall pass rate"""
           if not self.results:
               return 0.0
           
           passed = sum(1 for r in self.results if r.status == 'passed')
           total = len(self.results)
           
           if not include_skipped:
               skipped = sum(1 for r in self.results if r.status == 'skipped')
               total -= skipped
           
           return (passed / total * 100) if total > 0 else 0.0
       
       def calculate_fail_rate(self):
           """Calculate fail rate"""
           if not self.results:
               return 0.0
           
           failed = sum(1 for r in self.results if r.status == 'failed')
           total = len([r for r in self.results if r.status != 'skipped'])
           
           return (failed / total * 100) if total > 0 else 0.0
       
       def get_status_breakdown(self):
           """Get count of each status"""
           breakdown = {
               'passed': 0,
               'failed': 0,
               'skipped': 0,
               'blocked': 0
           }
           
           for result in self.results:
               if result.status in breakdown:
                   breakdown[result.status] += 1
           
           return breakdown
       
       def get_failed_tests(self):
           """Get list of failed tests"""
           return [r for r in self.results if r.status == 'failed']
       
       def generate_summary(self):
           """Generate test summary"""
           breakdown = self.get_status_breakdown()
           total = len(self.results)
           
           summary = {
               'total_tests': total,
               'passed': breakdown['passed'],
               'failed': breakdown['failed'],
               'skipped': breakdown['skipped'],
               'blocked': breakdown['blocked'],
               'pass_rate': self.calculate_pass_rate(),
               'fail_rate': self.calculate_fail_rate(),
               'timestamp': datetime.now().isoformat()
           }
           
           return summary
   
   # Usage
   if __name__ == '__main__':
       calculator = PassRateCalculator()
       
       # Add test results
       calculator.add_result(TestResult('test_boot', 'passed', 2.5, datetime.now()))
       calculator.add_result(TestResult('test_wifi', 'failed', 10.2, datetime.now(), 'Connection timeout'))
       calculator.add_result(TestResult('test_bluetooth', 'passed', 5.1, datetime.now()))
       calculator.add_result(TestResult('test_usb', 'skipped', 0.0, datetime.now()))
       
       summary = calculator.generate_summary()
       print(json.dumps(summary, indent=2))

Jenkins JUnit XML Parsing
--------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Parse JUnit XML and extract metrics"""
   
   import xml.etree.ElementTree as ET
   from pathlib import Path
   
   class JUnitParser:
       def __init__(self, xml_path):
           self.tree = ET.parse(xml_path)
           self.root = self.tree.getroot()
       
       def get_test_count(self):
           """Get total test count"""
           return int(self.root.attrib.get('tests', 0))
       
       def get_failure_count(self):
           """Get failure count"""
           return int(self.root.attrib.get('failures', 0))
       
       def get_error_count(self):
           """Get error count"""
           return int(self.root.attrib.get('errors', 0))
       
       def get_skip_count(self):
           """Get skip count"""
           return int(self.root.attrib.get('skipped', 0))
       
       def get_total_time(self):
           """Get total execution time"""
           return float(self.root.attrib.get('time', 0.0))
       
       def get_failed_tests(self):
           """Get list of failed test cases"""
           failed = []
           
           for testcase in self.root.iter('testcase'):
               failure = testcase.find('failure')
               error = testcase.find('error')
               
               if failure is not None or error is not None:
                   failed.append({
                       'name': testcase.attrib.get('name'),
                       'classname': testcase.attrib.get('classname'),
                       'time': float(testcase.attrib.get('time', 0.0)),
                       'message': (failure.attrib.get('message') if failure is not None 
                                 else error.attrib.get('message'))
                   })
           
           return failed
       
       def get_slowest_tests(self, n=10):
           """Get N slowest tests"""
           tests = []
           
           for testcase in self.root.iter('testcase'):
               tests.append({
                   'name': testcase.attrib.get('name'),
                   'classname': testcase.attrib.get('classname'),
                   'time': float(testcase.attrib.get('time', 0.0))
               })
           
           tests.sort(key=lambda x: x['time'], reverse=True)
           return tests[:n]
       
       def get_metrics(self):
           """Get all metrics"""
           total = self.get_test_count()
           failures = self.get_failure_count()
           errors = self.get_error_count()
           skipped = self.get_skip_count()
           
           passed = total - failures - errors - skipped
           
           metrics = {
               'total': total,
               'passed': passed,
               'failed': failures + errors,
               'skipped': skipped,
               'pass_rate': (passed / total * 100) if total > 0 else 0.0,
               'fail_rate': ((failures + errors) / total * 100) if total > 0 else 0.0,
               'total_time': self.get_total_time(),
               'avg_time': self.get_total_time() / total if total > 0 else 0.0
           }
           
           return metrics
   
   # Jenkins Pipeline Integration
   # Groovy script
   """
   def parseTestResults() {
       def junit = junit testResults: '**/test-results/*.xml'
       
       def metrics = [
           total: junit.totalCount,
           passed: junit.passCount,
           failed: junit.failCount,
           skipped: junit.skipCount,
           passRate: (junit.passCount / junit.totalCount * 100).round(2)
       ]
       
       echo "Test Metrics: ${metrics}"
       
       // Store as JSON
       writeJSON file: 'test-metrics.json', json: metrics
       archiveArtifacts 'test-metrics.json'
   }
   """

🔄 Flake Detection
===================

Identify Flaky Tests
--------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Flake detection and analysis"""
   
   from collections import defaultdict
   from dataclasses import dataclass
   from typing import List, Dict
   import statistics
   
   @dataclass
   class TestRun:
       build_number: int
       test_name: str
       status: str
       duration: float
   
   class FlakeDetector:
       def __init__(self, runs: List[TestRun]):
           self.runs = runs
           self.test_history = defaultdict(list)
           
           # Group by test name
           for run in runs:
               self.test_history[run.test_name].append(run)
       
       def calculate_flake_rate(self, test_name):
           """Calculate flake rate for a test"""
           runs = self.test_history[test_name]
           if len(runs) < 2:
               return 0.0
           
           # Count status changes
           status_changes = 0
           for i in range(1, len(runs)):
               if runs[i].status != runs[i-1].status:
                   status_changes += 1
           
           return status_changes / (len(runs) - 1) * 100
       
       def get_flaky_tests(self, threshold=10.0):
           """Get tests with flake rate above threshold"""
           flaky = []
           
           for test_name in self.test_history:
               flake_rate = self.calculate_flake_rate(test_name)
               
               if flake_rate >= threshold:
                   runs = self.test_history[test_name]
                   
                   flaky.append({
                       'test_name': test_name,
                       'flake_rate': flake_rate,
                       'total_runs': len(runs),
                       'passed': sum(1 for r in runs if r.status == 'passed'),
                       'failed': sum(1 for r in runs if r.status == 'failed'),
                       'avg_duration': statistics.mean(r.duration for r in runs)
                   })
           
           flaky.sort(key=lambda x: x['flake_rate'], reverse=True)
           return flaky
       
       def detect_duration_variance(self, test_name):
           """Detect tests with high duration variance"""
           runs = self.test_history[test_name]
           
           if len(runs) < 5:
               return None
           
           durations = [r.duration for r in runs]
           mean = statistics.mean(durations)
           stdev = statistics.stdev(durations)
           
           # Coefficient of variation
           cv = (stdev / mean * 100) if mean > 0 else 0
           
           return {
               'test_name': test_name,
               'mean_duration': mean,
               'stdev_duration': stdev,
               'coefficient_of_variation': cv,
               'min_duration': min(durations),
               'max_duration': max(durations)
           }
       
       def get_unstable_tests(self, cv_threshold=50.0):
           """Get tests with high duration variance"""
           unstable = []
           
           for test_name in self.test_history:
               variance = self.detect_duration_variance(test_name)
               
               if variance and variance['coefficient_of_variation'] >= cv_threshold:
                   unstable.append(variance)
           
           unstable.sort(key=lambda x: x['coefficient_of_variation'], reverse=True)
           return unstable
       
       def generate_report(self):
           """Generate flake detection report"""
           flaky = self.get_flaky_tests()
           unstable = self.get_unstable_tests()
           
           report = {
               'total_tests': len(self.test_history),
               'flaky_tests': flaky,
               'flaky_count': len(flaky),
               'unstable_tests': unstable,
               'unstable_count': len(unstable)
           }
           
           return report
   
   # Usage
   if __name__ == '__main__':
       runs = [
           TestRun(1, 'test_wifi', 'passed', 5.2),
           TestRun(2, 'test_wifi', 'failed', 10.5),
           TestRun(3, 'test_wifi', 'passed', 5.1),
           TestRun(4, 'test_wifi', 'failed', 15.2),
           TestRun(5, 'test_wifi', 'passed', 5.3),
       ]
       
       detector = FlakeDetector(runs)
       report = detector.generate_report()
       
       print(f"Flaky tests: {len(report['flaky_tests'])}")
       for test in report['flaky_tests']:
           print(f"  {test['test_name']}: {test['flake_rate']:.1f}% flake rate")

Retry Logic with Tracking
--------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Test retry with metric tracking"""
   
   import functools
   import time
   from dataclasses import dataclass
   from typing import Callable, Any
   
   @dataclass
   class RetryMetrics:
       test_name: str
       attempts: int
       success_on_attempt: int
       total_duration: float
       error_messages: list
   
   class RetryTracker:
       def __init__(self):
           self.metrics = []
       
       def track_retry(self, func: Callable, max_retries=3, delay=1.0):
           """Decorator to track test retries"""
           @functools.wraps(func)
           def wrapper(*args, **kwargs):
               test_name = func.__name__
               attempts = 0
               start_time = time.time()
               error_messages = []
               
               for attempt in range(1, max_retries + 1):
                   attempts = attempt
                   try:
                       result = func(*args, **kwargs)
                       
                       # Success
                       duration = time.time() - start_time
                       
                       self.metrics.append(RetryMetrics(
                           test_name=test_name,
                           attempts=attempts,
                           success_on_attempt=attempt,
                           total_duration=duration,
                           error_messages=error_messages
                       ))
                       
                       return result
                   
                   except Exception as e:
                       error_messages.append(f"Attempt {attempt}: {str(e)}")
                       
                       if attempt < max_retries:
                           time.sleep(delay)
                       else:
                           # All retries exhausted
                           duration = time.time() - start_time
                           
                           self.metrics.append(RetryMetrics(
                               test_name=test_name,
                               attempts=attempts,
                               success_on_attempt=0,  # Failed
                               total_duration=duration,
                               error_messages=error_messages
                           ))
                           
                           raise
           
           return wrapper
       
       def get_retry_stats(self):
           """Get retry statistics"""
           if not self.metrics:
               return {}
           
           total = len(self.metrics)
           succeeded = sum(1 for m in self.metrics if m.success_on_attempt > 0)
           failed = total - succeeded
           
           # Tests that needed retries
           retried = sum(1 for m in self.metrics if m.attempts > 1)
           
           # Average attempts
           avg_attempts = sum(m.attempts for m in self.metrics) / total
           
           return {
               'total_tests': total,
               'succeeded': succeeded,
               'failed': failed,
               'success_rate': (succeeded / total * 100) if total > 0 else 0.0,
               'retried_count': retried,
               'retry_rate': (retried / total * 100) if total > 0 else 0.0,
               'avg_attempts': avg_attempts
           }
   
   # Usage
   tracker = RetryTracker()
   
   @tracker.track_retry
   def test_flaky_operation():
       import random
       if random.random() < 0.7:  # 70% failure rate
           raise Exception('Flaky failure')
       return True
   
   # Run multiple times
   for i in range(10):
       try:
           test_flaky_operation()
       except:
           pass
   
   stats = tracker.get_retry_stats()
   print(f"Retry stats: {stats}")

⏱️ Duration Analysis
=====================

Test Duration Tracking
-----------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Duration tracking and analysis"""
   
   from datetime import datetime, timedelta
   from typing import List, Dict
   import statistics
   
   class DurationAnalyzer:
       def __init__(self):
           self.durations: Dict[str, List[float]] = {}
       
       def record_duration(self, test_name: str, duration: float):
           """Record test duration"""
           if test_name not in self.durations:
               self.durations[test_name] = []
           
           self.durations[test_name].append(duration)
       
       def get_stats(self, test_name: str):
           """Get duration statistics for a test"""
           durations = self.durations.get(test_name, [])
           
           if not durations:
               return None
           
           return {
               'test_name': test_name,
               'count': len(durations),
               'min': min(durations),
               'max': max(durations),
               'mean': statistics.mean(durations),
               'median': statistics.median(durations),
               'stdev': statistics.stdev(durations) if len(durations) > 1 else 0.0,
               'p95': statistics.quantiles(durations, n=20)[18] if len(durations) >= 20 else max(durations),
               'p99': statistics.quantiles(durations, n=100)[98] if len(durations) >= 100 else max(durations)
           }
       
       def get_slowest_tests(self, n=10):
           """Get N slowest tests by mean duration"""
           stats = []
           
           for test_name in self.durations:
               test_stats = self.get_stats(test_name)
               if test_stats:
                   stats.append(test_stats)
           
           stats.sort(key=lambda x: x['mean'], reverse=True)
           return stats[:n]
       
       def detect_slow_tests(self, threshold_seconds=60.0):
           """Detect tests exceeding duration threshold"""
           slow = []
           
           for test_name in self.durations:
               stats = self.get_stats(test_name)
               
               if stats and stats['mean'] > threshold_seconds:
                   slow.append(stats)
           
           slow.sort(key=lambda x: x['mean'], reverse=True)
           return slow
       
       def detect_duration_regression(self, test_name: str, window=10):
           """Detect if recent runs are slower than historical average"""
           durations = self.durations.get(test_name, [])
           
           if len(durations) < window * 2:
               return None
           
           # Compare recent window to historical average
           recent = durations[-window:]
           historical = durations[:-window]
           
           recent_mean = statistics.mean(recent)
           historical_mean = statistics.mean(historical)
           
           # Calculate percentage change
           change = ((recent_mean - historical_mean) / historical_mean * 100) if historical_mean > 0 else 0
           
           return {
               'test_name': test_name,
               'historical_mean': historical_mean,
               'recent_mean': recent_mean,
               'change_percent': change,
               'is_regression': change > 20.0  # 20% threshold
           }
       
       def get_total_duration(self):
           """Get total duration across all tests"""
           total = 0.0
           
           for durations in self.durations.values():
               total += sum(durations)
           
           return total
       
       def generate_report(self):
           """Generate duration analysis report"""
           slowest = self.get_slowest_tests()
           slow_tests = self.detect_slow_tests()
           
           report = {
               'total_tests': len(self.durations),
               'total_duration': self.get_total_duration(),
               'slowest_tests': slowest,
               'slow_tests_count': len(slow_tests),
               'slow_tests': slow_tests
           }
           
           return report
   
   # PyTest Plugin
   """
   # conftest.py
   import pytest
   import time
   
   duration_analyzer = DurationAnalyzer()
   
   @pytest.hookimpl(tryfirst=True, hookwrapper=True)
   def pytest_runtest_makereport(item, call):
       outcome = yield
       report = outcome.get_result()
       
       if report.when == 'call':
           duration_analyzer.record_duration(
               test_name=item.nodeid,
               duration=report.duration
           )
   
   @pytest.fixture(scope='session', autouse=True)
   def report_durations(request):
       yield
       
       # After all tests
       report = duration_analyzer.generate_report()
       print(f"\nDuration Report:")
       print(f"Total duration: {report['total_duration']:.2f}s")
       print(f"Slowest tests:")
       for test in report['slowest_tests'][:5]:
           print(f"  {test['test_name']}: {test['mean']:.2f}s")
   """

Build Time Tracking
-------------------

.. code-block:: groovy

   // Jenkins Pipeline - Build time tracking
   
   def trackBuildTimes() {
       def startTime = System.currentTimeMillis()
       
       def stageTimes = [:]
       
       stage('Checkout') {
           def stageStart = System.currentTimeMillis()
           // ... checkout code
           stageTimes['Checkout'] = System.currentTimeMillis() - stageStart
       }
       
       stage('Build') {
           def stageStart = System.currentTimeMillis()
           // ... build
           stageTimes['Build'] = System.currentTimeMillis() - stageStart
       }
       
       stage('Test') {
           def stageStart = System.currentTimeMillis()
           // ... test
           stageTimes['Test'] = System.currentTimeMillis() - stageStart
       }
       
       def totalTime = System.currentTimeMillis() - startTime
       
       // Store metrics
       def metrics = [
           build_number: env.BUILD_NUMBER,
           total_time: totalTime,
           stage_times: stageTimes,
           timestamp: new Date().format('yyyy-MM-dd HH:mm:ss')
       ]
       
       writeJSON file: 'build-metrics.json', json: metrics
       archiveArtifacts 'build-metrics.json'
       
       // Publish to InfluxDB
       publishInfluxData(metrics)
   }
   
   def publishInfluxData(metrics) {
       influxDbPublisher(
           selectedTarget: 'influxdb',
           customProjectName: 'embedded-builds',
           customData: [
               'build_time,job=${env.JOB_NAME} total=${metrics.total_time}i ${System.currentTimeMillis()}000000',
               "build_time,job=${env.JOB_NAME},stage=Build value=${metrics.stage_times['Build']}i ${System.currentTimeMillis()}000000",
               "build_time,job=${env.JOB_NAME},stage=Test value=${metrics.stage_times['Test']}i ${System.currentTimeMillis()}000000"
           ]
       )
   }

📈 Dashboards & Visualization
================================

Grafana Dashboard Configuration
--------------------------------

.. code-block:: yaml

   # grafana-dashboard.json (simplified)
   {
     "dashboard": {
       "title": "Embedded Test Metrics",
       "panels": [
         {
           "title": "Pass Rate Over Time",
           "type": "graph",
           "targets": [
             {
               "query": "SELECT mean(pass_rate) FROM test_metrics WHERE $timeFilter GROUP BY time($interval)"
             }
           ]
         },
         {
           "title": "Test Duration",
           "type": "graph",
           "targets": [
             {
               "query": "SELECT mean(duration) FROM test_executions WHERE $timeFilter GROUP BY test_name, time($interval)"
             }
           ]
         },
         {
           "title": "Flake Rate",
           "type": "stat",
           "targets": [
             {
               "query": "SELECT last(flake_rate) FROM test_metrics"
             }
           ],
           "thresholds": [
             { "value": 0, "color": "green" },
             { "value": 5, "color": "yellow" },
             { "value": 10, "color": "red" }
           ]
         },
         {
           "title": "Failed Tests",
           "type": "table",
           "targets": [
             {
               "query": "SELECT test_name, count(*) as failures FROM test_results WHERE status='failed' AND time > now() - 7d GROUP BY test_name ORDER BY failures DESC LIMIT 10"
             }
           ]
         }
       ]
     }
   }

**InfluxDB Data Model:**

.. code-block:: text

   Measurement: test_executions
   Tags: test_name, status, build_number
   Fields: duration, timestamp
   
   Measurement: test_metrics
   Tags: build_number, job_name
   Fields: pass_rate, fail_rate, flake_rate, total_tests

Python Dashboard Generator
---------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Generate HTML dashboard from test metrics"""
   
   import json
   from pathlib import Path
   from datetime import datetime
   
   class DashboardGenerator:
       def __init__(self, metrics_file):
           with open(metrics_file) as f:
               self.metrics = json.load(f)
       
       def generate_html(self):
           """Generate HTML dashboard"""
           html = f"""
   <!DOCTYPE html>
   <html>
   <head>
       <title>Test Metrics Dashboard</title>
       <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
       <style>
           body {{ font-family: Arial, sans-serif; margin: 20px; }}
           .metric-card {{ 
               display: inline-block; 
               padding: 20px; 
               margin: 10px; 
               border: 1px solid #ddd; 
               border-radius: 5px;
               min-width: 200px;
           }}
           .metric-value {{ font-size: 32px; font-weight: bold; }}
           .metric-label {{ font-size: 14px; color: #666; }}
           .chart {{ width: 100%; height: 400px; margin: 20px 0; }}
       </style>
   </head>
   <body>
       <h1>Test Metrics Dashboard</h1>
       <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
       
       <div class="metric-card">
           <div class="metric-value">{self.metrics['pass_rate']:.1f}%</div>
           <div class="metric-label">Pass Rate</div>
       </div>
       
       <div class="metric-card">
           <div class="metric-value">{self.metrics['total_tests']}</div>
           <div class="metric-label">Total Tests</div>
       </div>
       
       <div class="metric-card">
           <div class="metric-value">{self.metrics['failed']}</div>
           <div class="metric-label">Failed</div>
       </div>
       
       <div class="metric-card">
           <div class="metric-value">{self.metrics.get('flake_rate', 0):.1f}%</div>
           <div class="metric-label">Flake Rate</div>
       </div>
       
       <div id="passRateChart" class="chart"></div>
       <div id="durationChart" class="chart"></div>
       
       <script>
           // Pass rate trend
           var passRateData = {{
               x: {json.dumps([m['date'] for m in self.metrics.get('history', [])])},
               y: {json.dumps([m['pass_rate'] for m in self.metrics.get('history', [])])},
               type: 'scatter',
               name: 'Pass Rate'
           }};
           
           Plotly.newPlot('passRateChart', [passRateData], {{
               title: 'Pass Rate Trend',
               yaxis: {{title: 'Pass Rate (%)', range: [0, 100]}}
           }});
           
           // Duration chart
           var durationData = {{
               x: {json.dumps([t['name'] for t in self.metrics.get('slowest_tests', [])])},
               y: {json.dumps([t['duration'] for t in self.metrics.get('slowest_tests', [])])},
               type: 'bar',
               name: 'Duration'
           }};
           
           Plotly.newPlot('durationChart', [durationData], {{
               title: 'Slowest Tests',
               yaxis: {{title: 'Duration (seconds)'}}
           }});
       </script>
   </body>
   </html>
           """
           
           return html
       
       def save_dashboard(self, output_path='dashboard.html'):
           """Save dashboard to file"""
           html = self.generate_html()
           
           with open(output_path, 'w') as f:
               f.write(html)
           
           print(f'Dashboard saved to {output_path}')
   
   # Usage
   if __name__ == '__main__':
       generator = DashboardGenerator('test-metrics.json')
       generator.save_dashboard()

Jenkins Blue Ocean Metrics
---------------------------

.. code-block:: groovy

   // Jenkins Pipeline with Blue Ocean metrics
   
   pipeline {
       agent any
       
       stages {
           stage('Test') {
               steps {
                   script {
                       // Run tests
                       sh 'pytest --junitxml=results.xml'
                       
                       // Parse results
                       def testResults = junit 'results.xml'
                       
                       // Custom metrics
                       def metrics = [
                           total: testResults.totalCount,
                           passed: testResults.passCount,
                           failed: testResults.failCount,
                           pass_rate: (testResults.passCount / testResults.totalCount * 100).round(2)
                       ]
                       
                       // Publish to build description
                       currentBuild.description = "Pass Rate: ${metrics.pass_rate}%"
                       
                       // Set build status based on metrics
                       if (metrics.pass_rate < 90) {
                           currentBuild.result = 'UNSTABLE'
                       }
                   }
               }
           }
       }
       
       post {
           always {
               // Publish test results
               junit 'results.xml'
               
               // Archive artifacts
               archiveArtifacts artifacts: 'results.xml', allowEmptyArchive: true
           }
       }
   }

📉 Trend Analysis
==================

Historical Trend Tracking
-------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Track metrics trends over time"""
   
   import json
   from datetime import datetime, timedelta
   from pathlib import Path
   from typing import List, Dict
   
   class TrendAnalyzer:
       def __init__(self, metrics_dir):
           self.metrics_dir = Path(metrics_dir)
           self.history = self.load_history()
       
       def load_history(self):
           """Load historical metrics"""
           history = []
           
           for metrics_file in self.metrics_dir.glob('metrics_*.json'):
               with open(metrics_file) as f:
                   data = json.load(f)
                   history.append(data)
           
           # Sort by timestamp
           history.sort(key=lambda x: x.get('timestamp', ''))
           return history
       
       def calculate_trend(self, metric_name, window=7):
           """Calculate trend for a metric"""
           if len(self.history) < 2:
               return None
           
           recent = self.history[-window:]
           
           values = [m.get(metric_name, 0) for m in recent]
           
           # Simple linear regression
           n = len(values)
           x = list(range(n))
           
           mean_x = sum(x) / n
           mean_y = sum(values) / n
           
           numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
           denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
           
           slope = numerator / denominator if denominator != 0 else 0
           
           return {
               'metric': metric_name,
               'current_value': values[-1],
               'trend_slope': slope,
               'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
           }
       
       def detect_anomalies(self, metric_name, threshold_stdev=2.0):
           """Detect anomalous values"""
           values = [m.get(metric_name, 0) for m in self.history]
           
           if len(values) < 10:
               return []
           
           mean = statistics.mean(values)
           stdev = statistics.stdev(values)
           
           anomalies = []
           
           for i, (value, data) in enumerate(zip(values, self.history)):
               z_score = abs((value - mean) / stdev) if stdev > 0 else 0
               
               if z_score > threshold_stdev:
                   anomalies.append({
                       'index': i,
                       'timestamp': data.get('timestamp'),
                       'value': value,
                       'z_score': z_score,
                       'deviation': value - mean
                   })
           
           return anomalies
       
       def compare_periods(self, metric_name, period_days=7):
           """Compare current period to previous period"""
           cutoff_date = datetime.now() - timedelta(days=period_days)
           
           current_period = []
           previous_period = []
           
           for data in self.history:
               timestamp = datetime.fromisoformat(data.get('timestamp', ''))
               value = data.get(metric_name, 0)
               
               if timestamp >= cutoff_date:
                   current_period.append(value)
               else:
                   previous_period.append(value)
           
           if not current_period or not previous_period:
               return None
           
           current_avg = statistics.mean(current_period)
           previous_avg = statistics.mean(previous_period)
           
           change = ((current_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
           
           return {
               'metric': metric_name,
               'current_avg': current_avg,
               'previous_avg': previous_avg,
               'change_percent': change,
               'improving': (change > 0 and metric_name in ['pass_rate', 'coverage']) or 
                           (change < 0 and metric_name in ['fail_rate', 'duration', 'flake_rate'])
           }
       
       def generate_trend_report(self):
           """Generate comprehensive trend report"""
           metrics_to_track = ['pass_rate', 'fail_rate', 'flake_rate', 'duration']
           
           report = {
               'generated_at': datetime.now().isoformat(),
               'data_points': len(self.history),
               'trends': {},
               'comparisons': {},
               'anomalies': {}
           }
           
           for metric in metrics_to_track:
               report['trends'][metric] = self.calculate_trend(metric)
               report['comparisons'][metric] = self.compare_periods(metric)
               report['anomalies'][metric] = self.detect_anomalies(metric)
           
           return report

🎯 Test Coverage Metrics
==========================

Code Coverage Tracking
-----------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Code coverage metric tracking"""
   
   import xml.etree.ElementTree as ET
   from pathlib import Path
   
   class CoverageAnalyzer:
       def __init__(self, coverage_xml):
           self.tree = ET.parse(coverage_xml)
           self.root = self.tree.getroot()
       
       def get_line_coverage(self):
           """Get line coverage percentage"""
           lines_covered = int(self.root.attrib.get('lines-covered', 0))
           lines_valid = int(self.root.attrib.get('lines-valid', 0))
           
           return (lines_covered / lines_valid * 100) if lines_valid > 0 else 0.0
       
       def get_branch_coverage(self):
           """Get branch coverage percentage"""
           branches_covered = int(self.root.attrib.get('branches-covered', 0))
           branches_valid = int(self.root.attrib.get('branches-valid', 0))
           
           return (branches_covered / branches_valid * 100) if branches_valid > 0 else 0.0
       
       def get_uncovered_files(self):
           """Get files with low coverage"""
           uncovered = []
           
           for package in self.root.findall('.//package'):
               for cls in package.findall('classes/class'):
                   filename = cls.attrib.get('filename')
                   
                   lines_covered = int(cls.attrib.get('lines-covered', 0))
                   lines_valid = int(cls.attrib.get('lines-valid', 0))
                   
                   coverage = (lines_covered / lines_valid * 100) if lines_valid > 0 else 0.0
                   
                   if coverage < 80.0:  # Threshold
                       uncovered.append({
                           'file': filename,
                           'coverage': coverage,
                           'lines_covered': lines_covered,
                           'lines_valid': lines_valid
                       })
           
           uncovered.sort(key=lambda x: x['coverage'])
           return uncovered
       
       def get_metrics(self):
           """Get all coverage metrics"""
           return {
               'line_coverage': self.get_line_coverage(),
               'branch_coverage': self.get_branch_coverage(),
               'uncovered_files': self.get_uncovered_files()
           }

📖 Best Practices
==================

1. **Track key metrics consistently** - Pass rate, duration, flake rate minimum
2. **Set thresholds and alerts** - Notify on metric degradation
3. **Visualize trends** - Dashboards for visibility
4. **Automate metric collection** - No manual steps
5. **Act on insights** - Fix flaky tests, optimize slow tests
6. **Compare across builds** - Identify regressions early
7. **Share dashboards** - Team visibility
8. **Review metrics regularly** - Weekly/sprint reviews
9. **Correlate metrics** - Duration vs pass rate relationships
10. **Continuous improvement** - Iterate based on data

📚 References
==============

* **JUnit XML Format**: https://github.com/testmoapp/junitxml
* **Grafana**: https://grafana.com/docs/
* **InfluxDB**: https://docs.influxdata.com/
* **Jenkins Metrics Plugin**: https://plugins.jenkins.io/metrics/
* **PyTest Coverage**: https://pytest-cov.readthedocs.io/
* **Plotly Dashboards**: https://plotly.com/python/

================================
Last Updated: January 2026
Version: 3.0
================================
