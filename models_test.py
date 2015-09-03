# -*- coding: utf-8 -*-
import arrow

from hbc import db
from hbc.models import Hpys, Hbc


def hpys_test():
    hpys = Hpys.query.all()
    print hpys
    for i in hpys:
        print i.hpys_name

def hbc_add():
    datetime = '2013-05-11 21:23:58'
    t = arrow.get(datetime).replace(hours=-8)
    hbc = Hbc(date=t.format('YYYY-MM-DD'), jgsj=t.datetime, hphm='粤L12345',
              kkdd_id='441302002', hpys_id=2, fxbh_id=4, cdbh=5,
              imgurl='httP;//123', imgpath='c:123', banned=0)
    db.session.add(hbc)
    db.session.commit()
    print hbc.id


if __name__ == '__main__':
    #hpys_test()
    hbc_add()
