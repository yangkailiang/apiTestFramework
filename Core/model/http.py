from pydantic import BaseModel, field_validator, Field, BaseConfig, ConfigDict
from Core.enmu import RequestMethod, ResponseType, RequestType
from Core.model.controller import ControllerStructural
from configs import PROTOCOL_DEFAULT, HTTP_REQUEST_TYPE_DEFAULT, HTTP_RESPONSE_TYPE_DEFAULT, HTTP_REQUEST_METHOD_DEFAULT


class HttpApiStructural(ControllerStructural):
    name: str = Field(description="接口名称")
    url: str = Field(description="接口路径")
    method: RequestMethod | None = Field(default=HTTP_REQUEST_METHOD_DEFAULT,
                                         description=f"接口的请求方式, 默认值为:{HTTP_REQUEST_METHOD_DEFAULT}")
    headers: dict | None = Field(default=None, description="请求头")
    proxies: dict | None = Field(default=None, description="代理")
    requestType: RequestType | None = Field(default=HTTP_REQUEST_TYPE_DEFAULT, description=f"请求体类型默认:{HTTP_REQUEST_TYPE_DEFAULT}")
    responseType: ResponseType | None = Field(default=HTTP_RESPONSE_TYPE_DEFAULT, description=f"响应类型,默认：{HTTP_RESPONSE_TYPE_DEFAULT}")
    body: dict | str | None = Field(default=None, description="请求体")
    protocol: str = Field(default=PROTOCOL_DEFAULT, description=f"请求协议，默认值为{PROTOCOL_DEFAULT}")

    @field_validator("method", mode="before")
    def pre_method(cls, method: str):
        return method.lower()

    model_config = ConfigDict(use_enum_values=True)


class HTTPRequestStructura(BaseModel):
    """ 接口请求配置 """
    method: RequestMethod = Field(default='post')  # 请求方法，字符串，例如 'GET', 'POST', 'PUT' 等
    url: str = Field(default='')  # 请求的 URL，字符串
    params: dict = Field(default=None)  # URL 参数，字典或字符串，默认为 None
    jsonData: dict = Field(default=None, alias='json')  # 请求数据
    data: dict = Field(default=None)  # 请求数据，字典、字符串或文件，默认为 None
    headers: dict = Field(default=None)  # 请求头部，字典，默认为 None
    files: dict = Field(default=None)  # 上传文件，字典，默认为 None
    timeout: int = Field(default=10)  # 超时时间，浮点数或元组，默认为 None
    # proxies: dict = field(default=None)  # 代理服务器，字典，默认为 None
    stream: bool = Field(default=False)  # 是否使用流式传输，布尔值，默认为 False
    verify: bool = Field(default=True)  # 是否验证 SSL 证书，布尔值，默认为 True
