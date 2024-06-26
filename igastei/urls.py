from django.contrib import admin
from django.urls import path, include
from django.urls import path
from igastei.views import CustomTokenObtainPairView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Index.as_view(), name = 'index'),
    path('gastos/', include('gastos.urls'), name='gastos'),
    path('autenticacao-api/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
