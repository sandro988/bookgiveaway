from .views import BookViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", BookViewSet, basename="books")
urlpatterns = router.urls
