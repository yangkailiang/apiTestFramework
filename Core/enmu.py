from enum import Enum


class Operator(Enum):
    preSql = 'sql'
    postSql = 'redis'
    preScript = 'cmd'
    postScript = 'script'


class SqlType(Enum):
    query = 'query'
    nonQuery = 'nonQuery'


class TZP(Enum):
    mysql = 'mysql'


class NatsRequestMethod(Enum):
    request = 'request'
    publish = 'publish'


class RequestMethod(Enum):
    get = 'get'
    post = 'post'
    put = 'put'
    delete = 'delete'
    head = 'head'
    patch = 'patch'
    options = 'options'
    trace = 'trace'

class RequestType(Enum):
    json = 'json'
    data = 'data'
    xml = 'xml'


class ResponseType(Enum):
    json = 'json'
    text = 'text'
    xml = 'xml'

class Protocol(Enum):
    HTTP = 'HTTP'
    GRPC = 'GRPC'
    NATS = 'NATS'


class Status(Enum):
    success = 0
    assert_fail = 1
    error = 2
    skip = 3


class CaseType(Enum):
    API = 'API'
    WEB = 'WEB'


class Source(Enum):
    resBody = 'resBody'
    resHeader = 'resHeader'
    reqHeader = 'reqHeader'
    reqQuery = 'reqQuery'
    reqBody = 'reqBody'
    resCode = 'resCode'


class ExtractMethod(Enum):
    jsonpath = 'jsonpath'
    re = 're'
    jinja = 'jinja'


class ContentType(Enum):
    file = 'file'
    json = 'json'
    raw = 'raw'
    form = 'form-data'


class FormType(Enum):
    String = 'String'
    Int = 'Int'
    Float = 'Float'
    Boolean = 'Boolean'
    JSONObject = 'JSONObject'
    JSONArray = 'JSONArray'
    File = 'File'
