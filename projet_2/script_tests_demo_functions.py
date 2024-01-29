import pytest
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
from proveitadmin.service import AUTHENTICATION_CREDENTIALS
from proveitadmin.globals.constants import AUTHENTICATION_MODE
from proveitadmin.authentication.realm import Realm
from proveitadmin.service.group import ServiceGroup
from scripts_elmoustapha_malick.projet_2.script_table_joined import all_services_for_user_realm_demo,all_users_from_service_realm_demo,list_authen_mode,list_authen_creden,enum_string
from scripts_elmoustapha_malick.projet_2.script_all_flatten_info import all_services_demo,all_royaumes_demo,all_users_demo,all_servers_demo,all_policies_demo
from proveitadmin.authentication.ldap import LdapServer
from proveitadmin.authorization import UserRole
from proveitadmin.authorization.accesspolicy.accesspolicy import AccessPolicy
from proveitadmin.authorization.filter.datefilter import DateFilter
import pytz

"""
#@author elmoustapha.malick@rubycat.eu
"""

################################# READ ME : 
                                # The functions starting with *_demo are functions witch are tested here so it can give us 
                                # a good understanding of these functions and how they work 
                                # These functions where created to have : review of authorizations
                                # so the aim of Projet 2 is to create the prototypes or demos of functions that will give us review of authorizations
                                # and Projet 3 will take this functions and can modifie it so the functions of Projet 2 and Projet 3 are not exactly the same
 
class Test_script_table_joined:
    # Function : all_services_for_user_realm_demo  
    # show for user and a realm all services whitch are accessed by the user and other information about the services
    # like filtres, authentication mode and credentials.
    
    # Function : all_users_from_service_realm_demo
    # show for a service and a realm all users witch can access to this service and also give the some information about
    # the service.
    
    # We test functions :all_services_for_user_realm_demo,all_users_from_service_realm_demo with thess cases : 
    
    #### Case 1 :
    #Services
    #grp_service1=serviceA
    #grp_service2=serviceB
    #grp_service3=serviceC
    
    #Roles
    #role1=userA
    #role2=userB
    #role3=userC
    
    
    #Policies
    #Policy1=role1,grp_service1
    #Policy2=role2,grp_service2
    #Policy3=role3,grp_service3
    
    
    #### Case 2 :
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
    def test_input_error_of_user_forfunction_all_services_for_user_realm_case1_policy1(self):
        with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    userA = RoleUser(name='userA',realmId=realm1.id)
                    self.adminDb.addObject(userA)

                    # Roles
                    role1 = UserRole(name='role1',
                                        description='descr1',users=[userA])
                    self.adminDb.addObject(role1)
          
                    # Services 
                    serviceA = RdpService(name='serviceA',
                                            description='descriptionA')
                    self.adminDb.addObject(serviceA)
                    
                    
                    # Group of services
                    grp_service1 = ServiceGroup(name='grp_service1')
                    grp_service1.services=[serviceA]
                    self.adminDb.addObject(grp_service1)
                           
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1]
                    policy1.serviceGroups=[grp_service1]
                    self.adminDb.addObject(policy1)
                    ####################################################
                    # Testing
                    # For user2 witch does not exist
                    assert(all_services_for_user_realm_demo('user2','realm1',self.adminDb)=="Veuillez saisir un utilisateur et/ou royaume valide !")
    
    
    def test_input_error_of_realm_forfunction_all_services_for_user_realm_case1_policy1(self):
        with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    userA = RoleUser(name='userA',realmId=realm1.id)
                    self.adminDb.addObject(userA)

                    # Roles
                    role1 = UserRole(name='role1',
                                        description='descr1',users=[userA])
                    self.adminDb.addObject(role1)
          
                    # Services 
                    serviceA = RdpService(name='serviceA',
                                            description='descriptionA')
                    self.adminDb.addObject(serviceA)
                    
                    
                    # Group of services
                    grp_service1 = ServiceGroup(name='grp_service1')
                    grp_service1.services=[serviceA]
                    self.adminDb.addObject(grp_service1)
                           
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1]
                    policy1.serviceGroups=[grp_service1]
                    self.adminDb.addObject(policy1)
                    ####################################################
                    # Testing
                    # For realm2 witch does not exist
                    assert(all_services_for_user_realm_demo('userA','realm2',self.adminDb)=="Veuillez saisir un utilisateur et/ou royaume valide !")
            
    def test_input_error_of_service_forfunction_all_users_from_service_realm_case1_policy1(self):
        with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    userA = RoleUser(name='userA',realmId=realm1.id)
                    self.adminDb.addObject(userA)

                    # Roles
                    role1 = UserRole(name='role1',
                                        description='descr1',users=[userA])
                    self.adminDb.addObject(role1)
          
                    # Services 
                    serviceA = RdpService(name='serviceA',
                                            description='descriptionA')
                    self.adminDb.addObject(serviceA)
                    
                    
                    # Group of services
                    grp_service1 = ServiceGroup(name='grp_service1')
                    grp_service1.services=[serviceA]
                    self.adminDb.addObject(grp_service1)
                           
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1]
                    policy1.serviceGroups=[grp_service1]
                    self.adminDb.addObject(policy1)
                    ####################################################
                    # Testing
                    # For ServiceB witch does not exist
                    assert(all_users_from_service_realm_demo('serviceB','realm1',self.adminDb)=="Veuillez saisir un service et/ou royaume valide !")
    
    
    def test_input_error_of_realm_forfunction_all_users_from_service_realm_case1_policy1(self):
        with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    userA = RoleUser(name='userA',realmId=realm1.id)
                    self.adminDb.addObject(userA)

                    # Roles
                    role1 = UserRole(name='role1',
                                        description='descr1',users=[userA])
                    self.adminDb.addObject(role1)
          
                    # Services 
                    serviceA = RdpService(name='serviceA',
                                            description='descriptionA')
                    self.adminDb.addObject(serviceA)
                    
                    
                    # Group of services
                    grp_service1 = ServiceGroup(name='grp_service1')
                    grp_service1.services=[serviceA]
                    self.adminDb.addObject(grp_service1)
                           
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1]
                    policy1.serviceGroups=[grp_service1]
                    self.adminDb.addObject(policy1)
                    ####################################################
                    # Testing
                    # For realm2
                    assert(all_users_from_service_realm_demo('serviceA','realm2',self.adminDb)=="Veuillez saisir un service et/ou royaume valide !")
            
   
        
    def test_all_services_for_user_realm_case1_policy1(self):
        with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    userA = RoleUser(name='userA',realmId=realm1.id)
                    self.adminDb.addObject(userA)

                    # Roles
                    role1 = UserRole(name='role1',
                                        description='descr1',users=[userA])
                    self.adminDb.addObject(role1)
          
                    # Services 
                    serviceA = RdpService(name='serviceA',
                                            description='descriptionA')
                    self.adminDb.addObject(serviceA)
                    
                    
                    # Group of services
                    grp_service1 = ServiceGroup(name='grp_service1')
                    grp_service1.services=[serviceA]
                    self.adminDb.addObject(grp_service1)
                           
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1]
                    policy1.serviceGroups=[grp_service1]
                    self.adminDb.addObject(policy1)
                    ####################################################
                    # Testing
                    # For userA
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('userA','realm1',self.adminDb)
                    assert (set_service_with_info=={('serviceA', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'userA', 'realm1'})

    def test_all_user_from_service_realm_case1_policy1(self):
                with self.adminDb.session_scope():
                        ################################################## Adding information
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
                        userA = RoleUser(name='userA',realmId=realm1.id)
                        self.adminDb.addObject(userA)

                        # Roles
                        role1 = UserRole(name='role1',
                                            description='descr1',users=[userA])
                        self.adminDb.addObject(role1)
            
                        # Services 
                        serviceA = RdpService(name='serviceA',
                                                description='descriptionA')
                        self.adminDb.addObject(serviceA)
                        
                        
                        # Group of services
                        grp_service1 = ServiceGroup(name='grp_service1')
                        grp_service1.services=[serviceA]
                        self.adminDb.addObject(grp_service1)
                            
                
                        # Policies
                        policy1 = UserAccessPolicy(name='policy1',
                                            description='policy 1')
                        policy1.roles=[role1]
                        policy1.serviceGroups=[grp_service1]
                        self.adminDb.addObject(policy1)
                        ####################################################
                        # Testing
                        # For serviceA
                        set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('serviceA','realm1',self.adminDb)
                        assert (set_user_with_info=={('userA', 'realm1')})
                        assert (set_info_service_realm== {'serviceA', 'PASSWORD', 'NONE','NO FILTRE'})
                
        
    def test_all_services_for_user_realm_case2_policy1_with_filtre(self):

            with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    
                    # Filtres 
                    filter1 = DateFilter(name = 'filter1',
                                    description = 'filter one')
                    self.adminDb.addObject(filter1)
                    filter2 = DateFilter(name = 'filter2',
                                    description = 'filter one')
                    self.adminDb.addObject(filter2)
                    
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1,role2]
                    policy1.serviceGroups=[grp_service1]
                    policy1.filters=[filter1,filter2]
                    self.adminDb.addObject(policy1)    
                    
                    ####################################################
                    # Testing
                    # For user1
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user1','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','filter1','filter2'), ('service2', 'PASSWORD', 'NONE','filter1','filter2'), ('service3', 'PASSWORD', 'NONE','filter1','filter2')})
                    assert (set_info_user_realm=={'user1', 'realm1'})
                    # For user2
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user2','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','filter1','filter2'), ('service2', 'PASSWORD', 'NONE','filter1','filter2'), ('service3', 'PASSWORD', 'NONE','filter1','filter2')})
                    assert (set_info_user_realm=={'user2', 'realm1'})            
 
     
    def test_all_services_for_user_realm_case2_no_filtre(self):

            with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    # For user1
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user1','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','NO FILTRE'), ('service2', 'PASSWORD', 'NONE','NO FILTRE'), ('service3', 'PASSWORD', 'NONE','NO FILTRE'), ('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'user1', 'realm1'})
                    # For user2
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user2','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','NO FILTRE'), ('service2', 'PASSWORD', 'NONE','NO FILTRE'), ('service3', 'PASSWORD', 'NONE','NO FILTRE'), ('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE')})                    
                    assert (set_info_user_realm=={'user2', 'realm1'})
                    # For user3
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user3','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','NO FILTRE'), ('service2', 'PASSWORD', 'NONE','NO FILTRE'), ('service3', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'user3', 'realm1'})
                    # For user4
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user4','realm1',self.adminDb)
                    assert (set_service_with_info=={('service1', 'PASSWORD', 'NONE','NO FILTRE'), ('service2', 'PASSWORD', 'NONE','NO FILTRE'), ('service3', 'PASSWORD', 'NONE','NO FILTRE'), ('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE')})                    
                    assert (set_info_user_realm=={'user4', 'realm1'})
                    # For user5
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user5','realm1',self.adminDb)
                    assert (set_service_with_info=={('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'user5', 'realm1'})
                    # For user6
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user6','realm1',self.adminDb)
                    assert (set_service_with_info=={('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE'),('service7', 'PASSWORD', 'NONE','NO FILTRE'), ('service8', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'user6', 'realm1'})
                    # For user7
                    set_service_with_info,set_info_user_realm=all_services_for_user_realm_demo('user7','realm1',self.adminDb)
                    assert (set_service_with_info=={('service4', 'PASSWORD', 'NONE','NO FILTRE'), ('service5', 'PASSWORD', 'NONE','NO FILTRE'), ('service6', 'PASSWORD', 'NONE','NO FILTRE'),('service7', 'PASSWORD', 'NONE','NO FILTRE'), ('service8', 'PASSWORD', 'NONE','NO FILTRE')})
                    assert (set_info_user_realm=={'user7', 'realm1'})   
                    
                    
    def test_all_users_from_service_realm_case2_policy1_with_filtre(self):

            with self.adminDb.session_scope():
                    ################################################## Adding information
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
                    
                    # Filtres 
                    filter1 = DateFilter(name = 'filter1',
                                    description = 'filter one')
                    self.adminDb.addObject(filter1)
                    filter2 = DateFilter(name = 'filter2',
                                    description = 'filter one')
                    self.adminDb.addObject(filter2)
                    
            
                    # Policies
                    policy1 = UserAccessPolicy(name='policy1',
                                        description='policy 1')
                    policy1.roles=[role1,role2]
                    policy1.serviceGroups=[grp_service1]
                    policy1.filters=[filter1,filter2]
                    self.adminDb.addObject(policy1)    
                    
                    ####################################################
                    
                    # Testing
                    # For service1
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service1','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user3', 'realm1'), ('user4', 'realm1')})
                    assert (set_info_service_realm=={'service1', 'PASSWORD','NONE','filter1','filter2'})
                    # For service2
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service2','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user3', 'realm1'), ('user4', 'realm1')})
                    assert (set_info_service_realm=={'service2', 'PASSWORD','NONE','filter1','filter2'})
                    
                    
    def test_all_users_from_service_realm_case2_no_filtre(self):

            with self.adminDb.session_scope():
                    ##################################################################### Adding information
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
                    #####################################################################
                    
                    
                    # Testing
                    # For service1
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service1','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user3', 'realm1'), ('user4', 'realm1')})
                    assert (set_info_service_realm=={'service1', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service2
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service2','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user3', 'realm1'), ('user4', 'realm1')})
                    assert (set_info_service_realm=={'service2', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service3
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service3','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user3', 'realm1'), ('user4', 'realm1')})
                    assert (set_info_service_realm=={'service3', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service4
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service4','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user4', 'realm1'),('user5', 'realm1'), ('user6', 'realm1'), ('user7', 'realm1')})
                    assert (set_info_service_realm=={'service4', 'PASSWORD','NONE','NO FILTRE'})
                    # For service5
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service5','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'),  ('user4', 'realm1'),('user5', 'realm1'), ('user6', 'realm1'), ('user7', 'realm1')})
                    assert (set_info_service_realm=={'service5', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service6
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service6','realm1',self.adminDb)
                    assert (set_user_with_info=={('user1', 'realm1'), ('user2', 'realm1'), ('user4', 'realm1'),('user5', 'realm1'), ('user6', 'realm1'), ('user7', 'realm1')})
                    assert (set_info_service_realm=={'service6', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service7
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service7','realm1',self.adminDb)
                    assert (set_user_with_info=={('user6', 'realm1'), ('user7', 'realm1')})
                    assert (set_info_service_realm=={'service7', 'PASSWORD','NONE','NO FILTRE'})
                    
                    # For service8
                    set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service8','realm1',self.adminDb)
                    assert (set_user_with_info=={('user6', 'realm1'), ('user7', 'realm1')})
                    assert (set_info_service_realm=={'service8', 'PASSWORD','NONE','NO FILTRE'})
                
class Test_script_all_flatten_info:
        # Functions : all_services_demo,all_royaumes_demo,all_users_demo,all_servers_demo,all_policies_demo
        
        # Function : all_services_demo show all available services 
        # Function : all_royaumes_demo show all available realm with their id but we are not testing it id because it changes
        # Function : all_users_demo show all available users and the id of it realm but we are not testing it id because it changes
        # Function : all_servers_demo show all available servers
        # Function : all_policies_demo show all available policies
        
        # We are going to tests all four functions with this case : 

        #### Case default :
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
        
        def test_all_functions_case_default(self):
            with self.adminDb.session_scope():
                        ##################################################################### Adding information
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
                        ##########################################################
            # Testing
            assert(all_services_demo(self.adminDb)=={'service1', 'service2', 'service3', 'service4', 'service5', 'service6', 'service7', 'service8'})
            assert(all_users_demo(self.adminDb)=={'user1', 'user2', 'user3','user4', 'user5', 'user6', 'user7'})
            assert(all_royaumes_demo(self.adminDb)=={'realm1'})
            assert(all_servers_demo(self.adminDb)=={'ldap1'})
            assert(all_policies_demo(self.adminDb)=={'policy1', 'policy2', 'policy3'})            
                      
if __name__ == '__main__':
   main()