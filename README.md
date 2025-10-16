# DEVOPS_FETCH

devopsfetch-displaying_information
Devopsfetch: Server Information Retrieval and Monitoring Tool Let's break down the concepts and walk through how you would approach building this tool step by step.

Devopsfetch Devopsfetch is a modular Python-based tool for collecting and monitoring system, service, and container information. It is organized for use in automated DevOps pipelines and local infrastructure diagnostics.

Information Retrieval Modules Ports: List all network ports currently in use, showing the associated services. Docker: List all Docker images and running containers. Nginx: Display all configured domains (server_names) and ports from Nginx configs. Users: List system users and their last login times; for a specific user, show groups Time Range: Filter logs or activities based on a date/time window for compliance or investigation.

Output Formatting Use tables with descriptive headers for all main outputs. This improves readability and makes monitoring easier.

Features Docker container info retrieval

Nginx server status extraction

Active ports enumeration

User activity monitoring

System activity tracking

Structured logging

Extensible utility functions

File structure

File/Folder Description modules/: Main source folder containing all logic modules devopsfetch.py: Entry-point script; runs main collection routine devopsfetch.service: Example systemd service unit for daemonizing install.sh: Dependency installation script requirements.txt: Python dependencies list venv/: Local Python virtual environment

Modules docker_info.py : Gets Docker stats and metadata.

nginx_info.py : Checks Nginx status and config.

monitor.py : Monitors system-level metrics/resources.

ports_info.py : Lists active ports and related details.

time_activity.py : Tracks system uptime and activity period.

users_info.py : Fetches user login and session info.

logger_config.py : Configures logging framework.

utils.py : Utility functions shared by multiple modules.

init.py : Package marker for imports.

3.Installation Run the included shell script to set up dependencies: bash sh install.sh

4.manually install Python requirements: bash pip install -r requirements.txt

5.Usage To run Devopsfetch directly: bash python devopsfetch.py

6.Copy the provided systemd service file: bash sudo cp devopsfetch.service /etc/systemd/system/

7.Enable and start the service bash sudo systemctl enable devopsfetch sudo systemctl start devopsfetch

8.check the service status bash sudo systemctl status devopsfetch

9.Quick to run commands Ports python devopsfetch.py --port

Docker python devopsfetch.py --docker

Nginx python devopsfetch.py --nginx

Users python devopsfetch.py --users

Time python devopsfetch.py --time 2025-10-01 2025-10-15

Monitor python devopsfetch.py --monitor

CONCLUSION DevOpsfetch is organized for modularity, maintainability, and extensible automation. A well-documented structure combined with organized code modules and clear deployment scripts makes it easy to integrate with your DevOps pipeline or infrastructure monitoring stack.It simplifies system Diagnostics and Devops Monitoring by providing clean, scriptable access to critical infrastructure data all in place.
