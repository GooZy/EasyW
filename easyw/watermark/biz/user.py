#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:11
# @Author  : GUO Ziyao
from easyw.watermark.service.user import UserService


class UserBiz(object):

    @classmethod
    def register_user(cls, username, password, password2):
        if not username or not password or not password2:
            return "Please fill in all textbox!"
        else:
            result = UserService.get_user_by_name(username)
            if result:
                return "Username exist!"
            elif password != password2:
                return "Entered passwords differ!"
        return None
