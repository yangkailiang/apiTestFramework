import argparse
import os
import sys

import pytest

from configs import CASE_DIR, ENVS, ALLURE_REPORT_DIR, ENV_DEFAULT
from contextlib import contextmanager


@contextmanager
def set_temporary_env_vars(env_vars):
    """
    A context manager to temporarily set multiple environment variables.

    Args:
        env_vars (dict): A dictionary of environment variables to set.
    """
    env_vars = {k: v for k, v in env_vars.items() if v is not None}
    original_values = {key: os.getenv(key) for key in env_vars}

    # Set new environment variables
    os.environ.update(env_vars)

    try:
        yield
    finally:
        # Restore original environment variables
        for key, value in original_values.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value

def unicode_escape(text):
    return text.encode('unicode_escape').decode('ascii')

def write_allure_environment(file, db, redis, domain, server):
    with open(file, 'w', encoding="utf-8") as f:
        f.write(f'{unicode_escape("作者=杨")}\n')
        f.write(f'{unicode_escape("域名")}={domain}\n')
        for k, v in db.items():
            f.write(f'{unicode_escape("数据库")}-{k}={v}\n')
        for k, v in redis.items():
            f.write(f'Redis-{k}={v}\n')
        for k, v in server.items():
            f.write(f'{unicode_escape("服务器")}-{k}={v}\n')

def exists(path):
    path = os.path.join(CASE_DIR, str(path))
    if os.path.exists(path) is False:
        raise FileExistsError(f"文件不存在: {path}")
    return path


# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='执行测试用例')
parser.add_argument('--file', type=exists, action='append', required=True, help='用例文件')
parser.add_argument('--env', type=str, help='执行环境')

# 解析命令行参数
args = vars(parser.parse_args())

with set_temporary_env_vars({
    "file": ','.join(args["file"]),
    "env": args.get("env", ENV_DEFAULT),
}):
    pytest.main(["Test/test_api.py", f"--alluredir={ALLURE_REPORT_DIR}", "--clean-alluredir"])
    write_allure_environment(os.path.join(ALLURE_REPORT_DIR, "environment.properties"), **ENVS[args.get('env') or ENV_DEFAULT])
    os.system(f"allure serve {ALLURE_REPORT_DIR} -p 8000")
