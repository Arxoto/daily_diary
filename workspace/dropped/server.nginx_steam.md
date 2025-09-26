# 使用 Nginx 本地反代访问 steam

## 原理

G_F__W 通过【 SNI 阻断】来实现（之前是通过【 DNS 污染】）

> SNI，服务器名称指示，简单来说，是用于在一台服务器的相同端口上部署不同证书的方法。服务器根据收到请求中的SNI域名来处理相应的请求，如果SNI域名为空，会按照预先设置好的默认域名处理请求。

> 审查机构会对当中的域名进行检测和阻断，也就是TCP重置攻击，通过对双方疯狂发送RST报文使连接重置，如果是浏览器访问就会出现ERR_CONNECTION_RESET错误。  

> 在Client Hello阶段不携带SNI或者携带无效的SNI，隐藏真实的连接网站来规避互联网审查。当CDN检测到无效的SNI，会返回一张默认证书以便能够继续连接。碰巧的是，Akamai所返回的默认证书就是Steam的泛域名证书（毕竟Steam是最大的客户）。这种技术叫做域前置，截至目前对Steam、Pixiv、Github等大型网站都有效。

see https://www.cnblogs.com/night-ray/articles/15964334.html#22-%E9%82%A3%E4%B9%88%E6%9C%89%E4%BB%80%E4%B9%88%E5%8A%9E%E6%B3%95%E5%8F%AF%E4%BB%A5%E8%A7%A3%E5%86%B3%E5%91%A2

see https://www.zhmoegirl.com/posts/7b1b67ee672a/

## 方案

### 获取 steam 域名

参考 https://help.steampowered.com/zh-cn/faqs/view/2EA8-4D75-DA21-31EB

参考 https://www.dogfight360.com/blog/686/

配置 Hosts 文件 from steamcommunity_302

```
# steam 社区 # Reverse_Proxy_for_Steam
127.0.0.1 steamcommunity.com # Reverse_Proxy_for_Steam
127.0.0.1 www.steamcommunity.com # Reverse_Proxy_for_Steam
# steam 商店/API/客服 # Reverse_Proxy_for_Steam
127.0.0.1 store.steampowered.com # Reverse_Proxy_for_Steam
127.0.0.1 checkout.steampowered.com # Reverse_Proxy_for_Steam
127.0.0.1 api.steampowered.com # Reverse_Proxy_for_Steam
127.0.0.1 help.steampowered.com # Reverse_Proxy_for_Steam
127.0.0.1 login.steampowered.com # Reverse_Proxy_for_Steam
127.0.0.1 store.akamai.steamstatic.com # Reverse_Proxy_for_Steam
# 网页样式/图片 # Reverse_Proxy_for_Steam
127.0.0.1 steambroadcast.akamaized.net # Reverse_Proxy_for_Steam
127.0.0.1 steamvideo-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 steamusercontent-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 steamstore-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 steamcommunity-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 steamcdn-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 steamuserimages-a.akamaihd.net # Reverse_Proxy_for_Steam
127.0.0.1 community.akamai.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 avatars.akamai.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 community.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 cdn.akamai.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 avatars.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 cdn.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 community.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 store.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 video.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 avatars.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 dfs.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
127.0.0.1 clan.cloudflare.steamstatic.com # Reverse_Proxy_for_Steam
# 好友聊天 # Reverse_Proxy_for_Steam
127.0.0.1 steam-chat.com # Reverse_Proxy_for_Steam
# 聊天发送图片 # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-ugc.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 community.akamai.steamstatic.com # Reverse_Proxy_for_Steam
# 验证码 # Reverse_Proxy_for_Steam
127.0.0.1 www.google.com # Reverse_Proxy_for_Steam
# 创意工坊 # Reverse_Proxy_for_Steam
127.0.0.1 www.youtube.com # Reverse_Proxy_for_Steam
# 云同步 # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-eu-ams.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-eu-fra.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-finland.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-saopaulo.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-singapore.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-sydney.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-taiwan.storage.googleapis.com # Reverse_Proxy_for_Steam
127.0.0.1 steamcloud-eu.storage.googleapis.com # Reverse_Proxy_for_Steam
```

### 生成并安装证书

参考 server.md 中搜索“生成根证书和服务端证书”

也可直接用 steamcommunity_302 生成的
- steamcommunity.crt
- steamcommunity.key
- steamcommunityCA.pem （自签的CA根证书，需要服务器中添加并信任根证书）

比如放在 /etc/nginx/ca-certificates/ 下统一管理，配置中写相对路径

### 找到 Akamai ip

可以用 UsbEAm Hosts Editor

### 配置启动 Nginx

```conf
server {# 部署一个虚拟主机
        listen localhost:443 ssl;# 监听localhost的443端口
        server_name steamcommunity.com;# 添加要监听的域名，与Hosts文件里的域名一致
        server_name www.steamcommunity.com;
        server_name store.steampowered.com;
        server_name api.steampowered.com;

        ssl_certificate ca-certificates/steamcommunity.crt;# 设置证书，这里使用了相对路径，绝对路径也行
        ssl_certificate_key ca-certificates/steamcommunity.key;# 设置与证书匹配的密钥，同上

        location / {# 当监听的端口检测到通往上述域名的流量时，执行下列操作
                proxy_pass https://223.119.248.24/;# 将流量送往223.119.248.24主机，理论上任何一个Akamai服务器IP都可以
                proxy_set_header Host $http_host;# 务必要加上，否则会报错URL非法
        }
}
```

启动命令

```shell
nginx -c /etc/nginx/nginx.conf -p /etc/nginx/
```