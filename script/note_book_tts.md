see also [TTS Kaldi](/workspace/phone.android.md)

```powershell

cd ./novel_path/tts

$files = Get-ChildItem -Path "../parts" -Filter "novel_part*.txt" | Select-Object -First 2 # | Get-Content
foreach ($file in $files) {
    $inputname = $file.Name
    $outputname = "$inputname.wav"
    Write-Output "$outputname"

    $content = (Get-Content -Path $file.FullName -TotalCount 3) -join "`n"
    # $content = Get-Content -Path $file.FullName -Raw
    Write-Output "$content"
}

$files = Get-ChildItem -Path "../parts" -Filter "novel_part*.txt"
foreach ($file in $files) {
    $inputname = $file.Name
    $outputname = "$inputname.wav"

    # $content = (Get-Content -Path $file.FullName -TotalCount 3) -join "`n"
    $content = Get-Content -Path $file.FullName -Raw
    D:\develop\code\tts\sherpa-onnx-v1.12.10-win-x64-static\bin\sherpa-onnx-offline-tts.exe `
        --vits-model=D:\develop\code\tts/sherpa-onnx-vits-zh-ll/model.onnx `
        --vits-dict-dir=D:\develop\code\tts/sherpa-onnx-vits-zh-ll/dict `
        --vits-lexicon=D:\develop\code\tts/sherpa-onnx-vits-zh-ll/lexicon.txt `
        --vits-tokens=D:\develop\code\tts/sherpa-onnx-vits-zh-ll/tokens.txt `
        --output-filename="$outputname" `
        --sid=1 `
        --vits-length-scale=1.2 `
        --tts-rule-fsts=D:\develop\code\tts/sherpa-onnx-vits-zh-ll/new_heteronym.fst,D:\develop\code\tts/sherpa-onnx-vits-zh-ll/date.fst,D:\develop\code\tts/sherpa-onnx-vits-zh-ll/phone.fst,D:\develop\code\tts/sherpa-onnx-vits-zh-ll/number.fst `
        "$content"
}

```