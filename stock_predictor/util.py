# -*- coding: utf-8 -*-
import time;

class Need_Update:
    ONE_DAY = 86400;
    @classmethod
    def is_weekendToday( cls):
        today = time.localtime(time.time())
        if time.strftime( '%a',today)=='Sat' or time.strftime('%a',today)=='Sun':
            return True
        else:
            return False
            
    @classmethod        
    def Ndays_before( cls, N):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()-N*cls.ONE_DAY))
        
    @classmethod
    def get_yesterday( cls):
        today = time.localtime(time.time())
        if time.strftime('%a',today)=='Sun':
            return cls.Ndays_before(2)
        elif time.strftime('%a',today) =='Mon':
            return cls.Ndays_before(3)
        else:
            return cls.Ndays_before(1)
            
    @classmethod        
    def need_update( cls, date, today=None):
        if not today:
            today = time.localtime(time.time())
        else:
            today = time.strptime(today, '%Y-%m-%d')
        date_today = time.strftime('%Y-%m-%d',today)
        if not cls.is_weekendToday():
            if (today.tm_hour<15 and date != cls.get_yesterday()) \
            or (today.tm_hour>=15 and date != date_today):
                return True
            else:
                return False
        else:
            week = time.strftime('%a',time.strptime(date,'%Y-%m-%d'))
            if week != 'Fri':
                return True
            else:
                return False