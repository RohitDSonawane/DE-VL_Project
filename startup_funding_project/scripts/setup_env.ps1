# PowerShell script to create a virtual environment and install dependencies
$venvName = ".venv"
if (-Not (Test-Path $venvName)) {
    python -m venv $venvName
}
Write-Host "Activating virtual environment..."
.\$venvName\Scripts\Activate.ps1
Write-Host "Installing requirements..."
pip install -r "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)\..\requirements.txt"
Write-Host "Done. To deactivate, run: deactivate"
