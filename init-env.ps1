# run `. .\init-env.ps1` in powershell terminal

. .\.venv\Scripts\Activate.ps1
python -V

fnm env | Out-String | Invoke-Expression
fnm use
