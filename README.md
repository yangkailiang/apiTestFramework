# 自动化测试框架 - 接口和 UI 测试

## 概述

本项目旨在提供一个高效可靠的自动化测试框架，支持对 API 和用户界面进行全面的自动化测试。
实现0代码执行自动化测试

## 框架
- 语言: Python

- 测试框架: pytest
- 报告：allure
- 接口测试
    - requests: http协议
    - nats-py: Nats协议
- ui测试: selenium
  
## 功能特性

- **接口测试**：
    - 支持对 http、nats等协议 进行自动化测试。
    - 使用 pytest 作为测试运行器。

- **UI 测试（暂未实现）**：
    - 使用 Selenium WebDriver 进行浏览器自动化操作。
    - 支持多种浏览器（Chrome、Firefox 等）。
    - 集成 Allure 报告生成。

- **通用功能**：
    - 支持测试数据管理和生成。
    - 提供丰富的日志记录和报告输出。
    - 支持并行执行测试用例。
    - 提供易于扩展和定制的配置文件。

## 环境要求

- Python 3.11+
- Chrome 或 Firefox 浏览器

## 安装依赖

1. **克隆项目代码**：

    ```bash
    git clone https://github.com/yangkailiang/apiTestFramework
    
    ```

2. **安装依赖**：

    ```bash
    pip install -r requirements.txt
    ```
3. **运行Demo**：

    ```bash
    python3 manage.py --file demo.yaml
    ```

## 配置项目

1. **配置文件**：

   在 `config.py` 文件夹中配置执行环境，如接口域名、测试线上环境、数据库、redis配置等
2. **编写测试用例**：

   在 `Case` 文件夹中配置测试数据，如接口 URL、用户名、密码等。

## 运行测试

### 接口测试

运行所有接口测试用例：

```bash
python3 manage.py --file demo.yaml --evn test

-- file: 用例文件名
-- evn: 运行环境，再 config.py 中配置的执行环境
```
