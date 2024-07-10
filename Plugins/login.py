from Core.api.httpApi import HttpApiTestCase
from Core.utils import url_join
from Common import logger


def login(case: HttpApiTestCase, username, password, guid):
    res = case.session.request(
        url=url_join(domain=case.env.domain, path="api/v1/sys/login",
                     json={"guId": 1,
                           "password": "test@123456",
                           "userName": "ykl"})
    ).json()
    if res["code"] == 10000:
        case.request.headers = {"Sessionkey": res.headers["Sessionkey"]}
        logger.info("登录成功")
    else:
        logger.info(f"登录失败: {res}")
