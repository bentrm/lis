from django.contrib.auth.models import User
from cms.models import Memorial


def migrate_memorial_authors():
    user = User.objects.get(username="bthurm")
    for memorial in Memorial.objects.all():
        page = memorial.get_latest_revision_as_page()
        is_live = page.live
        for author in page.authors.all():
            page.remembered_authors.add(author.author)
        revision = page.save_revision(user=user)
        if is_live:
            revision.publish()
