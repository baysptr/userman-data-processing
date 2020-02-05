from flask import Flask, jsonify, request
import pymongo
from argon2 import PasswordHasher
from bson.objectid import ObjectId
from datetime import datetime
from helper import pretty_respon_users, str2bool, respon_action, pretty_respon_acrawler, pretty_respon_monitor, pretty_respon_woc, pretty_respon_trending, pretty_respon_minfluencer
from flask_jwt_extended import (
    JWTManager, jwt_optional,jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
client = pymongo.MongoClient('mongodb://30.30.30.44:27017/')
db = client['sosmon_ori']
um = db['user_management']
acw = db['account_crawler']
mon = db['monitor']
ori_data = db['ori_data']
woc = db['word_cloud']
setxt = db['text_sentiment']
ph = PasswordHasher()

app.config['JWT_SECRET_KEY'] = 'super-secret-super-rahasia-xcjvhaweurhvskjhn'  # Change this!
jwt = JWTManager(app)

# is Structure storing to collection user_management
# users = {}
# users['nama'] = "Paijo"
# users['username'] = "paijo"
# users['password'] = ph.hash("1qaz2wsx3edc")
# users['is_fb'] = True
# users['is_tw'] = True
# users['is_ig'] = True
# users['is_tg'] = True
# um.insert(users)
# print(users)
# =====================================================

# is structure storing to collection account_crawler
# account_crawler = {}
# account_crawler['account_name'] = "Cemungut eaaa"
# account_crawler['username'] = "cemungut.ea"
# account_crawler['password'] = "1qaz2wsx3edc"
# account_crawler['api_key'] = "https://api.exampleapi.id/"
# account_crawler['secret_key'] = "213edcvbght56yuhgbhy7"
# account_crawler['type'] = "twitter" # twitter / facebook / telegram / instagram
# acw.insert(account_crawler)
# print(account_crawler)
# =====================================================


# is structure storing to collection monitor
# monitor = {}
# monitor['text'] = "#hti" # hashtag atau user ex: #hti atau @hti_official
# monitor['userid'] = "1234567" # id user yang akan dimonitor ex: fahri hamzah > id > 12345678
# monitor['source'] = ["FACEBOOK", "TWITTER", "INSTAGRAM", "ALL"] # user dimedia mana yang dimonitoring
# monitor['type'] = "HASHTAG" # hashtag atau user type baris ini
# monitor['tgl_post'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
# mon.insert(monitor)
# print(monitor)
# =====================================================


@app.route('/', methods=['GET', 'POST'])
def init():
    return "Hallo sobat!"

# =========================================================================
# USER ROLE MANAGEMENT
# =========================================================================

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'isAuth': False,
        'status': 'Token has expired'
    }), 401

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = ph.hash(request.json['password']).hexdigest()
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    us = um.find_one( { "username": username,"password":password  } )
    if not us:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity={   'username':username,
                                                    'akses': [
                                                            {'is_fb':us['is_fb']},
                                                            {'is_tw':us['is_tw']},
                                                            {'is_ig':us['is_ig']},
                                                            {'is_tg':us['is_tg']},
                                                            {'is_superadmin':us['is_superadmin']}
                                                            ]})
    return jsonify(access_token=access_token), 200

@app.route('/list_users', methods=['GET'])
@jwt_required
def list_users():
    data = um.find({"is_superadmin": False})
    return jsonify(pretty_respon_users(data))

@app.route('/where_id/<string:_id>', methods=['GET'])
@jwt_required
def where_id(_id):
    data = um.find({"_id": ObjectId(_id)})
    return jsonify(pretty_respon_users(data))

@app.route('/delete_users', methods=['POST'])
@jwt_required
def delete_users():
    req = request.values
    id = req['id']
    um.delete_one({'_id': ObjectId(id)})
    return jsonify(respon_action(200, "Success delete data!"))

@app.route('/add_users', methods=['POST'])
@jwt_required
def add_users():
    users = {}
    req = request.values
    users['nama'] = req['nama'].upper()
    users['username'] = req['username']
    users['password'] = ph.hash(req['password'])
    users['is_fb'] = str2bool(req['facebook'])
    users['is_tw'] = str2bool(req['twitter'])
    users['is_ig'] = str2bool(req['instagram'])
    users['is_tg'] = str2bool(req['telegram'])
    users['is_superadmin'] = False
    users['tgl_post'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    um.insert(users)
    return jsonify(respon_action(200, "Success save data!"))

@app.route('/update_role', methods=['POST', 'PUT'])
@jwt_required
def update_role():
    users = {}
    req = request.values
    id = req['id']
    users['nama'] = req['nama'].upper()
    users['username'] = req['username']
    # users['password'] = ph.hash(req['password'])
    users['is_fb'] = str2bool(req['facebook'])
    users['is_tw'] = str2bool(req['twitter'])
    users['is_ig'] = str2bool(req['instagram'])
    users['is_tg'] = str2bool(req['telegram'])
    # users['is_superadmin'] = False
    users['tgl_post'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    um.update({"_id": ObjectId(id)}, {"$set": users})
    return jsonify(respon_action(200, "Success update data!"))

# =========================================================================
# ACCOUNT CRAWLER MANAGEMENT
# =========================================================================

@app.route("/add_account_craw", methods=['POST'])
def add_account_craw():
    req = request.values
    account_crawler = {}
    account_crawler['account_name'] = req['account_name'].upper()
    account_crawler['username'] = req['username']
    account_crawler['password'] = req['password']
    account_crawler['api_key'] = req['api_key']
    account_crawler['secret_key'] = req['secret_key']
    account_crawler['type'] = req['type'].upper()  # twitter / facebook / telegram / instagram
    acw.insert(account_crawler)
    return jsonify(respon_action(200, "Success save data account crawler!"))

@app.route('/update_account', methods=['POST', 'PUT'])
def update_account():
    req = request.values
    id = req['id']
    account_crawler = {}
    account_crawler['account_name'] = req['account_name'].upper()
    account_crawler['username'] = req['username']
    account_crawler['password'] = req['password']
    account_crawler['api_key'] = req['api_key']
    account_crawler['secret_key'] = req['secret_key']
    account_crawler['type'] = req['type'].upper()  # twitter / facebook / telegram / instagram
    acw.update({"_id": ObjectId(id)}, {"$set": account_crawler})
    return jsonify(respon_action(200, "Success update data!"))

@app.route('/delete_account_crawler', methods=['POST'])
def delete_account_craw():
    req = request.values
    id = req['id']
    acw.delete_one({'_id': ObjectId(id)})
    return jsonify(respon_action(200, "Success delete data!"))

@app.route('/list_account_crawler', methods=['GET'])
def list_acrawler():
    data = acw.find()
    return jsonify(pretty_respon_acrawler(data))

@app.route('/where_id_account/<string:_id>', methods=['GET'])
def where_id_account(_id):
    data = acw.find({"_id": ObjectId(_id)})
    return jsonify(pretty_respon_acrawler(data))

# =========================================================================
# MONITOR TARGET MANAGEMENT
# =========================================================================

@app.route('/list_monitor', methods=["GET"])
def list_monitor():
    obj = mon.find()
    return jsonify(pretty_respon_monitor(obj))

@app.route('/add_target', methods=["POST"])
def add_target():
    req = request.values
    source = req['source'].split(',') # input harus dengan pemisah koma (,)
    monitor = {}
    monitor['text'] = req['text']
    monitor['userid'] = req['userid']
    monitor['source'] = source
    monitor['type'] = req['type']
    monitor['tgl_post'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    mon.insert(monitor)
    return jsonify(respon_action(200, "Success save data!"))


# =========================================================================
# FRONTEND API
# =========================================================================

@app.route('/dashboard', methods=["POST"])
def dashbord():
    req = request.values
    mentions = ori_data.find({'text':{  '$regex' : ".*"+req['hastag']+".*"},'source':{ '$in':req['sources'] } }).count()
    positiv = ori_data.find({'text':{  '$regex' : ".*"+req['hastag']+".*"},'source':{ '$in':req['sources'] },'sentiment':1 }).count()
    negativ = ori_data.find({'text':{  '$regex' : ".*"+req['hastag']+".*"},'source':{ '$in':req['sources'] },'sentiment':2 }).count()
    netral = ori_data.find({'text':{  '$regex' : ".*"+req['hastag']+".*"},'source':{ '$in':req['sources'] },'sentiment':0 }).count()
    data = {
        'hastag': req['hastag'],
        'sources': req['sources'],
        'mentions_count': mentions,
        'mentions_positiv': positiv,
        'mentions_negativ': negativ,
        'mentions_netral': netral,
    }

    return jsonify(data), 200

@app.route('/trending/<int:limit>', methods=['GET'])
def trending(limit):
    trend = ori_data.find().sort([("total_like", -1)]).limit(limit)
    data = pretty_respon_trending(trend)
    return jsonify(data), 200

@app.route('/word_cloud/<int:limit>', methods=['GET'])
def word_cloud(limit):
    w = woc.find({}).sort([("instagram.count", -1), ("telegram.count", -1), ("facebook.count", -1), ("twitter.count", -1)]).limit(limit)
    data = pretty_respon_woc(w, 200, "Word Clouds")
    return jsonify(data), 200

@app.route('/categori_count', methods=['GET'])
def categori_count():
    ig = ori_data.find({"source": "instagram"})
    tw = ori_data.find({"source": "twitter"})
    tg = ori_data.find({"source": "telegram"})
    fb = ori_data.find({"source": "facebook"})
    data = {
        "code": 200,
        "message": "All count data sources",
        "data": {
            "instagram": ig.count(True),
            "twitter": tw.count(True),
            "telegram": tg.count(True),
            "facebook": fb.count(True)
        }
    }
    return jsonify(data), 200

@app.route('/sentiment_count', methods=['GET'])
def setiment_count():
    pos = setxt.find({"sentiment": "positive"})
    neg = setxt.find({"sentiment": "negative"})
    neu = setxt.find({"sentiment": "neutral"})
    data = {
        "code": 200,
        "message": "All count data sentiment",
        "data": {
            "positive": pos.count(True),
            "negative": neg.count(True),
            "neutral": neu.count(True)
        }
    }
    return jsonify(data), 200

@app.route("/most_user/<int:limit>", methods=['POST'])
def most_user(limit):
    req = request.values
    sources = req['sources'].split(',')
    sbc = ori_data.aggregate([
        { "$match": { "text": {  '$regex' : ".*"+req['hastag']+".*"},"source":{ '$in':sources } } },
        { "$group": {
            "_id": {
                "user_id": "$user_id"
            },
            "count": { "$sum": 1 }
        }},
        {"$sort":{"count":-1}},
        {"$limit":limit}
    ])
    data = pretty_respon_minfluencer(sbc)
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)