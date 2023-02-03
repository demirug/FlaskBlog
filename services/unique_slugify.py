from slugify import slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def unique_slugify(instance, value, max_length=None):
    _slug = slugify(''.join(alphabet.get(w, w) for w in value.lower()))

    if max_length:
        _slug = _slug[:max_length]

    slugs = [blog.slug for blog in instance.__class__.query.filter(instance.__class__.slug.startswith(_slug))]

    slug = _slug
    id = 1
    while slug in slugs:
        slug = f"{_slug}-{id}"
        id += 1

    return slug