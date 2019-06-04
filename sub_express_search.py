#-*- coding:utf-8 -*-
#-----------------------------------------------------------------------------------
#------------*-------------打印分项指定时间mongodb查询命令------------*-------------
#-----------------------------------------------------------------------------------

import MySQLdb
import pymongo
import re
from datetime import datetime


def SUB_Search(BUILDID,Stime,Etime):
    client = pymongo.MongoClient('mongodb://192.168.1.21:27017')
    modb=client.secom
    
    db=MySQLdb.connect("192.168.1.21","se_writer","Se@#w2018","energy_monitor")
    cur=db.cursor()
    sql='''SELECT BUILDID,NUMBER,EXPRESSION FROM `DmSubentry` WHERE BUILDID=%s'''
    cur.execute(sql,BUILDID)
    res=cur.fetchall()
    for i in res:
        BUILDID1=BUILDID[0]
        print
        print 
        print i[0]+" "+i[1]+" "+i[2]
        filename='T_SUB_HOUR_'+BUILDID1+"_"+i[1]+"_"+i[2]
        print filename
        subid1=i[1]
        print '''db.T_SUB_HOUR.find({"BID":"%s","CD":"%s","TM":{"$gte":ISODate("%sZ"),"$lte":ISODate("%sZ")}}).sort({"TM" :-1})'''%(BUILDID1,subid1,Stime.isoformat(),Etime.isoformat())

        mors0=modb.T_SUB_HOUR.find({'BID':BUILDID1,"CD":subid1,"TM":{"$gte": Stime,"$lte": Etime}})
        print('all_count',mors0.count())
        print
        sub_list=re.split("[|\+|\-|\*|\/]",i[2])
        for sub_len in sub_list:
            subid=sub_len[1:-1]
            #print subid
            #BUILDID1=BUILDID[0]
            #print BUILDID[0]
            if sub_len[0:1]=="<":
                #print "查分项能耗"
                filename='T_SUB_HOUR_'+BUILDID1+"_"+i[1]+"_"+subid
                print filename
                print '''db.T_SUB_HOUR.find({"BID":"%s","CD":"%s","TM":{"$gte":ISODate("%sZ"),"$lte":ISODate("%sZ")}}).sort({"TM" :-1})'''%(BUILDID1,subid,Stime.isoformat(),Etime.isoformat())
                print
                mors1=modb.T_SUB_HOUR.find({'BID':BUILDID1,"CD":subid,"TM":{"$gte": Stime,"$lte": Etime}})
                print('sub_all_count',mors1.count())
                #for sub_hour in mors1:
                    #print sub_hour

                #mors=modb.T_SUB_HOUR.find_one({'BID':BUILDID1,"CD":subid})
                #if(mors):
                    #CURTOTAL=mors['TM']
                    #print CURTOTAL
            elif sub_len[0:1]=="[":
                filename='T_HT_HOUR_'+BUILDID1+"_"+i[1]+"_"+subid
                print filename
                print '''db.T_HT_HOUR.find({"BID":"%s","MID":"%s","TM":{"$gte":ISODate("%sZ"),"$lte":ISODate("%sZ")}}).sort({"TM" :-1})'''%(BUILDID1,subid,Stime.isoformat(),Etime.isoformat())
                mors2=modb.T_HT_HOUR.find({'BID':BUILDID1,"MID":subid,"TM":{"$gte": Stime,"$lte": Etime}})
                print('sub_all_count',mors2.count())
                print
                    
                

    

    

if __name__=="__main__":
    BUILDID=['440300A080']
    Stime=datetime(2018,11,17,23,0)
    Etime=datetime(2018,11,20,0,0)
    SUB_Search(BUILDID,Stime,Etime)
