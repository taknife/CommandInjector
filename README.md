# CommandInjector
![logo](./images/logo.png)ABT设备命令执行工具，自动化刷入设备配置

## 支持平台

* Windows 10/11
* Linux/MacOS



## 部署方式

### Windows平台安装部署

* 直接下载发行版本[CommandInjector 发行版本](https://github.com/taknife/CommandInjector/releases/tag/Beta)



### Linux/MacOS

* 下载源代码

    ```bash
    git clone https://github.com/taknife/CommandInjector.git
    ```

* 本地安装Python3.13 + 环境

* 创建Python项目，建议使用虚拟环境`venv`，通过`requirements.txt`安装依赖

    ```bash
    pip install -r requirements.txt
    ```

    如果安装很慢，安装报错，可以更换pip安装源，下文为清华源

    ```bash
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

* 安装完成后，将源代码中的`src`、`images`、`ui`三个目录复制到项目中，运行`src/main.py`即可



## 使用方法

1. 确认配置下发终端与设备的网络连通性

    ![image1](./images/image1.png)

2. 工具采用SSH协议进行连接，确认设备SSH端口，选择配置文件（也可自行编辑txt文本文件进行导入上传）和需要提取的配置模块，填写IP、端口、用户名和密码点击提交。

    ![image2](./images/image2.png)

    当出现save config时，完成保存配置的命令下发，此时可以在设备web页面进行查看，看是否下发成功。

