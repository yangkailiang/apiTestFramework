from pydantic import BaseModel, Field


class WebOperationStructural(BaseModel):
    operationType: str = Field(description="操作编码")
    operationId: str = Field(description="操作编码")
    operationName: str = Field(default=None, description="操作编码")
    operationDesc: str | None = Field(default='', description="操作编码")
    operationTrans: str = Field(default=None, description="操作编码")
    operationCode: str | None = Field(default=None, description="操作编码")
    operationElement: dict | None = Field(default_factory=dict)
    operationData: dict | None = Field(default_factory=dict)
