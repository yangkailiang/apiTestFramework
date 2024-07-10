import pytest
from pydantic import BaseModel, Field, model_validator, ValidationError

from Core.enmu import Protocol
from Core.model.http import HttpApiStructural
from Core.model.nats import NatsApiStructural


class Settings(BaseModel):
    # api测试配置
    session: bool | None = Field(default=False, description="是否启用session，只对http接口有用")
    # web测试配置
    startDriver: bool | None = Field(default=True, description="开始启动驱动")
    closeDriver: bool | None = Field(default=True, description="结束关闭驱动")
    driverSetting: dict | None = Field(default_factory=dict, description="驱动配置信息")


class CaseStructural(BaseModel):
    story: str | None = Field(default='', description="集合名称")
    title: str = Field(description="用例名称")
    desc: str = Field(description="用例描述")
    setup: list | None = Field(default_factory=list, description="前置操作")
    teardown: list | None = Field(default_factory=list, description="后置操作")
    settings: Settings = Field(default_factory=Settings, description="设置")
    params: dict | None = Field(default_factory=dict, description="公共参数")
    marks: list | str | None = Field(default_factory=list, description="用例标签")
    xfail: str | None = Field(default=None, description="是否预期失败")
    apiList: list = Field(default=None, description="接口列表")

    @model_validator(mode="after")
    def inCarModelValidator(cls, model):
        marks = model.marks
        if not isinstance(marks, list):
            marks = [marks]

        model.marks = [getattr(pytest.mark, i) for i in marks]
        if model.xfail is not None:
            model.marks.append(pytest.mark.xfail(reason=model.xfail))
        for index, api in enumerate(model.apiList):
            try:

                if api.get("protocol") == Protocol.NATS.name:
                    model.apiList[index] = NatsApiStructural(**api)
                else:
                    model.apiList[index] = HttpApiStructural(**api)
            except ValidationError as e:
                raise RuntimeError(f"{model.story}-{model.title}-{api.get('name', '')}:参数校验失败，中断执行：\n{e}")

        return model


class CollectionStructural(BaseModel):
    story: str = Field(description="集合名称")
    collection: list = Field(default=None, description="用例")


class CollectionListStructural(BaseModel):
    collectionList: list[CollectionStructural] = Field(default=None, description="集合")
