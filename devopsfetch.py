#!/usr/bin/env python3
import argparse
import os
import socket
import subprocess
import psutil
from tabulate import tabulate
from flask import Flask, render_template_string

app = Flask(__name__)

def show_ports(port_filter="ALL"):
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
        pid = conn.pid or "-"
        process = "-"
        try:
            process = psutil.Process(pid).name() if pid != "-" else "-"
        except Exception:
            pass
        if port_filter == "ALL" or str(conn.laddr.port) == str(port_filter):
            connections.append([conn.type, laddr, raddr, conn.status, process])
    if connections:
        print(tabulate(connections, headers=["PROTO", "LOCAL", "REMOTE", "STATUS", "PROCESS"], tablefmt="fancy_grid"))
    else:
        print(f"No connections found for port {port_filter}")

def show_docker(detail_name="ALL"):
    try:
        output = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}\t{{.Image}}\t{{.Ports}}"])
        lines = output.decode().strip().split("\n")
        if not lines or lines == ['']:
            print("No running Docker containers.")
            return
        data = [line.split("\t") for line in lines]
        print(tabulate(data, headers=["CONTAINER", "IMAGE", "PORTS"], tablefmt="fancy_grid"))
    except subprocess.CalledProcessError:
        print("Docker not running or not installed.")

def show_nginx(domain="ALL"):
    nginx_dir = "/etc/nginx/sites-enabled"
    if not os.path.isdir(nginx_dir):
        print("Nginx config directory not found.")
        return
    for file in os.listdir(nginx_dir):
        path = os.path.join(nginx_dir, file)
        if os.path.isfile(path):
            with open(path) as f:
                content = f.read()
                if domain == "ALL" or domain in content:
                    print(f"\n=== {file} ===\n{content}")

def show_users(detail_user="ALL"):
    output = subprocess.check_output(["who"]).decode().strip().split("\n")
    if not output or output == ['']:
        print("No logged-in users.")
        return
    users = [line.split()[:2] for line in output]
    print(tabulate(users, headers=["USER", "TTY"], tablefmt="fancy_grid"))

def monitor_loop():
    print("Monitoring CPU and memory usage. Press Ctrl+C to stop.")
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            print(f"CPU: {cpu}% | Memory: {mem}%")
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

@app.route("/")
def index():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return render_template_string("""
        <html>
        <head><title>DevOpsFetch Dashboard</title></head>
        <body style='font-family:Arial;margin:40px;'>
        <h1>DevOpsFetch Web Dashboard</h1>
        <p><b>CPU Usage:</b> {{cpu}}%</p>
        <p><b>Memory Usage:</b> {{mem}}%</p>
        </body>
        </html>
    """, cpu=cpu, mem=mem)

def main():
    parser = argparse.ArgumentParser(description="devopsfetch: system info & monitoring tool")
    parser.add_argument("-p", "--port", nargs='?', const="ALL", help="Show port usage or filter by port")
    parser.add_argument("-d", "--docker", nargs='?', const="ALL", help="Show Docker info or inspect container/image")
    parser.add_argument("-n", "--nginx", nargs='?', const="ALL", help="Show nginx vhost info or filter by domain")
    parser.add_argument("-u", "--users", nargs='?', const="ALL", help="Show user login info or specific user")
    parser.add_argument("--monitor", action="store_true", help="Run continuous monitoring loop")
    parser.add_argument("--web", action="store_true", help="Run web dashboard on http://localhost:8080")

    args = parser.parse_args()

    if args.port:
        show_ports(port_filter=args.port)
    elif args.docker:
        show_docker(detail_name=args.docker)
    elif args.nginx:
        show_nginx(domain=args.nginx)
    elif args.users:
        show_users(detail_user=args.users)
    elif args.monitor:
        monitor_loop()
    elif args.web:
        print("Starting DevOpsFetch web server on http://localhost:8080 ...")
        app.run(host="0.0.0.0", port=8080, debug=False)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
