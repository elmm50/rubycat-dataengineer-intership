#!/usr/bin/env python
"""
# #@author elmoustapha.malick@rubycat.eu
"""
# Copyright Rubycat

from proveitadmin.audit.service import Service
from proveitadmin.audit.event.user.userserviceconnectionsummaryevent import UserServiceConnectionSummaryEvent
from proveitadmin.audit.auditdatabase import AuditDatabase
from rccore.utils.dateutils import datetime, getUtcTimestamp,convertDateToString,datetime, datetime
import proveitadmin.audit.event.types as EventTypes
from proveitadmin.audit.hbsource import HbSource
from proveitadmin.audit.event.user.userevent import UserEvent
import matplotlib.pyplot as plt
import numpy as np
import time
import pytz
from datetime import datetime
from script_proveit import max_session_simultany


                           #### Database : VM developpment
   
   
#### Configuration of my vm development
# for connecting with with database(db) of vm                           
dev_conf = [
    "localhost",
    5432,
    "rubydbuser",
    "rubydbuser",
    False   
]
                    
#### Connection to the database
def database_connection():
    return AuditDatabase(
        *dev_conf
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



def main():
    
     db = database_connection()
     # For UTC time we have different results !
     #
     event1=create_event(datetime(2023,3,13,1,32,tzinfo=None),datetime(2023,3,13,3,25,tzinfo=None),'user1') 
     event2=create_event(datetime(2023,3,13,4,15,tzinfo=None),datetime(2023,3,13,5,7,tzinfo=None),'user3') 
     event3=create_event(datetime(2023,3,13,7,3,tzinfo=None),datetime(2023,3,13,8,36,tzinfo=None),'user2') 

     event4=create_event(datetime(2023,3,13,7,41,tzinfo=None),datetime(2023,3,13,9,48,tzinfo=None),'user1') 
     event5=create_event(datetime(2023,3,13,7,57,tzinfo=None),datetime(2023,3,13,10,2,tzinfo=None),'user1') 
    
     with db.session_scope():
         
         db.addObject(event1)
         db.addObject(event2)
         db.addObject(event3)

         queryevent = db.session.query(UserServiceConnectionSummaryEvent).all()
         for i in queryevent : 
             print("begindate : ",i.beginDate,"enddate : ",i.endDate)
         date_start=datetime(2023,3,13,0,0,tzinfo=None)
         date_finish=datetime(2023,3,13,10,0,tzinfo=None)
         
         l1,l2=max_session_simultany(date_start,date_finish,60*60,queryevent)
         print(l1)
         print(l2)
         # reset the db
         reponse=input("Voulez vous reset la db (o/n) ? :")
         if(reponse =='o'):
            db.deleteTables()
   
        
if __name__ == '__main__':
    main()
