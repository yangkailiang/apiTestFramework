from Common.utils import str_to_num, str_to_dict, str_to_bool, str_to_list
from selenium.webdriver import ChromeOptions, Chrome, chrome, Firefox, FirefoxOptions, firefox

from selenium.webdriver.chrome.service import Service


PARAMS = {
    'String': str,
    'Int': str_to_num,
    'Float': str_to_num,
    'BooLean': str_to_bool,
    'JSONObject': str_to_dict,
    'JSONArray': str_to_list,
}

BROWSER_MAP = {
    1: {
        'option': ChromeOptions,
        'driver': Chrome,
        'service': chrome.service.Service
    },
    2: {
        'option': FirefoxOptions,
        'driver': Firefox,
        'service': firefox.service.Service
    },
}


