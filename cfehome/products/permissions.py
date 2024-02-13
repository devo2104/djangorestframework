from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    # i don't know but this perms_map is working like magic , earlier when i give view permission, it gave it all the premissions as shown by below code when i return True

    # but now, when i give view perm in django admin, the api view have only view perms, which is as expected
    

    def has_permission(self, request, view):
        # i have given the permisson in th django admin though, it is still getting denied here if the user is not staff
        if not request.user.is_staff:
            return False
        return super().has_permission(request, view)

    # def has_permission(self, request, view):
    #     user = request.user
    #     print(user)
    #     print(user.get_all_permissions())
    #     if user.is_staff:
    #         if user.has_perm('products.view_product'): #app_name.verb_modelName
    #             return True
    #         return False
    #     print('----------------', user.get_all_permissions())
    #     return False