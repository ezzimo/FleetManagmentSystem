from django.contrib import admin

from .models import Address, Bank, City, Customer, Driver, EmployeeSalary, Region, User

admin.site.register(Customer)
admin.site.register(Bank)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(User)
admin.site.register(Driver)
admin.site.register(EmployeeSalary)
admin.site.register(Address)
