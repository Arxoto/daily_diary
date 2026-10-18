#Requires AutoHotkey v2.0
#SingleInstance Force

targetExe := "ahk_exe scrcpy.exe"

; === 通用函数 ===

; 点击，相对坐标，在 scrcpy 客户区
ClickClient(xRatio, yRatio) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(, , &cw, &ch, targetExe)
    MouseClick("Left", cw * xRatio, ch * yRatio)
    MouseMove(cw - 1, ch * 0.5, 0)
}

; 横向滑动，相对坐标，在 scrcpy 客户区
SwipeHorizontal(fromRatio, toRatio) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(, , &cw, &ch, targetExe)

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

; === 热键 ===

#HotIf WinActive(targetExe)

; 空格 点击中心位置
Space:: ClickClient(0.5, 0.5)

; 上方向键 返回（模拟 scrcpy 的 MOD+b，默认 MOD 是左 Alt）
Up:: Send("!b")

; 下方向键 点击书架第一本书
Down:: {
    ClickClient(0.17, 0.3)
}

; 右方向键 从右向左拖拽
Right:: SwipeHorizontal(0.8, 0.2)

; 左方向键 从左向右拖拽
Left:: SwipeHorizontal(0.2, 0.8)

#HotIf