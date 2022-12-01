import django_filters
from .models import Client

class ClientFilter(django_filters.FilterSet):

    class Meta:
        model = Client
        fields = ['first_name',
                    'last_name',
                    'blood_group',
                    'age',
                    'weight',
                    'is_verified']