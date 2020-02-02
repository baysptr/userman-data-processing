def pretty_respon_users(obj):
    resp = {}
    resp['code'] = 200
    resp['message'] = "Your get all list data users"
    resp_data = []
    st = 0
    for i in obj:
        row = {}
        row['_id'] = str(i['_id'])
        row['nama'] = i['nama']
        row['username'] = i['username']
        # row['password'] = i['password']
        row['is_facebook'] = i['is_fb']
        row['is_twitter'] = i['is_tw']
        row['is_instagram'] = i['is_ig']
        row['is_telegram'] = i['is_tg']
        resp_data.insert(st, row)
        st += 1
    resp['data'] = resp_data
    return resp

def pretty_respon_monitor(obj):
    resp = {}
    resp['code'] = 200
    resp['message'] = "Your get all list data users"
    resp_data = []
    st = 0
    for i in obj:
        row = {}
        row['_id'] = str(i['_id'])
        row['text'] = i['text']
        row['userid'] = i['userid']
        row['source'] = i['source']
        row['type'] = i['type']
        row['tgl_post'] = i['tgl_post']
        resp_data.insert(st, row)
        st += 1
    resp['data'] = resp_data
    return resp

def pretty_respon_acrawler(obj):
    resp = {}
    resp['code'] = 200
    resp['message'] = "Your get all list data account crawler"
    resp_data = []
    st = 0
    for i in obj:
        row = {}
        row['_id'] = str(i['_id'])
        row['account_crawler'] = i['account_name']
        row['username'] = i['username']
        row['password'] = i['password']
        row['api_key'] = i['api_key']
        row['secret_key'] = i['secret_key']
        row['type'] = i['type']
        resp_data.insert(st, row)
        st += 1
    resp['data'] = resp_data
    return resp

def respon_action(code, message):
    resp = {}
    resp['code'] = code
    resp['message'] = message
    return resp

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")