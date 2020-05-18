from routepang.model.UrlModel import Url

class UrlController():

    def insertUrl(self, request, location_id):

        if not Url.objects.filter(url=request).exists():
            Url(url=request, location_id=location_id).save()

        return