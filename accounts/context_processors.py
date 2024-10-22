from vendor.models import vendor


def get_vendor(request):
    try:
      vendor1=vendor.objects.get(user=request.user)
    except:
       vendor1=None
    return dict(vendor=vendor1)