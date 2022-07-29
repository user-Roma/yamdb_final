from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(year):
    """Validates year of title."""

    start_year = settings.MAGIC_VARS['YEAR']
    current_year = timezone.now().year
    if not start_year <= year <= current_year:
        raise ValidationError(
            f'Год указан не корректно, '
            f'должен быть в диапазоне {start_year}-{current_year}')
    return year
