from django.db import models
# from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Party(models.Model):
    name =  models.CharField(max_length=100,unique=True)
    # phone_regex =RegexValidator(regex=r'^\ ?1?\d{9,15}$', message="Phone number must be entered in the format: ' 999999999'. Up to 10 digits allowed.")
    # phone=models.CharField(validators=[phone_regex],max_length=10,default=None,null=False)
    phone = models.CharField(max_length=10,default=None,null=False)
    email = models.EmailField()
    billing_address=models.CharField(max_length=150,default=None,null=True)
    # pincode_regex= RegexValidator(regex=r'^[1-9][0-9]{5}$', message="Pincode must be entered in the format: ' 999999'. Up to 6 digits allowed.")
    pincode=models.CharField(max_length=6,default=None,null=True)

    def __str__(self):
        return f'{self.name}'

class Quotation(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,default = 1)
    qno = models.CharField(max_length=20,default='CSPL/')
    enq_ref = models.CharField(max_length=30,default='')
    party = models.ForeignKey(Party,on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)
    total = models.FloatField(default=0.0)
    totalnos = models.IntegerField(default=0.0)
    is_converted = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.id} {self.party.name}'

class TandC(models.Model):
    prices = models.CharField(max_length=50,default='Prices are net')
    taxes = models.CharField(max_length=50,default="18% GST extra as applicable")
    delivery = models.CharField(max_length=20,default="Ex stock at vasai")
    payment = models.CharField(max_length=80,default="50% advance payment along with po & balance against proforma invoice")
    validity = models.CharField(max_length=30,default="30 days from today.")
    freight = models.CharField(max_length=20,default="On to pay basis")
    comments = models.TextField(default="We are looking forward to your response, regarding the above.\nIn case on any query please contact us immediately\nFrom Citroenswitchgears Pvt Ltd\nRegards\nJatin Parikh")
    quotation = models.ForeignKey(Quotation,on_delete=models.CASCADE)
    
    # @classmethod
    # def get_default_id(cls):
    #     exam, created = cls.objects.get_or_create()
    #     return exam.pk

    def __str__(self):
        return f'Qid:{self.quotation} {self.prices} {self.taxes} {self.delivery} {self.payment} {self.validity} {self.freight}'

class QuotationItems(models.Model):
    item_code = models.CharField(max_length=50,default='')
    qno = models.CharField(max_length=20,default='CSPL/')
    refno = models.CharField(max_length=20,default='')
    item_description = models.CharField(max_length=75,null=True)
    # item_code = models.ForeignKey(Item,on_delete=models.DO_NOTHING,default=Item.objects.all().first())
    # profit_margin = models.FloatField(default=0.0)
    price_quoted = models.FloatField(default=0)
    qty =models.IntegerField(default=0)
    discount = models.FloatField(default=0.0,null=True)
    margin = models.FloatField(default=0.0,null=True)
    sub_total = models.FloatField(default=0.0)
    is_converted = models.BooleanField(default=False)
    quotation = models.ForeignKey(Quotation,on_delete=models.CASCADE)
    brand_choices = [('abb','ABB'),('legrand','LEGRAND'),('phoenix mecano','PHEONIX MECANO'),('eaton','EATON'),('Bussmann','Bussmann')]
    brand = models.CharField(choices = brand_choices,max_length = 40,default="Bussmann",null = True)
    
    def __str__(self):
        return f'{self.quotation.party.name} {self.item_code}'

class Item(models.Model):
    item_code = models.CharField(max_length=50,default='',unique=True)
    item_description = models.CharField(max_length=75,null=True)
    MRP = models.FloatField(default=0)
    BP = models.FloatField(default=0)
    MOQ = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item_code}'



