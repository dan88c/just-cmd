#!/usr/bin/env python3
import sys
import json
import os
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_parts.append(cleaned)

    def get_text(self):
        return " ".join(self.text_parts[:50])

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

        url = data.get("target_url")
        action = data.get("action")
        task = data.get("task", "")

        # Guard: Validate URL scheme to prevent arbitrary file reading
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("Only http and https schemes are permitted")

        # Emulate bounded OpenClaw scraping with standard urllib & timeout
        req = urllib.request.Request(url, headers={"User-Agent": "Wallop-OpenClaw-Demo/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            html_content = response.read().decode("utf-8", errors="ignore")

        parser = TextExtractor()
        parser.feed(html_content)
        extracted_summary = parser.get_text()

        print(json.dumps({
            "status": "success",
            "url": url,
            "action": action,
            "task_acknowledged": task,
            "summary": extracted_summary
        }))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error in openclaw_gateway: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()