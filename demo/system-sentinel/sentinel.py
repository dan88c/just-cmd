#!/usr/bin/env python3
import sys
import json
import platform
import os

def get_stats(metric):
    if metric == "resources":
        # Pure standard library metrics (zero external pip dependencies)
        load = os.getloadavg() if hasattr(os, "getloadavg") else [0.0, 0.0, 0.0]
        return {
            "cpu_cores": os.cpu_count(),
            "load_avg_1m": load[0],
            "load_avg_5m": load[1]
        }
    elif metric == "os":
        return {
            "system": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine()
        }
    elif metric == "uptime":
        return {"status": "online"}
    raise ValueError(f"Unsupported metric: {metric}")

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

        metric = data.get("metric")
        result = get_stats(metric)
        print(json.dumps(result))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error in system_sentinel: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()