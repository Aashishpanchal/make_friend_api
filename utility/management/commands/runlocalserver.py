from django.core.management.commands.runserver import Command as BaseCommand

from utility import get_local_ip_address


class Command(BaseCommand):
    default_addr = get_local_ip_address() or "127.0.0.1"
