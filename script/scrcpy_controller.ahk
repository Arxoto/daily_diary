#Requires AutoHotkey v2.0
#SingleInstance Force

; ============================================================
; 配置
; ============================================================
SCRCPY_WIN := "ahk_exe scrcpy.exe"

; 一行有几列按钮，赋值 1 或 8
COLS_IN_ROW := 1

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

guiClass := "+AlwaysOnTop"
if COLS_IN_ROW == 1 {
    guiClass .= " -MinimizeBox -MaximizeBox"
}
MyGui := Gui(guiClass, "scrcpy 控制面板")
MyGui.SetFont("s10", "Segoe UI")

; 系统快捷键
shortcuts := [
    ["解锁", "!m"],
    ["电源键", "!p"],
    ["关闭显示", "!o"],
    ["APPS", "!s"],
    ["HOME", "!h"],
    ["BACK", "!b"],
    ["复制", "!c"],
    ["粘贴", "!v"],
    ["音量+", "{Alt down}{Up}{Alt up}"],
    ["音量-", "{Alt down}{Down}{Alt up}"],
    ["向左旋转", "{Alt down}{Left}{Alt up}"],
    ["向右旋转", "{Alt down}{Right}{Alt up}"],
    ["水平翻转", "{Alt down}{Shift down}{Left}{Shift up}{Alt up}"],
    ["垂直翻转", "{Alt down}{Shift down}{Up}{Shift up}{Alt up}"],
]

btnWidth := 120
btnHeight := 30
margin := 10

btnCount := 0

/**
 * 计算控件宽高和坐标
 * @returns {String} 控件选项
 */
genBtnPosition() {
    global btnCount
    col := Mod(btnCount, COLS_IN_ROW)
    row := (btnCount) // COLS_IN_ROW
    x := margin + col * (btnWidth + margin)
    y := margin + row * (btnHeight + margin)
    btnCount++
    return "w" btnWidth " h" btnHeight " x" x " y" y
}

; 标题栏宽度不够，不显示最小化和最大化按钮，手动添加
if COLS_IN_ROW == 1 {
    btn := MyGui.AddButton(genBtnPosition(), "【收起面板】")
    btn.OnEvent("Click", (*) => MyGui.Minimize())
}

for index, item in shortcuts {
    btn := MyGui.AddButton(genBtnPosition(), item[1])
    btn.OnEvent("Click", SendShortcut.Bind(item[2]))
}

; ============================================================
; 【阅读】热键
; ============================================================

readerHotkeyTextOn := "阅读热键已开启"
readerHotkeyTextOff := "阅读热键已关闭"
readerHotkeyBtn := MyGui.AddButton(
    genBtnPosition(),
    readerHotkeysEnabled ? readerHotkeyTextOn : readerHotkeyTextOff
)
readerHotkeyBtn.OnEvent("Click", ToggleHotkeys)
ToggleHotkeys(*) {
    global readerHotkeysEnabled
    readerHotkeysEnabled := !readerHotkeysEnabled
    readerHotkeyBtn.Text := readerHotkeysEnabled ? readerHotkeyTextOn : readerHotkeyTextOff
}

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

; ============================================================
; 窗口
; ============================================================

MyGui.OnEvent("Close", (*) => ExitApp())
MyGui.Show("AutoSize")