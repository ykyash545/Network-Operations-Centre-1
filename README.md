# Network-Operations-Centre-1
# 1. Introduction

This document outlines the initial scope and design of the Network Operations Centre (NOC) v0.0.1, a tool developed using Python and Streamlit to monitor the health and status of network devices (servers).

# 2. Project Goals

Real-time monitoring of server availability.
Data visualization for clear and concise insights.
Key Performance Indicators (KPIs) for quick status assessment.
User-friendly interface for easy interaction and navigation.

# 3. Features
> Server Management:
> Add and manage a list of target servers (IP addresses or hostnames).
> Real-time Ping Monitoring:
> Continuously monitor server reachability using ICMP ping checks.
# Server Status:
>> Display real-time server status (UP/DOWN).
# KPIs:
> Total Servers
> Servers Up
> Servers Down
> Data Visualization:
> Ping History Chart (line chart)
> Server Status Distribution (bar chart)
> Server Uptime/Downtime

# User Interface:
Customizable dark/light mode.
Intuitive and user-friendly layout.
Refresh button for real-time data updates.

# 4. Technology Stack

Python: Core programming language.
Streamlit: Framework for building interactive web applications.
Pandas: Data manipulation and analysis.
Matplotlib/Seaborn: Data visualization.
Subprocess: System command execution (for ping).

# 5. Project Structure (Simplified)

NOC_v0.0.1/
├── main.py # Main application file
└── requirements.txt # List of dependencies

# 6. Development Process

Phase 1: Initial development and implementation of core features.
Phase 2: User interface enhancements and visual refinements.
Phase 3: Testing and bug fixes.

# 7. Future Enhancements (Roadmap)

Advanced Ping Options: Configure ping timeout, packet count, and interval.
Traceroute Functionality: Network path analysis for deeper troubleshooting.
Server Grouping: Organize servers into groups for easier management and monitoring.
Data Storage and Reporting: historical data for trend analysis and reporting.
Alert : Email Notifications for critical servers

# FULLY DEVLOPED IN PYTHON
