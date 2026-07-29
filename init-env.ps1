# run `. .\init-env.ps1` in powershell terminal

. "$PSScriptRoot\.venv\Scripts\Activate.ps1"
python -V

Push-Location $PSScriptRoot
fnm env | Out-String | Invoke-Expression
fnm use
Pop-Location
