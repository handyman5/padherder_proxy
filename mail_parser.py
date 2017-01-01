import json
import os
import requests
import traceback

from datetime import datetime as DT
from datetime import timedelta

import tzlocal
import wx

import custom_events
from constants import *
from padherder_sync import *

class PADMail:
    def __init__(self, json):
        self.type = json['type']
        self.from_id = json['from']
        if self.from_id != 0:
            ID = str(self.from_id)
            self.from_id = ''.join(ID[x-1] for x in [1,5,9,6,3,8,2,4,7])
        else:
            self.from_id = "0"
        self.subject = json['sub']
        self.offered = json['offered']
        self.amount = json['amount']
        self.bonus_id = json['bonus_id']
        self.date = DT.strptime(json['date'], '%y%m%d%H%M%S')
        self.date = self.date.replace(tzinfo=tzlocal.get_localzone())
    
    def get_bonus_contents(self, monster_data, us_to_jp_map):
        if self.bonus_id == 0:
            return "None"
        elif self.bonus_id == 9900:
            return "%d coins" % self.amount
        elif self.bonus_id == 9901:
            if self.amount == 1:
                return "1 magic stone"
            else:
                return "%d magic stones" % self.amount
        elif self.bonus_id == 9902:
            return "%d Pal points" % self.amount
        else:
            try:
                jp_id = us_to_jp_map.get(self.bonus_id, self.bonus_id)
                return monster_data[jp_id]['name']
            except KeyError:
                pass


def parse_mail(mail_contents):
    mail = json.loads(mail_contents)
    #print mail
    ret = []
    for msg in mail['mails']:
        # Pal pts: {"id":126887704,"from":0,"date":"160417103251","fav":0,"sub":"*Official Twitch Stream Rewards*","type":3,"offered":0,"bonus_id":9902,"amount":1000}
        ret.append(PADMail(msg))
    return ret


if __name__ == '__main__':
    app = wx.App(False)
    config = wx.Config("padherder_proxy_testing")
    wx.ConfigBase.Set(config)

    session = requests.Session()
    session.headers = headers
    # Limit the session to a single concurrent connection
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1))
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1))
    
    raw_monster_data = get_cached_data(session, 8, os.path.join(module_path(), 'monster_data.pickle'), URL_MONSTER_DATA)
    # Build monster data map and us->jp mapping
    us_to_jp_map = {}
    monster_data = {}
    for monster in raw_monster_data:
        if 'us_id' in monster:
            us_to_jp_map[monster['us_id']] = monster['id']
        monster_data[monster['id']] = monster

    f = open('captured_mail.txt', "r")
    contents = f.read()
    f.close()

    mails = parse_mail(contents)
    
    for mail in mails:
        print mail.get_bonus_contents(monster_data, us_to_jp_map)