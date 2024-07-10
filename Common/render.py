
from jinja2 import Environment
from functools import partial

from Common import logger
from Common.random_data import RandomData


class Render(RandomData):

    def __init__(self):
        super().__init__()
        self.env = Environment()
        self.env.globals.update({
            'Template': self.string,
            'Choice': self.choice,
            'Datetime': self.random_datetime,
            'LengthInt': self.length_int,
            'RangeInt': self.range_int,
            'LengthFloat': self.length_float,
            'RangeFloat': self.range_float,
            'Timestamp': self.other_timestamp,
            'Map': self.map,
            'ImageUrl': self.image_url,
            "RandomPlate": self.random_plate
        })
        self.env.filters.update({
            'int': partial(self.set_type, value_type=int),
            'list': partial(self.set_type, value_type=list),
            'dict': partial(self.set_type, value_type=dict),
            'float': partial(self.set_type, value_type=float),
        })
        self.type = None

    def set_type(self, value, value_type):
        self.type = value_type
        return value

    def render(self, string, params):
        if all(['{{' not in string, "{%" not in string]):
            # print(string, '没有匹配上')
            return string
        try:
            string = self.env.from_string(string).render(params)
            # return result or string
        except Exception as e:
            logger.error(f"{string}渲染失败：{e}")

        if self.type is not None:
            try:
                string = self.type(string)
            except Exception as e:
                logger.error(f'【{string}】转换类型错误:{str(e)}')
            finally:
                self.type = None
        if string == 'None':
            string = None
        return string

    def render_dict(self, dct, params):
        if isinstance(dct, dict):
            for k, v in dct.items():
                # self.render_dict(dct[k], params)
                dct[k] = self.render_dict(v, params)

        elif isinstance(dct, str):
            return self.render(dct, params)

        elif isinstance(dct, list | tuple):
            for i, a in enumerate(dct):
                dct[i] = self.render_dict(a, params)
        return dct


if __name__ == '__main__':
    aa = Render().render_dict({"a": "{{ b|int }}"}, {"b": 1})
    print(type(aa["a"]))