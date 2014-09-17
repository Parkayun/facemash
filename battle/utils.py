# -*- coding:utf-8 -*-
def get_friends(fb_id, access_token):
    url = u'https://graph.facebook.com/' + str(fb_id) + '/friends?' \
        + u'fields=id,name,picture.type(square).width(1000).height(1000)&' \
        + u'access_token=' + access_token
    
    import requests
    res = requests.get(url)

    import json
    return json.loads(res.content)
