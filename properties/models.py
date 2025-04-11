from django.db import models
from django.contrib.auth.models import User
from modeltranslation.translator import register, TranslationOptions

class PropertyType(models.Model):
  name_en = models.CharField(max_length=50)
  name_ar = models.CharField(max_length=50)

  def __str__(self):
    return self.name_en

class Amenity(models.Model):
  name_en = models.CharField(max_length=50)
  name_ar = models.CharField(max_length=50)

  def __str__(self):
    return self.name_en

class Property(models.Model):
  PROPERTY_STATUS = [
    ('available', 'Available'),
    ('rented', 'Rented'),
    ('under_maintenance', 'Under Maintenance'),
  ]
  title_en = models.CharField(max_length=200)
  title_ar = models.CharField(max_length=200)
  description_en = models.TextField()
  description_ar = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  area = models.FloatField()
  status = models.CharField(max_length=20, choices=PROPERTY_STATUS)
  property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
  amenities = models.ManyToManyField(Amenity, blank=True)
  owner = models.ForeignKey('Owner', on_delete=models.CASCADE)

  def __str__(self):
    return self.title_en

class PropertyImage(models.Model):
  property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='property_images/')

class Owner(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=15)

  def __str__(self):
    return self.user.get_full_name()

class Company(models.Model):
  name_en = models.CharField(max_length=100)
  name_ar = models.CharField(max_length=100)
  commercial_number = models.CharField(max_length=50)
  
  def __str__(self):
    return self.name_en

class Tenant(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
  is_company = models.BooleanField(default=False)

  def __str__(self):
    return self.company.name_en if self.is_company else self.user.get_full_name()

class Investor(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  investment_share = models.FloatField()
  
  def __str__(self):
    return self.user.get_full_name()

class Building(models.Model):
  name_en = models.CharField(max_length=100)
  name_ar = models.CharField(max_length=100)
  location_en = models.CharField(max_length=200)
  location_ar = models.CharField(max_length=200)
  investors = models.ManyToManyField(Investor)

  def __str__(self):
    return self.name_en

class Floor(models.Model):
  building = models.ForeignKey(Building, on_delete=models.CASCADE)
  number = models.IntegerField()
  
  def __str__(self):
    return f"{self.building.name_en} - Floor {self.number}"

class Unit(models.Model):
  property = models.OneToOneField(Property, on_delete=models.CASCADE)
  floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
  unit_number = models.CharField(max_length=10)
  
  def __str__(self):
    return f"{self.property.title_en} - {self.unit_number}"

class LeaseContract(models.Model):
  property = models.ForeignKey(Property, on_delete=models.CASCADE)
  tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
  start_date = models.DateField()
  end_date = models.DateField()
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f"Contract for {self.property.title_en}"

class Payment(models.Model):
  contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date_paid = models.DateField()
  is_paid = models.BooleanField(default=False)

  def __str__(self):
    return f"Payment #{self.id}"

class MaintenanceRequest(models.Model):
  property = models.ForeignKey(Property, on_delete=models.CASCADE)
  tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
  description_en = models.TextField()
  description_ar = models.TextField()
  status = models.CharField(max_length=20, default='pending')

  def __str__(self):
    return f"Maintenance Request for {self.property.title_en}"
