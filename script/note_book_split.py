import re
import os
from typing import List


def split_novel_by_chapters(
    input_file,
    chapter_pattern_match,
    output_prefix="novel_part",
    chapters_per_file=10,
    folder_path=".",
):
    """
    将小说文本按章节分割，每指定数量的章节保存为一个新文件

    参数:
    input_file: 输入的大文本文件路径
    output_prefix: 输出文件前缀
    chapters_per_file: 每个输出文件包含的章节数量
    """
    # 当前正在处理的内容
    current_context: List[str] = []
    # 当前分区的开头章节
    begin_chapter_count = 0
    # 当前分组已收集的章节数
    current_chapter_count = 0

    def process_chapter_group():
        nonlocal current_context
        nonlocal begin_chapter_count
        nonlocal current_chapter_count

        output_file_path = os.path.join(
            folder_path,
            f"{output_prefix}.{begin_chapter_count}-{current_chapter_count}.txt",
        )
        write_novel_part(current_context, output_file_path)
        # 重置
        current_context = []
        begin_chapter_count = current_chapter_count

    # 正则模式：匹配行首的章节标题 如 r"^第\d+章"
    pattern = re.compile(chapter_pattern_match)

    input_file_path = os.path.join(folder_path, input_file)
    print("目录", folder_path)
    print("文件", input_file)
    print("路径", input_file_path)
    print("===========================")
    with open(input_file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 检查是否为章节标题
            if pattern.match(line):
                # 章节标题：章节数加一
                current_chapter_count += 1
                # 检查是否达到分组大小
                if current_chapter_count % chapters_per_file == 0:
                    # 满足分组要求，写入文件
                    process_chapter_group()
            # 无论如何都将每行内容推入
            current_context.append(line)

    # 处理最后一个未满的分组
    if current_context:
        process_chapter_group()


def write_novel_part(novel_part: List[str], output_file):
    """将章节组写入文件"""
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入当前章节的所有行（包含换行符）
        f.writelines(novel_part)
    print(f"已保存: {output_file}")


def test():
    ACTION_NAME = __file__.split(os.sep)[-1].split(".")[0] + ".example"
    TEST_WORKSPACE = "./1test_workspace"

    # 配置参数
    INPUT_FILE = f"{ACTION_NAME}.txt"

    # 生成测试文件
    with open(os.path.join(TEST_WORKSPACE, INPUT_FILE), "w", encoding="utf-8") as f:
        f.writelines(["\n", "\n", "《xxxxxx》\n", "\n", "\n"])
        for i in range(1, 8):
            f.writelines(["\n", f"第{i}章 xxx\n", "1\n", "2\n", "3\n"])

    # 章节标题的正则匹配
    CHAPTER_PATTERN_MATCH = r"^第\d+章"

    # 执行分割
    split_novel_by_chapters(
        INPUT_FILE,
        CHAPTER_PATTERN_MATCH,
        output_prefix=ACTION_NAME,
        chapters_per_file=3,
        folder_path=TEST_WORKSPACE,
    )


def main():
    # 配置参数
    INPUT_FILE = "big_novel.txt"

    # 章节标题的正则匹配
    # 检查匹配章节开头是否正确 `grep -E '^第[[:digit:]]+章' ./xxxx.txt | less -N`
    CHAPTER_PATTERN_MATCH = r"^第\d+章"

    # 执行分割
    split_novel_by_chapters(INPUT_FILE, CHAPTER_PATTERN_MATCH)


if __name__ == "__main__":
    test()

    # main()

    # split_novel_by_chapters(
    #     r"xxx.txt",
    #     r"^第\d+章",
    #     folder_path=r"D:\book",
    # )
