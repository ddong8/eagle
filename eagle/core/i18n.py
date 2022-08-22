# -*- coding: utf-8 -*-
"""
本模块提供i18n国际化翻译

@Author  : donghaixing
@File    : i18n.py
@Time    : 08/10/2021 11:24 AM
"""

import gettext

from loguru import logger


class Translator():
    """
    i18n国际化翻译器
    用户可以调用setup来更改当前locale
    """

    def __init__(self):
        self.translation = None

    def __call__(self, value):
        if self.translation:
            return self.translation.gettext(value)
        else:
            return value

    def setup(self, app, locales, lang):
        try:
            self.translation = gettext.translation(app, locales, [lang])
        except IOError:
            logger.warning(
                'language(%s) files not found, no translation will be used', lang)


_ = Translator()

