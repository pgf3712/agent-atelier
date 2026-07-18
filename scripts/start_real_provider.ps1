$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

python -c "import openai" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "The optional OpenAI package is not installed." -ForegroundColor Yellow
    Write-Host 'Install it first with: python -m pip install -e ".[real]"'
    Read-Host "Press Enter to close"
    exit 1
}

$model = Read-Host "Model ID enabled in your own API project"
if ([string]::IsNullOrWhiteSpace($model)) {
    Write-Host "No model was entered. Nothing was started." -ForegroundColor Yellow
    Read-Host "Press Enter to close"
    exit 1
}

$secureKey = Read-Host "Paste your OpenAI API key (the text is hidden)" -AsSecureString
$keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer)
}

if ([string]::IsNullOrWhiteSpace($plainKey)) {
    Write-Host "No key was entered. Nothing was started." -ForegroundColor Yellow
    $plainKey = $null
    Read-Host "Press Enter to close"
    exit 1
}

try {
    $env:OPENAI_API_KEY = $plainKey
    $env:AGENT_ATELIER_MODEL = $model.Trim()
    $env:PYTHONPATH = "src"
    $plainKey = $null
    Remove-Variable secureKey -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "Starting the local preview. Real API calls require your explicit consent in Chapter 10." -ForegroundColor Cyan
    python -m agent_atelier.preview
}
finally {
    Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:AGENT_ATELIER_MODEL -ErrorAction SilentlyContinue
    $plainKey = $null
}
