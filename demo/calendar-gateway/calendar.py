#!/usr/bin/env python3
import sys
import json
import os

def load_payload():
    if len(sys.argv) > 1:
        raw_payload = sys.argv[1]
        if os.path.isfile(raw_payload):
            with open(raw_payload, "r", encoding="utf-8") as f:
                return json.load(f)
        return json.loads(raw_payload)
    raw_payload = sys.stdin.read()
    if not raw_payload.strip():
        sys.stderr.write("Missing JSON payload\n")
        sys.exit(1)
    return json.loads(raw_payload)

def main():
    try:
        data = load_payload()

        action = data.get("action")
        if action == "sync":
            target_date = data.get("date", "all")
            print(json.dumps({
                "status": "synchronized",
                "target_date": target_date,
                "events_found": 0
            }))
            sys.exit(0)
        elif action == "create_event":
            title = data.get("title")
            if not title:
                raise ValueError("Missing title for create_event")
            print(json.dumps({
                "status": "created",
                "title": title,
                "start_time": data.get("start_time", "2026-09-17T09:00:00Z")
            }))
            sys.exit(0)
        else:
            raise ValueError(f"Unsupported action: {action}")
    except Exception as e:
        sys.stderr.write(f"Error in calendar_gateway: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()