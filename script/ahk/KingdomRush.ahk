#Requires AutoHotkey v2.0
#SingleInstance Force
; 若无效，尝试以管理员身份运行本脚本

KR_VERSION_CONFIG := [
    ["ahk_exe Kingdom Rush.exe", "版本：初代", 0.93, 0.96],
    ["ahk_exe Kingdom Rush Frontiers.exe", "版本：前线", 0.96, 0.96],
    ["ahk_exe Kingdom Rush Origins.exe", "版本：起源", 0.96, 0.96],
]

g := Gui("+AlwaysOnTop -MinimizeBox", "KR 点击器")
g.SetFont("s12")
g.OnEvent("Close", (*) => ExitApp())

targetVersion := 1
btnVersion := g.Add("Button", "w200 h44", KR_VERSION_CONFIG[targetVersion][2])
btnVersion.OnEvent("Click", ToggleVersion)

ToggleVersion(*) {
    global targetVersion
    tmp := targetVersion + 1
    if tmp > KR_VERSION_CONFIG.Length {
        tmp := 1
    }
    targetVersion := tmp
    btnVersion.Text := KR_VERSION_CONFIG[targetVersion][2]
}

btn_text_on := "自动出怪：[已打开]"
btn_text_off := "自动出怪：[已关闭]"
switchOn := false
btnSwitch := g.Add("Button", "w200 h44", switchOn ? btn_text_on : btn_text_off)
btnSwitch.OnEvent("Click", ToggleSwitch)

ToggleSwitch(*) {
    global switchOn
    switchOn := !switchOn
    if switchOn {
        btnSwitch.Text := btn_text_on
        DoClick()
        SetTimer(DoClick, 1000)
    } else {
        btnSwitch.Text := btn_text_off
        SetTimer(DoClick, 0)
    }
}

DoClick() {
    targetExe := KR_VERSION_CONFIG[targetVersion][1]
    hwnd := WinExist(targetExe)
    if !hwnd
        return

    try
        WinGetClientPos(, , &cw, &ch, "ahk_id " hwnd)
    catch
        return

    x := Round(cw * KR_VERSION_CONFIG[targetVersion][3])
    y := Round(ch * KR_VERSION_CONFIG[targetVersion][4])

    lParam := (y << 16) | x

    ; WM_MOUSEMOVE
    PostMessage(0x200, 0, lParam, , "ahk_id " hwnd)
    ; WM_LBUTTONDOWN, wParam = MK_LBUTTON(0x1)
    PostMessage(0x201, 0x1, lParam, , "ahk_id " hwnd)
    ; WM_LBUTTONUP
    PostMessage(0x202, 0, lParam, , "ahk_id " hwnd)
}

g.Show()