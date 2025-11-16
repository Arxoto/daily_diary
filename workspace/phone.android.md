# 手机环境

## 小说

Legado https://github.com/gedoor/legado

书源

- 源仓库 https://www.yckceo.sbs/yuedu/shuyuan/index.html
- 大灰狼 https://github.com/shidahuilang/shuyuan
- 一程书源合集 https://raw.githubusercontent.com/yc-sy/yd/refs/heads/master/sy.json
- Yuedu https://github.com/XIU2/Yuedu

### TTS Kaldi

1. GitHub 官网
    - see https://github.com/k2-fsa/sherpa-onnx
1. 右侧连接
    - 跳转至 https://k2-fsa.github.io/sherpa/onnx/index.html
1. 左侧导航栏选择 TTS ，右侧列表中点击 vits
    - 跳转至 https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/vits.html
1. 因为需要下载 Android APKs ，点击 Hint
    - 跳转至 https://k2-fsa.github.io/sherpa/onnx/tts/apk.html
1. 因为要使用 TTS 引擎，点击 text-to-speech engine APKs
    - 跳转至 https://k2-fsa.github.io/sherpa/onnx/tts/apk-engine.html

推荐（流畅都不如手机原生的，虽然原生的有机械感，但至少发音标准）

- sherpa-onnx-1.12.14-arm64-v8a-zh-tts-engine-sherpa-onnx-vits-zh-ll.apk （选择 1 号男声，声音自然、发音标准，但延迟较大）
- sherpa-onnx-1.12.14-arm64-v8a-zh-tts-engine-matcha-icefall-zh-baker.apk （延迟基本没有，但发音不标准、标点停顿不自然）
- sherpa-onnx-1.12.14-arm64-v8a-zh_en-tts-engine-vits-melo-tts-zh_en.apk （延迟较小，发音尚可、标点停顿不自然）

设置

1. 系统-辅助-文字转语音-选择该引擎
1. 应用内点击朗读即可

#### 自部署（todo）

see https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/vits.html#csukuangfj-sherpa-onnx-vits-zh-ll-chinese-5-speakers

```shell

# 仅支持中文 仅生成音频文件
.\sherpa-onnx-v1.12.10-win-x64-static\bin\sherpa-onnx-offline-tts.exe `
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx `
  --vits-dict-dir=./sherpa-onnx-vits-zh-ll/dict `
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt `
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt `
  --output-filename=./sherpa-onnx-vits-zh-ll.wav `
  --sid=1 `
  --vits-length-scale=1.2 `
  --tts-rule-fsts=./sherpa-onnx-vits-zh-ll/new_heteronym.fst,./sherpa-onnx-vits-zh-ll/date.fst,./sherpa-onnx-vits-zh-ll/phone.fst,./sherpa-onnx-vits-zh-ll/number.fst `
  '“Are you ok”是雷军2015年4月小米在印度举行新品发布会时说的。他还说过“I am very happy to be in China.”，雷军事后在微博上表示「万万没想到，视频火速传到国内，全国人民都笑了」、「现在国际米粉越来越多，我的确应该把英文学好，不让大家失望！加油！」。小米的核心价值观是什么？答案是真诚热爱！小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。而最终……他完成了他的使命！有困难，请拨打110或者18601200909，或者仰天长啸3.141592653。'

# 同时支持中英文 生成音频文件同时播放
.\sherpa-onnx-v1.12.10-win-x64-static\bin\sherpa-onnx-offline-tts-play.exe `
  --vits-model=./vits-melo-tts-zh_en/model.onnx `
  --vits-dict-dir=./vits-melo-tts-zh_en/dict `
  --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt `
  --vits-tokens=./vits-melo-tts-zh_en/tokens.txt `
  --output-filename=./vits-melo-tts-zh_en.wav `
  --vits-length-scale=1.2 `
  --tts-rule-fsts=./sherpa-onnx-vits-zh-ll/new_heteronym.fst,./sherpa-onnx-vits-zh-ll/date.fst,./sherpa-onnx-vits-zh-ll/phone.fst,./sherpa-onnx-vits-zh-ll/number.fst `
  '“Are you ok”是雷军2015年4月小米在印度举行新品发布会时说的。他还说过“I am very happy to be in China.”，雷军事后在微博上表示「万万没想到，视频火速传到国内，全国人民都笑了」、「现在国际米粉越来越多，我的确应该把英文学好，不让大家失望！加油！」。小米的核心价值观是什么？答案是真诚热爱！小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。而最终……他完成了他的使命！有困难，请拨打110或者18601200909，或者仰天长啸3.141592653。'

```

#### TTS服务合集

https://www.cnblogs.com/HGNET/p/18437123

## Termux

### snapdrop

see <https://github.com/Arxoto/snapdrop_runner>

