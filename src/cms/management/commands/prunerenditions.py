from django.core.management.base import BaseCommand
from cms.media import ImageMediaRendition

class Command(BaseCommand):
    """Used to prune image renditions."""

    help = "Remove all renditions from database and the file system."

    def handle(self, *args, **kwargs):
        count = 0
        for rendition in ImageMediaRendition.objects.all():
            self.stdout.write(self.style.SUCCESS(f"Pruning rendition '{rendition.image.title}' ({rendition.filter_spec})."))
            rendition.delete()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Pruned {count} renditions."))
