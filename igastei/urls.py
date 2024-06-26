from django.contrib import admin
from django.urls import path, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Index.as_view(), name = 'index'),
    path('gastos/', include('gastos.urls'), name='gastos'),
]
