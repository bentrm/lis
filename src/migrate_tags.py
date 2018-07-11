"""One-off script that migrates legacy AuthorPage tags."""

from cms.models import AuthorPage
from cms.tags import LanguageTag, GenreTag, LiteraryPeriodTag

for author in AuthorPage.objects.order_by("title"):
    page = author.get_latest_revision_as_page()
    has_changes = False
    for author_literary_category in page.literary_categories.all():
        old_genre = author_literary_category.literary_category
        if old_genre:
            try:
                new_genre = GenreTag.objects.get(title=old_genre.title)
                page.genre_tags.add(new_genre)
                has_changes = True
            except GenreTag.DoesNotExist:
                print(f"No genre tag for {old_genre}")
    for author_language in page.languages.all():
        old_language = author_language.language
        if old_language:
            try:
                new_language = LanguageTag.objects.get(title=old_language.title)
                page.language_tags.add(new_language)
                has_changes = True
            except LanguageTag.DoesNotExist:
                print(f"No language tag for {old_language}")
    for author_literary_period in page.literary_periods.all():
        old_literary_period = author_literary_period.literary_period
        if old_literary_period:
            try:
                new_literary_period = LiteraryPeriodTag.objects.get(title=old_literary_period.title)
                page.literary_period_tags.add(new_literary_period)
                has_changes = True
            except LiteraryPeriodTag.DoesNotExist:
                print(f"No literary period tag for {old_literary_period}")
    if has_changes:
        page.save_revision()
