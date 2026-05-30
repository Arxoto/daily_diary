BEGIN {
    if (!output_split) {
        output_split = "__from__"
    }
}

{
    # 解析 csv 分隔符

    if (substr($0, 1, 1) == "\"") {
        the_line = substr($0, 2)
        split_by = "\",\""

        line_array_len = split(the_line, line_array, split_by)

        track_name = line_array[1]
        gsub(/""/, "\"", track_name)
        artist_name = line_array[2]
    } else {
        the_line = $0
        split_by = ","

        line_array_len = split(the_line, line_array, split_by)

        track_name = line_array[1]
        artist_name = line_array[2]
    }

    # 特殊处理

    will_print = 1
    if (track_name == "Landing Guy - Cover") {
        track_name = "Landing Guy"
        artist_name = "刘昊霖"
    } else if (track_name == "女儿情（《西游记女儿国》电影推广曲）") {
        track_name = "女儿情"
        artist_name = "吴静"
    } else if (track_name == "女兒情") {
        will_print = 0
    }

    # 打印

    if (will_print) {
        print track_name, output_split, artist_name
    }   
}

END {
    track_name = "七剑战歌(Seven Swords' Victory)"
    artist_name = "川井憲次"
    print track_name, output_split, artist_name
}