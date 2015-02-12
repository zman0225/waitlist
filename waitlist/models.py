#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Created by: Ziyuan Liu
#
#

import base64
import shortuuid
import redis
import re

# get a UUID - URL safe, Base64
def get_a_uuid():
    return shortuuid.uuid().lower()

def check_email(str_to_check):
    pattern = '[^@]+@[^@]+\.[^@]+'
    return True if str_to_check and re.match(pattern, str_to_check.lower()) else False

class UserModelManager:
    r = redis.Redis() # default local redis
    EMAIL = 'email'
    REFERRALS = 'referrals'
    ID = 'uuid'
    REFERRED ='referred:{0}'
    USER_COUNT = 'total_users'

    @classmethod
    def get_total_users(cls):
        cnt = cls.r.get(cls.USER_COUNT)
        return cnt if cnt else 0

    @classmethod
    def check_email(cls,email):
        return check_email(email)

    @classmethod
    def email_exists(cls,email):
        email = email.lower()
        return cls.r.exists(email)

    @classmethod
    def add_email(cls,email,referer="root"):
        email = email.lower()

        if not check_email(email):
            return False

        uuid = get_a_uuid().lower()
        while cls.r.exists(uuid):
            uuid = get_a_uuid().lower()

        data = {cls.EMAIL:email,
            cls.REFERRALS:0}

        pipe = cls.r.pipeline()
        pipe.hmset(uuid,data) # uuid -> data
        pipe.set(email,uuid) # email -> uuid (secondary index)
        if cls.r.exists(cls.USER_COUNT):
            pipe.incr(cls.USER_COUNT)
        else:
            pipe.set(cls.USER_COUNT,1)

        if referer:
            pipe.hincrby(referer,cls.REFERRALS,1)
            ref_key = cls.REFERRED.format(referer)
            pipe.lpush(ref_key,uuid)
        pipe.execute()
        return uuid

    @classmethod
    def get_info(cls,email):
        email = email.lower()
        uuid = cls.r.get(email)

        if not uuid:
            return None

        pipe = cls.r.pipeline()
        pipe.hget(uuid,cls.EMAIL)
        pipe.hget(uuid,cls.REFERRALS)
        email,referrals = pipe.execute()

        return {cls.EMAIL:email,cls.REFERRALS:referrals,cls.ID:uuid}

    @classmethod
    def get_all_referred(cls,email):
        email = email.lower()
        uuid = cls.r.get(email)

        if not uuid:
            return None

        llen = cls.r.hget(uuid,cls.REFERRALS)
        ref_key = cls.REFERRED.format(uuid)
        return cls.r.lrange(ref_key,0,llen)
