set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

python_bin := "python"
root_dir   := justfile_directory()

# Print absolute directory path of the active justfile
path:
    @Write-Host "{{root_dir}}"

# List all available recipes
check:
    just-cmd --list

# -----------------------------------------------------------------------------
# Demo Tasks (Subdirectory Path Variations)
# -----------------------------------------------------------------------------

# Pattern 1: Execute from repository root with relative script path
demo-sentinel payload="demo/system-sentinel/sample_payload.json":
    Set-Location "{{root_dir}}"; & {{python_bin}} demo/system-sentinel/sentinel.py {{payload}}

# Pattern 2: Switch execution context into the specific gateway subdirectory
demo-calendar payload="sample_payload.json":
    Set-Location "{{root_dir}}/demo/calendar-gateway"; & {{python_bin}} calendar.py {{payload}}

# Pattern 3: Execute from gateway folder while resolving payload path from root
demo-openclaw payload="demo/openclaw-gateway/sample_payload.json":
    Set-Location "{{root_dir}}/demo/openclaw-gateway"; & {{python_bin}} openclaw_runner.py (Join-Path "{{root_dir}}" "{{payload}}")

# Run all demo pipelines sequentially
demo-all: demo-sentinel demo-calendar demo-openclaw