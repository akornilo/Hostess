from flask import Flask
app = Flask(__name__)

#local
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localhost/anastassia'

# not so local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://dgczbrcwydbwsz:hOCd1n3h6xy5cf0Syfz_QyDn9A@ec2-107-22-163-140.compute-1.amazonaws.com:5432/d1mkrfsq4b9lv1'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.secret_key = "\x02\xe2C'\x95\xe5\xc2\x90\x11\x9f\xed\xe6\t\xd4\x8e`\xdbK\x945\xdaK\xcet"

import hostessapp.views
