"""
URL configuration for backendshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from inetshop.views import ProductInfoView, CategoryView, ShopView, PartnerUpdate

app_name = 'inetshop'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories', CategoryView.as_view(), name='categories'),
    path('shops', ShopView.as_view(), name='shops'),
    path('products', ProductInfoView.as_view(), name='product'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    # path('user/register', RegisterAccount.as_view(), name='user-register'),
]
