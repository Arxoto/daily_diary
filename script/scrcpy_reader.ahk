#Requires AutoHotkey v2.0

#HotIf WinActive("ahk_exe scrcpy.exe")

; 上方向键 返回（模拟 scrcpy 的 MOD+b，默认 MOD 是左 Alt）
Up:: Send("!b")

; 下方向键 点击书架第一本书
Down:: {
    CoordMode("Mouse", "Client")
    WinGetClientPos(&cx, &cy, &cw, &ch, "ahk_exe scrcpy.exe")
    MouseClick("Left", cw * 0.17, ch * 0.24)
    MouseMove(cw - 1, ch * 0.5, 0)
}

; 右方向键 从右向左拖拽
Right:: SwipeHorizontal(0.8, 0.5)

; 左方向键 从左向右拖拽
Left:: SwipeHorizontal(0.5, 0.8)

#HotIf


; ---------- 辅助函数 ----------

; 在 scrcpy 客户区内做水平拖拽
;   fromRatio / toRatio：起始/结束点的横向比例（0.0 ~ 1.0），纵向固定在 50%
;   durationMs：拖拽耗时，太小可能被识别为点击，太大动作会慢
SwipeHorizontal(fromRatio, toRatio, durationMs := 10) {
    CoordMode("Mouse", "Client")
    WinGetClientPos(&cx, &cy, &cw, &ch, "ahk_exe scrcpy.exe")

    posY := ch * 0.5

    MouseClickDrag("Left", cw * fromRatio, posY, cw * toRatio, posY, durationMs)
    MouseMove(cw - 1, posY, 0)
}
