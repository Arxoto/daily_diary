# 运行时版本管理器

## python

python 和依赖都使用 uv 管理

环境创建

```powershell
uv init
uv sync # 安装依赖

python -V
```

## nodejs

nodejs 版本使用 fnm 管理，包依赖管理器使用 pnpm(corepack) 控制

环境创建

```powershell
cd xxx

fnm env | Out-String | Invoke-Expression
fnm use 22 # 先手动指定版本
node -v > .node-version # 生成 fnm 识别的版本

# 若使用 npm ，则锁定版本跟随 nodejs
npm pkg set packageManager="npm@$(npm -v)"
npm install # 安装依赖

# 若使用 yarn/pnpm ，则手动找一个 nodejs 支持的版本，只写大版本号会自动找一个最新的，或者直接指定小版本
corepack enable
corepack use pnpm@latest-11 # pnpm v11 中最新的版本，依赖 nodejs v22+
pnpm install # 安装依赖

# ========= 验证 =========

fnm env | Out-String | Invoke-Expression
fnm use

cat .node-version
node -v

cat package.json | findstr packageManager
npm -v
yarn -v
pnpm -v
```

## One-Key load env

```powershell
# powershell script

# run `. .\init-env.ps1` in powershell terminal

. .\.venv\Scripts\Activate.ps1
python -V

fnm env | Out-String | Invoke-Expression
fnm use

```