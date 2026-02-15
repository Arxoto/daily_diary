# Home Lab

## 虚拟化平台

[Proxmox VE](https://www.proxmox.com/en/downloads) 选择下面的 "Proxmox VE 9.1 ISO Installer"

可选：多台宿主机组建 PVE 集群，统一管理界面、支持虚机在线迁移。
但是为了防止其自带的高可用机制与下面的容器平台的高可用相冲突，可以取消容器虚机的 HA 。

使用 [Ventoy](https://github.com/ventoy/Ventoy) ，制作 U 盘启动

辅助脚本 [Proxmox VE Helper Scripts](https://community-scripts.github.io/ProxmoxVE/scripts) （原 tteck 开发的那套）
- 系统优化（去除订阅、换源） <https://community-scripts.github.io/ProxmoxVE/scripts?id=post-pve-install>
  - 国内由于网络问题建议使用 <https://github.com/Mapleawaa/PVE-Tools-9> ，之后再去上面的网站中寻找一键脚本
- 一键创建常用的 LXC 容器

## NAS

[TrueNAS](https://www.truenas.com/truenas-community-edition/) （社区版就是原 SCALE 版）

TrueNAS 建议直接安装（存算分离），如资源紧缺或性能过剩需要安装在虚机上的话：
- ZFS 文件系统需要硬盘直通，建议给 TrueNAS 系统预留 8-16G 内存

P.S. NAS 共享的是文件夹，商用云挂载云盘用的是分布式块存储（对应到 PVE 上是 Ceph ），在 HomeLab 场景下没必要这么硬核（资源浪费）

P.S. 注意 NAS 共享协议的选择
- SMB 写独占锁避免并发冲突，兼容性好，适合跨平台协作
- NFS 高性能但存在并发冲突风险，性能好，适合 Linux/容器
- iSCSI 块存储，性能最好（但还是不如虚拟盘）、维护复杂，模拟物理硬盘（复用 NAS 底层的高可靠），具有排他性，适合数据库用
  - 但在 k3s 中使用配置较为复杂，可直接使用虚拟盘（推荐），高性能且软件自带高可用的场景下直接选择直通盘
- WebDAV & FTP/SFTP ，不建议使用，推荐替代 [见下](./home.server.md#私人网盘)
- S3 对象存储，虽然 TrueNAS 兼容该协议，但其底层 ZFS 有重复冗余，且为单机架构，不适合用于提供 S3 服务
  - 若要使用 S3 服务，直接部署 MinIO （容器部署，使用虚拟盘或直通盘）

## 容器

容器管理工具/容器编排平台，仍然建议部署在 VM 中。

如 K3s
- 会深度修改宿主机的网络防火墙(iptables/nftables)、安装大量的依赖库、修改内核参数，网络插件崩溃时能通过 PVE 控制。
- 作为强状态系统，变更异常可能需要查阅大量日志， PVE 的快照支持快速回滚。

### Podman

[Podman](https://podman.io/)

定位： Docker 的平替，开源、轻量、安全(Rootless)、零学习成本(`alias docker=podman`)

建议使用一键脚本安装(LXC) <https://community-scripts.github.io/ProxmoxVE/scripts?id=podman>

### k3s

[k3s](https://docs.k3s.io/zh/)

定位：轻量化的 k8s 编排平台，适用于：多节点高可用、自动运维、学习 DevOps

在 PVE 中创建 Debian VM ，然后使用 [k3sup](https://github.com/alexellis/k3sup) 一键安装集群

可以选择 [arkade](https://github.com/alexellis/arkade) 快速安装常用镜像（简化操作， HomeLab 场景推荐）

## 软件选型

### 流媒体

- Ingress 反向代理和负载均衡
  - podman
    - 反向代理 Caddy ，开启 HTTP/3 (QUIC)
    - 部署方式 Quadlet 将容器转换为 systemd 服务，能很好地解决依赖关系（ NFS 挂载成功后再启动 Jellyfin 容器）
    - 网络 Rootless 模式
  - k3s
    - 反向代理 Traefik （ k3s 内置），开启 HTTP/3 (QUIC)
- 存储层
  - 媒体文件，用 NAS 的 NFS 共享
  - 数据库和缓存，用虚拟盘
- 下载层
  - qBittorrent + Prowlarr （种子管理）
- 管理层
  - Sonarr （剧集订阅） + Radarr （电影订阅）
- 展示层
  - Jellyfin （核显硬解）
  - Stash 私密管理
- 交互层
  - Jellyseerr/Overseerr （点片系统）

### 私人网盘

推荐组合
- FileBrowser Quantum 手动管理
- Syncthing 自动管理
- Immich 相册和视频的展示层

详细对比
- Nextcloud 全能协作办公
  - 占用高，架构复杂；生态丰富（日历、邮件、通讯录、会议、在线文档），移动端体验优秀
  - 存储格式为原始文件，但需要数据库索引
- Seafile 专业同步工具
  - 占用低；性能好，大文件稳定
  - 存储格式分块存储，存储黑盒
- FileBrowser 轻量文件管理
  - 占用最低，最透明
  - 原始文件存储，所见即所得
  - 增强版 FileBrowser Quantum 性能占用稍高
  - 仅 WEB 端，可通过 WebDAV 协议 + 专业传输软件
- Syncthing 去中心化的自动同步工具
  - 其实不算是一个网盘，后台静默同步，和其他软件一起组合使用
  - 客户端 <https://docs.syncthing.net/users/contrib.html#gui-wrappers>
- Immich 相册和多媒体管理
  - AI 分类，因此服务端有一定性能要求，移动端体验极佳
  - 一般建议作为展示层（只读外部库）与上面软件组合使用
- [OpenList](https://github.com/OpenListTeam/OpenList) 多网盘聚合，原 AList

### 在线文档

推荐组合
- OnlyOffice + FileBrowser Quantum 通用办公套件
- CryptPad & Excalidraw 临时画布，手动导出

详细对比
- OnlyOffice 需配合 FileBrowser Quantum / Nextcloud 丝滑流转
  - 对 Microsoft Office 兼容性最佳，支持多人协作（类似 Google Docs 的实时光标显示），需要在服务端注册账号
  - 服务端和客户端占用一般，每次打开稍慢（引擎初始化）
  - 部署时需要进行一定配置
  - 管理方便， FileBrowser 原始文件存储
- CryptPad
  - 隐私至上的开源协作办公套件（端到端加密、零知识证明），无需注册账号
  - 服务端占用极低、客户端占用高（加解密、渲染、协作都在浏览器运行），启动速度快
  - 部署简单
  - 超多文件管理时会比较麻烦，但可以导出为 Office 兼容格式
- Excalidraw
  - 思维导图和架构图的画板
  - 占用较低，无服务端存储、纯前端绘画保存（可保存到 NAS 上），多人协作使用 excalidraw-room
  - 部署简单
  - 手动管理文件，也可在 CryptPad 中集成

### DevOps

轻量组合（省内存）：
- Gitea/Forgejo （代码仓）
- Gitea Actions （流水线 CI/CD ）

### 广告隔离

- AdGuard Home

### 智能家居

- Home Assistant
  - Home Assistant OS 带应用商店，可直接安装 Zigbee2MQTT 等
  - 容器，仅包含核心功能
- Zigbee2MQTT （跨品牌联动）

### 私有 AI 大语言模型

- Ollama
- Open WebUI

