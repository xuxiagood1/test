#-*- coding:utf-8 -*-
#-----------------------------------------------------------------------------------
#------------*-------------根据错误表达式导出分项指定时间能耗到EXCEL------------*-------------
#-----------------------------------------------------------------------------------
import MySQLdb
import pymongo
import re
from datetime import datetime
import xlrd,xlwt,json

def Read_err_express(x,y):
    file_path=r'err_express.xls'
    file_path=file_path.decode('utf-8')
    data=xlrd.open_workbook(file_path)
    table=data.sheet_by_name("Sheet1")
    nrows=table.nrows
    nclos=table.ncols
    cell_values=table.cell(x,y).value
    tlen=len(cell_values)
    tname=cell_values[0:10]
    tbuid=cell_values[11:21]
    tsub=cell_values[22:27]
    texp=cell_values[28:]
    print tname
    print tbuid
    print tsub
    tlist= [] 
    texpLen=len(cell_values[28:])
    sub_list = re.split("[|\+|\-|\*|\/]",texp)
    for sub_len in sub_list:
        subid=sub_len[1:-1]
        tlist.append(subid)
        print subid
    return tname,tbuid,tsub,texp,tlist
    


def SUB_Search(BUILDID,subid1,Stime,Etime):
    client = pymongo.MongoClient('mongodb://192.168.1.21:27017')
    modb=client.secom
    mors0=modb.T_SUB_HOUR.find({'BID':BUILDID,"CD":subid1,"TM":{"$gte": Stime,"$lte": Etime}})
    mors1=modb.T_SUB_HOUR.find({'BID':'440300B047',"CD":'01000',"TM":{"$gte": Stime,"$lte": Etime}})
    print mors0.count()
    #for i in mors0:
        #print i
    
def HT_Search(BUILDID,subid1,Stime,Etime):
    client = pymongo.MongoClient('mongodb://192.168.1.21:27017')
    modb=client.secom
    mors2=modb.T_HT_HOUR.find({'BID':BUILDID,"MID":subid1,"TM":{"$gte": Stime,"$lte": Etime}})
    
    #print mors2.count()
    return mors2[0]['TTL']
    #for i in mors2:
        #print i['TTL']
        #return i['TTL']




if __name__=="__main__":
    Stime=datetime(2018,11,21,15,0)
    Etime=datetime(2018,11,21,15,30)
    excelCell=Read_err_express(1,0)
    #print excelCell[0]
    #tname=excelCell[0]
    BUILDID=excelCell[1].encode("utf-8")
    subid1=excelCell[2].encode("utf-8")
    subid_ht=excelCell[4]
    #BUILDID='440300B047'
    for i  in range(0,len(subid_ht)):
        subid2=subid_ht[i].encode("utf-8")
        if (len(subid2)>6):
            #subid2='000000210850'
            TTL=HT_Search(BUILDID,subid2,Stime,Etime)
            
        elif(len(subid2)<6):
            TTL=SUB_Search(BUILDID,subid1,Stime,Etime)
            print TTL
    
