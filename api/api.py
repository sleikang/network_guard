from system.log import log
from system.yaml_config import YamlConfig
from network.network import Network
import time
import paramiko


class Api:
    def __init__(self):
        pass

    def start(self):
        try:
            yaml_config = YamlConfig()
            config = yaml_config.get_config()
            if config is None:
                log().error(f"启动失败, 请检查配置文件")
                return False
            network = Network()
            err_num = 0
            while True:
                try:
                    urls = config["api"]["urls"]
                    success_num = 0
                    for url in urls:
                        p, err = network.get(url=url)
                        if p:
                            success_num += 1
                        else:
                            log().info(f"[{url}]请求失败, {err}")

                    if success_num < 1:
                        log().info(f"获取数据失败, {err}")
                        err_num += 1
                        if err_num >= 3:
                            log().info(f"连续3次获取数据失败开始重启WAN")
                            # 创建 SSH 客户端
                            client = paramiko.SSHClient()
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                            # 连接远程服务器
                            client.connect(
                                hostname=config["openwrt"]["host"],
                                port=config["openwrt"]["port"],
                                username=config["openwrt"]["username"],
                                password=config["openwrt"]["password"],
                            )

                            # 执行远程命令
                            log().info(f"开始重启WAN")
                            _, _, _ = client.exec_command("ifup wan")
                            log().info(f"重启WAN成功")

                            # 关闭连接
                            client.close()
                            err_num = 0
                    else:
                        log().info(f"网络正常")
                        err_num = 0

                    time.sleep(config["api"]["sleep"])

                except Exception as e:
                    log().error(f"异常错误, {e}")
        except Exception as e:
            log().error(f"启动失败, {e}")
        return False
