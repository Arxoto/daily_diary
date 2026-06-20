import os


def parse_song_id(line: str) -> str:
    line = line.strip()
    if line.endswith('"'):
        last_index = len(line) - 1
        second_last_index = line.rfind('"', 0, last_index)
        song_id = line[second_last_index + 1 : last_index]
        return song_id
    else:
        index = line.rfind(",")
        song_id = line[index + 1]
        return song_id


def main():
    script_path = os.path.abspath(__file__)
    the_dir = os.path.dirname(script_path)

    songs_all: set[str] = set()
    songs_ccc: set[str] = set()
    songs_eee: set[str] = set()
    with open(os.path.join(the_dir, "./all.csv"), mode="r", encoding="utf-8") as all_file:
        for line in all_file:
            song_id = parse_song_id(line)
            if song_id in songs_all:
                print("song_id already in all:", song_id)
            else:
                songs_all.add(song_id)
    with open(os.path.join(the_dir, "./ccc.csv"), mode="r", encoding="utf-8") as all_file:
        for line in all_file:
            song_id = parse_song_id(line)
            if song_id in songs_ccc:
                print("song_id already in ccc:", song_id)
            else:
                songs_ccc.add(song_id)
    with open(os.path.join(the_dir, "./eee.csv"), mode="r", encoding="utf-8") as all_file:
        for line in all_file:
            song_id = parse_song_id(line)
            if song_id in songs_eee:
                print("song_id already in eee:", song_id)
            else:
                songs_eee.add(song_id)
    
    # print(songs_all)
    # print(songs_ccc)
    # print(songs_eee)

    for song_id in songs_all:
        if song_id not in songs_ccc and song_id not in songs_eee:
            print("song_id not in ccc or eee:", song_id)

    for song_id in songs_ccc:
        if song_id not in songs_all:
            print("song_id (ccc) not in all:", song_id)
    for song_id in songs_eee:
        if song_id not in songs_all:
            print("song_id (eee) not in all:", song_id)


if __name__ == "__main__":
    main()
