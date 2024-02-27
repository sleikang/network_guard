# NetworkGuard

软路由(OpenWrt|iStoreOS)网络守护

1.用于宽带经常被运营主动断开后没有重新拨号等其他原因无法上网 2.软件流程是尝试 GET 请求用户配置的 API，可以配置多个，有一个上网即认为网络正常，如果全部请求失败累计 3 次以后会尝试连接用户设置的路由器 SSH，连接成功后执行重启 WAN 命令，达到守护网络的目的

配置文件在首次启动时会自动拷贝到 config 目录下

```
openwrt:
    # 路由器地址
    host: 192.168.100.1
    # 路由器用户名
    username: root
    # 路由器密码
    password: password
    # 路由器SSH端口
    port: 22

api:
    # 尝试网络请求地址 支持多个地址 只要一个请求成功即认为网络正常
    urls:
        - https://www.tsa.cn/api/time/getCurrentTime
        - https://f.m.suning.com/api/ct.do
        - https://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp
        - https://vv.video.qq.com/checktime?otype=json
    # 每次查询间隔秒数 当三次连续失败即重启WAN
    sleep: 300
```

-   源码运行

1. 配置文件 config/config.yaml
2. win 下使用安装 Python3 安装过程连续点击下一步
3. 安装依赖模块

-   python -m pip install -r requirement.txt

4. 启动 cmd 输入 python main.py

-   docker compose 运行

```
version: '3'

services:
  jd_server:
    image: sleikang/network_guard:latest
    container_name: network_guard
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - /your_path/network_guard/log:/app/log #日志文件目录
      - /your_path/network_guard/config:/app/config #配置文件目录
    restart: always

```

-   docker run

```
docker run -d \
  --name network_guard \
  -e TZ=Asia/Shanghai \
  -v /your_path/network_guard/log:/app/log \
  -v /your_path/network_guard/config:/app/config \
  --restart always \
  sleikang/network_guard:latest

```
