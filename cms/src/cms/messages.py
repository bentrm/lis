"""Helper module to manage and override message translations."""

from django.utils.translation import gettext_noop as _

# flake8: noqa
# pylint: disable=line-too-long


OVERRIDE = {"owner": _("Owner"), "editor": _("editor")}

TXT = {
    "age_group.plural": _("Age groups"),
    "age_group": _("Age group"),
    "author_genre.author.help": _("Author that this mapping is referencing."),
    "author_genre.author": _("Author"),
    "author_genre.genre.help": _("Literary genre that the author is associated with."),
    "author_genre.genre": _("Literary genre"),
    "author_genre.plural": _("Genres of the author"),
    "author_genre": _("Genre of the author"),
    "author_language.author.help": _("Author that this mapping is referencing."),
    "author_language.author": _("Author"),
    "author_language.language.help": _("Language that the author has been active in."),
    "author_language.language": _("Language"),
    "author_language.plural": _("Languages of the author"),
    "author_language": _("Language of the author"),
    "author_period.author.help": _("Author that this mapping is referencing."),
    "author_period.author": _("Author"),
    "author_period.period.help": _(
        "Literary period that the author is associated with."
    ),
    "author_period.period": _("Literary period"),
    "author_period.plural": _("Literary periods of the author"),
    "author_period": _("Literary period of the author"),
    "author.date_of_birth_day.help": _("The day that the author is born on."),
    "author.date_of_birth_day": _("Day of birth"),
    "author.date_of_birth_month.help": _("The month that the author is born in."),
    "author.date_of_birth_month": _("Month of birth"),
    "author.date_of_birth_year.help": _("The year that the author is born in."),
    "author.date_of_birth_year": _("Year of birth"),
    "author.date_of_birth": _("Date of birth"),
    "author.date_of_death_day.help": _("The day that the author is born on."),
    "author.date_of_death_day": _("Day of death"),
    "author.date_of_death_month.help": _("The month that the author is born in."),
    "author.date_of_death_month": _("Month of death"),
    "author.date_of_death_year.help": _("The year that the author is born in."),
    "author.date_of_death_year": _("Year of death"),
    "author.date_of_death": _("Date of death"),
    "author.gender": _("Gender"),
    "author.genre.help": _("The literary genres the author is associated with."),
    "author.genre.plural": _("Genre"),
    "author.language.help": _("The languages that the author has been active in."),
    "author.language.plural": _("Languages"),
    "author.literary_category.help": _(
        "The literary categories the author is associated with."
    ),
    "author.literary_category.plural": _("Literary categories"),
    "author.literary_period.help": _(
        "The literary periods the author has been active in."
    ),
    "author.literary_period.plural": _("Literary periods"),
    "author.name.birth_name_cs.help": _(
        "Birth name of the author if different from international spelling."
    ),
    "author.name.birth_name_de.help": _(
        "Birth name of the author if different from international spelling."
    ),
    "author.name.birth_name.help": _(
        "Birth name of the author if different from last name."
    ),
    "author.name.birth_name": _("Birth name"),
    "author.name.first_name_cs.help": _(
        "The first name in Czech if different from international spelling."
    ),
    "author.name.first_name_de.help": _(
        "The first name in German if different from international spelling."
    ),
    "author.name.first_name": _("First name"),
    "author.name.help": _("The name of the author"),
    "author.name.is_pseudonym.help": _(
        "This name has been used as a pseudonym by the author."
    ),
    "author.name.is_pseudonym": _("Is pseudonym"),
    "author.name.last_name_cs.help": _(
        "The first name in Czech if different from international spelling."
    ),
    "author.name.last_name_de.help": _(
        "The last name in German if different from international spelling."
    ),
    "author.name.last_name": _("Last name"),
    "author.name.plural": _("Names"),
    "author.name.title_cs.help": _(
        "Academic title of the author in Czech if different from international spelling."
    ),
    "author.name.title_de.help": _(
        "Academic title of the author in German if different from international spelling."
    ),
    "author.name.title.help": _("Academic title of the author if any."),
    "author.name.title": _("Title"),
    "author.name.validation": _(
        "Name entries must at least contain a first name or a last name."
    ),
    "author.name": _("Name"),
    "author.place_of_birth_cs.help": _(
        "Place of birth if different in Czech spelling."
    ),
    "author.place_of_birth_de.help": _(
        "Place of birth if different in German spelling."
    ),
    "author.place_of_birth.help": _("The city or village where the author was born."),
    "author.place_of_birth": _("Place of birth"),
    "author.place_of_death_cs.help": _(
        "Place of death if different in Czech spelling."
    ),
    "author.place_of_death_de.help": _(
        "Place of death if different in German spelling."
    ),
    "author.place_of_death.help": _("The city or village the author died in."),
    "author.place_of_death": _("Place of death"),
    "author.plural": _("Authors"),
    "author_name": _("Author name"),
    "author_name.plural": _("Author names"),
    "author.title_image.help": _(
        "A meaningful image that will be used to present the author to the user."
    ),
    "author.title_image": _("Title image"),
    "author": _("Author"),
    "blog.plural": _("Blog pages"),
    "blog": _("Blog page"),
    "contact_type.plural": _("Contact types"),
    "contact_type": _("Contact type"),
    "content.plural": _("Content"),
    "content": _("Content"),
    "document_media.summary_cs": _("Czech summary"),
    "document_media.summary_de": _("German summary"),
    "document_media.summary.help": _(
        "A short and concise summary of the content of the document."
    ),
    "document_media.summary": _("Summary"),
    "gender.female": _("female"),
    "gender.male": _("male"),
    "gender.unknown": _("unknown"),
    "genre.plural": _("Genres"),
    "genre": _("Genre"),
    "heading.cs": _("Czech"),
    "heading.de": _("German"),
    "heading.en": _("English"),
    "heading.general": _("General"),
    "heading.meta": _("Meta information"),
    "heading.promote": _("Promote"),
    "heading.settings": _("Settings"),
    "home.plural": _("Homepages"),
    "home": _("Homepage"),
    "image_media.caption_cs.help": _("Caption in Czech translations."),
    "image_media.caption_cs": _("Czech caption"),
    "image_media.caption_de": _("German caption"),
    "image_media.caption.help": _("A caption that may be presented with the file."),
    "image_media.caption": _("Caption"),
    "language.cs": _("Czech"),
    "language.de": _("German"),
    "language.en": _("English"),
    "language.plural": _("Languages"),
    "language": _("Language"),
    "level1.biography.help": _(
        "An introductory biography of the author aimed at laymen."
    ),
    "level1.biography": _("Biography"),
    "level1.works.help": _(
        "An introduction to the works of the author aimed at laymen."
    ),
    "level1.works": _("Literary works"),
    "level1": _("I. Discovery"),
    "level2.biography.help": _(
        "An introductory biography of the author aimed at laymen."
    ),
    "level2.biography": _("Biography"),
    "level2.connections.help": _(
        "A short description of important connections (i.e. people) that have been mentioned in the text."
    ),
    "level2.connections": _("Connections"),
    "level2.full_texts.help": _(
        "Short full texts (i.e. poems, short stories) by the author that have been mentioned or are partially quoted in the text about the author."
    ),
    "level2.full_texts": _("Full texts"),
    "level2.reception.help": _(
        "A more in-depth description for interested users on how the author has been received."
    ),
    "level2.reception": _("Reception"),
    "level2.works.help": _(
        "An introduction to the works of the author aimed at laymen."
    ),
    "level2.works": _("Literary works"),
    "level2": _("II. Delving deeper"),
    "level3.primary_literature.help": _(
        "A more in-depth presentation of primary literature of the author for an academic user."
    ),
    "level3.primary_literature": _("Primary literature"),
    "level3.secondary_literature.help": _(
        "Further secondary literature about the author and his works aimed at academic users."
    ),
    "level3.secondary_literature": _("Secondary literature"),
    "level3.testimony.help": _(
        "Extant documents about the author by other people, e.g. correspondence with the author, lecture notes."
    ),
    "level3.testimony": _("Testimony"),
    "level3": _("III. Material"),
    "literary_period.description.help": _(
        "A general description of the literary period and its significance."
    ),
    "literary_period.description": _("Description"),
    "literary_period.plural": _("Literary periods"),
    "literary_period": _("Literary period"),
    "memorial_type.plural": _("Types of memorials"),
    "memorial_type": _("Type of memorials"),
    "location.address.help": _("The postal address of the location if any."),
    "location.address": _("Address"),
    "location.contact_info.help": _(
        "An address, a weblink or phone contact that may be helpful to visit this place."
    ),
    "location.contact_info": _("Contact info"),
    "location.contacts.help": _("Contacts of this location."),
    "location.contacts": _("Contact information"),
    "location.coordinates.help": _("The actual geographic location."),
    "location.coordinates": _("Location coordinates"),
    "location.directions.help": _(
        "A short description of directions to find the location."
    ),
    "location.directions": _("How to get there"),
    "location.location_type_tags.help": _(
        "The location types that describe this location best."
    ),
    "location.location_type_tags.plural": _("Location types"),
    "location.plural": _("Locations"),
    "location.title_image.help": _(
        "A meaningful image that will be used to present the location to the user."
    ),
    "location.title_image": _("Title image"),
    "location": _("Location"),
    "media.title_cs": _("Czech title"),
    "media.title_de": _("German title"),
    "media.title.help": _("Title of the media item."),
    "media.title": _("Title"),
    "memorial_site_author.author.help": _(
        "The author that is remebered by this memorial site."
    ),
    "memorial_site_author.author": _("Author"),
    "memorial_site_author.memorial_site.help": _(
        "The memorial site this mapping references to."
    ),
    "memorial_site_author.memorial_site": _("Memorial site"),
    "memorial_site_author.plural": _("Dedicated sites"),
    "memorial_site_author": _("Dedicated site"),
    "memorial_site.address.help": _("The postal address of the location if any."),
    "memorial_site.address": _("Address"),
    "memorial_site.authors.help": _(
        "The authors that this memorial site is dedicated to."
    ),
    "memorial_site.authors": _("Authors"),
    "memorial_site.contact_info.help": _(
        "An address, a weblink or phone contact that may be helpful to visit this place."
    ),
    "memorial_site.contact_info": _("Contact info"),
    "memorial_site.contacts.help": _("Contacts of this location."),
    "memorial_site.contacts": _("Contact information"),
    "memorial_site.coordinates.help": _("The actual geographic location."),
    "memorial_site.coordinates": _("Location coordinates"),
    "memorial_site.description.help": _(
        "A description of the memorial site and its significance to the referenced authors."
    ),
    "memorial_site.description": _("I. Discover - Memorial site"),
    "memorial_site.detailed_description.help": _(
        "A detailed description of the memorial site and its significance to the referenced authors."
    ),
    "memorial_site.detailed_description": _("II. Delving deeper - Memorial site"),
    "memorial_site.directions.help": _(
        "A short description of directions to find the location."
    ),
    "memorial_site.directions": _("How to get there"),
    "memorial_site.introduction.help": _("A short introduction text."),
    "memorial_site.introduction": _("Introduction"),
    "memorial_site.location_type_tags.help": _(
        "The location types that describe this location best."
    ),
    "memorial_site.location_type_tags.plural": _("Location types"),
    "memorial_site.memorial_type_tags.help": _(
        "The location types that describe this location best."
    ),
    "memorial_site.memorial_type_tags.plural": _("Location types"),
    "memorial_site.plural": _("Memorial sites"),
    "memorial_site.title_image.help": _(
        "A meaningful image that will be used to present the memorial site to the user."
    ),
    "memorial_site.title_image": _("Title image"),
    "memorial_site": _("Memorial site"),
    "memorial": _("Memorial site"),
    "memorial.plural": _("Memorial sites"),
    "page.draft_title_cs.help": _(
        "Czech title of the page as given of the latest draft."
    ),
    "page.draft_title_cs": _("Czech draft title"),
    "page.draft_title_de.help": _(
        "German title of the page as given of the latest draft."
    ),
    "page.draft_title_de": _("German draft title"),
    "page.draft_title.help": _("Title of the page as given of the lastest draft."),
    "page.draft_title": _("Draft title"),
    "page.editor.help": _("Name or initials of the author of this content page."),
    "page.editor": _("Editor"),
    "page.original_language.help": _(
        "The language this content has been originally written in."
    ),
    "page.original_language": _("Original language"),
    "page.temporary_redirect.help": _(
        "A target url or slug that this page will redirect to."
    ),
    "page.temporary_redirect": _("Temporary redirect target"),
    "page.title_cs.help": _("Czech title of the page."),
    "page.title_cs": _("Czech title"),
    "page.title_de.help": _("German title of the page."),
    "page.title_de": _("German title"),
    "page.title.help": _("Title of the page."),
    "page.title": _("Title"),
    "rendition.image.help": _("The image this rendition is based on."),
    "rendition.image": _("Image rendition"),
    "tag.description.help": _("A short description of the tag."),
    "tag.description": _("Description"),
    "tag.plural": _("Tags"),
    "tag.sort_order.help": _("Defines the relative order of the tag in the UI."),
    "tag.sort_order": _("Sort order"),
    "tag.title_cs.help": _("The czech title of the tag as show to the user."),
    "tag.title_cs": _("Czech title"),
    "tag.title_de.help": _("The german title of the tag as shown to the user."),
    "tag.title_de": _("German title"),
    "tag.title.help": _("The title of this tag as shown to the user."),
    "tag.title": _("Title"),
    "tag": _("Tag"),
}
