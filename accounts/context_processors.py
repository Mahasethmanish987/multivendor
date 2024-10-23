from vendor.models import vendor
from django.conf import settings

def get_vendor(request):
    try:
      vendor1=vendor.objects.get(user=request.user)
    except:
       vendor1=None
    return dict(vendor=vendor1)


def get_google_api(request):
   return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}