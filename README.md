# daily

## submodule

项目自带几个 submodule

```shell
# 添加一个新的子模块
git remote add submodule_alias xxx.git # 定义别名
git submodule add submodule_alias submodule_folder # 下载代码并注册激活
git add . && git commit -m "" && git push # 而后需要在主仓库将这次改动提交


# clone 项目
git clone xxx.git main_folder --recurse-submodules # 一键克隆主项目及子模块
# or
git clone xxx.git main_folder
cd main_folder # 注意此时项目的 submodule 子目录是空的
# 注册并更新子模块  recursive 参数表示递归：当子模块拥有子模块的时候使用
git submodule update --init --recursive


# pull 项目
git pull --recurse-submodules # 一键拉取主项目及子模块
# or
git pull
git submodule update --init --recursive
# 若想强制更新子模块版本（如升级依赖版本）
git submodule update --remote --recursive


# push 项目
cd submodule_folder # submodule
git add . && git commit -m "" && git push # push submodule
cd .. # main_project
git add submodule_folder && git commit -m "" && git push # update main_project's submodule commit_id


# 其他常用 submodule 命令
# 查看子模块的 commit_id
git submodule status
# git submodule update --init 解析 本质为如下两个命令
git submodule init # 将根目录下的 .gitmodules 文件中的子模块信息复制到本地仓库的配置中 .git/config （激活子模块）
git submodule update # 根据本地配置中的 url 以及当前记录中的 commit_id 去更新子模块代码

```

## subtree

submodule 仅仅是一个“指针/引用”，相对的 subtree 则是“深拷贝”

```shell
# 先添加别名
git remote add subtree_alias xxx.git

# 添加一个新的子树
# squash 将子树的历史提交合并成一个 防止主仓库的历史记录被子树污染（合并提交的描述中包含了原始 commit_id ）
git subtree add --prefix=${subtree_folder} subtree_alias ${branch} --squash

# clone
git clone xxx.git main_folder # 无需额外操作

# pull
# 正常拉取主项目
git pull
# 仅子树被其他项目更新时手动拉取（本项目不感知）
# add 的时候用了 squash 那么每次 pull 都要加 否则会因为找不到对应的 commit_id 产生冲突
git subtree pull --prefix=${subtree_folder} subtree_alias ${branch} --squash

# push
# 正常推送主项目
git add subtree_folder && git commit -m "" && git push
# 然后才能推送 subtree 的远程分支（自动提出不涉及子树的代码、提交信息与主项目一致）
git subtree push --prefix=${subtree_folder} subtree_alias ${branch}
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
