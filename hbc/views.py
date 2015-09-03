# -*- coding: utf-8 -*-
from functools import wraps

import arrow
from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, app, api, auth, limiter, logger, cache
from models import Hbc, Hpys
from help_func import *


def verify_addr(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return {'status': '403.6',
                    'error': u'禁止访问:客户端的 IP 地址被拒绝'}, 403
        return f(*args, **kwargs)
    return decorated_function

@auth.verify_password
def verify_password(username, password):
    if username.lower() == 'admin':
        user = Users.query.filter_by(username='admin').first()
    else:
        return False
    if user:
        return sha256_crypt.verify(password, user.password)
    return False


def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Access-Token'):
            return {'error': 'access_token error'}, 401
        token_result = verify_auth_token(request.headers['Access-Token'],
                                         app.config['SECRET_KEY'])
        if not token_result:
            return {'error': 'access_token invalid'}, 401
        elif token_result == 'expired':
            return {'error': 'access_token expired'}, 401
        g.uid = token_result['uid']
        g.scope = set(token_result['scope'])

        return f(*args, **kwargs)
    return decorated_function

def verify_scope(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print 'scope'
        try:
            scope = '_'.join([request.path[1:], request.method.lower()])
            print scope
        except Exception as e:
            print (e)
        if 'all' in g.scope or scope in g.scope:
            pass
        else:
            return {'status': 405, 'error': 'Method Not Allowed'}, 405
        return f(*args, **kwargs)
    return decorated_function


class Index(Resource):

    def get(self):
        return {
            'hbc_url': 'http://%s:%s/hbc/' % (request.remote_addr, app.config['PORT'])
        }, 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class HbcListV1(Resource):
    decorators = [limiter.limit("600/minute"), verify_addr]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('jgsj', type=unicode, required=True,
                            help='A jgsj field is require', location='json')
        parser.add_argument('hphm', type=unicode, required=True,
                            help='A hphm field is require', location='json')
        parser.add_argument('kkdd_id', type=unicode, required=True,
                            help='A kkdd_id field is require', location='json')
        parser.add_argument('hpys_id', type=int, required=True,
                            help='A hpys field is require', location='json')
        parser.add_argument('fxbh_id', type=int, required=True,
                            help='A fxbh field is require', location='json')
        parser.add_argument('cdbh', type=int, required=True,
                            help='A cdbh field is require', location='json')
        parser.add_argument('imgurl', type=unicode, required=True,
                            help='A imgurl field is require', location='json')
        parser.add_argument('imgpath', type=unicode,
                            help='A imgurl field is require', location='json')
        args = parser.parse_args()

        t = arrow.get(request.json['jgsj']).replace(hours=-8).to('local')
        hbc = Hbc(date=t.format('YYYY-MM-DD'),
                  jgsj=t.datetime,
                  hphm=request.json['hphm'],
                  kkdd_id=request.json['kkdd_id'],
                  hpys_id=request.json['hpys_id'],
                  fxbh_id=request.json['fxbh_id'],
                  cdbh=request.json['cdbh'],
                  imgurl=request.json['imgurl'],
                  imgpath=request.json.get('imgpath', ''),
                  banned=0)
        db.session.add(hbc)
        db.session.commit()

        result = row2dict(hbc)
        result['jgsj'] = str(result['jgsj'])
        del result['date']
        return result, 201


api.add_resource(Index, '/')
api.add_resource(HbcListV1, '/hbc')



