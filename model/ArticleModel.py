from django.db import models

class Article(models.Model):
    article_id = models.BigAutoField(blank=False, primary_key=True)
    location_id = models.BigIntegerField(blank=False)

    # id 대신 link_url
    # link_id = models.BigIntegerField(null=True, blank=False)
    image = models.CharField(max_length=1000, null=True, blank=False, default="no image")
    summary = models.CharField(max_length=500, null=True, blank=False)
    reg_date = models.DateTimeField(null=True, blank=False)

    # 불필
    # user_id = models.IntegerField(blank=False)

    # 출처를 위한 link 필요?
    url = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.article_id