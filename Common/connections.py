from paramiko import SSHClient, AutoAddPolicy
from time import sleep
from redis import ConnectionPool, Redis
from pymysql import connect
from pymysql.cursors import DictCursor
from datetime import datetime
from Common import logger

class ConnectMysql:

    def __init__(self, database: dict):
        self.conn = connect(charset='utf8', cursorclass=DictCursor, **database)
        self.now = datetime.now

    def execute(self, sql: str):
        try:
            with self.conn.cursor() as cursor:
                start_time = self.now()
                line = cursor.execute(sql)
                if line == 0:
                    logger.error("[ROW:0] {}".format(sql))
                    return False, None
                data = cursor.fetchall()
                logger.info('[ROW:{}][{}MS] {}'.format(line, round((self.now() - start_time).total_seconds() * 1000, 2), sql))
                return data
        except Exception as e:
            self.conn.rollback()
            logger.error(f"执行SQL报错 ：{sql}, {e}")
            raise RuntimeError(f"执行SQL报错 ：{sql}, {e}")

    def __del__(self):
        self.conn.close()


class ConnectRedis:

    def __init__(self, redis):

        pool = ConnectionPool(**redis)  # 实现一个连接池
        self.redis_connection = Redis(connection_pool=pool)

    def rotation_get(self, key: str, interval: int = 1, timeout=60):
        used_times = 0
        while used_times < timeout:
            result = self.redis_connection.get(key)
            if result:
                return result
            sleep(interval)
            used_times += interval

    def __del__(self):
        self.redis_connection.close()


class ConnectServer:
    def __init__(self, server: dict):
        """ 连接服务器 """
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(**server)

    def __del__(self):
        self.ssh.close()

    def run_cmd(self, command: str, is_login: bool = False) -> (bool, str):
        if is_login:
            command = f"bash --login -c '{command}'"
        # 打开一个新的通道
        channel = self.ssh.get_transport().open_session()
        # 执行远程命令
        channel.exec_command(command)
        # 等待命令执行完成
        channel.recv_exit_status()
        # 获取退出代码
        exit_code = channel.recv_exit_status()
        if exit_code == 0:
            return True, channel.makefile().read().decode()
        else:
            return False, channel.makefile_stderr().read().decode()


__all__ = ['ConnectMysql', 'ConnectRedis', 'ConnectServer']
