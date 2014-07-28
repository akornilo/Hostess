from flask import Flask
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sis:redcarnation@localhost/hostess'

#local
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/anastassia'

# not so local
#'postgres://dgczbrcwydbwsz:hOCd1n3h6xy5cf0Syfz_QyDn9A@ec2-107-22-163-140.compute-1.amazonaws.com:5432/d1mkrfsq4b9lv1'

app.secret_key = "\x02\xe2C'\x95\xe5\xc2\x90\x11\x9f\xed\xe6\t\xd4\x8e`\xdbK\x945\xdaK\xcet"

import hostessapp.views
