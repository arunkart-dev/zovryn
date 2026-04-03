from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = router.urls

# Routes this generates:
#   POST   /users/          → create (register)
#   POST   /users/login/    → login, returns JWT
#   GET    /users/me/       → current user profile
#   GET    /users/          → list all users      (admin only)
#   GET    /users/<id>/     → retrieve user       (admin only)
#   PUT    /users/<id>/     → update user         (admin only)
#   DELETE /users/<id>/     → delete user         (admin only)