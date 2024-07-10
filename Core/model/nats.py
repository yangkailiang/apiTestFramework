from pydantic import BaseModel, field_validator, Field, Json, ConfigDict
from Core.enmu import NatsRequestMethod
from Core.model.controller import ControllerStructural
from configs import PROTOCOL_DEFAULT


class NatsApiStructural(ControllerStructural):
    name: str = Field(description="接口名称")
    server: str = Field(description="nats地址：ip:prot")
    topic: str = Field(description="nats主题")
    method: NatsRequestMethod | None = Field(default=NatsRequestMethod.request.name, description="接口的请求方式")
    headers: dict | None = Field(default=None, description="请求头")
    body: dict | str = Field(description="请求体")
    protocol: str = Field(default=PROTOCOL_DEFAULT, description=f"请求协议，默认值为{PROTOCOL_DEFAULT}")

    model_config = ConfigDict(use_enum_values=True)


class NatsRequestStructura(BaseModel):
    """ 接口请求配置 """
    server: str = Field(default='', description='host + prot')
    method: NatsRequestMethod = Field(default='request', description='请求方法 request、pub')
    topic: str = Field(default='', description='nats主题')
    data: Json = Field(default_factory=dict, description='请求参数')
    timeout: int = Field(default=10)
    headers: dict = Field(default=None)
