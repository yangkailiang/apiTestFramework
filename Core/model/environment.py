from typing import Dict

from pydantic import BaseModel, Field, model_validator, Json


class RedisStructural(BaseModel):
    host: str = Field(description="主机")
    port: int | None = Field(default=6379, description="端口")


class ServerStructural(BaseModel):
    hostname: str = Field(description="主机")
    port: int | None = Field(default=22, description="端口")
    username: str | int = Field(description="用户名")
    password: str | int = Field(description="密码")


class DBStructural(BaseModel):
    host: str = Field(description="主机")
    port: int | None = Field(default=3306, description="端口")
    user: str | int = Field(description="用户")
    passwd: str | int = Field(description="密码")


class EnvironmentStructural(BaseModel):
    domain: str = Field(description="域名配置")
    redis: Dict[str, RedisStructural] = Field(description="Redis连接配置")
    db: Dict[str, DBStructural] = Field(description="数据库连接配置")
    server: Dict[str, ServerStructural] = Field(description="服务器连接配置")
