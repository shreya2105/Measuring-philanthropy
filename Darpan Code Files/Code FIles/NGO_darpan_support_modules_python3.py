# -*- coding: utf-8 -*-
import json
import sqlite3
from datetime import datetime
null=None


'''
HOW TO USE

PRELIMINARIES
1. download 'NGO_darpan.db' and this file and store it in the same directory as your main script
2. make sure the following module is installed in python : sqlite3
3. at the top of your code after all the imports write: "import NGO_darpan_support_modules"


IN YOUR CODE:

1. before downloading the data for any NGO, you want to check whether the id already exists in the database:
check=processDB.checkID(id)
if check is True:
    ###then proceed with the downloading of data and go below###



2. assuming you have compiled a list of data from processing each id (i.e. the info for each id has been returned and compiled in a python list called dataout), and you want to insert it into the database, at that point in the code :
    for item in dataout:
        item=processDB.processDict(item)
        processDB.AppendToDB(dataout)
        processDB.closeConnection()


'''



class sqlite_interface:
    def __init__(self):
        self._conn=sqlite3.connect('NGO_darpan.db')
        self._c=self._conn.cursor()

    def closeConnection(self):
        self._conn.close()
        


    def processDict(self,d):
      for k, v in d.items():
        if isinstance(v, dict):
          self.processDict(v)
        else:
          if isinstance(v,str):
            d[k]=v.encode('utf-8').decode('utf-8')
          else:
            d[k]=v

      return d

    def checkID(self,id):
        id=int(id)
        dat=[]
        for row in self._c.execute('''select * from main where digitalID=?''',(id,)):
            dat.append(row)
 #       self._conn.close()

        if len(dat)>0:
            return False
        else:
            return True


    def AppendToDB(self,lst):

            main_table_keys=["Email","Major_Activities1","Mobile","Off_phone1","UniqueID","ngo_name","ngo_url","pan_updDocId","reg_updDocId","issues_working_db","operational_district_db","operational_states_db","StateName","TypeDescription","fcrano","ngo_reg_date","nr_actName","nr_add","nr_city","nr_isFcra","nr_orgName","nr_regNo","nr_updDocId","reg_name","status","digitalID","timestamp"]

            member_table_keys=["digitalID","DesigName","EmailId","FName","LName","MobileNo","aadhaar_updDocId","pan_updDocId","timestamp"]

            source_table_keys=["digitalID","amount_sanctioned","datefrom","dateto","deptt_name","purpose","sourcefund","timestamp"]


            main_table_data=[]
            member_info_data=[]
            source_info_data=[]

            for row in lst:
                main_dict={}
                main_dict['status']=str(row['status']).encode('utf-8')
                for key,val in row['infor']['0'].items():
                    main_dict[key]=val
                main_dict['issues_working_db']=row['infor']['issues_working_db'].encode('utf-8')
                main_dict['operational_district_db']=row['infor']['operational_district_db'].encode('utf-8')
                main_dict['operational_states_db']=row['infor']['operational_states_db'].encode('utf-8')
                for key,val in row['registeration_info'][0].items():
                    main_dict[key]=val
                main_dict['digitalID']=int(row['digitalID'])

                main_dict["ngo_reg_date"]=datetime.strptime(main_dict["ngo_reg_date"],"%d-%m-%Y")

                main_dict["timestamp"]=datetime.now()

                #print json.dumps(main_dict,indent=4)
                outputrow=tuple([main_dict[k] for k in main_table_keys])
                main_table_data.append(outputrow)

                for item in row['source_info']:
                    
                    item['digitalID']=int(row['digitalID'])
                    item['amount_sanctioned']=int(item['amount_sanctioned'])
                    item['datefrom']=datetime.strptime(item['datefrom'],"%Y-%m-%d")
                    item['dateto']=datetime.strptime(item['dateto'],"%Y-%m-%d")
                    item["timestamp"]=datetime.now()

                    source_info_data.append(tuple([item[k] for k in source_table_keys]))


                for item2 in row['member_info']:
                    item2['digitalID']=int(row['digitalID'])
                    item2["timestamp"]=datetime.now()
                    member_info_data.append(tuple([item2[k] for k in member_table_keys]))



            self._c.executemany('INSERT INTO main('+','.join(main_table_keys)+') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',main_table_data)

            self._c.executemany('INSERT INTO member_info('+','.join(member_table_keys)+') VALUES (?,?,?,?,?,?,?,?,?)',member_info_data)

            self._c.executemany('INSERT INTO source_info('+','.join(source_table_keys)+') VALUES (?,?,?,?,?,?,?,?)',source_info_data)

            self._conn.commit()
            

            






#import requests
#s=requests.Session()
##sourcelist=['183236','96779','176294']#,172642]
##dataout=[]
##processDB=sqlite_interface()
#i=processDB.checkID(172642)
#print i
##for ngo in sourcelist:
##    check = processDB.checkID(ngo)
##    print(check)
##processDB.closeConnection()
## r = s.get("https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf")
## s.headers["X-Requested-With"]="XMLHttpRequest"
## my_dict=json.loads(r.text)
## csrf_token=my_dict['csrf_token']
## data = dict (id = str(ngo), csrf_test_name = csrf_token)
## p = s.post("https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info", data=data)
## outputdict=json.loads(p.text)
## outputdict['digitalID']=int(ngo)
## dataout.append(outputdict)


##for item in dataout:
## item=processDB.processDict(item)
##processDB.AppendToDB(dataout)


