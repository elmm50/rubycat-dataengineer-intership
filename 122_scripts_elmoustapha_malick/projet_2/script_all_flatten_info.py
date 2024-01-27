#!/usr/bin/env python
#
# Copyright Rubycat
"""
#@author elmoustapha.malick@rubycat.eu
"""
from proveitadmin.admin.admindatabase import AdminDatabase
from proveitadmin.service.service import Service
from proveitadmin.authorization.role.role import RoleUser, RoleGroup
from proveitadmin.authentication.realm import Realm
from proveitadmin.authentication.server import Server
from proveitadmin.authorization.accesspolicy.accesspolicy import AccessPolicy
import numpy as np

                  # Make sure to be connected to the db of proveit (ssh tunnel)

#### Database : PROVEIT
#### Configuration of PROVIT
# for connecting with database(db) of PROVEIT 
proveit_conf = [
                    "127.0.0.1",
                    33333,
                    "rubydbuser",
                    "9KVIIUrsPsY9fNOndenzxobsK74dTy4gfRTsNF3ZT0AIkSlz1l",
                    False
                ]
#### Connection to the database
def database_connection():
    return AdminDatabase(
        *proveit_conf
    )


######################################### Functions #########################################
#####################
def all_services_demo(db):
    set_service=set() # Only for testing can be commented
    with db.session_scope():
        queryservice = db.session.query(Service).all()
        print("______Les services disponibles sont les suivants :______")
        for i in queryservice:
            print(">","Service : ",i.name)
            set_service.add(i.name) # Only for testing can be commented
    return set_service # Only for testing can be commented   
#####################
   
def all_royaumes_demo(db):
    set_royaume=set() # Only for testing can be commented
    with db.session_scope():
        queryroyaume = db.session.query(Realm).all()
        print("______Les royaumes disponibles sont les suivants :______")
        for i in queryroyaume:
            print(">","Royaume : ",i.name, " ----  Royaume Id :",i.id)
            set_royaume.add(i.name)  # Only for testing can be commented
    return set_royaume  # Only for testing can be commented
#####################

def all_users_demo(db):
    set_user=set()  # Only for testing can be commented
    with db.session_scope():
        queryuser = db.session.query(RoleUser.name,RoleUser.realmId).distinct()
        print("______Les utilisateurs disponibles sont les suivants :______")
        
        for i,j in queryuser:
            print(">","User : ",i, "  ----   Royaum Id : ",j)
            set_user.add(i)  # Only for testing can be commented
    return set_user  # Only for testing can be commented
#####################

def all_servers_demo(db):
    set_server=set()  # Only for testing can be commented
    with db.session_scope():
        queryserver = db.session.query(Server).all()
        print("______Les serveurs disponibles sont les suivants :______")
        for i in queryserver:
            print(">","Server : ",i.name)
            set_server.add(i.name)  # Only for testing can be commented
    return set_server  # Only for testing can be commented
#####################

def all_policies_demo(db):
    set_policie=set()  # Only for testing can be commented
    with db.session_scope():
        querypolicy = db.session.query(AccessPolicy).\
            filter(AccessPolicy.name!='administrator_proveit-administrator-profile_baseadminaccesspolicy').all()
        print("______Les politiques disponibles sont les suivantes :______")
        for i in querypolicy:
            print(">","Policy : ",i.name)
            set_policie.add(i.name)  # Only for testing can be commented
    return set_policie  # Only for testing can be commented
##############################################################################################   
    
    

################################## START ##########################################

def main():
        db = database_connection()
        
        all_services_demo(db)
        all_royaumes_demo(db)
        all_users_demo(db)
        all_servers_demo(db)       
        all_policies_demo(db)
        

if __name__ == '__main__':
   main()