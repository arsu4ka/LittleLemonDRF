from django.contrib.auth.models import Group
from LittleLemon.settings import MANAGER_GROUP_NAME, DELIVERY_CREW_GROUP_NAME


def get_manager_group():
    return Group.objects.filter(name=MANAGER_GROUP_NAME).first()


def get_delivery_crew_group():
    return Group.objects.filter(name=DELIVERY_CREW_GROUP_NAME).first()