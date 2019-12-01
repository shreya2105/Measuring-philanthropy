# -*- coding: utf-8 -*-
import json
import sqlite3
from datetime import datetime
null=None




class sqlite_interface:
	def __init__(self):
		self._conn=sqlite3.connect('ITScrapeNGOs.db')
		self._c=self._conn.cursor()

	def closeConnection(self):
		self._conn.close()
		

	def checkID(self,Name, Approved_under_Section):
		# pan=str(pan)
		dat=[]
		query="select * from main where Name=? and Approved_under_Section=?".format(Name,Approved_under_Section)
		#print (query)
		for row in self._c.execute(query,(Name,Approved_under_Section)):
		 	dat.append(row)


		if len(dat)>0:
			return False
		else:
			return True


	def AppendToDB(self,lst):

			main_table_keys=["Name", "Pancard",  "Address", "State", "City", "CCIT_DGIT_Exemptions", "CCIT", "CIT", "Approved_under_Section", "Date_of_order", "Date_of_withdrawal",  "Date_of_Expiry", "Remarks"]

			main_table=[]
			
			for row in lst:
					



					
					outputrow=tuple([row[k] for k in main_table_keys])
					main_table.append(outputrow)




			self._c.executemany('INSERT INTO main('+','.join(main_table_keys)+') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',main_table)
			self._conn.commit()



