What our system is
SafeSight Analytics is an intelligent, real-time video surveillance system for public safety.
It connects to one or more CCTV/IP cameras (or webcams/phone cameras for demo) and analyzes live video in real time.

It performs:
Face detection and face recognition: detects faces from the video stream and compares them with a stored face database (e.g., wanted/suspect list, authorized persons).
Object detection: detects specific high-risk objects such as weapons or other restricted items.
Behavior/condition rules: combines detections with simple rules (e.g., “person with weapon and no uniform”) to raise alerts.
When a detected face matches a stored record, or when a high-risk object/behavior is observed, the system automatically issues alerts to security operators via a dashboard.​

For the capstone, we will build a functional prototype that shows:
Real-time video processing from one or more cameras.
Face detection and matching against a local database.
Object detection for selected classes (e.g., person, gun, knife).
Automated alert generation and visualization in a web-based control panel.​

What problems we are solving and for which users
Main problems in current security environments:
Security operators must watch many camera feeds at once and can easily miss a suspect or dangerous object in real time.
Identifying wanted or banned individuals usually depends on human memory or slow manual checks.
Dangerous objects (weapons, restricted items) might not be noticed quickly, especially in crowded events.​

Our system addresses these by:
Automatically scanning faces in live video and matching them against a database of “persons of interest” (wanted, banned, or VIP), then raising alerts when there is a match.
Detecting selected high-risk objects and notifying operators when someone appears armed or is carrying something suspicious in a restricted area.
Providing a dashboard that shows alerts with timestamps, camera source, and basic context, improving situational awareness and response speed.​

Target users:
Public safety and law enforcement units (city surveillance centers, transport hubs).
Campus and organizational security teams (universities, offices, hospitals, factories).
Event security teams (concerts, stadiums, festivals) who set up temporary control rooms with multiple cameras.​

Key functional points to emphasize:
Multi-camera or multi-stream input.
Real-time face detection and database-based face matching.
Object detection for selected dangerous or restricted items.
Rule-based alert generation (e.g., wanted person detected, weapon detected in restricted zone).
Web dashboard to view live feeds, alerts, and event history

