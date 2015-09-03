# -*- coding: utf-8 -*-

from app import db


class Hbc(db.Model):
    """车身颜色"""
    __bind_key__ = 'hz_hbc'
    __tablename__ = 'hbc'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    jgsj = db.Column(db.DateTime)
    hphm = db.Column(db.String(12), default='-')
    kkdd_id = db.Column(db.String(9))
    hpys_id = db.Column(db.Integer)
    fxbh_id = db.Column(db.Integer)
    cdbh = db.Column(db.Integer)
    imgurl = db.Column(db.String(256))
    imgpath = db.Column(db.String(256))
    banned = db.Column(db.Integer, default=0)

    def __init__(self, date, jgsj, hphm='-', kkdd_id='441301001', hpys_id=1,
                 fxbh_id=1, cdbh=1, imgurl='', imgpath='', banned=0):
        self.date = date
        self.jgsj = jgsj
        self.hphm = hphm
        self.kkdd_id = kkdd_id
        self.hpys_id = hpys_id
        self.fxbh_id = fxbh_id
        self.cdbh = cdbh
        self.imgurl = imgurl
        self.imgpath = imgpath
        banned = banned

    def __repr__(self):
        return '<Hbc %r>' % self.id


class Hpys(db.Model):
    """车身颜色"""
    __bind_key__ = 'hz_hbc'
    __tablename__ = 'hpys'
    id = db.Column(db.Integer, primary_key=True)
    hpys_name = db.Column(db.String(10))
    cf_hpys = db.Column(db.String(16))

    def __init__(self, hpys_name, cf_hpys):
        self.hpys_name = hpys_name
        self.cf_hpys = cf_hpys

    def __repr__(self):
        return '<Hpys %r>' % self.id



