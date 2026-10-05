# See tool - automatic Windows installer.
# Run this line in PowerShell and follow what it says:
# powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/humbleangel/opencode-tool-see/main/install-windows.ps1 | iex"
$ErrorActionPreference = "Stop"
$Repo = "humbleangel/opencode-tool-see"
$Files = @("see.py", "see.ts", "see.json")
$ToolsDir = Join-Path $HOME ".config\opencode\tools"

Write-Host ""
Write-Host "=== See tool installer ==="
Write-Host "This will check Python, copy the 3 tool files, and optionally save your API key."
Write-Host ""

function Refresh-Path {
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Host "Python not found. Trying to install it automatically..."
  try {
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    Refresh-Path
  } catch {
    Write-Host "Automatic install did not work."
    Write-Host "Please install Python from https://www.python.org/downloads/ (tick 'Add python.exe to PATH'),"
    Write-Host "then run this installer again."
    exit 1
  }
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Host "Python was installed, but this window cannot see it yet."
  Write-Host "Close this window, open a new one, and run the installer again."
  exit 1
}
python --version

Write-Host "Copying the tool files..."
New-Item -ItemType Directory -Path $ToolsDir -Force | Out-Null
foreach ($f in $Files) {
  Invoke-WebRequest -Uri "https://raw.githubusercontent.com/$Repo/main/$f" -OutFile (Join-Path $ToolsDir $f)
  Write-Host "  installed $f"
}

Write-Host ""
Write-Host "This tool looks at pictures through your OpenCode account."
Write-Host "In OpenCode, run /connect and copy your Zen or Go key."
$key = Read-Host "Paste the key here (or press Enter to skip - you can add it later)"
if ($key) {
  setx ZEN_API_KEY $key | Out-Null
  Write-Host "Key saved. Close this window and open a new one so it takes effect."
} else {
  Write-Host "Skipped. Later, save your key with: setx ZEN_API_KEY ""your key here"""
}

Write-Host ""
Write-Host "Done! Now restart OpenCode, then point at any picture and ask what is in it."
