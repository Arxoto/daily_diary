#Requires AutoHotkey v2.0
#SingleInstance Force
; 若无效，尝试以管理员身份运行本脚本

targetExe := "ahk_exe Kingdom Rush Origins.exe"

g := Gui("+AlwaysOnTop -MinimizeBox", "KR 点击器")
g.SetFont("s12")
g.OnEvent("Close", (*) => ExitApp())

btn_text_on := "自动出怪：[已打开]"
btn_text_off := "自动出怪：[已关闭]"
btn := g.Add("Button", "w220 h44", btn_text_off)
btn.OnEvent("Click", Toggle)
g.Show()

Toggle(*) {
    static on := false
    on := !on
    if on {
        btn.Text := btn_text_on
        DoClick()
        SetTimer(DoClick, 1000)
    } else {
        btn.Text := btn_text_off
        SetTimer(DoClick, 0)
    }
}

DoClick() {
    hwnd := WinExist(targetExe)
    if !hwnd
        return

    try
        WinGetClientPos(, , &cw, &ch, "ahk_id " hwnd)
    catch
        return

    x := Round(cw * 0.96)
    y := Round(ch * 0.96)

    lParam := (y << 16) | x

    ; WM_MOUSEMOVE  —— 部分程序靠它更新"当前鼠标位置"
    PostMessage(0x200, 0, lParam, , "ahk_id " hwnd)
    ; WM_LBUTTONDOWN —— wParam = MK_LBUTTON(0x1) 表示左键按下
    PostMessage(0x201, 0x1, lParam, , "ahk_id " hwnd)
    ; WM_LBUTTONUP   —— wParam = 0
    PostMessage(0x202, 0, lParam, , "ahk_id " hwnd)
}
