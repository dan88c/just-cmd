set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

python_bin   := "python"
bridge_root  := "C:/work/just-bridge"
wallop_root  := "C:/work/wallop-bare"

# 印出當前 justfile 所在的絕對目錄路徑
path:
    @Write-Host "{{justfile_directory()}}"

# 列出可用任務
check:
    just-cmd --list

# -----------------------------------------------------------------------------
# Demo Tasks
# -----------------------------------------------------------------------------

# 1. 執行於 C:\work\just-bridge
demo-sentinel payload="demo/system-sentinel/sample_payload.json":
    Set-Location "{{bridge_root}}"; & {{python_bin}} demo/system-sentinel/sentinel.py {{payload}}

# 2. 執行於 C:\work\wallop-bare
demo-calendar payload="demo/calendar-gateway/sample_payload.json":
    Set-Location "{{wallop_root}}"; & {{python_bin}} demo/calendar-gateway/calendar.py {{payload}}

# 3. 執行於 C:\work\wallop-bare
demo-openclaw payload="demo/openclaw-gateway/sample_payload.json":
    Set-Location "{{wallop_root}}"; & {{python_bin}} demo/openclaw-gateway/openclaw_runner.py {{payload}}

# 一鍵依序執行
demo-all: demo-sentinel demo-calendar demo-openclaw