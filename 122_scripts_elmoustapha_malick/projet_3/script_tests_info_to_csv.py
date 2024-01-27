import pytest
import csv
import os
from proveitadmin.admin.admindatabase import AdminDatabase
from proveitadmin.authorization.role.role import RoleUser
from proveitadmin.authorization.role.role import RolesUserAssociation 
from proveitadmin.authorization.accesspolicy.useraccesspolicy import UserRoleUserAccessPolicyAssociation
from proveitadmin.authorization.accesspolicy.useraccesspolicy import ServiceGroupUserAccessPolicyAssociation
from proveitadmin.authorization.accesspolicy.useraccesspolicy import UserAccessPolicy
from proveitadmin.service.rdpservice import RdpService
from proveitadmin.service.service import Service
from proveitadmin.authorization.role.role import Role
from proveitadmin.authorization.filter.filter import Filter
from proveitadmin.authorization.accesspolicy.accesspolicy import FilterAccessPolicyAssociation
from proveitadmin.authentication.realm import Realm
from proveitadmin.service.group import ServiceGroup
from scripts_elmoustapha_malick.projet_3.script_info_to_csv import table_service_realm_user_to_csv,table_realm_user_serviceINFO_to_csv,all_services_for_user_realm,all_users_from_service_realm
from proveitadmin.authentication.ldap import LdapServer
from proveitadmin.authorization import UserRole
from proveitadmin.authorization.accesspolicy.accesspolicy import AccessPolicy
from proveitadmin.authorization.filter.datefilter import DateFilter

"""
#@author elmoustapha.malick@rubycat.eu
"""
                         ### Make sure to execut it multiple time

 
class Test_export_to_csv:    
    # Function : table_realm_user_serviceINFO  
    # Export all informations to csv file
    # These informations are represented in a table with six fixed column:
    
    # Realm, User, Service, Authentication Mode, Authentication Credentials, Filtres
    # It means for each user in a Realm he access to a service with it corresponding information
    
    
    # Function : table_service_realm_user_to_csv
    # Export all inforamtions to csv file 
    # Service, Realm, User
    # It means for each existing service give us the user and it realm that can acces to this service

    # In this class we are going to test these functions so the method of tests will be the following :
    # We execut the function then we read the content of the csv file that will be generated and test (in a set)
    # if the content of the csv file is that is expected 
    
    #### Case :
    #Services
    #grp_service1=service1, service2,service3
    #grp_service2=service4, service5,service6
    #grp_service3=service7,service8
    
    #Roles
    #role1=user1,user2
    #role2=user3,user4
    #role3=user4,user5
    #role4=user6,user7
    
    #Policies
    #Policy1=role1,role2,grp_service1
    #Policy2=role1,role3,grp_service2
    #Policy3=role4,grp_service2,grp_service3
    
    
    def setup_method(self):
            # Configuration for Database 
            # the database is AdminDatabase
            dev_conf = [
            "localhost",
            5432,
            "rubydbuser",
            "rubydbuser",
            False   
            ]
            self.adminDb = AdminDatabase(*dev_conf)
            
    # Delete the database and close connection
    def teardown_method(self):
        self.adminDb.deleteTables()
        self.adminDb.disposeConnectionPool()
        
        
    # Testing function 
    def test_function_table_realm_user_serviceINFO_to_csv(self):

        with self.adminDb.session_scope():
                ################################################## Adding information to the database
                # Server
                ldap1 = LdapServer(name = 'ldap1')
                self.adminDb.addObject(ldap1)
                
                # Realm
                realm1 = Realm(name='realm1',
                    authenticationServers=[ldap1],
                    directoryServer=ldap1)
                self.adminDb.addObject(realm1)
                
                #################################################### Policy 1
                # Users
                user1 = RoleUser(name='user1',realmId=realm1.id)
                self.adminDb.addObject(user1)
                user2 = RoleUser(name='user2',realmId=realm1.id)
                self.adminDb.addObject(user2)
                user3 = RoleUser(name='user3',realmId=realm1.id)
                self.adminDb.addObject(user3)
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                
                # Roles
                role1 = UserRole(name='role1',
                                    description='descr1',users=[user1,user2])
                self.adminDb.addObject(role1)
                role2 = UserRole(name='role2',
                                    description='descr2',users=[user3,user4])
                self.adminDb.addObject(role2)            
                
                # Services 
                service1 = RdpService(name='service1',
                                        description='description1')
                self.adminDb.addObject(service1)
                service2 = RdpService(name='service2',
                                        description='description2')
                self.adminDb.addObject(service2)
                service3 = RdpService(name='service3',
                                        description='description3')
                self.adminDb.addObject(service3)
                
                # Group of services
                grp_service1 = ServiceGroup(name='grp_service1')
                grp_service1.services=[service1,service2,service3]
                self.adminDb.addObject(grp_service1)
                
                # Policies
                policy1 = UserAccessPolicy(name='policy1',
                                    description='policy 1')
                policy1.roles=[role1,role2]
                policy1.serviceGroups=[grp_service1]
                self.adminDb.addObject(policy1)
                
                
                #################################################### Policy 2
                # Users
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                user5 = RoleUser(name='user5',realmId=realm1.id)
                self.adminDb.addObject(user5)

                # Roles
                role3 = UserRole(name='role3',
                                    description='descr3',users=[user4,user5])
                self.adminDb.addObject(role3)            
                
                # Services 
                service4 = RdpService(name='service4',
                                        description='description4')
                self.adminDb.addObject(service4)
                service5 = RdpService(name='service5',
                                        description='description5')
                self.adminDb.addObject(service5)
                service6 = RdpService(name='service6',
                                        description='description6')
                self.adminDb.addObject(service6)
                
                # Group of services
                grp_service2 = ServiceGroup(name='grp_service2')
                grp_service2.services=[service4,service5,service6]
                self.adminDb.addObject(grp_service2)
                
                # Policies
                policy2 = UserAccessPolicy(name='policy2',
                                    description='policy 2')
                policy2.roles=[role1,role3]
                policy2.serviceGroups=[grp_service2]
                self.adminDb.addObject(policy2)
                
                #################################################### Policy 3
                # Users
                user6 = RoleUser(name='user6',realmId=realm1.id)
                self.adminDb.addObject(user6)
                user7 = RoleUser(name='user7',realmId=realm1.id)
                self.adminDb.addObject(user7)

                # Roles
                role4 = UserRole(name='role4',
                                    description='descr4',users=[user6,user7])
                self.adminDb.addObject(role4)            
                
                # Services 
                service7 = RdpService(name='service7',
                                        description='description7')
                self.adminDb.addObject(service7)
                service8 = RdpService(name='service8',
                                        description='description8')
                self.adminDb.addObject(service8)

                
                # Group of services
                grp_service3 = ServiceGroup(name='grp_service3')
                grp_service3.services=[service7,service8]
                self.adminDb.addObject(grp_service3)
                
                # Policies
                policy3 = UserAccessPolicy(name='policy3',
                                    description='policy 3')
                policy3.roles=[role4]
                policy3.serviceGroups=[grp_service2,grp_service3]
                self.adminDb.addObject(policy3)
                ####################################################
                
                
        # Testing 
        # We are going to convert the list to a set just for testing
        table_realm_user_serviceINFO_to_csv(self.adminDb,'test_realm_user_serviceINFO.csv')
        all_content=set()
        file_path = os.path.join(os.getcwd(), "test_realm_user_serviceINFO.csv")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader :
                row_to_tuple=()
                for l in row :
                    row_to_tuple=row_to_tuple+(l,)
                all_content.add(row_to_tuple)
        expected_content={('realm1', 'user6', 'service8', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user4', 'service1', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service3', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user4', 'service2', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user7', 'service8', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user3', 'service1', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service1', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service2', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user6', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user5', 'service4', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service4', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user7', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('Realm', 'User', 'Service', 'Authentication Mode', 'Authentication credentials', 'Filters'), ('realm1', 'user4', 'service3', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user4', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user7', 'service7', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user4', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user7', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service1', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user7', 'service4', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user6', 'service7', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user3', 'service2', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user3', 'service3', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user1', 'service3', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user5', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user6', 'service4', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user5', 'service5', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service4', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user2', 'service2', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user6', 'service6', 'PASSWORD', 'NONE', 'NONE'), ('realm1', 'user4', 'service4', 'PASSWORD', 'NONE', 'NONE')}
        assert(expected_content==all_content)                
                
                
    def test_function_table_service_realm_user_to_csv(self):

        with self.adminDb.session_scope():
                ################################################## Adding information to the database
                # Server
                ldap1 = LdapServer(name = 'ldap1')
                self.adminDb.addObject(ldap1)
                
                # Realm
                realm1 = Realm(name='realm1',
                    authenticationServers=[ldap1],
                    directoryServer=ldap1)
                self.adminDb.addObject(realm1)
                
                #################################################### Policy 1
                # Users
                user1 = RoleUser(name='user1',realmId=realm1.id)
                self.adminDb.addObject(user1)
                user2 = RoleUser(name='user2',realmId=realm1.id)
                self.adminDb.addObject(user2)
                user3 = RoleUser(name='user3',realmId=realm1.id)
                self.adminDb.addObject(user3)
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                
                # Roles
                role1 = UserRole(name='role1',
                                    description='descr1',users=[user1,user2])
                self.adminDb.addObject(role1)
                role2 = UserRole(name='role2',
                                    description='descr2',users=[user3,user4])
                self.adminDb.addObject(role2)            
                
                # Services 
                service1 = RdpService(name='service1',
                                        description='description1')
                self.adminDb.addObject(service1)
                service2 = RdpService(name='service2',
                                        description='description2')
                self.adminDb.addObject(service2)
                service3 = RdpService(name='service3',
                                        description='description3')
                self.adminDb.addObject(service3)
                
                # Group of services
                grp_service1 = ServiceGroup(name='grp_service1')
                grp_service1.services=[service1,service2,service3]
                self.adminDb.addObject(grp_service1)
                
                # Policies
                policy1 = UserAccessPolicy(name='policy1',
                                    description='policy 1')
                policy1.roles=[role1,role2]
                policy1.serviceGroups=[grp_service1]
                self.adminDb.addObject(policy1)
                
                
                #################################################### Policy 2
                # Users
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                user5 = RoleUser(name='user5',realmId=realm1.id)
                self.adminDb.addObject(user5)

                # Roles
                role3 = UserRole(name='role3',
                                    description='descr3',users=[user4,user5])
                self.adminDb.addObject(role3)            
                
                # Services 
                service4 = RdpService(name='service4',
                                        description='description4')
                self.adminDb.addObject(service4)
                service5 = RdpService(name='service5',
                                        description='description5')
                self.adminDb.addObject(service5)
                service6 = RdpService(name='service6',
                                        description='description6')
                self.adminDb.addObject(service6)
                
                # Group of services
                grp_service2 = ServiceGroup(name='grp_service2')
                grp_service2.services=[service4,service5,service6]
                self.adminDb.addObject(grp_service2)
                
                # Policies
                policy2 = UserAccessPolicy(name='policy2',
                                    description='policy 2')
                policy2.roles=[role1,role3]
                policy2.serviceGroups=[grp_service2]
                self.adminDb.addObject(policy2)
                
                #################################################### Policy 3
                # Users
                user6 = RoleUser(name='user6',realmId=realm1.id)
                self.adminDb.addObject(user6)
                user7 = RoleUser(name='user7',realmId=realm1.id)
                self.adminDb.addObject(user7)

                # Roles
                role4 = UserRole(name='role4',
                                    description='descr4',users=[user6,user7])
                self.adminDb.addObject(role4)            
                
                # Services 
                service7 = RdpService(name='service7',
                                        description='description7')
                self.adminDb.addObject(service7)
                service8 = RdpService(name='service8',
                                        description='description8')
                self.adminDb.addObject(service8)

                
                # Group of services
                grp_service3 = ServiceGroup(name='grp_service3')
                grp_service3.services=[service7,service8]
                self.adminDb.addObject(grp_service3)
                
                # Policies
                policy3 = UserAccessPolicy(name='policy3',
                                    description='policy 3')
                policy3.roles=[role4]
                policy3.serviceGroups=[grp_service2,grp_service3]
                self.adminDb.addObject(policy3)
                ####################################################
               
               
        # Testing 
        table_service_realm_user_to_csv(self.adminDb,'test_service_realm_user.csv')
        all_content=[]
        file_path = os.path.join(os.getcwd(), "test_service_realm_user.csv")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader :
                all_content.append(row)
        expected_content=[['Service', 'Realm', 'User'], ['service1', 'realm1', 'user1'], ['service1', 'realm1', 'user2'], ['service1', 'realm1', 'user3'], ['service1', 'realm1', 'user4'], ['service2', 'realm1', 'user1'], ['service2', 'realm1', 'user2'], ['service2', 'realm1', 'user3'], ['service2', 'realm1', 'user4'], ['service3', 'realm1', 'user1'], ['service3', 'realm1', 'user2'], ['service3', 'realm1', 'user3'], ['service3', 'realm1', 'user4'], ['service4', 'realm1', 'user1'], ['service4', 'realm1', 'user2'], ['service4', 'realm1', 'user4'], ['service4', 'realm1', 'user5'], ['service4', 'realm1', 'user6'], ['service4', 'realm1', 'user7'], ['service5', 'realm1', 'user1'], ['service5', 'realm1', 'user2'], ['service5', 'realm1', 'user4'], ['service5', 'realm1', 'user5'], ['service5', 'realm1', 'user6'], ['service5', 'realm1', 'user7'], ['service6', 'realm1', 'user1'], ['service6', 'realm1', 'user2'], ['service6', 'realm1', 'user4'], ['service6', 'realm1', 'user5'], ['service6', 'realm1', 'user6'], ['service6', 'realm1', 'user7'], ['service7', 'realm1', 'user6'], ['service7', 'realm1', 'user7'], ['service8', 'realm1', 'user6'], ['service8', 'realm1', 'user7']]
        assert (all_content==expected_content)



class Test_function_all_services_or_all_users:
    # Function : all_services_for_user_realm
    # Give us all services for a specific user in a realm

    
    
    # Function : all_users_from_service_realm
    # Give us all users in a realm for a specific service

    
    #### Case :
    #Services
    #grp_service1=service1, service2,service3
    #grp_service2=service4, service5,service6
    #grp_service3=service7,service8
    
    #Roles
    #role1=user1,user2
    #role2=user3,user4
    #role3=user4,user5
    #role4=user6,user7
    
    #Policies
    #Policy1=role1,role2,grp_service1
    #Policy2=role1,role3,grp_service2
    #Policy3=role4,grp_service2,grp_service3
    
    
    def setup_method(self):
            # Configuration for Database 
            # the database is AdminDatabase
            dev_conf = [
            "localhost",
            5432,
            "rubydbuser",
            "rubydbuser",
            False   
            ]
            self.adminDb = AdminDatabase(*dev_conf)
            
    # Delete the database and close connection
    def teardown_method(self):
        self.adminDb.deleteTables()
        self.adminDb.disposeConnectionPool()

    def test_function_all_services_for_user_realm(self):

        with self.adminDb.session_scope():
                ################################################## Adding information to the database
                # Server
                ldap1 = LdapServer(name = 'ldap1')
                self.adminDb.addObject(ldap1)
                
                # Realm
                realm1 = Realm(name='realm1',
                    authenticationServers=[ldap1],
                    directoryServer=ldap1)
                self.adminDb.addObject(realm1)
                
                #################################################### Policy 1
                # Users
                user1 = RoleUser(name='user1',realmId=realm1.id)
                self.adminDb.addObject(user1)
                user2 = RoleUser(name='user2',realmId=realm1.id)
                self.adminDb.addObject(user2)
                user3 = RoleUser(name='user3',realmId=realm1.id)
                self.adminDb.addObject(user3)
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                
                # Roles
                role1 = UserRole(name='role1',
                                    description='descr1',users=[user1,user2])
                self.adminDb.addObject(role1)
                role2 = UserRole(name='role2',
                                    description='descr2',users=[user3,user4])
                self.adminDb.addObject(role2)            
                
                # Services 
                service1 = RdpService(name='service1',
                                        description='description1')
                self.adminDb.addObject(service1)
                service2 = RdpService(name='service2',
                                        description='description2')
                self.adminDb.addObject(service2)
                service3 = RdpService(name='service3',
                                        description='description3')
                self.adminDb.addObject(service3)
                
                # Group of services
                grp_service1 = ServiceGroup(name='grp_service1')
                grp_service1.services=[service1,service2,service3]
                self.adminDb.addObject(grp_service1)
                
                # Policies
                policy1 = UserAccessPolicy(name='policy1',
                                    description='policy 1')
                policy1.roles=[role1,role2]
                policy1.serviceGroups=[grp_service1]
                self.adminDb.addObject(policy1)
                
                
                #################################################### Policy 2
                # Users
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                user5 = RoleUser(name='user5',realmId=realm1.id)
                self.adminDb.addObject(user5)

                # Roles
                role3 = UserRole(name='role3',
                                    description='descr3',users=[user4,user5])
                self.adminDb.addObject(role3)            
                
                # Services 
                service4 = RdpService(name='service4',
                                        description='description4')
                self.adminDb.addObject(service4)
                service5 = RdpService(name='service5',
                                        description='description5')
                self.adminDb.addObject(service5)
                service6 = RdpService(name='service6',
                                        description='description6')
                self.adminDb.addObject(service6)
                
                # Group of services
                grp_service2 = ServiceGroup(name='grp_service2')
                grp_service2.services=[service4,service5,service6]
                self.adminDb.addObject(grp_service2)
                
                # Policies
                policy2 = UserAccessPolicy(name='policy2',
                                    description='policy 2')
                policy2.roles=[role1,role3]
                policy2.serviceGroups=[grp_service2]
                self.adminDb.addObject(policy2)
                
                #################################################### Policy 3
                # Users
                user6 = RoleUser(name='user6',realmId=realm1.id)
                self.adminDb.addObject(user6)
                user7 = RoleUser(name='user7',realmId=realm1.id)
                self.adminDb.addObject(user7)

                # Roles
                role4 = UserRole(name='role4',
                                    description='descr4',users=[user6,user7])
                self.adminDb.addObject(role4)            
                
                # Services 
                service7 = RdpService(name='service7',
                                        description='description7')
                self.adminDb.addObject(service7)
                service8 = RdpService(name='service8',
                                        description='description8')
                self.adminDb.addObject(service8)

                
                # Group of services
                grp_service3 = ServiceGroup(name='grp_service3')
                grp_service3.services=[service7,service8]
                self.adminDb.addObject(grp_service3)
                
                # Policies
                policy3 = UserAccessPolicy(name='policy3',
                                    description='policy 3')
                policy3.roles=[role4]
                policy3.serviceGroups=[grp_service2,grp_service3]
                self.adminDb.addObject(policy3)
                ####################################################
               
               
                # Testing
                 
                # Error input
                data_error_1=all_services_for_user_realm('userq','realm1',self.adminDb)
                assert(data_error_1=="Veuillez saisir un utilisateur et/ou royaume valide !")
                data_error_2=all_services_for_user_realm('user1','realmQ',self.adminDb)
                assert(data_error_2=="Veuillez saisir un utilisateur et/ou royaume valide !")
                
                # User 1
                data_user_1=all_services_for_user_realm('user1','realm1',self.adminDb)
                assert(data_user_1==[['realm1', 'user1', 'service1', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user1', 'service2', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user1', 'service3', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user1', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user1', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user1', 'service6', 'PASSWORD', 'NONE', 'NONE']])
                # User 2
                data_user_2=all_services_for_user_realm('user2','realm1',self.adminDb)
                assert(data_user_2==[['realm1', 'user2', 'service1', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user2', 'service2', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user2', 'service3', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user2', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user2', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user2', 'service6', 'PASSWORD', 'NONE', 'NONE']])
                # User 3
                data_user_3=all_services_for_user_realm('user3','realm1',self.adminDb)
                assert(data_user_3==[['realm1', 'user3', 'service1', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user3', 'service2', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user3', 'service3', 'PASSWORD', 'NONE', 'NONE']])
                # User 4
                data_user_4=all_services_for_user_realm('user4','realm1',self.adminDb)
                assert(data_user_4==[['realm1', 'user4', 'service1', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user4', 'service2', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user4', 'service3', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user4', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user4', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user4', 'service6', 'PASSWORD', 'NONE', 'NONE']])
                # User 5
                data_user_5=all_services_for_user_realm('user5','realm1',self.adminDb)
                assert(data_user_5==[['realm1', 'user5', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user5', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user5', 'service6', 'PASSWORD', 'NONE', 'NONE']])
                # User 6
                data_user_6=all_services_for_user_realm('user6','realm1',self.adminDb)
                assert(data_user_6==[['realm1', 'user6', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user6', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user6', 'service6', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user6', 'service7', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user6', 'service8', 'PASSWORD', 'NONE', 'NONE']])
                # User 7
                data_user_7=all_services_for_user_realm('user7','realm1',self.adminDb)
                assert(data_user_7==[['realm1', 'user7', 'service4', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user7', 'service5', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user7', 'service6', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user7', 'service7', 'PASSWORD', 'NONE', 'NONE'], ['realm1', 'user7', 'service8', 'PASSWORD', 'NONE', 'NONE']])                


    def test_function_all_users_from_service_realm(self):

        with self.adminDb.session_scope():
                ################################################## Adding information to the database
                # Server
                ldap1 = LdapServer(name = 'ldap1')
                self.adminDb.addObject(ldap1)
                
                # Realm
                realm1 = Realm(name='realm1',
                    authenticationServers=[ldap1],
                    directoryServer=ldap1)
                self.adminDb.addObject(realm1)
                
                #################################################### Policy 1
                # Users
                user1 = RoleUser(name='user1',realmId=realm1.id)
                self.adminDb.addObject(user1)
                user2 = RoleUser(name='user2',realmId=realm1.id)
                self.adminDb.addObject(user2)
                user3 = RoleUser(name='user3',realmId=realm1.id)
                self.adminDb.addObject(user3)
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                
                # Roles
                role1 = UserRole(name='role1',
                                    description='descr1',users=[user1,user2])
                self.adminDb.addObject(role1)
                role2 = UserRole(name='role2',
                                    description='descr2',users=[user3,user4])
                self.adminDb.addObject(role2)            
                
                # Services 
                service1 = RdpService(name='service1',
                                        description='description1')
                self.adminDb.addObject(service1)
                service2 = RdpService(name='service2',
                                        description='description2')
                self.adminDb.addObject(service2)
                service3 = RdpService(name='service3',
                                        description='description3')
                self.adminDb.addObject(service3)
                
                # Group of services
                grp_service1 = ServiceGroup(name='grp_service1')
                grp_service1.services=[service1,service2,service3]
                self.adminDb.addObject(grp_service1)
                
                # Policies
                policy1 = UserAccessPolicy(name='policy1',
                                    description='policy 1')
                policy1.roles=[role1,role2]
                policy1.serviceGroups=[grp_service1]
                self.adminDb.addObject(policy1)
                
                
                #################################################### Policy 2
                # Users
                user4 = RoleUser(name='user4',realmId=realm1.id)
                self.adminDb.addObject(user4)
                user5 = RoleUser(name='user5',realmId=realm1.id)
                self.adminDb.addObject(user5)

                # Roles
                role3 = UserRole(name='role3',
                                    description='descr3',users=[user4,user5])
                self.adminDb.addObject(role3)            
                
                # Services 
                service4 = RdpService(name='service4',
                                        description='description4')
                self.adminDb.addObject(service4)
                service5 = RdpService(name='service5',
                                        description='description5')
                self.adminDb.addObject(service5)
                service6 = RdpService(name='service6',
                                        description='description6')
                self.adminDb.addObject(service6)
                
                # Group of services
                grp_service2 = ServiceGroup(name='grp_service2')
                grp_service2.services=[service4,service5,service6]
                self.adminDb.addObject(grp_service2)
                
                # Policies
                policy2 = UserAccessPolicy(name='policy2',
                                    description='policy 2')
                policy2.roles=[role1,role3]
                policy2.serviceGroups=[grp_service2]
                self.adminDb.addObject(policy2)
                
                #################################################### Policy 3
                # Users
                user6 = RoleUser(name='user6',realmId=realm1.id)
                self.adminDb.addObject(user6)
                user7 = RoleUser(name='user7',realmId=realm1.id)
                self.adminDb.addObject(user7)

                # Roles
                role4 = UserRole(name='role4',
                                    description='descr4',users=[user6,user7])
                self.adminDb.addObject(role4)            
                
                # Services 
                service7 = RdpService(name='service7',
                                        description='description7')
                self.adminDb.addObject(service7)
                service8 = RdpService(name='service8',
                                        description='description8')
                self.adminDb.addObject(service8)

                
                # Group of services
                grp_service3 = ServiceGroup(name='grp_service3')
                grp_service3.services=[service7,service8]
                self.adminDb.addObject(grp_service3)
                
                # Policies
                policy3 = UserAccessPolicy(name='policy3',
                                    description='policy 3')
                policy3.roles=[role4]
                policy3.serviceGroups=[grp_service2,grp_service3]
                self.adminDb.addObject(policy3)
                ####################################################
               
               
                # Testing
                 
                # Error input
                data_error_1=all_users_from_service_realm('serviceQ',self.adminDb)
                assert(data_error_1=="Veuillez saisir un service et/ou royaume valide !")

                
                # Service 1
                data_Service_1=all_users_from_service_realm('service1',self.adminDb)
                assert(data_Service_1==[['service1', 'realm1', 'user1'], ['service1', 'realm1', 'user2'], ['service1', 'realm1', 'user3'], ['service1', 'realm1', 'user4']])
                # Service 2
                data_Service_2=all_users_from_service_realm('service2',self.adminDb)
                assert(data_Service_2==[['service2', 'realm1', 'user1'], ['service2', 'realm1', 'user2'], ['service2', 'realm1', 'user3'], ['service2', 'realm1', 'user4']])
                # Service 3
                data_Service_3=all_users_from_service_realm('service3',self.adminDb)
                assert(data_Service_3==[['service3', 'realm1', 'user1'], ['service3', 'realm1', 'user2'], ['service3', 'realm1', 'user3'], ['service3', 'realm1', 'user4']])
                # Service 4
                data_Service_4=all_users_from_service_realm('service4',self.adminDb)
                assert(data_Service_4==[['service4', 'realm1', 'user1'], ['service4', 'realm1', 'user2'], ['service4', 'realm1', 'user4'], ['service4', 'realm1', 'user5'], ['service4', 'realm1', 'user6'], ['service4', 'realm1', 'user7']])
                # Service 5
                data_Service_5=all_users_from_service_realm('service5',self.adminDb)
                assert(data_Service_5==[['service5', 'realm1', 'user1'], ['service5', 'realm1', 'user2'], ['service5', 'realm1', 'user4'], ['service5', 'realm1', 'user5'], ['service5', 'realm1', 'user6'], ['service5', 'realm1', 'user7']])
                # Service 6
                data_Service_6=all_users_from_service_realm('service6',self.adminDb)
                assert(data_Service_6==[['service6', 'realm1', 'user1'], ['service6', 'realm1', 'user2'], ['service6', 'realm1', 'user4'], ['service6', 'realm1', 'user5'], ['service6', 'realm1', 'user6'], ['service6', 'realm1', 'user7']])
                # Service 7
                data_Service_7=all_users_from_service_realm('service7',self.adminDb)
                assert(data_Service_7==[['service7', 'realm1', 'user6'], ['service7', 'realm1', 'user7']])
                # Service 8
                data_Service_8=all_users_from_service_realm('service8',self.adminDb)
                assert(data_Service_8==[['service8', 'realm1', 'user6'], ['service8', 'realm1', 'user7']])




if __name__ == '__main__':
    main()
    