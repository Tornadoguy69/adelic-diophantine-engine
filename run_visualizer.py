#!/usr/bin/env python3
"""
Adelic Diophantine Engine — One-Click Interactive Visualizer Launcher
----------------------------------------------------------------------
Starts a local zero-dependency HTTP server and automatically opens
the interactive 3D WebGL / Canvas visualizer in your default browser.
"""

import http.server
import os
import socketserver
import sys
import threading
import time
import webbrowser

PORT = 8000
HTML_FILE = "visualizer.html"

def find_available_port(start_port=8000, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        try:
            with socketserver.TCPServer(("", port), None) as s:
                return port
        except OSError:
            continue
    return start_port

def main():
    # Change working directory to the directory where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if not os.path.exists(HTML_FILE):
        print(f"Error: Could not find '{HTML_FILE}' in {script_dir}")
        sys.exit(1)

    port = find_available_port(PORT)
    handler = http.server.SimpleHTTPRequestHandler
    
    # Silence access logs in the terminal for clean output
    handler.log_message = lambda self, format, *args: None

    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/{HTML_FILE}"
        
        print("\n" + "=" * 64)
        print(" Adelic Diophantine Engine — Interactive 3D Visualizer")
        print("=" * 64)
        print(f" Local Server Running: {url}")
        print(" Opening in your default web browser now...")
        print(" Press Ctrl+C in this terminal to stop the server.")
        print("=" * 64 + "\n")

        # Open browser in a separate thread after a brief delay
        def open_browser():
            time.sleep(0.6)
            webbrowser.open(url)

        threading.Thread(target=open_browser, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!\n")
            httpd.server_close()

if __name__ == "__main__":
    main()
