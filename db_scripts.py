# create roles in database
# user = Role(type="user")
# user.save()
# admin = Role(type="admin")
# admin.save()
# Permission(name="Can view ticket", codename="view_ticket").save()
# Permission(name="Can create ticket", codename="create_ticket").save()
# Permission(name="Can modify ticket", codename="modify_ticket").save()
# Permission(name="Can assign ticket", codename="assign_ticket").save()
# Permission(name="Can accept ticket", codename="accept_ticket").save()
#  admin = User.objects.get(username='adedayo')

# >>> admin_user = Roles.objects.get(type='admin')
#
# >>> admin_user = Role.objects.get(type='admin')
# >>> admin_user
#
# >>> admin_user.permissions
# >>> p1 = Permission.objects.get(codename='view_ticket')
# >>> admin_user.permissions.add(p1)
# >>> admin_user.permissions.add( Permission.objects.get(codename='accept_ticket'))
# >>> admin_user.permissions.add( Permission.objects.get(codename='reject_ticket'))
# user = User.objects.get(username='lumexRalph')
# >>> non_admin_user = Role.objects.get(type='user')
# >>> non_admin_user.permissions.add(Permission.objects.get(codename='view_ticket'))
# >>> non_admin_user.permissions.add(Permission.objects.get(codename='create_ticket'))
# >>> non_admin_user.permissions.add(Permission.objects.get(codename='assign_ticket'))
# >>> admin_user.permissions.add( Permission.objects.get(codename='modify_ticket'))
