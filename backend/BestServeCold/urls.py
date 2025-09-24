from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.urls import include, path
from django.shortcuts import redirect


from DraftGenerator.views import (
    DraftGeneratorAPIView,
    DraftListAPIView,
    BatchListAPIView,
)
from User.views import UserListAPIView, UserDetailAPIView

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "draftgenerator": reverse("draftgenerator", request=request, format=format),
        "drafts": reverse("draft-list", request=request, format=format),
        "batches": reverse("batch-list", request=request, format=format),
        "users": reverse("user-list", request=request, format=format),
    })


urlpatterns = [

    path("admin/", admin.site.urls),
    # path("", include(router.urls)),
    path("", api_root, name="api-root"),

    path("draftgenerator/", DraftGeneratorAPIView.as_view(), name="draftgenerator"),
    path("drafts/", DraftListAPIView.as_view(), name="draft-list"),
    path("batches/", BatchListAPIView.as_view(), name="batch-list"),
    path('batches/<int:id>/', BatchListAPIView.as_view()),


    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),

    # path("users/", include("users.urls")),
    # path("accounts/", include("allauth.urls")),
    
]
   
