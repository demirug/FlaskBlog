import re

from slugify import slugify

pattern = "^(({slug})|({slug}-[0-9]+))$"


def unique_slugify(instance, value, slug_field_name='slug', max_length=None):
    """ Generate unique slug for the model instance by value """
    _slug = slugify(value)

    # Limit slug
    if max_length:
        _slug = _slug[:max_length]

    # If given slug already used by instance return it
    cur_slug = getattr(instance, slug_field_name)
    if re.match(pattern.format(slug=_slug), cur_slug):
        return cur_slug

    # Get all slugs that are the same as a given slug or given slug with a numeric index
    slug_field = getattr(instance.__class__, slug_field_name)
    slugs = [el[0] for el in
             instance.query.filter(slug_field.regexp_match(pattern.format(slug=_slug))).values(slug_field)]

    # If same slugs not used yet
    if len(slugs) == 0:
        return _slug

    # Get all used numerics of the current slug
    numbers = [int(el.split('-')[-1]) for el in slugs if el.split('-')[-1].isdigit()]

    # If numerics not found, default will be 1
    if len(numbers) == 0:
        return f"{_slug}-1"

    # Sorting to get the latest numeric
    numbers.sort()
    return f"{_slug}-{numbers[-1] + 1}"
