
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

NAME_REGEX = re.compile(r'[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm):
        # empty strings
        firstMatch = True
        lastMatch = True
        emailMatch = True
        passwordLength = True
        passwordMatch = True
        #keep this
        userNotExist = True
        passedValues = []

        if not NAME_REGEX.match(first_name) or len(first_name) < 2:
            firstMatch = False
            # firstMatch = "First name can only..."
            #passedVAlues.append
        if not NAME_REGEX.match(last_name) or len(last_name) < 2:
            lastMatch = False
        if not EMAIL_REGEX.match(email) or len(email) < 1:
            emailMatch = False
        if not len(password) >= 8:
            passwordLength = False
        if not password == confirm:
            passwordMatch = False
        if User.objects.filter(email=email).exists():
            userNotExist = False

        # only pass back the strings that aren't ""

        passedValues = [userNotExist, firstMatch, lastMatch, emailMatch, passwordLength, passwordMatch]
        return passedValues


    def login(self, email, password):
        logged = [False]
        passedValues = []
        
        if User.objects.filter(email=email).exists():
            
            user = User.objects.get(email = email)
            # print "input password = " + bcrypt.hashpw(password.encode(), user.password.encode())
            # print "saved password = " + bcrypt.hashpw(user.password.encode(), user.password.encode())
            if not user.password == bcrypt.hashpw(password.encode(), user.password.encode()):
                logged = [False]
            else:
                logged = [True, user.first_name]
        return logged


class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()