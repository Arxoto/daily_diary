环境创建

```powershell
fnm env | Out-String | Invoke-Expression

cd xxx

fnm use 22 # 先手动指定版本
node -v > .node-version # 生成 fnm 识别的版本

# npm 版本跟随 nodejs
npm pkg set packageManager="npm@$(npm -v)"

# yarn/pnpm 手动找一个 nodejs 支持的版本，只写大版本号会自动找一个最新的，或者直接指定小版本
corepack use pnpm@10
```

模拟验证

```powershell
cd xxx

fnm use

cat .node-version
node -v

cat package.json | findstr packageManager
npm -v
yarn -v
pnpm -v

```
