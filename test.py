import logging

import allure
import pytest
import requests
import os

from pydantic import ValidationError

from Common.logger import CustomFormatter
# 文件目录配置
from Core.enmu import Protocol
from Common.utils import read_yaml
from Common.render import Render
from Core.model.case import CollectionListStructural, CollectionStructural, CaseStructural
from Core.model.environment import EnvironmentStructural
from Core.api.httpApi import HttpApiTestCase

from configs import ENV_DEFAULT, ENVS
from Common import logger

render_instance = Render()
session = requests


def read_case(paths: list):
    cases = []
    for path in paths:
        for data in read_yaml(path):
            try:
                collection = CollectionStructural(**data)
                for case in collection.collection:
                    try:
                        case = CaseStructural(**case)
                        case.story = collection.story
                        cases.append(case)

                        # cases.append(pytest.param(case, marks=case.marks))
                    except ValidationError as e:
                        logger.error(f"{data['story']}-{case['title']}: 测试集参数校验失败，中断执行：\n{e}")
                        raise RuntimeError(f"{data['story']}-{case['title']}: 测试集参数校验失败，中断执行：\n{e}")
            except ValidationError as e:
                logger.error(f"{data['story']}: 测试集参数校验失败，中断执行：\n{e}")
                raise RuntimeError(f"{data['story']}: 测试集参数校验失败，中断执行：\n{e}")
    return cases


def run(case: CaseStructural):
    global session
    if case.settings.session is True:
        session = requests.Session()
    else:
        session = requests

    relation_params = dict()

    env = EnvironmentStructural(**ENVS[os.getenv('env') or ENV_DEFAULT])

    for api in case.apiList:
        # result = []
        # result_handler = ResultHandler(result)
        # logger.addHandler(result_handler)
        # print(logger.handlers)
        with allure.step(api.name):
            print(api.protocol, Protocol.HTTP.name)
            if api.protocol == Protocol.HTTP.name:

                HttpApiTestCase(
                    env=env,
                    api=api,
                    public_params=case.params,
                    relation_params=relation_params,
                    session=session,
                    render=render_instance
                ).main()
        # allure.attach("\n".join(result), name="Step Two Log", attachment_type=allure.attachment_type.TEXT)
        # print(result)
        # logger.removeHandler(result_handler)


for i in read_case(["/Users/apple/python_file/apiTestFramework/Case/ccc.yaml"]):

    run(i)
