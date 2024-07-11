import datetime
from collections import ChainMap
from functools import partial

from Common import logger
from Common.render import Render
from Common.utils import custom_dumps

from Core.api.controller import ApiController
from Core.model.environment import EnvironmentStructural
from Core.model.nats import NatsRequestStructura, NatsApiStructural
import asyncio
import json
from nats.aio.client import Client as NATS


async def _nats_api(server, method, topic: str, data: dict, timeout, headers) -> dict:
    # 连接nats
    nc = NATS()
    await nc.connect(server)
    # 处理请求参数，传入的是字典，转换为字节
    data = json.dumps(data).encode()
    # 发送请求
    response = await getattr(nc, method)(subject=topic, payload=data, headers=headers, timeout=timeout)
    await nc.close()
    if method == 'request':
        return json.loads(response.data.decode())
    return dict()


def send_nats_request(server, method, topic: str, data: dict, timeout, headers):
    """
    发送nats请求
    :param server: nats地址 ip:prot
    :param method: 请求方法
    :param topic: 主题
    :param data: 请求参数
    :param timeout: 超时时间
    :param headers: 请求头
    :return: 响应参数
    """
    return asyncio.run(_nats_api(server, method, topic, data, timeout, headers))


class NatsApiTestCase(ApiController):

    def __init__(self, env: EnvironmentStructural, api: NatsApiStructural, public_params, relation_params, session, render: Render):
        self.env = env
        self.api = api
        self.session = session
        self.run_params = {
            'reqHeader': dict(),
            'reqBody': dict(),
            'reqQuery': dict(),
            'resHeader': None,
            'resStatus': None,
            'resBody': None
        }
        self.relation_params = relation_params
        self.params = ChainMap(public_params, self.run_params, relation_params)
        self.render = partial(render.render, params=self.params)
        self.render_dict = partial(render.render_dict, params=self.params)
        self.request = NatsRequestStructura()

    def send_request(self, **kwargs):
        response = send_nats_request(**kwargs)
        logger.info(f"接口响应:{custom_dumps(response)}")
        self.params.update({"resBody": response})

    def assemble_request_params(self):
        self.request.server = self.api.server
        self.request.method = self.api.method
        topic = self.render(self.api.topic)
        self.request.topic = topic
        logger.info(f"method: {self.request.method}")
        logger.info(f"server: {self.request.server}")
        logger.info(f"topic: {self.request.topic}")

        # 处理请求头
        if self.api.headers:
            self.request.headers = self.render_dict(self.api.headers, )
            self.params['reqHeader'].update(self.request.headers)
            logger.info(f"请求头:{self.request.headers}")
        # 处理请求体
        self.params['reqBody'] = self.render_dict(self.api.body)
        logger.info(f"请求参数: {custom_dumps(self.params['reqBody'])}")

    def main(self):
        """ 主函数，执行接口测试 """
        # 1. 执行前置
        self.execute_plugin(opts=self.api.pre)
        # 2. 处理参数
        self.assemble_request_params()
        # 3. 逻辑判断是否跳过
        self.execute_whetherExec(whetherExec=self.api.whetherExec)
        # 4. 请求接口
        self.extract_auto_plugin(when="beforeRequest")
        self.send_request(**self.request.model_dump(by_alias=True))
        self.extract_auto_plugin(when="afterRequest")
        # 5. 执行后置操作
        self.execute_plugin(opts=self.api.post)
        # 6. 断言
        self.execute_assertion(assertions=self.api.assertions, errorContinue=self.api.errorContinue)
        # 7. 写入关联参数
        self.extract_relation_params(relations=self.api.relations)