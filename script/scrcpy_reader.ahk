#Requires AutoHotkey v2.0

; === 通用函数 ===

; 点击，相对坐标，在 scrcpy 客户区
ClickClient(xRatio, yRatio) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(&cx, &cy, &cw, &ch, "ahk_exe scrcpy.exe")
    MouseClick("Left", cw * xRatio, ch * yRatio)
    MouseMove(cw - 1, ch * 0.5, 0)
}

; 横向滑动，相对坐标，在 scrcpy 客户区
SwipeHorizontal(fromRatio, toRatio, durationMs := 10) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(&cx, &cy, &cw, &ch, "ahk_exe scrcpy.exe")

    posY := ch * 0.5

    MouseClickDrag("Left", cw * fromRatio, posY, cw * toRatio, posY, durationMs)
    MouseMove(cw - 1, posY, 0)
}

; === 热键 ===

#HotIf WinActive("ahk_exe scrcpy.exe")

; 空格 点击中心位置
Space:: ClickClient(0.5, 0.5)

; 上方向键 返回（模拟 scrcpy 的 MOD+b，默认 MOD 是左 Alt）
Up:: Send("!b")

; 下方向键 点击书架第一本书
Down:: {
    ClickClient(0.17, 0.3)
    Sleep 1100
    ClickClient(0.5, 0.5)
}

; 右方向键 从右向左拖拽
Right:: SwipeHorizontal(0.8, 0.5)

; 左方向键 从左向右拖拽
Left:: SwipeHorizontal(0.5, 0.8)

#HotIf