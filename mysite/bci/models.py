import uuid

from django.db import models


class ProccesDetails(models.Model):
    patient = models.CharField(max_length=100)
    filter_low = models.FloatField()
    filter_high = models.FloatField()
    psd_freq = models.CharField(max_length=100)
    split_persent = models.FloatField()
    svm_c = models.FloatField()
    svm_l1 = models.FloatField()
    svm_l2 = models.FloatField()
    result_acc = models.FloatField(null=True)
    result_loss = models.FloatField(null=True)
    result_f1_score = models.FloatField(null=True)
    img_url = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.patient


# class Status(models.Model):

