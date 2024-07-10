
fields = {
    'apiId': '接口ID',
    'apiName': '接口名称',
    'apiDesc': '接口描述',
    'protocol': '接口协议',
    'proxies': '代理',
    'body': '请求体',
    'body.file': '请求体',
    'body.file.id': '请求体',
    'body.file.name': '请求体',

    # http
    'url': '接口地址',
    'path': '接口路径',
    'method': '请求方式',
    'headers': '请求头',
    # nats
    'domain': 'nats/rpc地址',
    'topic': 'nats主题',

    # grpc
    'repository': '仓库名',
    'branch': '分支',
    'protoc': 'proto文件名',
    'server': 'rpc服务',
    'func': 'rpc方法',
    'messageType': 'rpc请求参数类型',

    'body.form': '请求体的表单',
    'body.form.name': '请求体的表单名称',
    'body.form.type': '请求体的表单类型',
    'body.form.value': '请求体的表单值',
    'body.form.required': '请求体的表单的是否必填',

    'body.json': '请求体的JSON',
    'body.raw': '请求体的RAW',
    'body.type': '请求体的类型',


    'query': '查询参数',
    'rest': '自定义参数',
    'relations': '关联参数',
    'relations.expression': '关联参数',
    'relations.method': '关联参数',
    'relations.name': '关联参数',
    'relations.from': '关联参数',

    'assertions': '断言',
    'assertions.expression': '断言的表达式',
    'assertions.from': '断言数据来源',
    'assertions.method': '断言的匹配方法',
    'assertions.assertion': '断言的判断条件',
    'assertions.expect': '判断的预期值',

    'controller': '逻辑控件',
    'controller.whetherExec.target': '逻辑控件的条件控制器的表达式',
    'controller.whetherExec.assertion': '条件控制器的判断条件',
    'controller.whetherExec.expect': '条件控制器的预期值',
    'controller.pre.name': '条件控制器的前置操作的类型',
    'controller.post.name': '条件控制器的后置操作的类型',
    'controller.pre.value': '条件控制器的前置操作的内容',
    'controller.post.value': '条件控制器的前置操作的内容',

    'controller.sleepBeforeRun': '条件控制器的前置延时',
    'controller.sleepAfterRun': '条件控制器的后置延时',
    'controller.timeout': '条件控制器的接口超时时间',
    'controller.saveSession': '条件控制器的存储Session',
    'controller.requireStream': '条件控制器的下载缓冲',
    'controller.requireVerify': '条件控制器的证书验证间',
    'controller.useSession': '条件控制器的接口超时时间',
    'controller.errorContinue': '条件控制器的引用Session',

}