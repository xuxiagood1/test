#-*- coding:utf-8-*-
import re
import MySQLdb
import pymongo
import os

print os.getcwd()
path=os.getcwd()+"\\sub_express.xls"
if os.path.exists(path):
    os.remove(path)
BUILD_ID=['440300H008']
dt='20180414204500'
db=MySQLdb.connect("192.168.1.17","root","root2018!@#","smp_365_emx_dev_1_0")
cur=db.cursor()
sql='''SELECT SUB_CODE,EXPRESSION FROM t_emx_subentry WHERE BUILD_ID=%s'''
cur.execute(sql,BUILD_ID)
res1=cur.fetchall()
for i in res1:
    if(i[1]):
        print i[0]+ ':'+i[1]
    str_id=BUILD_ID[0]+'-'+bytes(i[0])+'-'+dt
    client = pymongo.MongoClient('mongodb://192.168.1.90:27017')
    modb=client.emx_history
    mors=modb.T_MG_SUB_TIME.find_one({'_id':str_id})
    if(mors):
        CURTOTAL=mors['CURTOTAL']
        print i[0]+ '=			'+bytes(CURTOTAL)
        f=open('sub_express.xls',"a")
        f.write(i[0]+ '\t'+bytes(CURTOTAL)+'\t'+i[1]+'\r')
        f.close()
    sub_str='<'
    met_str='['
    sub_id=i[0]
    sub_express=i[1]
    
    if(sub_express) is  None:
        print 'no subentry'
    elif(sub_express.find(sub_str)>=0):
        CURTOTAL1s=[]
        p1=r'<.+?>'
        pat1=re.compile(p1)
        sub_express1=pat1.sub("%s",sub_express)
        #print sub_express1
        for i in range(0,len(pat1.findall(sub_express))):
            #print pat1.findall(sub_express)[i][1:-1]
            sub=pat1.findall(sub_express)[i][1:-1]
            str_id1=BUILD_ID[0]+'-'+sub+'-'+dt
            print 
            mors1=modb.T_MG_SUB_TIME.find_one({'_id':str_id1})
            
            if(mors1):
                CURTOTAL1=mors1['CURTOTAL']
                CURTOTAL1s.append(CURTOTAL1)
                print sub+'			'+bytes(CURTOTAL1)
                f=open('sub_express.xls',"a")
                f.write(sub+'\t'+bytes(CURTOTAL1)+'\r')
                f.write(sub+'\t'+bytes(CURTOTAL1)+'\r')
                f.close()
            else:
                CURTOTAL1=0
                CURTOTAL1s.append(CURTOTAL1)
        sdf=tuple(CURTOTAL1s)
        #print sdf   
        ss=sub_express1%sdf
        f=open('sub_express.xls',"a")
        f.write('\t'+bytes(eval(ss))+'\t'+'total'+'\r')

        f.close()               
        
    elif(sub_express.find(met_str)>=0):
        CURTOTAL1ss=[]
        p2=r'\[.+?\]'
        pat1=re.compile(p2)
        sub_express2=pat1.sub("%s",sub_express)
        for i in range(0,len(pat1.findall(sub_express))):
            #print pat1.findall(sub_express)[i][1:-1]
            met=pat1.findall(sub_express)[i][1:-1]
            

            str_id2=BUILD_ID[0]+'-'+met+'-'+dt
            print 
            mors2=modb.T_MG_HT_TIME.find_one({'_id':str_id2})
            if(mors2):
                CURTOTAL2=mors2['CURTOTAL']
                CURTOTAL1ss.append(CURTOTAL2)
                print met+'		'+bytes(CURTOTAL2)
                f=open('sub_express.xls',"a")
                f.write('\''+met+'\t'+bytes(CURTOTAL2)+'\r')
                f.close()
            else:
                CURTOTAL2=0
                CURTOTAL1ss.append(CURTOTAL2)
        sdf=tuple(CURTOTAL1ss)
        print sdf   
        ss=sub_express2%sdf
        print ss
        f=open('sub_express.xls',"a")
        f.write('\t'+bytes(eval(ss))+'\t'+'total'+'\r')

        f.close()               
        
            #f=open('sub_express.xls',"a")
            #f.write('\r')
            #f.close()
