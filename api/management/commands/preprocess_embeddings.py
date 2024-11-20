from django.core.management.base import BaseCommand
from api.utils import preprocess_and_store_embeddings,pri


class Command(BaseCommand):
    help = 'Preprocess and store embeddings for TravelPlace images'

    def handle(self, *args, **kwargs):
        preprocess_and_store_embeddings()
        self.stdout.write(self.style.SUCCESS('Successfully processed embeddings'))
