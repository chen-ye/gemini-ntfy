#!/usr/bin/env python3
import sys
import json
import os
import urllib.request
import socket

def log(msg):
    """Logs message to stderr."""
    sys.stderr.write(f"[hook] {msg}\n")

def send_ntfy(topic, title, message, notification_id=None, priority="default", tags=None, click=None):
    """Sends a notification via ntfy."""
    base_url = os.environ.get("GEMINI_NTFY_SERVER", "https://ntfy.sh").rstrip('/')
    url = f"{base_url}/{topic}"
    
    if topic.startswith("http://") or topic.startswith("https://"):
        url = topic

    try:
        data = message.encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header("Title", title)
        req.add_header("Priority", priority)
        req.add_header("Content-Type", "text/markdown")
        
        if notification_id:
            req.add_header("X-Ntfy-Id", notification_id)
        
        if tags:
            req.add_header("Tags", ",".join(tags))

        if click:
            req.add_header("Click", click)
        
        with urllib.request.urlopen(req) as response:
            log(f"Notification sent to {url} (ID: {notification_id})")
            
    except Exception as e:
        log(f"Error sending ntfy to {url}: {e}")

def main():
    # 1. Configuration: Get ntfy topic (Argument > Environment Variable)
    topic = os.environ.get("GEMINI_NTFY_TOPIC")
    if len(sys.argv) > 1:
        topic = sys.argv[1]

    if not topic:
        log("GEMINI_NTFY_TOPIC not set. Skipping notification.")
        return

    # Configuration: Get Notification ID (Environment Variable > Hostname)
    notification_id = os.environ.get("GEMINI_NTFY_ID", socket.gethostname())
    
    # Configuration: Click URL (defaults to opening Termux)
    click_url = os.environ.get("GEMINI_NTFY_CLICK", "intent://#Intent;package=com.termux;end")

    # 2. Parse Input from stdin
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        data = json.loads(input_data)
    except Exception as e:
        log(f"Error parsing input JSON: {e}")
        return

    event = data.get("hook_event_name")
    log(f"Handling event: {event}")

    # 3. Handle Events
    if event == "AfterAgent":
        # evergreen: prompt_response is provided directly
        response_text = data.get("prompt_response", "Agent finished execution.")
        send_ntfy(topic, f"Gemini: {event}", response_text, notification_id, priority="default", tags=["diamond_shape_with_a_dot_inside"], click=click_url)

    elif event == "Notification":
        # evergreen: message is provided directly
        message = data.get("message", "User attention required.")
        send_ntfy(topic, f"Gemini: {event}", message, notification_id, priority="default", tags=["hand"], click=click_url)
        
        # Feedback to the CLI
        print(json.dumps({"systemMessage": "Notification sent via ntfy." }))

if __name__ == "__main__":
    main()
