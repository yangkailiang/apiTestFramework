from typing import Any

from pydantic import BaseModel, field_validator, Field, Json, model_validator, ValidationError, ConfigDict

from Core.enmu import Operator, SqlType, TZP, Source, ExtractMethod, ContentType, FormType
from configs import EXTRACT_METHOD_DEFAULT, TZP_DEFAULT


class _Sql(BaseModel):
    sqlType: SqlType = Field(description="sql类型，查询sql和费查询sql")
    sqlText: str = Field(description="SQL")
    name: str = Field(default='', description="当为查询sql时必填，用于赋值查询结果")
    db: str = Field(description="数据库连接")
    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode='after')
    def pre_jsonData(cls, values):
        if values.sqlType == 'query':
            if not values.names:
                raise ValueError("查询结果命名不能为空")
        return values

    @field_validator("sqlText", mode="after")
    def post_field_validator(cls, value: str):
        if not value:
            raise ValueError(f"输入值：{value!r}不符合规则，请检查")
        return value


class _PreAndPostOperate(BaseModel):
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


class _Assertion(BaseModel):
    expression: str = Field(description="表达式")
    method: ExtractMethod = Field(default=EXTRACT_METHOD_DEFAULT, description="提取方式")
    assertion: str = Field(description="校验类型")
    expect: Any = Field(default=None, description="预期结果")

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("expression", "method", "assertion", mode="after")
    def post_field_validator(cls, value: str):
        if not value:
            raise ValueError(f"输入值：{value!r}不符合规则，请检查")
        return value


class _Relation(BaseModel):
    expression: str = Field(description="表达式")
    method: ExtractMethod = Field(default=EXTRACT_METHOD_DEFAULT, description="提取方式")
    name: str = Field(description="字段名称")

    @field_validator("expression", "method", "name", mode="after")
    def post_field_validator(cls, value: str):
        if not value:
            raise ValueError(f"输入值：{value!r}不符合规则，请检查")
        return value

    model_config = ConfigDict(use_enum_values=True)


class ControllerStructural(BaseModel):
    """ 逻辑判断 """
    whetherExec: Json[list[_WhetherExec]] | None = Field(default=None, description="条件控制器")
    pre: list[_PreAndPostOperate] | None = Field(default=None, description="前置操作")
    post: list[_PreAndPostOperate] | None = Field(default=None, description="后置操作")
    errorContinue: bool | None = Field(default=False, description="出现错误后是否接着执行")
    assertions: None | list[_Assertion] = Field(default=None, description="接口断言")
    relations: None | list[_Relation] = Field(default=None, description="接口关联参数")
    model_config = ConfigDict(validate_assignment=True)

# class
