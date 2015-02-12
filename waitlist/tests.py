import unittest
import redis
from models import UserModelManager
UserModelManager.r = redis.Redis(db=1)

def setup_module(module):
    UserModelManager.r.flushdb()

def teardown_module(module):
    UserModelManager.r.flushdb()

class TestFunction:
    def test_all(self):

        # the system will be represented by a single user named root
        root_email = 'test@wondrous.co'
        if not UserModelManager.check_email(root_email):
            uuid = UserModelManager.add_email(root_email)
            data = UserModelManager.get_info(root_email)
            assert root_email == data['email']
            assert uuid == data['uuid']
            assert 0 == int(data['referrals'])
        emails = ['test'+str(i)+'@wondrous.co' for i in range(10)]

        for email in emails:
            if not UserModelManager.check_email(email):
                key = UserModelManager.add_email(email,uuid)

        data = UserModelManager.get_info(root_email)
        assert 10 == int(data['referrals'])
        assert 10 == len(UserModelManager.get_all_referred(root_email))
