import shutil
from system.log import log
import os
from api.api import Api


def main():
    # 创建设备
    if not os.path.exists(os.path.join(os.getcwd(), "config", "config.yaml")):
        log().info(
            "配置文件不存在, 拷贝默认配置文件[config.default.yaml]->[/config/config.yaml]"
        )
        shutil.copy("config.default.yaml", "config/config.yaml")
    api = Api()
    api.start()


if __name__ == "__main__":
    main()
