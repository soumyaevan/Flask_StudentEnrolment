import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xc2\x9b\xf2\xb9\xc9]\x15\xd4\xae\xa8@\xfc*"Q\''
    MONGODB_SETTINGS = {'db':'STA_Enrolment',
                        'host':'mongodb://localhost:27017/STA_Enrolment'}