#Requires AutoHotkey v2.0
#SingleInstance Force

MOD_KEY := "Alt"
SCRCPY_WIN := "ahk_exe scrcpy.exe"

BuildKeys(modKey, key, shift := false) {
    str := "{" . modKey . " down}"
    if (shift)
        str .= "{Shift down}"
    str .= "{" . key . "}"
    if (shift)
        str .= "{Shift up}"
    str .= "{" . modKey . " up}"
    return str
}

SendShortcut(keys, *) {
    if WinExist(SCRCPY_WIN) {
        WinActivate(SCRCPY_WIN)
        if WinWaitActive(SCRCPY_WIN, , 1) {
            Send(keys)
        }
    } else {
        ToolTip("未找到 scrcpy 窗口")
        SetTimer(() => ToolTip(), -1500)
    }
}

shortcuts := [
    {label: "BACK", keys: BuildKeys(MOD_KEY, "b")},
    {label: "HOME", keys: BuildKeys(MOD_KEY, "h")},
    {label: "概览屏幕", keys: BuildKeys(MOD_KEY, "s")},
    {label: "关闭显示", keys: BuildKeys(MOD_KEY, "o")},
    {label: "电源键", keys: BuildKeys(MOD_KEY, "p")},
    {label: "解锁", keys: BuildKeys(MOD_KEY, "m")},
    {label: "音量+", keys: BuildKeys(MOD_KEY, "Up")},
    {label: "音量-", keys: BuildKeys(MOD_KEY, "Down")},
    {label: "复制", keys: BuildKeys(MOD_KEY, "c")},
    {label: "粘贴", keys: BuildKeys(MOD_KEY, "v")},
    {label: "向左旋转", keys: BuildKeys(MOD_KEY, "Left")},
    {label: "向右旋转", keys: BuildKeys(MOD_KEY, "Right")},
    {label: "水平翻转", keys: BuildKeys(MOD_KEY, "Left", true)},
    {label: "垂直翻转", keys: BuildKeys(MOD_KEY, "Up", true)},
]

MyGui := Gui("+AlwaysOnTop -MinimizeBox -MaximizeBox", "scrcpy 控制")
MyGui.SetFont("s10", "Segoe UI")

; 每行几个按钮
cols := 8
btnWidth := 120
btnHeight := 30
margin := 10

for index, item in shortcuts {
    col := Mod(index - 1, cols)
    row := (index - 1) // cols
    x := margin + col * (btnWidth + margin)
    y := margin + row * (btnHeight + margin)
    btn := MyGui.AddButton("w" btnWidth " h" btnHeight " x" x " y" y, item.label)
    btn.OnEvent("Click", SendShortcut.Bind(item.keys))
}

MyGui.Show("AutoSize")