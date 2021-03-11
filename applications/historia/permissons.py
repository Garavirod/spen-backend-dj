from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """ 
        Da el acceso a los usuarios que son propietarios de una hisotria,
        en caso de querer eliminarla, leerla (puede no estar terminada) o
        editarla. 
    """
    def has_object_permission(self,request,view,obj):        
        return obj.autor == request.user        