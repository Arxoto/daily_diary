#Requires AutoHotkey v2.0
#SingleInstance Force

; ============================================================
; 配置
; ============================================================
SCRCPY_WIN := "ahk_exe scrcpy.exe"

; 快捷键开关（由 GUI 复选框控制，默认开启以保持原脚本行为）
readerHotkeysEnabled := false

; ============================================================
; 通用函数
; ============================================================

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

; 点击，相对坐标，在 scrcpy 客户区
ClickClient(xRatio, yRatio) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(, , &cw, &ch, SCRCPY_WIN)
    MouseClick("Left", cw * xRatio, ch * yRatio)
    MouseMove(cw - 1, ch * 0.5, 0)
}

; 横向滑动，相对坐标，在 scrcpy 客户区
SwipeHorizontal(fromRatio, toRatio) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(, , &cw, &ch, SCRCPY_WIN)

    posY := Round(ch * 0.5)
    fromX := Round(cw * fromRatio)
    toX := Round(cw * toRatio)

    ; 手动实现 MouseClickDrag 在打开导航栏的时候也能正常翻页
    MouseMove(fromX, posY, 0)
    MouseClick("Left", , , 1, 0, "D")
    try {
        loopCount := 50
        deltaX := toX - fromX
        loop loopCount {
            currentX := Round(fromX + deltaX / loopCount * A_Index)
            MouseMove(currentX, posY, 0)
        }
    } finally {
        MouseMove(toX, posY, 0)
        MouseClick("Left", , , 1, 0, "U")
    }

    ; MouseClickDrag("Left", fromX, posY, toX, posY)
    MouseMove(cw - 1, posY, 0)
}

; ============================================================
; GUI
; ============================================================

; 系统快捷键
shortcuts := [
    ["BACK", "!b"],
    ["HOME", "!h"],
    ["概览屏幕", "!s"],
    ["关闭显示", "!o"],
    ["电源键", "!p"],
    ["解锁", "!m"],
    ["复制", "!c"],
    ["粘贴", "!v"],
    ["音量+", "{Alt down}{Up}{Alt up}"],
    ["音量-", "{Alt down}{Down}{Alt up}"],
    ["向左旋转", "{Alt down}{Left}{Alt up}"],
    ["向右旋转", "{Alt down}{Right}{Alt up}"],
    ["水平翻转", "{Alt down}{Shift down}{Left}{Shift up}{Alt up}"],
    ["垂直翻转", "{Alt down}{Shift down}{Up}{Shift up}{Alt up}"],
]

MyGui := Gui("+AlwaysOnTop -MinimizeBox -MaximizeBox", "scrcpy 控制面板")
MyGui.SetFont("s10", "Segoe UI")

; 每行几个按钮
cols := 8
btnWidth := 120
btnHeight := 30
margin := 10

/**
 * 计算控件宽高和坐标
 * @param {Integer} index 编号
 * @returns {String} 控件选项
 */
calcBtnPosition(index) {
    col := Mod(index - 1, cols)
    row := (index - 1) // cols
    x := margin + col * (btnWidth + margin)
    y := margin + row * (btnHeight + margin)
    return "w" btnWidth " h" btnHeight " x" x " y" y
}

for index, item in shortcuts {
    btn := MyGui.AddButton(calcBtnPosition(index), item[1])
    btn.OnEvent("Click", SendShortcut.Bind(item[2]))
}

readerHotkeyTextOn := "阅读热键已开启"
readerHotkeyTextOff := "阅读热键已关闭"
readerHotkeyBtn := MyGui.AddButton(
    calcBtnPosition(shortcuts.Length + 1),
    readerHotkeysEnabled ? readerHotkeyTextOn : readerHotkeyTextOff
)
readerHotkeyBtn.OnEvent("Click", ToggleHotkeys)
ToggleHotkeys(*) {
    global readerHotkeysEnabled
    readerHotkeysEnabled := !readerHotkeysEnabled
    readerHotkeyBtn.Text := readerHotkeysEnabled ? readerHotkeyTextOn : readerHotkeyTextOff
}

MyGui.Show("AutoSize")

; ============================================================
; 【阅读】热键
; ============================================================

#HotIf WinActive(SCRCPY_WIN) && readerHotkeysEnabled

; 上方向键 返回
Up:: Send("!b")

; 下方向键 点击书架第一本书
Down:: ClickClient(0.17, 0.3)

; 右方向键 从右向左拖拽
Right:: SwipeHorizontal(0.8, 0.2)

; 左方向键 从左向右拖拽
Left:: SwipeHorizontal(0.2, 0.8)

#HotIf