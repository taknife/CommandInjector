#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:54
# @Author  : taknife
# @Project : CommandInjector
# @File    : device_link.py

import paramiko
import time
import socket
from typing import Optional

class DeviceLink:
    def __init__(self, ip: str, port: int, username: str, password: str) -> None:
        self.__username = username
        self.__password = password
        self.__transport: Optional[paramiko.Transport] = None
        self.__ssh: Optional[paramiko.SSHClient] = None
        self.__shell = None

        try:
            # 设置连接超时（10秒）
            sock = socket.create_connection((ip, port), timeout=10)
            self.__transport = paramiko.Transport(sock)
            self.__transport.connect(username=self.__username, password=self.__password)

            self.__ssh = paramiko.SSHClient()
            self.__ssh._transport = self.__transport
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__shell = self.__ssh.invoke_shell()
            self.__shell.settimeout(5)
        except socket.timeout:
            raise ConnectionError(f"连接 {ip}:{port} 超时，请检查网络和主机状态")
        except paramiko.AuthenticationException:
            raise ConnectionError("用户名或密码错误")
        except paramiko.SSHException as e:
            raise ConnectionError(f"SSH连接失败: {str(e)}")
        except Exception as e:
            self._cleanup()
            raise ConnectionError(f"连接异常: {str(e)}")

    def _cleanup(self):
        """安全清理资源"""
        if self.__shell:
            self.__shell.close()
        if self.__transport:
            self.__transport.close()
        if self.__ssh:
            self.__ssh.close()

    def __enter__(self):
        """支持with语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with块时自动清理"""
        self._cleanup()

    def __del__(self):
        """析构函数作为最后保障"""
        self._cleanup()

    # def executive_command(self):
    #     self.__shell.send(bytes("show version\n", "utf-8"))
    #     time.sleep(0.2)
    #     print(self.__shell.recv(1024).decode())

    def executive_command(self, command: str) -> str:
        """执行命令并返回完整输出"""
        if not self.__shell:
            raise RuntimeError("连接未建立")

        try:
            # 清空接收缓冲区
            time.sleep(0.5)
            while self.__shell.recv_ready():
                self.__shell.recv(4096)

            # 发送命令（注意不同设备可能需要不同的行结束符）
            self.__shell.send(bytes(command, "utf-8"))  # 尝试使用 \r\n 而不仅是 \n
            time.sleep(1)  # 初始等待时间延长

            command_output = ""
            max_attempts = 10  # 最大尝试次数防止无限循环
            attempt = 0

            while attempt < max_attempts:
                attempt += 1
                try:
                    # 非阻塞检查是否有数据可读
                    if self.__shell.recv_ready():
                        part = self.__shell.recv(4096).decode("utf-8", errors="ignore")
                        if part:
                            print(part)
                            command_output += part

                            # 检查分页提示
                            if "--More--" in part:
                                self.__shell.send(bytes(" ", "utf-8"))  # 发送空格继续
                                time.sleep(0.5)
                                continue

                            # 检查命令结束标记
                            if any(prompt in command_output for prompt in ["#", "$", ">"]):
                                break
                    else:
                        # 没有数据时短暂等待
                        time.sleep(0.1)

                except socket.timeout:
                    # 检查是否已经收到提示符
                    if any(prompt in command_output for prompt in ["#", "$", ">"]):
                        break
                    continue

            return command_output.strip()

        except Exception as e:
            raise RuntimeError(f"命令执行失败: {str(e)}")


def main(ip, port, username, password):
    try:
        # 使用with语句确保资源释放
        test_list = []
        with DeviceLink(ip, port, username, password) as link:
            output = link.executive_command("enable\n")
            test_list.append(output)
            output1 = link.executive_command("configure terminal\n")
            test_list.append(output1)
            #
            # for i in test_list:
            #     print(i)

            # print("命令输出:", test_list)

    except ConnectionError as e:
        print(f"连接错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")


main("192.168.211.101", 22, "admin", "admin.123")
