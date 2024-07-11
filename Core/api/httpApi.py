import requests

from collections import ChainMap
from functools import partial

from Common.utils import exception_handler, custom_dumps, url_join
from Common import logger
from Common.render import Render

from Core.model.http import HttpApiStructural, HTTPRequestStructura
from Core.model.environment import EnvironmentStructural
from Core.api.controller import ApiController


class HttpApiTestCase(ApiController):

    def __init__(self, env: EnvironmentStructural, api: HttpApiStructural, public_params, relation_params, session, render: Render):
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
        self.request = HTTPRequestStructura()

    def send_request(self, **kwargs):

        response: requests.models.Response = self.session.request(**kwargs)
        if self.api.responseType == "json":
            try:
                res = response.json()
            except:
                res = response.text
        elif self.api.responseType == "text":
            res = response.text
        else:
            raise RuntimeError(f"未知的响应类型: {self.api.responseType}")
        logger.info(f"接口响应时间: {int(response.elapsed.total_seconds() * 1000)}MS")
        logger.info(f"接口响应:{custom_dumps(res)}")
        self.params.update({"resHeader": response.headers, "resStatus": response.status_code, "resBody": res})
        return res

    @exception_handler(message="拼接URL失败：", throw_exception=RuntimeError)
    def montage_url(self, url):
        """ 拼接URL """
        url_path = self.render(url_join(domain=self.env.domain, path=url))
        logger.info(f"接口请求地址:{url_path}")

        return url_path

    def assemble_request_params(self):
        # 请求方法
        self.request.method = self.api.method
        logger.info(f"接口请求方法:{self.request.method}")
        # 拼接URL
        self.request.url = self.montage_url(url=self.api.url)
        # 处理请求头
        if self.api.headers:
            self.request.headers = self.render_dict(self.api.headers)
            self.params['reqHeader'].update(self.request.headers)
            logger.info(f"请求头:{self.request.headers}")

        reqBody = self.render_dict(self.api.body)
        self.params['reqBody'] = reqBody

        if self.api.requestType == "json":
            self.request.jsonData = reqBody
        elif self.api.requestType == "data":
            self.request.data = reqBody
        logger.info(f"请求参数: {custom_dumps(reqBody)}")

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
