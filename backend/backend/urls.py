from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views.static import serve
# from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from usermanagement.views import (
    MyTokenObtainPairView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('webcourse.urls')),
    path('api/', include('usermanagement.urls')),
    # path('api/', include('usermanagement.urls'))
    path('api/', include('crawl.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]