from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.urls import include, path
from django.shortcuts import redirect


from fileparser.views import CSVUploadView
# router.register(r"fileparser", FileparserViewset)


# @api_view(["GET"])
# def api_root(request, format=None):
#     return Response(
#         {
#             # "experience": reverse("experience-list", request=request, format=format),

#         }
#     )


urlpatterns = [

    path("admin/", admin.site.urls),
    # path("", api_root),
    path('', CSVUploadView.as_view(), name='fileparser'),
     # path("auth/", include("userauth.urls")),
]
   
