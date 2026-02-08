
import fontforge # type: ignore
import os

# ================= 配置区域 =================
NEW_COPYRIGHT = "Created by Wom"      # 版权信息
NEW_DESIGNER = "Wom"               # 设计者名称
NEW_URL = "https://wom.com"     # 个人主页或项目主页
NEW_VERSION = "1.000"                    # 版本号

# 自定义字体家族名称
NEW_FAMILY_NAME = "WomPunctuationFixed"
# 基础全角宽度（对应2个西文字符，通常是 1000 ）
FULL_WIDTH = 1000 
# 双倍全角宽度（对应4个西文字符，用于破折号和省略号，通常是 2000 ）
DOUBLE_FULL_WIDTH = 2000

# 需要处理的字符及其对应的 Unicode 码点
# 1. 设置为全角的标点 (1000 unit)
TARGETS_FULL = {
    0x2018: "quoteleft",      # ‘
    0x2019: "quoteright",     # ’
    0x201C: "quotedblleft",   # “
    0x201D: "quotedblright",  # ”
    0x00B7: "periodcentered", # · (间隔号)
}

# 2. 设置为双倍全角的标点 (2000 unit)
TARGETS_DOUBLE = {
    0x2014: "emdash",         # — (破折号)
    0x2026: "ellipsis",       # … (省略号)
}
# ===========================================

def process_font(file_path):
    print(f"\n正在处理: {file_path}")
    try:
        font = fontforge.open(file_path)
    except:
        print(f"无法打开文件: {file_path}")
        return
    
    # 彻底禁用垂直指标，这是解决那堆 .vert 报错的关键（仅用于水平排版）
    font.hasvmetrics = False
    # 移除所有的 OpenType 查找表 (Lookups)
    # 这一步能解决你遇到的 "unused glyph" 报错，让补丁字体变“干净”
    for lookup in font.gsub_lookups + font.gpos_lookups:
        font.removeLookup(lookup)
    # 彻底清除所有的 Unicode 变体表 (Variation Selectors)
    # 这是解决 Format 14 报错的关键
    # 遍历所有字形，不仅清除 altuni，还要清除变体数据
    for glyph in font.glyphs():
        glyph.altuni = None
    # 手动清理变体表数据结构
    # 这一步能从底层抹除 Format 14 表的引用
    try:
        # 有些版本的 FontForge 支持直接操作非标准子表
        # 强制重置编码为基础 Unicode (BMP)，这会丢弃变体映射
        font.reencode('iso10646-1') 
    except:
        font.reencode('UnicodeFull')

    # ========= 核心逻辑开始 =========
    # 获取样式的后缀，例如 Regular, Bold, SemiBold
    style_weight = font.weight
    style_italic = "Italic" if font.italicangle != 0 else ""
    # 注意： fontname (PostScript Name) 不允许有空格
    style_name = style_weight.replace(' ', '')
    if style_italic:
        style_name = style_name + "-" + style_italic
    print(f"style: {style_weight} {style_italic}")
    
    # 重新设置字体信息
    font.familyname = NEW_FAMILY_NAME
    font.fontname = f"{NEW_FAMILY_NAME}-{style_name}"
    font.fullname = f"{NEW_FAMILY_NAME} {style_weight} {style_italic}".strip()

    # 保留需要的字符，删除其他所有字符
    keep_codes = list(TARGETS_FULL.keys()) + list(TARGETS_DOUBLE.keys())

    # 反向删除：先选中所有，然后取消选中我们要保留的，最后删除
    font.selection.all()
    for code in keep_codes:
        if code in font:
            font.selection.select(("less", "unicode"), code)
    font.clear() # 删除选中的所有其他字符

    # 处理全角标点
    for code in TARGETS_FULL:
        if code in font:
            font[code].width = FULL_WIDTH
            print(f"  - 已设为全角: {hex(code)}")

    # 处理双倍全角标点（破折号、省略号占4个西文位）
    for code in TARGETS_DOUBLE:
        if code in font:
            font[code].width = DOUBLE_FULL_WIDTH
            print(f"  - 已设为双全角: {hex(code)}")
    # ========= 核心逻辑结束 =========

    # 修改元数据
    
    # 修改版权与元数据
    font.copyright = NEW_COPYRIGHT
    font.version = NEW_VERSION
    
    # 修改具体的 Naming 字段 (SFNT 表)  FontForge 里打开字体，进入 Element -> Font Info -> TTF Names
    # 7: Trademark, 8: Manufacturer, 9: Designer, 12: URL
    # 定义我们需要强制覆盖的 ID
    name_entries = [
        (0, NEW_COPYRIGHT), # 0: Copyright
        (1, NEW_FAMILY_NAME), # 1: Family
        (2, style_name), # 2: Subfamily (Style)
        (3, f"{NEW_FAMILY_NAME}-{style_name}-{NEW_VERSION}"), # 3: UniqueID
        (4, font.fullname), # 4: Full Name
        (6, font.fontname), # 6: PostScript
        (16, NEW_FAMILY_NAME), # Preferred Family
        (17, style_name),    # Preferred Subfamily
        ('Version', NEW_VERSION),
        ('Manufacturer', NEW_DESIGNER),
        ('Designer URL', NEW_URL),
        ('Vendor URL', NEW_URL),
    ]

    for name_id, name_str in name_entries:
        # 同时修改 English (US) 和 English (UK) 等常见区域，确保 Windows 命中
        font.appendSFNTName('English (US)', name_id, name_str)
        # 有些字体包含中文元数据，Windows 会优先读取中文，所以建议也覆盖掉
        font.appendSFNTName('Chinese (PRC)', name_id, name_str)

    # 导出新文件
    old_filename: str = os.path.basename(file_path)
    new_filename_ext = old_filename.split('.')[-1]
    new_filename = f"{NEW_FAMILY_NAME}-{style_name}.{new_filename_ext}"
    font.generate(new_filename)
    font.close()
    print(f"完成! 已保存为: {new_filename}\n")

# 运行处理逻辑
if __name__ == "__main__":
    files = [f for f in os.listdir('.') if f.endswith(('.ttf', '.otf'))]
    for f in files:
        process_font(f)
