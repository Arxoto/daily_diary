/**
 * @typedef {{id: number, name: string, artists: string[]}} MusicInfo
 */


/**
 * 网易云搜索音乐，注意跨域限制必须在 网易云 页面使用
 * @param {string} keyword
 * @returns {Promise<{musicInfos: MusicInfo[], retry: boolean}>}
 */
const searchMusicForNetease = async (keyword) => {
    const response = await fetch(`https://music.163.com/api/search/get?s=${encodeURIComponent(keyword)}&type=1&limit=5`, {
        method: 'GET',
        "referrer": "https://music.163.com/",
    });
    const data = await response.json();

    // 操作频繁，请稍候再试
    if (data.code === 405) return { musicInfos: [], retry: true };

    const musicInfos = data.result?.songs?.map((song) => ({
        id: song.id,
        name: song.name,
        artists: song.artists?.map((ar) => ar.name) || [],
    })) || [];
    return { musicInfos: musicInfos, retry: false };
}

/**
 * 添加歌曲到网易云歌单，注意跨域限制必须在 网易云 页面使用
 * @param {number} playListId
 * @param {number} musicId
 * @returns {Promise<{code: number, message: string, success: boolean, retry: boolean}>}
 */
const addToPlayListForNetease = async (playListId, musicId) => {
    const response = await fetch('https://music.163.com/api/playlist/manipulate/tracks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `op=add&pid=${playListId}&trackIds=%5B${musicId}%5D&imme=true`,
    });
    const data = await response.json();
    if (data.code === 200) return { code: data.code, message: '添加成功', success: true, retry: false };
    if (data.code === 502) return { code: data.code, message: '歌曲已存在', success: true, retry: false };
    if (data.code === 512) return { code: data.code, message: '未付费歌曲无法收藏', success: false, retry: false };
    if (data.code === 401) return { code: data.code, message: '下架歌曲无法收藏', success: false, retry: false };
    throw new Error(`error_code: ${data.code}, error_msg: ${data.message}`);
}


/**
 * 英文单词粗略匹配
 * @param {string} target 
 * @param {string} source 
 */
const wordMatched = (target, source) => {
    let targetParts = target.split(' ');
    let sourceParts = source.split(' ');
    return targetParts.some(tp => sourceParts.includes(tp));
}

/**
 * 模糊匹配
 * @param {string} target 
 * @param {string} source 
 */
const fuzzyMatched = (target, source) => {
    let targetChars = [...target];
    let sourceChars = [...source];
    let score = 0;
    for (const ch of sourceChars) {
        for (let i = 0; i < targetChars.length; i++) {
            const tc = targetChars[i];
            if (tc === ch) {
                source++;
                targetChars[i] = '';
            }
        }
    }
    return score >= (target.length < source.length ? target.length : source.length) / 2;
}

/**
 * 最佳匹配
 * @param {MusicInfo[]} musicList 
 * @param {string} track_name
 * @param {string} artist_name
 * @return {MusicInfo|null}
 */
const findBestMatchMusic = (musicList, track_name, artist_name) => {
    if (musicList.length === 0) return null;

    let scoreList = musicList.map(m => 0);

    for (let i = 0; i < musicList.length; i++) {
        const music = musicList[i];

        if (music.name === track_name) {
            // 歌名完全匹配
            scoreList[i] += 100;
        } else if (music.name.includes(track_name) || track_name.includes(music.name)) {
            // 歌名部分包含
            scoreList[i] += 80;
        } else if (fuzzyMatched(music.name, track_name)) {
            // 歌名部分匹配
            scoreList[i] += 60;
        }

        if (music.artists.includes(artist_name)) {
            // 歌手包含
            scoreList[i] += 45;
        } else if (wordMatched(music.artists.join(' '), artist_name)) {
            // 歌手部分匹配 会把姓和名分开匹配
            scoreList[i] += 35;
        }
    }

    let currentScore = -1;
    let result = null;

    for (let i = 0; i < scoreList.length; i++) {
        const score = scoreList[i];

        if (score > currentScore) {
            currentScore = score;
            result = musicList[i];
        }
    }

    if (currentScore === 145) {
        console.success()
        console.log(`十分匹配!!! ${track_name} ${artist_name} --> ${result.name} ${result.artists}`)
    } else if (currentScore > 120) {
        console.log(`大概率匹配! ${track_name} ${artist_name} --> ${result.name} ${result.artists}`)
    } else {
        console.warn(`可能不太匹配... ${track_name} ${artist_name} --> ${result.name} ${result.artists}`)
    }
    return result;
}

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const playListId = 0;
const musicDataStr = ``;
const reallyDo = true;

// main
(async () => {
    if (location.hostname !== 'music.163.com') {
        throw new Error('need run this js-script in console of https://music.163.com/#/my/');
    }
    if (playListId === 0) {
        throw new Error('open https://music.163.com/#/my/ to get playListId in url');
    }
    if (!musicDataStr) {
        throw new Error('set the musicDataStr first, like "track_name __from__ artist_name"');
    }

    /** @type {string[][]} */
    const musics = musicDataStr.split('\n').filter(line => line).map(line => line.split(' __from__ '));

    for (const music of musics) {
        for (let i = 0; i < 10; i++) {
            let musicInfoRes = await searchMusicForNetease(music.join(' '));
            if (musicInfoRes.retry) {
                await sleep(1000);
                continue;
            }

            let bestMusicInfo = findBestMatchMusic(musicInfoRes.musicInfos, music[0], music[1]);

            if (reallyDo) {
                if (bestMusicInfo) {
                    console.log(`will add music, track_name: ${bestMusicInfo.name}, artist_name: ${bestMusicInfo.artists}`);
                    let addedRes = await addToPlayListForNetease(playListId, bestMusicInfo.id);
                    if (!addedRes.success) {
                        console.warn(`add failed by ${addedRes.message}`);
                    }
                    if (addedRes.retry) {
                        continue;
                    }
                } else {
                    console.warn(`music not found: ${music}`);
                }
            } else {
                if (bestMusicInfo) {
                    console.log(`will add music, track_name: ${bestMusicInfo.name}, artist_name: ${bestMusicInfo.artists} <-- ${music}`);
                } else {
                    console.warn(`music not found: ${music}`);
                }
            }
            break;
        }
    }
    console.log('all done');
})();
