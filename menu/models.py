from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name 


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    menu_url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                               null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.title
    
    def get_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.menu_url
