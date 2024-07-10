import time
import re
from datetime import datetime

from faker import Faker
from typing import Dict, Callable, List


class RandomData:
    def __init__(self):

        self.faker = Faker(locale='zh_CN')
        self.template: Dict[str, Callable[[str], str]] = {
            '#': self.faker.numerify,
            '?': self.faker.lexify,
            '<plate>': self.plate,
            '<uuid>': self.uuid,
            '<url>': self.url,
            '<address>': self.address,
            '<email>': self.email,
            '<phone>': self.phone,
            '<timestamp>': self.timestamp,
            '<msg>': self.msg,
            '<name>': self.name,
            '<company>': self.company,
            '<bankNumber>': self.bank_number
        }
        self._re_plate = re.compile(r"<plate>")
        self._re_uuid = re.compile(r"<uuid>")
        self._re_url = re.compile(r"<url>")
        self._re_address = re.compile(r"<address>")
        self._re_email = re.compile(r"<email>")
        self._re_phone = re.compile(r"<phone>")
        self._re_timestamp = re.compile(r"<timestamp>")
        self._re_msg = re.compile(r"<msg>")
        self._re_name = re.compile(r"<name>")
        self._re_company = re.compile(r"<company>")
        self._re_bank_number = re.compile(r"<bankNumber>")

    def bank_number(self, expression: str) -> str:
        return self._re_bank_number.sub(lambda x: self.faker.credit_card_number(card_type='mastercard'), expression)

    def image_url(self, is_protocol=True):
        url = self.faker.image_url()
        if is_protocol is False:
            url = url.replace('https://', '')
        return url

    def address(self, expression: str) -> str:
        return self._re_address.sub(lambda x: self.faker.address(), expression)

    def name(self, expression: str) -> str:
        return self._re_name.sub(lambda x: self.faker.name(), expression)

    def company(self, expression: str) -> str:
        return self._re_company.sub(lambda x: self.faker.company(), expression)

    def msg(self, expression: str) -> str:
        return self._re_msg.sub(lambda x: self.faker.sentence(), expression)

    def timestamp(self, expression: str):
        return self._re_timestamp.sub(lambda x: str(int(time.time())), expression)

    def phone(self, expression: str):
        return self._re_phone.sub(lambda x: self.faker.phone_number(), expression)

    def email(self, expression: str):
        return self._re_email.sub(lambda x: self.faker.email(), expression)

    def url(self, expression: str):
        return self._re_url.sub(lambda x: self.faker.url(), expression)

    def plate(self, expression: str):
        return self._re_plate.sub(lambda x: self.random_plate(), expression)

    def random_plate(self):
        return self.faker.license_plate().replace('-', '')

    def uuid(self, expression: str):
        return self._re_uuid.sub(lambda x: self.faker.uuid4(), expression)

    def string(self, expression: str) -> str:
        """
        根据指定模板生成数据
        :param expression: 模板字符串
        :return:
        """
        for key, value in self.template.items():
            if key in expression:
                expression = value(expression)
        return expression

    def choice(self, source: List):
        """
        从列表中随机获取一项
        :param source: 列表
        :return:
        """
        return self.faker.random_element(source)

    @staticmethod
    def convert_string_to_datetime(result, fmt, raise_error=True):
        try:
            return datetime.strptime(result, fmt)
        except Exception as e:
            if raise_error:
                raise TypeError(f"【{result}】转换类型失败：{str(e)}")
            return result

    @staticmethod
    def convert_datetime_to_string(result, fmt, raise_error=True) -> datetime | str:
        try:
            return result.strftime(fmt)
        except Exception as e:
            if raise_error:
                raise TypeError(f"【{result}】转换类型失败：{str(e)}")
            return result

    def random_datetime(self, start, end='now', fmt='%Y-%m-%d %H:%M:%S') -> datetime:
        start = self.convert_string_to_datetime(start, fmt, False)
        end = self.convert_string_to_datetime(end, fmt, False)
        return self.convert_datetime_to_string(self.faker.date_time_between(start_date=start, end_date=end), fmt)

    def length_int(self, length):
        return self.faker.random_number(digits=length, fix_len=False)

    def range_int(self, max, min):
        return self.faker.random.randint(min, max)

    def length_float(self, int_length, float_length):
        integer = self.faker.random_number(digits=int_length + float_length, fix_len=False)
        return integer / (10 ** float_length)

    def range_float(self, max, min, float_length):
        return self.faker.random.randint(min, max) / (10 ** float_length)

    @staticmethod
    def other_timestamp(unit):
        match unit:
            case 's':
                return int(time.time())
            case 'ms':
                return int(time.time() * 1000)
            case _:
                return int(time.time())

    @staticmethod
    def map(source, key):
        if isinstance(source, str):
            source = dict(source)
        return source.get(key, None)
