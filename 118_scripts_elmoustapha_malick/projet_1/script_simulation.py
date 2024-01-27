#!/usr/bin/env python
#
# Copyright Rubycat
"""
#@author elmoustapha.malick@rubycat.eu
"""
from proveitadmin.audit.service import Service
from proveitadmin.audit.event.user.userserviceconnectionsummaryevent import UserServiceConnectionSummaryEvent
from proveitadmin.audit.auditdatabase import AuditDatabase
from rccore.utils.dateutils import createLocalDateTime, getUtcTimestamp,convertDateToString,createLocalDateTime, createLocalDateTime
import proveitadmin.audit.event.types as EventTypes
from proveitadmin.audit.hbsource import HbSource
from proveitadmin.audit.event.user.userevent import UserEvent

import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import datetime 


                           #### Database : PROVEIT
   
   
#### Configuration of PROVIT
# for connecting with database(db) of PROVEIT                          
proveit_conf = [
        "127.0.0.1",
        33333,
        "rubydbuser",
        "ctuMycEZ9vnachl2S0kxJNi5wzZCtepDQKJFwZdwl9O9UjfKrl",
        False
]
                    
#### Connection to the database
def database_connection():
    return AuditDatabase(
        *proveit_conf
    )
 
  

#### Creation of a event
def create_event(begin_time,end_time,name_user):
     return UserServiceConnectionSummaryEvent(
                              service=Service('service1', host='ip1'),
                              connectionCtx={},
                              timestamp=end_time,
                              beginDate=begin_time,
                              endDate=end_time, 
                              source=HbSource(userName=name_user))


#### Fonction to create random events in the table of the database PROVEIT
def random_date(start):
   current = start
   curr = current + datetime.timedelta(hours=randrange(3),minutes=randrange(60))
   return curr
           
def random_event(year,month,day,nomb_event,nomb_day,db):
    for i in range(nomb_day):
         startDate = datetime.datetime(year,month,day,00,00)
         begin_time=[]
         end_time=[]
         done=False
         while done !=True :
            ini_date_begin=random_date(startDate)
            begin_time.append(ini_date_begin)
            ini_date_end=random_date(begin_time[-1])
            if ini_date_end >= ini_date_begin and ini_date_end<=datetime.datetime(year,month,day,23,59):
                  end_time.append(ini_date_end)
                  startDate=begin_time[-1]
            if len(begin_time)==len(end_time)==nomb_event:
               done = True
         for i in range(len(begin_time)):
             event_i=create_event(begin_time[i],end_time[i],"user_i")
             db.addObject(event_i)
         day=day+1
   
 


#######################################################   START   #######################################################

def main():
    
     db = database_connection()
     with db.session_scope():

         random_event(2023,1,1,5,10,db)
         queryevent = db.session.query(UserServiceConnectionSummaryEvent).all()
         for i in queryevent :
             print("begin date",i.beginDate,"      ","end date",i.endDate)
         # reset the db
         reponse=input("Voulez vous reset la db (o/n) ? :")
         if(reponse =='o'):
            db.deleteTables()

 
if __name__ == '__main__':
    main()

