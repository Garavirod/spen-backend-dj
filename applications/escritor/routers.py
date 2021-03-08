# third party app
from rest_framework.routers import DefaultRouter
# viewsets
from . import viewsets

# Creamos router para conectar con lso viewsets
router = DefaultRouter()

# Registramos rutas
router.register(r'register',viewsets.RegisterUserViewset, basename='register')
router.register(r'login',viewsets.LoginUserViewSet, basename='login')


# Definición de urlpatterns
urlpatterns = router.urls