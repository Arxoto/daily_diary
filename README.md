# daily

## submodule

项目自带几个 submodule ，在 clone 时需要一起下载下来

```shell
git clone xxx.git xxx
cd xxx
git submodule init
git submodule update
# if submodule has submodule
git submodule update --init --recursive

# or just one command
git clone xxx.git xxx --recursive
```

更新子模块

```shell
git submodule update --remote --recursive
```

## mpv-install

see <https://github.com/rossy/mpv-install>

```shell
cd ./workspace/mpv-install/
git pull -f public master # update
git push -f origin master # if updated

cp ./mpv-document.ico ~/scoop/apps/mpv/current
cp ./mpv-install.bat ~/scoop/apps/mpv/current
cd ~/scoop/apps/mpv/current
gsudo ./mpv-install.bat
# explorer.exe . # Right-click on mpv-install.bat and select "Run as administrator".
```
