from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sis:redcarnation@localhost/hostess'
app.secret_key = "\x02\xe2C'\x95\xe5\xc2\x90\x11\x9f\xed\xe6\t\xd4\x8e`\xdbK\x945\xdaK\xcet"

import hostessapp.views
