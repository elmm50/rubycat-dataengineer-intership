import pytest
from scripts_elmoustapha_malick.projet_1.script_proveit import max_session_simultany
from proveitadmin.audit.auditdatabase import AuditDatabase
from proveitadmin.audit.event.user.userserviceconnectionsummaryevent import UserServiceConnectionSummaryEvent
from proveitadmin.audit.service import Service
from rccore.utils.dateutils import createLocalDateTime, getUtcTimestamp, createLocalDateTime
from proveitadmin.audit.hbsource import HbSource
from proveitadmin.audit.event.constants import EVENT_SEVERITY, EVENT_CATEGORY, EVENT_SERVICE_CONNECTION_STATUS
from datetime import datetime,timedelta
import pytz

"""
#@author elmoustapha.malick@rubycat.eu
"""
# We put the events one by one in a very precise order ie we put the events archived
# in ascending order (the event which are finished rather are the first) which is the case in real life

#### Creating a event
def create_event(begin_time,end_time,name_user):
     return UserServiceConnectionSummaryEvent(
                              service=Service('service1', host='ip1'),
                              connectionCtx={},
                              timestamp=end_time,
                              beginDate=begin_time,
                              endDate=end_time, 
                              source=HbSource(userName=name_user))
    
    
#### Test initiation
class TestInit:
    
    def setup_method(self):
            # Configuration for Database
            dev_conf = [
            "localhost",
            5432,
            "rubydbuser",
            "rubydbuser",
            False   
            ]
            
            # Set up and create 3 events
            self.auditDb = AuditDatabase(*dev_conf)

            self.event1=create_event(datetime(2023,3,13,8,tzinfo=None),datetime(2023,3,13,11,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,12,tzinfo=None),datetime(2023,3,13,13,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,15,tzinfo=None),datetime(2023,3,13,17,tzinfo=None),'user3') 

    # Delete the database and close connection
    def teardown_method(self):
        self.auditDb.deleteTables()
        self.auditDb.disposeConnectionPool()
    
    # Testing each event timestamp, we have 3 events in our table    
    def test_Init1(self):
        assert (self.event1.source.userName == 'user1')
        assert (self.event1.timestamp == datetime(2023,3,13,11,tzinfo=None))

    def test_Init2(self):
        assert (self.event2.source.userName == 'user2')
        assert (self.event2.timestamp == datetime(2023,3,13,13,tzinfo=None))

    def test_Init3(self):
         assert (self.event3.source.userName == 'user3')
         assert (self.event3.timestamp == datetime(2023,3,13,17,tzinfo=None))        


#### Test per day ie testing the function max_session_simultany with delta_x=24h(one day)
class TestPerDay:
    
    def setup_method(self):
            # Configuration for Database
            dev_conf = [
            "localhost",
            5432,
            "rubydbuser",
            "rubydbuser",
            False   
            ]
            
            # Set up and create 2 events
            self.auditDb = AuditDatabase(*dev_conf)

    # Delete the database and close connection
    def teardown_method(self):
        self.auditDb.deleteTables()
        self.auditDb.disposeConnectionPool()


    # Test1 max_session_simultany function for the case : no row in the table 
    def test_no_row(self):

            with self.auditDb.session_scope(): 
        
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    assert dbevents==[]
                    date_start=datetime(1970,1,1,0,0,tzinfo=None)
                    date_finish=datetime(1970,1,1,0,0,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,24*60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==1
                    assert len(session_list)==1
                    
                    # Number of sessions per day
                    assert(session_list[0]==0)

                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='01/01/70')

                    
                    
    
    # Test2  for one row in the table
    def test_1day_1event(self):
            self.event1=create_event(datetime(2023,3,13,5,tzinfo=None),datetime(2023,3,13,11,tzinfo=None),'user1') 

            with self.auditDb.session_scope(): 
                    self.auditDb.addObject(self.event1)
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,24*60*60,dbevents)

                    # Length of ouput lists
                    assert len(axis_x_list)==1
                    assert len(session_list)==1   
                    
                    # Number of sessions per day
                    assert(session_list[0]==1)


                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23')

    
    #Test3  one day 9 events with no overlap 
    def test_1day_9events_no_overlap(self):
            self.event1=create_event(datetime(2023,3,13,5,tzinfo=None),datetime(2023,3,13,6,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,7,tzinfo=None),datetime(2023,3,13,8,tzinfo=None),'user1') 
            self.event3=create_event(datetime(2023,3,13,9,tzinfo=None),datetime(2023,3,13,10,tzinfo=None),'user1') 

            self.event4=create_event(datetime(2023,3,13,11,tzinfo=None),datetime(2023,3,13,12,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,13,tzinfo=None),datetime(2023,3,13,14,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,15,tzinfo=None),datetime(2023,3,13,16,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,13,17,tzinfo=None),datetime(2023,3,13,18,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,19,tzinfo=None),datetime(2023,3,13,20,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,21,tzinfo=None),datetime(2023,3,13,22,tzinfo=None),'user1')
            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,24*60*60,dbevents)

                    # Length of ouput lists
                    assert len(axis_x_list)==1
                    assert len(session_list)==1
                    
                    # Number of sessions per day
                    assert(session_list[0]==1)
                    
                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23')

                    
    #Test4 3days 3overlaps with different cases  
    def test_3days_3overlap_diff_case(self):
            self.event1=create_event(datetime(2023,3,13,5,10,tzinfo=None),datetime(2023,3,13,6,10,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,6,tzinfo=None),datetime(2023,3,13,8,tzinfo=None),'user1') 
            self.event3=create_event(datetime(2023,3,13,5,0,tzinfo=None),datetime(2023,3,13,10,0,tzinfo=None),'user1') 

            self.event4=create_event(datetime(2023,3,14,10,tzinfo=None),datetime(2023,3,14,12,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,14,10,tzinfo=None),datetime(2023,3,14,13,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,14,11,tzinfo=None),datetime(2023,3,14,13,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,15,17,00,1,tzinfo=None),datetime(2023,3,15,17,00,3,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,15,17,00,0,tzinfo=None),datetime(2023,3,15,17,00,4,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,15,17,00,2,tzinfo=None),datetime(2023,3,15,17,00,4,tzinfo=None),'user1')
            
            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)

                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,15,17,00,0,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,24*60*60,dbevents)

                    # Length of ouput lists
                    assert len(axis_x_list)==3
                    assert len(session_list)==3
                    
                    # Number of sessions per day
                    assert(session_list[0]==3)
                    assert(session_list[1]==3)
                    assert(session_list[2]==3)

                    
                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23')
                    assert(axis_x_list[1]=='14/03/23')
                    assert(axis_x_list[2]=='15/03/23')
                    
class TestPerHour:
    
    def setup_method(self):
            # Configuration for Database
            dev_conf = [
            "localhost",
            5432,
            "rubydbuser",
            "rubydbuser",
            False   
            ]
            
            # Set up and create 2 events
            self.auditDb = AuditDatabase(*dev_conf)

    # Delete the database and close connection
    def teardown_method(self):
        self.auditDb.deleteTables()
        self.auditDb.disposeConnectionPool()


    # Test1 max_session_simultany function for the case : no row in table 
    def test_no_row(self):

            with self.auditDb.session_scope(): 
        
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    assert dbevents==[]
                    date_start=datetime(1970,1,1,0,0,tzinfo=None)
                    date_finish=datetime(1970,1,1,0,0,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==1
                    assert len(session_list)==1
                    
                    # Number of sessions per day
                    assert(session_list[0]==0)
                    
                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='01/01/70 00:00')

    # Test2 for one row in table
    def test_1hour_1event(self):
            self.event1=create_event(datetime(2023,3,13,5,tzinfo=None),datetime(2023,3,13,11,tzinfo=None),'user1') 

            with self.auditDb.session_scope(): 
                    self.auditDb.addObject(self.event1)
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,11,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)

                    # Length of ouput lists
                    assert len(axis_x_list)==12
                    assert len(session_list)==12   

                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==0)
                    assert(session_list[5]==1)
                    assert(session_list[6]==1)
                    assert(session_list[7]==1)
                    assert(session_list[8]==1)
                    assert(session_list[9]==1)
                    assert(session_list[10]==1)
                    assert(session_list[11]==1)


                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')


    
    # Test3  one day 9 events with no overlaps
    def test_1day_9events_no_overlap(self):
            self.event1=create_event(datetime(2023,3,13,5,tzinfo=None),datetime(2023,3,13,6,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,7,tzinfo=None),datetime(2023,3,13,8,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,9,tzinfo=None),datetime(2023,3,13,10,tzinfo=None),'user3') 

            self.event4=create_event(datetime(2023,3,13,11,tzinfo=None),datetime(2023,3,13,12,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,13,tzinfo=None),datetime(2023,3,13,14,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,15,tzinfo=None),datetime(2023,3,13,16,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,13,17,tzinfo=None),datetime(2023,3,13,18,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,19,tzinfo=None),datetime(2023,3,13,20,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,21,tzinfo=None),datetime(2023,3,13,22,tzinfo=None),'user1')
            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==24
                    assert len(session_list)==24
                    
                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==0)
                    assert(session_list[5]==1)
                    assert(session_list[6]==1)
                    assert(session_list[7]==1)
                    assert(session_list[8]==1)
                    assert(session_list[9]==1)
                    assert(session_list[10]==1)
                    assert(session_list[11]==1)
                    assert(session_list[12]==1)
                    assert(session_list[13]==1)
                    assert(session_list[14]==1)
                    assert(session_list[15]==1)
                    assert(session_list[16]==1)
                    assert(session_list[17]==1)
                    assert(session_list[18]==1)
                    assert(session_list[19]==1)
                    assert(session_list[20]==1)
                    assert(session_list[21]==1)
                    assert(session_list[22]==1)
                    assert(session_list[23]==0)



                    
                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')
                    assert(axis_x_list[12]=='13/03/23 12:00')
                    assert(axis_x_list[13]=='13/03/23 13:00')
                    assert(axis_x_list[14]=='13/03/23 14:00')
                    assert(axis_x_list[15]=='13/03/23 15:00')
                    assert(axis_x_list[16]=='13/03/23 16:00')
                    assert(axis_x_list[17]=='13/03/23 17:00')
                    assert(axis_x_list[18]=='13/03/23 18:00')
                    assert(axis_x_list[19]=='13/03/23 19:00')
                    assert(axis_x_list[20]=='13/03/23 20:00')
                    assert(axis_x_list[21]=='13/03/23 21:00')
                    assert(axis_x_list[22]=='13/03/23 22:00')
                    assert(axis_x_list[23]=='13/03/23 23:00')                    


              
    # Test4 case1 from my notebook witch test if we spot micro events ho are one next to the others
    # and are like 10 min or less with large event 3 to 4 hours
    # 
    #  | 
    #  |
    #  |  
    #  |          |-| |-| |-| |-| |-|
    #  |      |------------------------|
    #  |   |-----------------------------|
    #  |     |-----------------------------|
    #  |    |-------------------------------|
    #  -----------------------------------------------------------> Hours
    #  
    def test_case1_with_micro_events(self):
            self.event1=create_event(datetime(2023,3,13,1,31,tzinfo=None),datetime(2023,3,13,1,51,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,2,15,tzinfo=None),datetime(2023,3,13,2,53,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,3,23,tzinfo=None),datetime(2023,3,13,3,58,tzinfo=None),'user3') 

            self.event4=create_event(datetime(2023,3,13,4,38,tzinfo=None),datetime(2023,3,13,4,51,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,5,32,tzinfo=None),datetime(2023,3,13,5,33,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,0,32,tzinfo=None),datetime(2023,3,13,6,15,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,13,0,12,tzinfo=None),datetime(2023,3,13,6,34,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,0,49,tzinfo=None),datetime(2023,3,13,7,12,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,0,26,tzinfo=None),datetime(2023,3,13,7,39,tzinfo=None),'user1')
            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==24
                    assert len(session_list)==24
                    
                    # Number of sessions per day
                    assert(session_list[0]==4)
                    assert(session_list[1]==5)
                    assert(session_list[2]==5)
                    assert(session_list[3]==5)
                    assert(session_list[4]==5)
                    assert(session_list[5]==5)
                    assert(session_list[6]==4)
                    assert(session_list[7]==2)
                    assert(session_list[8]==0)
                    assert(session_list[9]==0)
                    assert(session_list[10]==0)
                    assert(session_list[11]==0)
                    assert(session_list[12]==0)
                    assert(session_list[13]==0)
                    assert(session_list[14]==0)
                    assert(session_list[15]==0)
                    assert(session_list[16]==0)
                    assert(session_list[17]==0)
                    assert(session_list[18]==0)
                    assert(session_list[19]==0)
                    assert(session_list[20]==0)
                    assert(session_list[21]==0)
                    assert(session_list[22]==0)
                    assert(session_list[23]==0)

                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')
                    assert(axis_x_list[12]=='13/03/23 12:00')
                    assert(axis_x_list[13]=='13/03/23 13:00')
                    assert(axis_x_list[14]=='13/03/23 14:00')
                    assert(axis_x_list[15]=='13/03/23 15:00')
                    assert(axis_x_list[16]=='13/03/23 16:00')
                    assert(axis_x_list[17]=='13/03/23 17:00')
                    assert(axis_x_list[18]=='13/03/23 18:00')
                    assert(axis_x_list[19]=='13/03/23 19:00')
                    assert(axis_x_list[20]=='13/03/23 20:00')
                    assert(axis_x_list[21]=='13/03/23 21:00')
                    assert(axis_x_list[22]=='13/03/23 22:00')
                    assert(axis_x_list[23]=='13/03/23 23:00')     



    # Test5 case2 from my notebook witch test micro et large events if there are one over the other 
    #  
    #  | 
    #  |
    #  |           |-|
    #  |          |---| 
    #  |         |-----|
    #  |       |---------|
    #  |     |------------|         |--| 
    #  |    |--------------|       |-||-|   |-||-||-|     |----|
    #  -----------------------------------------------------------> Hours
    #  
    def test_case2(self):
            self.event1=create_event(datetime(2023,3,13,9,31,tzinfo=None),datetime(2023,3,13,9,32,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,9,29,tzinfo=None),datetime(2023,3,13,9,33,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,9,28,tzinfo=None),datetime(2023,3,13,9,34,tzinfo=None),'user3') 

            self.event4=create_event(datetime(2023,3,13,7,48,tzinfo=None),datetime(2023,3,13,10,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,8,21,tzinfo=None),datetime(2023,3,13,10,2,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,8,32,tzinfo=None),datetime(2023,3,13,10,15,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,13,11,12,tzinfo=None),datetime(2023,3,13,11,25,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,11,18,tzinfo=None),datetime(2023,3,13,11,28,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,11,26,tzinfo=None),datetime(2023,3,13,11,29,tzinfo=None),'user1')
            
            self.event10=create_event(datetime(2023,3,13,12,10,tzinfo=None),datetime(2023,3,13,12,15,tzinfo=None),'user1') 

            self.event11=create_event(datetime(2023,3,13,12,18,tzinfo=None),datetime(2023,3,13,12,25,tzinfo=None),'user1') 
            self.event12=create_event(datetime(2023,3,13,12,28,tzinfo=None),datetime(2023,3,13,12,29,tzinfo=None),'user1') 
            self.event13=create_event(datetime(2023,3,13,14,31,tzinfo=None),datetime(2023,3,13,14,33,tzinfo=None),'user1')
            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    self.auditDb.addObject(self.event10)
                    self.auditDb.addObject(self.event11)
                    self.auditDb.addObject(self.event12)
                    self.auditDb.addObject(self.event13)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==24
                    assert len(session_list)==24

                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==0)
                    assert(session_list[5]==0)
                    assert(session_list[6]==0)
                    assert(session_list[7]==1)
                    assert(session_list[8]==3)
                    assert(session_list[9]==6)
                    assert(session_list[10]==3)
                    assert(session_list[11]==2)
                    assert(session_list[12]==1)
                    assert(session_list[13]==0)
                    assert(session_list[14]==1)
                    assert(session_list[15]==0)
                    assert(session_list[16]==0)
                    assert(session_list[17]==0)
                    assert(session_list[18]==0)
                    assert(session_list[19]==0)
                    assert(session_list[20]==0)
                    assert(session_list[21]==0)
                    assert(session_list[22]==0)
                    assert(session_list[23]==0)

                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')
                    assert(axis_x_list[12]=='13/03/23 12:00')
                    assert(axis_x_list[13]=='13/03/23 13:00')
                    assert(axis_x_list[14]=='13/03/23 14:00')
                    assert(axis_x_list[15]=='13/03/23 15:00')
                    assert(axis_x_list[16]=='13/03/23 16:00')
                    assert(axis_x_list[17]=='13/03/23 17:00')
                    assert(axis_x_list[18]=='13/03/23 18:00')
                    assert(axis_x_list[19]=='13/03/23 19:00')
                    assert(axis_x_list[20]=='13/03/23 20:00')
                    assert(axis_x_list[21]=='13/03/23 21:00')
                    assert(axis_x_list[22]=='13/03/23 22:00')
                    assert(axis_x_list[23]=='13/03/23 23:00')     



    # Test6 case3 from my notebook witch is another possible case from case2
    #   
    #  | 
    #  |
    #  |           
    #  |           
    #  |                                     |-|
    #  |                                |-------|
    #  |     |------------|            |---------|
    #  |    |--| |--| |--|                |--|
    #  -----------------------------------------------------------> Hours
    #  
    def test_case3(self):
            self.event1=create_event(datetime(2023,3,13,8,0,tzinfo=None),datetime(2023,3,13,8,10,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,8,13,tzinfo=None),datetime(2023,3,13,8,14,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,8,28,tzinfo=None),datetime(2023,3,13,9,0,tzinfo=None),'user3') 

            self.event4=create_event(datetime(2023,3,13,8,2,tzinfo=None),datetime(2023,3,13,9,10,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,11,30,tzinfo=None),datetime(2023,3,13,11,31,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,11,31,tzinfo=None),datetime(2023,3,13,11,35,tzinfo=None),'user1') 

            self.event7=create_event(datetime(2023,3,13,11,25,tzinfo=None),datetime(2023,3,13,11,36,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,11,18,tzinfo=None),datetime(2023,3,13,11,37,tzinfo=None),'user1') 

            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)

                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==24
                    assert len(session_list)==24

                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==0)
                    assert(session_list[5]==0)
                    assert(session_list[6]==0)
                    assert(session_list[7]==0)
                    assert(session_list[8]==2)
                    assert(session_list[9]==2)
                    assert(session_list[10]==0)
                    assert(session_list[11]==3)
                    assert(session_list[12]==0)
                    assert(session_list[13]==0)
                    assert(session_list[14]==0)
                    assert(session_list[15]==0)
                    assert(session_list[16]==0)
                    assert(session_list[17]==0)
                    assert(session_list[18]==0)
                    assert(session_list[19]==0)
                    assert(session_list[20]==0)
                    assert(session_list[21]==0)
                    assert(session_list[22]==0)
                    assert(session_list[23]==0)

                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')
                    assert(axis_x_list[12]=='13/03/23 12:00')
                    assert(axis_x_list[13]=='13/03/23 13:00')
                    assert(axis_x_list[14]=='13/03/23 14:00')
                    assert(axis_x_list[15]=='13/03/23 15:00')
                    assert(axis_x_list[16]=='13/03/23 16:00')
                    assert(axis_x_list[17]=='13/03/23 17:00')
                    assert(axis_x_list[18]=='13/03/23 18:00')
                    assert(axis_x_list[19]=='13/03/23 19:00')
                    assert(axis_x_list[20]=='13/03/23 20:00')
                    assert(axis_x_list[21]=='13/03/23 21:00')
                    assert(axis_x_list[22]=='13/03/23 22:00')
                    assert(axis_x_list[23]=='13/03/23 23:00')     

    # Test7 case4 for delta_x=1h witch are combination of all 3 last cases
    #    
    #  | 
    #  |
    #  |           
    #  |           
    #  |                                                            |-|
    #  |           |-|                                             |---|
    #  |          |---|  |-|                                      |-----|
    #  |    |-||-|      |---|  |-||-||-| |-||-||-|               |-------|
    #  |  |---------------------------------------|             |---------|
    #  -------------------------------------------------------------------------> Hours
    #
    def test_case4(self):
            self.event1=create_event(datetime(2023,3,13,10,2,10,tzinfo=None),datetime(2023,3,13,10,2,12,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,10,3,13,tzinfo=None),datetime(2023,3,13,10,3,14,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,10,25,10,tzinfo=None),datetime(2023,3,13,10,25,12,tzinfo=None),'user3') 
            self.event4=create_event(datetime(2023,3,13,10,25,9,tzinfo=None),datetime(2023,3,13,10,25,13,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,11,10,tzinfo=None),datetime(2023,3,13,11,11,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,11,15,tzinfo=None),datetime(2023,3,13,11,18,tzinfo=None),'user1') 
            self.event7=create_event(datetime(2023,3,13,11,19,tzinfo=None),datetime(2023,3,13,11,25,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,12,5,tzinfo=None),datetime(2023,3,13,12,8,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,12,10,tzinfo=None),datetime(2023,3,13,12,11,tzinfo=None),'user1') 
            self.event10=create_event(datetime(2023,3,13,12,13,tzinfo=None),datetime(2023,3,13,12,14,tzinfo=None),'user1')
            self.event11=create_event(datetime(2023,3,13,9,55,tzinfo=None),datetime(2023,3,13,13,21,tzinfo=None),'user1')
            
            self.event12=create_event(datetime(2023,3,13,17,25,tzinfo=None),datetime(2023,3,13,17,26,tzinfo=None),'user1')
            self.event13=create_event(datetime(2023,3,13,17,24,tzinfo=None),datetime(2023,3,13,17,27,tzinfo=None),'user1')
            self.event14=create_event(datetime(2023,3,13,17,23,tzinfo=None),datetime(2023,3,13,17,28,tzinfo=None),'user1')
            self.event15=create_event(datetime(2023,3,13,17,13,tzinfo=None),datetime(2023,3,13,17,36,tzinfo=None),'user1')
            self.event16=create_event(datetime(2023,3,13,16,55,tzinfo=None),datetime(2023,3,13,18,2,tzinfo=None),'user1') 

            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    self.auditDb.addObject(self.event10)
                    self.auditDb.addObject(self.event11)
                    self.auditDb.addObject(self.event12)
                    self.auditDb.addObject(self.event13)
                    self.auditDb.addObject(self.event14)
                    self.auditDb.addObject(self.event15)
                    self.auditDb.addObject(self.event16)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,1*60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==24
                    assert len(session_list)==24

                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==0)
                    assert(session_list[5]==0)
                    assert(session_list[6]==0)
                    assert(session_list[7]==0)
                    assert(session_list[8]==0)
                    assert(session_list[9]==1)
                    assert(session_list[10]==3)
                    assert(session_list[11]==2)
                    assert(session_list[12]==2)
                    assert(session_list[13]==1)
                    assert(session_list[14]==0)
                    assert(session_list[15]==0)
                    assert(session_list[16]==1)
                    assert(session_list[17]==5)
                    assert(session_list[18]==1)
                    assert(session_list[19]==0)
                    assert(session_list[20]==0)
                    assert(session_list[21]==0)
                    assert(session_list[22]==0)
                    assert(session_list[23]==0)

                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 01:00')
                    assert(axis_x_list[2]=='13/03/23 02:00')
                    assert(axis_x_list[3]=='13/03/23 03:00')
                    assert(axis_x_list[4]=='13/03/23 04:00')
                    assert(axis_x_list[5]=='13/03/23 05:00')
                    assert(axis_x_list[6]=='13/03/23 06:00')
                    assert(axis_x_list[7]=='13/03/23 07:00')
                    assert(axis_x_list[8]=='13/03/23 08:00')
                    assert(axis_x_list[9]=='13/03/23 09:00')
                    assert(axis_x_list[10]=='13/03/23 10:00')
                    assert(axis_x_list[11]=='13/03/23 11:00')
                    assert(axis_x_list[12]=='13/03/23 12:00')
                    assert(axis_x_list[13]=='13/03/23 13:00')
                    assert(axis_x_list[14]=='13/03/23 14:00')
                    assert(axis_x_list[15]=='13/03/23 15:00')
                    assert(axis_x_list[16]=='13/03/23 16:00')
                    assert(axis_x_list[17]=='13/03/23 17:00')
                    assert(axis_x_list[18]=='13/03/23 18:00')
                    assert(axis_x_list[19]=='13/03/23 19:00')
                    assert(axis_x_list[20]=='13/03/23 20:00')
                    assert(axis_x_list[21]=='13/03/23 21:00')
                    assert(axis_x_list[22]=='13/03/23 22:00')
                    assert(axis_x_list[23]=='13/03/23 23:00')   
                    
                    
    # Test8 case4 from my notebook for delta_x=2h 
    def test_case4_delta_x_2h(self):
            self.event1=create_event(datetime(2023,3,13,10,2,10,tzinfo=None),datetime(2023,3,13,10,2,12,tzinfo=None),'user1') 
            self.event2=create_event(datetime(2023,3,13,10,3,13,tzinfo=None),datetime(2023,3,13,10,3,14,tzinfo=None),'user2') 
            self.event3=create_event(datetime(2023,3,13,10,25,10,tzinfo=None),datetime(2023,3,13,10,25,12,tzinfo=None),'user3') 
            self.event4=create_event(datetime(2023,3,13,10,25,9,tzinfo=None),datetime(2023,3,13,10,25,13,tzinfo=None),'user1') 
            self.event5=create_event(datetime(2023,3,13,11,10,tzinfo=None),datetime(2023,3,13,11,11,tzinfo=None),'user1') 
            self.event6=create_event(datetime(2023,3,13,11,15,tzinfo=None),datetime(2023,3,13,11,18,tzinfo=None),'user1') 
            self.event7=create_event(datetime(2023,3,13,11,19,tzinfo=None),datetime(2023,3,13,11,25,tzinfo=None),'user1') 
            self.event8=create_event(datetime(2023,3,13,12,5,tzinfo=None),datetime(2023,3,13,12,8,tzinfo=None),'user1') 
            self.event9=create_event(datetime(2023,3,13,12,10,tzinfo=None),datetime(2023,3,13,12,11,tzinfo=None),'user1') 
            self.event10=create_event(datetime(2023,3,13,12,13,tzinfo=None),datetime(2023,3,13,12,14,tzinfo=None),'user1')
            self.event11=create_event(datetime(2023,3,13,9,55,tzinfo=None),datetime(2023,3,13,13,21,tzinfo=None),'user1')
            
            self.event12=create_event(datetime(2023,3,13,17,25,tzinfo=None),datetime(2023,3,13,17,26,tzinfo=None),'user1')
            self.event13=create_event(datetime(2023,3,13,17,24,tzinfo=None),datetime(2023,3,13,17,27,tzinfo=None),'user1')
            self.event14=create_event(datetime(2023,3,13,17,23,tzinfo=None),datetime(2023,3,13,17,28,tzinfo=None),'user1')
            self.event15=create_event(datetime(2023,3,13,17,13,tzinfo=None),datetime(2023,3,13,17,36,tzinfo=None),'user1')
            self.event16=create_event(datetime(2023,3,13,16,55,tzinfo=None),datetime(2023,3,13,18,2,tzinfo=None),'user1') 

            with self.auditDb.session_scope(): 
                    # add events
                    self.auditDb.addObject(self.event1)
                    self.auditDb.addObject(self.event2)
                    self.auditDb.addObject(self.event3)
                    self.auditDb.addObject(self.event4)
                    self.auditDb.addObject(self.event5)
                    self.auditDb.addObject(self.event6)
                    self.auditDb.addObject(self.event7)
                    self.auditDb.addObject(self.event8)
                    self.auditDb.addObject(self.event9)
                    self.auditDb.addObject(self.event10)
                    self.auditDb.addObject(self.event11)
                    self.auditDb.addObject(self.event12)
                    self.auditDb.addObject(self.event13)
                    self.auditDb.addObject(self.event14)
                    self.auditDb.addObject(self.event15)
                    self.auditDb.addObject(self.event16)
                    
                    dbevents = self.auditDb.session.query(UserServiceConnectionSummaryEvent).all()
                    
                    date_start=datetime(2023,3,13,0,0,tzinfo=None)
                    date_finish=datetime(2023,3,13,23,00,tzinfo=None)
                    axis_x_list,session_list=max_session_simultany(date_start,date_finish,2*60*60,dbevents)
                    
                    # Length of ouput lists
                    assert len(axis_x_list)==12
                    assert len(session_list)==12

                    # Number of sessions per day
                    assert(session_list[0]==0)
                    assert(session_list[1]==0)
                    assert(session_list[2]==0)
                    assert(session_list[3]==0)
                    assert(session_list[4]==1)
                    assert(session_list[5]==3)
                    assert(session_list[6]==2)
                    assert(session_list[7]==0)
                    assert(session_list[8]==5)
                    assert(session_list[9]==1)
                    assert(session_list[10]==0)
                    assert(session_list[11]==0)


                    # Day corresponding the number of sessions
                    assert(axis_x_list[0]=='13/03/23 00:00')
                    assert(axis_x_list[1]=='13/03/23 02:00')
                    assert(axis_x_list[2]=='13/03/23 04:00')
                    assert(axis_x_list[3]=='13/03/23 06:00')
                    assert(axis_x_list[4]=='13/03/23 08:00')
                    assert(axis_x_list[5]=='13/03/23 10:00')
                    assert(axis_x_list[6]=='13/03/23 12:00')
                    assert(axis_x_list[7]=='13/03/23 14:00')
                    assert(axis_x_list[8]=='13/03/23 16:00')
                    assert(axis_x_list[9]=='13/03/23 18:00')
                    assert(axis_x_list[10]=='13/03/23 20:00')
                    assert(axis_x_list[11]=='13/03/23 22:00')            
                    
                    
if __name__ == '__main__':
    main()


