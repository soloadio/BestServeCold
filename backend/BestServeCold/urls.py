from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.urls import include, path
from django.shortcuts import redirect


from fileparser.views import FileParserAPIView


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "fileparser": reverse("fileparser", request=request, format=format),
        # "users": reverse("users", request=request, format=format),
    })


urlpatterns = [

    path("admin/", admin.site.urls),
    # path("", include(router.urls)),
    path("", api_root, name="api-root"),

    path("file-parser/", FileParserAPIView.as_view(), name="fileparser"),


    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    
]
   
