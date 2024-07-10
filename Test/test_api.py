
import allure
import pytest
import requests
import os

from pydantic import ValidationError

from Common.logger import ResultHandler
from Common.utils import read_yaml
from Common.render import Render
from Common import logger

from Core.enmu import Protocol
from Core.model.case import CollectionStructural, CaseStructural
from Core.model.environment import EnvironmentStructural
from Core.api.httpApi import HttpApiTestCase
from Core.api.natsApi import NatsApiTestCase
from configs import ENV_DEFAULT, ENVS

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
                        cases.append(pytest.param(case, marks=case.marks))
                    except ValidationError as e:
                        logger.error(f"{data['story']}-{case['title']}: 测试集参数校验失败，中断执行：\n{e}")
                        raise RuntimeError(f"{data['story']}-{case['title']}: 测试集参数校验失败，中断执行：\n{e}")
            except ValidationError as e:
                logger.error(f"{data['story']}: 测试集参数校验失败，中断执行：\n{e}")
                raise RuntimeError(f"{data['story']}: 测试集参数校验失败，中断执行：\n{e}")
    return cases


def run(case: CaseStructural):
    global session
    session = requests.Session() if case.settings.session is True else requests
    relation_params = dict()
    env = EnvironmentStructural(**ENVS[os.getenv('env') or ENV_DEFAULT])

    for api in case.apiList:
        result_handler = ResultHandler(list())
        logger.addHandler(result_handler)
        with allure.step(api.name):
            if api.protocol == Protocol.HTTP.name:
                func = HttpApiTestCase
            elif api.protocol == Protocol.NATS.name:
                func = NatsApiTestCase
            else:
                raise RuntimeError(f"未知的协议: {api.protocol}")
            try:
                func(
                    env=env,
                    api=api,
                    public_params=case.params,
                    relation_params=relation_params,
                    session=session,
                    render=render_instance
                ).main()
            except Exception as e:
                if api.errorContinue is True:
                    logger.error(f"{api.name}: 执行失败，但错误忽略，继续执行：\n{e}")
                else:
                    logger.removeHandler(result_handler)
                    raise e
            finally:
                allure.attach("\n".join(result_handler.result), name=f"{api.name}.log", attachment_type=allure.attachment_type.TEXT)
        logger.removeHandler(result_handler)


@pytest.mark.parametrize("case", read_case(os.getenv('file').split(',')))
def test_api(case: CaseStructural):
    allure.dynamic.story(case.story)
    allure.dynamic.title(case.title)
    run(case)
