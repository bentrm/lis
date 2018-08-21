from cms.models import LocationIndex, MemorialSite, TempLocation, LocationAuthor

TempLocation.objects.delete()

for site in MemorialSite.objects.all():
    root = LocationIndex.objects.first()
    parent = site.get_parent().specific
    parent_revision = parent.get_latest_revision()
    parent_revision.publish()

    revision = site.save_revision()
    revision.publish()

    obj = TempLocation(
        title=site.title,
        title_de=site.title_de,
        title_cs=site.title_cs,
        draft_title=site.draft_title,
        draft_title_de=site.draft_title_de,
        draft_title_cs=site.draft_title_cs,
        live=False,
        has_unpublished_changes=True,
        owner=site.owner,
        seo_title=site.seo_title,
        editor=site.editor,
        original_language=site.original_language,
        title_image=site.title_image,
        address=parent.address,
        address_de=parent.address_de,
        address_cs=parent.address_cs,
        contact_info=parent.contact_info,
        contact_info_de=parent.contact_info_de,
        contact_info_cs=parent.contact_info_cs,
        directions=parent.directions,
        directions_de=parent.directions_de,
        directions_cs=parent.directions_cs,
        coordinates=parent.coordinates,
        introduction=site.introduction,
        introduction_de=site.introduction_de,
        introduction_cs=site.introduction_cs,
        description=site.description,
        description_de=site.description_de,
        description_cs=site.description_cs,
        detailed_description=site.detailed_description,
        detailed_description_de=site.detailed_description_de,
        detailed_description_cs=site.detailed_description_cs,
    )
    root.add_child(instance=obj)

    for tag in parent.location_type_tags.all():
        obj.memorial_type_tags.add(tag)

    for old_sub in site.authors.all():
        obj.authors.add(LocationAuthor(author=old_sub.author, sort_order=old_sub.sort_order))

    obj.save_revision()
