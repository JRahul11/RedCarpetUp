from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core_app.models import *

class CustomGroups:


    # SuperUser Group
    def createAdminGroup(self):
        try:                                                                                                        # Check if the SuperUser Group exists
            Group.objects.get(name='SuperUser')
        except:
            superUserGroup = Group.objects.create(name ='SuperUser')                                                        # Create SuperUser Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                addPermission = Permission.objects.get(codename='admin_add_taxpayer')
            except:
                addPermission = Permission.objects.create(name='Add TaxPayer', codename='admin_add_taxpayer', content_type = content_type)    # Add Permission for SuperUser
                superUserGroup.permissions.add(addPermission)                                                           # Append the Add Permission to SuperUser Group
            try:
                viewPermission = Permission.objects.get(codename='admin_view_taxpayer')
            except:
                viewPermission = Permission.objects.create(name='View TaxPayer', codename='admin_view_taxpayer',content_type = content_type)  # View Permission for SuperUser
                superUserGroup.permissions.add(viewPermission)                                                          # Append the View Permission to SuperUser Group
            try:
                updatePermission = Permission.objects.get(codename='admin_update_taxpayer')
            except:
                updatePermission = Permission.objects.create(name='Update TaxPayer', codename='admin_update_taxpayer',content_type = content_type)  # Update Permission for SuperUser
                superUserGroup.permissions.add(updatePermission)                                                        # Append the Update Permission to SuperUser Group


    # TaxAccountant Group
    def createTaxAccountantGroup(self):
        try:                                                                                                        # Check if the TaxAccountant Group exists
            Group.objects.get(name='TaxAccountant')
        except:
            taxAccountantGroup = Group.objects.create(name ='TaxAccountant')                                        # Create TaxAccountant Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                addPermission = Permission.objects.get(codename='accountant_add_taxpayer')
            except:
                addPermission = Permission.objects.create(name='Add TaxPayer', codename='accountant_add_taxpayer', content_type = content_type)    # Add Permission for TaxAccountant
                taxAccountantGroup.permissions.add(addPermission)                                                   # Append the Add Permission to TaxAccountant Group
            try:
                viewPermission = Permission.objects.get(codename='admin_view_taxpayer')
            except:
                viewPermission = Permission.objects.create(name='View TaxPayer', codename='accountant_view_taxpayer',content_type = content_type)  # View Permission for TaxAccountant
                taxAccountantGroup.permissions.add(viewPermission)                                                  # Append the View Permission to TaxAccountant Group
            try:
                updatePermission = Permission.objects.get(codename='admin_update_taxpayer')
            except:
                updatePermission = Permission.objects.create(name='Update TaxPayer', codename='accountant_update_taxpayer',content_type = content_type)  # Update Permission for TaxAccountant
                taxAccountantGroup.permissions.add(updatePermission)                                                # Append the Update Permission to TaxAccountant Group


    # TaxPayer Group
    def createTaxPayerGroup(self):
        try:                                                                                                        # Check if the Group exists
            Group.objects.get(name='TaxPayer')
        except:
            taxPayerGroup = Group.objects.create(name ='TaxPayer')                                                  # Create TaxPayer Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                viewPermission = Permission.objects.get(codename='view_user')
            except:
                viewPermission = Permission.objects.create(name='View User', codename='view_user',content_type = content_type)  # View Permission for TaxPayer
                taxPayerGroup.permissions.add(viewPermission) 


    # Adding Users to Group
    # 1-> Tax Payer,    2-> Tax Accountant,    3-> Admin
    def addUserToGroup(self, user, user_type):
        if user_type == 1:
            taxPayerGroup = Group.objects.get(name ='TaxPayer')
            user.groups.add(taxPayerGroup)
        elif user_type == 2:
            taxAccountantGroup = Group.objects.get(name ='TaxAccountant')
            user.groups.add(taxAccountantGroup)
        elif user_type == 3:
            adminGroup = Group.objects.get(name ='SuperUser')
            user.groups.add(adminGroup)
