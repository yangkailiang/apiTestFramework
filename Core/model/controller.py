from typing import Any

from pydantic import BaseModel, field_validator, Field, Json, model_validator, ValidationError, ConfigDict

from Core.enmu import SqlType, ExtractMethod
from Core.assertion import ASSERT_MAP
from configs import EXTRACT_METHOD_DEFAULT, ASSERTION_METHOD_DEFAULT


class _Sql(BaseModel):
    sqlType: SqlType = Field(description="sql类型，查询sql和费查询sql")
    sqlText: str = Field(description="SQL")
    name: str = Field(default='', description="当为查询sql时必填，用于赋值查询结果")
    db: str = Field(description="数据库连接")
    model_config = ConfigDict(use_enum_values=True)


class Plugin(BaseModel):
    """ 前置或后置操作"""
    name: str = Field(description="操作类型")
    value: dict | Json | str | int = Field(description="值")


class _WhetherExec(BaseModel):
    """ """
    target: str = Field(description="表达式")
    assertion: str = Field(description="校验类型")
    expect: str = Field(description="预期值")

    @field_validator("target", "assertion", "expect", mode="after")
    def post_field_validator(cls, value: str):
        if not value:
            raise ValueError(f"输入值：{value!r}不符合规则，请检查")
        return value


class Assertion(BaseModel):
    expression: str = Field(description="表达式")
    method: ExtractMethod | None = Field(default=EXTRACT_METHOD_DEFAULT, description="提取方式")
    assertion: str | None = Field(default=ASSERTION_METHOD_DEFAULT, description=f"校验类型,默认:{ASSERTION_METHOD_DEFAULT}")
    expect: Any = Field(default=None, description="预期结果")
    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def inCarModelValidator(cls, model):
        if ASSERT_MAP.get(model.assertion) is None:
            raise KeyError(f"{model.assertion}未知的校验类型")
        return model


class _Relation(BaseModel):
    expression: str = Field(description="表达式")
    method: ExtractMethod = Field(default=EXTRACT_METHOD_DEFAULT, description="提取方式")
    name: str = Field(description="字段名称")
    model_config = ConfigDict(use_enum_values=True)


class ControllerStructural(BaseModel):
    """ 逻辑判断 """
    whetherExec: Json[list[_WhetherExec]] | None = Field(default=None, description="条件控制器")
    pre: list[Plugin] | None = Field(default=None, description="前置操作")
    post: list[Plugin] | None = Field(default=None, description="后置操作")
    errorContinue: bool | None = Field(default=False, description="出现错误后是否接着执行")
    assertions: None | list[Assertion] = Field(default=None, description="接口断言")
    relations: None | list[_Relation] = Field(default=None, description="接口关联参数")
    model_config = ConfigDict(validate_assignment=True)

# class
