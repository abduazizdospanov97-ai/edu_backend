from django.core.management.base import BaseCommand
from apps.students.models import Student

FEMALE_FIRST = [
    'Dilnoza', 'Nilufar', 'Zulfiya', 'Mohira', 'Feruza', 'Sabohat', 'Barno', 'Nargiza',
    'Nodira', 'Munira', 'Shahnoza', 'Mavluda', 'Kamola', 'Lola', 'Hulkar', 'Maftuna',
    'Sarvinoz', 'Oydin', 'Gulnora', 'Ziyoda', 'Malika',
]


def to_female_surname(last_name: str) -> str:
    if not last_name:
        return last_name
    if last_name.endswith(('ova', 'eva', 'yeva', 'iva')):
        return last_name
    if last_name.endswith('yev'):
        return last_name + 'a'
    if last_name.endswith('ev'):
        return last_name + 'a'
    if last_name.endswith('ov'):
        return last_name + 'a'
    return last_name + 'a'


class Command(BaseCommand):
    help = "Qiz studentlarining familiyalarini to'g'rilash (oxiriga 'a' qo'shish)"

    def handle(self, *args, **kwargs):
        girls = Student.objects.filter(first_name__in=FEMALE_FIRST)
        fixed = 0
        for s in girls:
            old = s.last_name
            new = to_female_surname(old)
            if new != old:
                s.last_name = new
                s.save(update_fields=['last_name'])
                self.stdout.write(f'  {old} -> {new}  ({s.first_name})')
                fixed += 1
        self.stdout.write(self.style.SUCCESS(f"\nJami {fixed} ta familiya tuzatildi"))
