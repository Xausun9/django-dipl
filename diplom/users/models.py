# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=64, unique=True, db_index=True)
#     email = models.EmailField(max_length=120, unique=True, db_index=True)
#     password_hash = models.CharField(max_length=128)
    
#     def set_password(self, password):
#         self.password_hash = make_password(password)
    
#     def check_password(self, password):
#         return check_password(self.password_hash, password)
    
#     def __str__(self):
#         return self.username
