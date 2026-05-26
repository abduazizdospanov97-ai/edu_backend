import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User
from apps.courses.models import Course
from apps.rooms.models import Room
from apps.teachers.models import Teacher
from apps.groups.models import Group
from apps.students.models import Student
from apps.payments.models import Payment
from apps.attendance.models import Attendance
from apps.tests.models import Test, TestResult


COURSES_DATA = [
    {'name': 'Frontend dasturlash', 'duration': 6, 'price': 800000, 'color': '#3B82F6', 'description': 'HTML, CSS, JavaScript, React'},
    {'name': 'Backend dasturlash', 'duration': 8, 'price': 900000, 'color': '#10B981', 'description': 'Python, Django, REST API'},
    {'name': 'Mobile dasturlash', 'duration': 6, 'price': 850000, 'color': '#8B5CF6', 'description': 'Flutter, Dart'},
    {'name': 'Ingliz tili', 'duration': 12, 'price': 500000, 'color': '#F59E0B', 'description': 'A1 dan C1 gacha'},
    {'name': 'Grafik dizayn', 'duration': 4, 'price': 600000, 'color': '#EF4444', 'description': 'Figma, Photoshop, Illustrator'},
]

ROOMS_DATA = [
    {'name': '101-xona', 'capacity': 20, 'floor': 1, 'status': 'AVAILABLE'},
    {'name': '102-xona', 'capacity': 15, 'floor': 1, 'status': 'OCCUPIED'},
    {'name': '201-xona', 'capacity': 25, 'floor': 2, 'status': 'AVAILABLE'},
    {'name': '202-xona', 'capacity': 20, 'floor': 2, 'status': 'AVAILABLE'},
    {'name': '301-xona', 'capacity': 12, 'floor': 3, 'status': 'MAINTENANCE'},
]

TEACHERS_DATA = [
    {'name': 'Alisher Nazarov', 'email': 'alisher@educrm.uz', 'subject': 'Frontend dasturlash', 'phone': '+998901234567', 'salary': 4500000},
    {'name': 'Nodira Yusupova', 'email': 'nodira@educrm.uz', 'subject': 'Backend dasturlash', 'phone': '+998902345678', 'salary': 5000000},
    {'name': 'Bobur Toshmatov', 'email': 'bobur@educrm.uz', 'subject': 'Mobile dasturlash', 'phone': '+998903456789', 'salary': 4800000},
    {'name': 'Malika Rahimova', 'email': 'malika@educrm.uz', 'subject': 'Ingliz tili', 'phone': '+998904567890', 'salary': 3500000},
    {'name': 'Jasur Mirzayev', 'email': 'jasur@educrm.uz', 'subject': 'Grafik dizayn', 'phone': '+998905678901', 'salary': 4000000},
]

MALE_FIRST = ['Ali', 'Sardor', 'Jasur', 'Bobur', 'Ulugbek', 'Sherzod', 'Kamol', 'Mirzo',
              'Otabek', 'Eldor', 'Firdavs', 'Temur', 'Sanjar', 'Doniyor', 'Hamza', 'Islom',
              'Asilbek', 'Mansur', 'Behruz', 'Ibrohim', 'Jahongir', 'Muhammadali']
MALE_LAST   = ['Karimov', 'Rahimov', 'Yusupov', 'Toshmatov', 'Nazarov', 'Mirzayev', 'Xolmatov',
               'Umarov', 'Ergashev', 'Holiqov', 'Botirov', 'Sultonov', 'Qodirov', 'Jurayev',
               'Abdullayev', 'Hasanov', 'Normatov', 'Sobirov', 'Razzaqov', 'Ismoilov', 'Tursunov']

FEMALE_FIRST = ['Dilnoza', 'Nilufar', 'Zulfiya', 'Mohira', 'Feruza', 'Sabohat', 'Barno', 'Nargiza',
                'Nodira', 'Munira', 'Shahnoza', 'Mavluda', 'Kamola', 'Lola', 'Hulkar', 'Maftuna',
                'Sarvinoz', 'Oydin', 'Gulnora', 'Ziyoda']
FEMALE_LAST = ['Karimova', 'Rahimova', 'Yusupova', 'Toshmatova', 'Nazarova', 'Mirzayeva',
               'Xolmatova', 'Umarova', 'Ergasheva', 'Holiqova', 'Botirova', 'Sultonova',
               'Qodirova', 'Jurayeva', 'Abdullayeva', 'Hasanova', 'Normatova', 'Sobirova',
               'Razzaqova', 'Ismoilova', 'Tursunova']

DAYS_OPTIONS = [
    ['Du', 'Ch', 'Ju'],
    ['Se', 'Pa', 'Sha'],
    ['Du', 'Se', 'Ch', 'Pa', 'Ju'],
    ['Du', 'Ch', 'Sha'],
    ['Se', 'Pa', 'Ju'],
    ['Du', 'Se', 'Ch', 'Sha'],
    ['Ch', 'Pa', 'Sha'],
    ['Du', 'Se', 'Ju', 'Sha'],
]

TIMES = [
    ('09:00', '11:00'),
    ('11:00', '13:00'),
    ('14:00', '16:00'),
    ('16:00', '18:00'),
    ('18:00', '20:00'),
]


class Command(BaseCommand):
    help = 'Fake ma\'lumotlar bilan bazani to\'ldirish'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Eski ma\'lumotlarni o\'chirib qayta yaratish')

    def handle(self, *args, **kwargs):
        if kwargs['reset']:
            self.stdout.write('Eski ma\'lumotlar o\'chirilmoqda...')
            TestResult.objects.all().delete()
            Test.objects.all().delete()
            Attendance.objects.all().delete()
            Payment.objects.all().delete()
            Student.objects.all().delete()
            Group.objects.all().delete()
            Teacher.objects.all().delete()
            Room.objects.all().delete()
            Course.objects.all().delete()
            self.stdout.write('  OK: tozalandi\n')

        self.stdout.write('Fake data qoshilmoqda...\n')

        # 1. Kurslar
        courses = []
        for data in COURSES_DATA:
            c, created = Course.objects.get_or_create(name=data['name'], defaults=data)
            courses.append(c)
        self.stdout.write(f'  OK: {len(courses)} ta kurs')

        # 2. Xonalar
        rooms = []
        for data in ROOMS_DATA:
            r, _ = Room.objects.get_or_create(name=data['name'], defaults=data)
            rooms.append(r)
        self.stdout.write(f'  OK: {len(rooms)} ta xona')

        # 3. O'qituvchilar
        teachers = []
        for i, data in enumerate(TEACHERS_DATA):
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={'name': data['name'], 'role': 'TEACHER', 'is_active': True}
            )
            if created:
                user.set_password('Teacher123')
                user.save()
            t, _ = Teacher.objects.get_or_create(
                user=user,
                defaults={'phone': data['phone'], 'salary': data['salary'], 'subject': data['subject']}
            )
            teachers.append(t)
        self.stdout.write(f'  OK: {len(teachers)} ta oquvchi')

        # 4. Guruhlar
        groups = []
        group_names = ['G-01', 'G-02', 'G-03', 'G-04', 'G-05', 'G-06', 'G-07', 'G-08']
        available_rooms = [r for r in rooms if r.status != 'MAINTENANCE']
        for i, name in enumerate(group_names):
            course = courses[i % len(courses)]
            teacher = teachers[i % len(teachers)]
            room = available_rooms[i % len(available_rooms)]
            days = DAYS_OPTIONS[i % len(DAYS_OPTIONS)]
            start_time, end_time = TIMES[i % len(TIMES)]
            g, _ = Group.objects.get_or_create(
                name=name,
                defaults={
                    'course': course, 'teacher': teacher, 'room': room,
                    'start_time': start_time, 'end_time': end_time,
                    'days': days, 'max_students': random.choice([15, 20, 25]),
                }
            )
            groups.append(g)
        self.stdout.write(f'  OK: {len(groups)} ta guruh')

        # 5. Talabalar
        students = []
        phones_used = set()
        for i in range(60):
            if random.random() < 0.45:
                first = random.choice(FEMALE_FIRST)
                last = random.choice(FEMALE_LAST)
            else:
                first = random.choice(MALE_FIRST)
                last = random.choice(MALE_LAST)
            while True:
                phone = f'+9989{random.randint(10000000, 99999999)}'
                if phone not in phones_used:
                    phones_used.add(phone)
                    break
            group = groups[i % len(groups)]
            course = group.course
            birth_year = random.randint(1998, 2007)
            balance = random.choice([-800000, -500000, -300000, 0, 0, 200000, 500000])
            status = random.choices(['ACTIVE', 'INACTIVE', 'GRADUATED'], weights=[80, 10, 10])[0]
            s, created = Student.objects.get_or_create(
                phone=phone,
                defaults={
                    'first_name': first, 'last_name': last, 'phone': phone,
                    'birth_date': date(birth_year, random.randint(1, 12), random.randint(1, 28)),
                    'address': f"Toshkent sh., {random.randint(1,12)}-mavze",
                    'course': course, 'group': group,
                    'balance': balance, 'status': status,
                }
            )
            students.append(s)
        self.stdout.write(f'  OK: {len(students)} ta talaba')

        # 6. To'lovlar
        payments_count = 0
        methods = ['CASH', 'CARD', 'TRANSFER']
        for student in students:
            n = random.randint(1, 4)
            for j in range(n):
                days_ago = random.randint(1, 90)
                Payment.objects.get_or_create(
                    student=student,
                    amount=random.choice([500000, 800000, 900000, 1000000]),
                    method=random.choice(methods),
                    defaults={
                        'status': 'PAID',
                        'note': '',
                        'created_at': timezone.now() - timedelta(days=days_ago),
                    }
                )
                payments_count += 1
        self.stdout.write(f'  OK: ~{payments_count} ta tolov')

        # 7. Davomat (oxirgi 14 kun)
        att_count = 0
        active_students = [s for s in students if s.status == 'ACTIVE']
        for day_offset in range(14, 0, -1):
            att_date = date.today() - timedelta(days=day_offset)
            if att_date.weekday() >= 6:
                continue
            for group in groups:
                group_students = [s for s in active_students if s.group == group]
                for student in group_students:
                    status = random.choices(
                        ['PRESENT', 'ABSENT', 'LATE'],
                        weights=[75, 15, 10]
                    )[0]
                    Attendance.objects.get_or_create(
                        student=student, group=group, date=att_date,
                        defaults={'status': status}
                    )
                    att_count += 1
        self.stdout.write(f'  OK: {att_count} ta davomat yozuvi')

        # 8. Testlar
        test_titles = [
            'HTML/CSS asoslari', 'JavaScript 1-test', 'React asoslari',
            'Python asoslari', 'Django REST API', 'Flutter UI test',
            'Ingliz tili — Grammar', 'Figma prototiplash',
        ]
        for i, title in enumerate(test_titles):
            group = groups[i % len(groups)]
            test, _ = Test.objects.get_or_create(
                title=title,
                defaults={
                    'group': group,
                    'total_questions': random.choice([20, 25, 30]),
                    'max_score': 100,
                }
            )
            group_students = [s for s in active_students if s.group == group]
            max_n = max(len(group_students), 1)
            n = random.randint(min(5, max_n), max_n)
            for student in group_students[:n]:
                TestResult.objects.get_or_create(
                    test=test, student=student,
                    defaults={'score': random.randint(40, 100)}
                )
        self.stdout.write(f'  OK: {len(test_titles)} ta test va natijalar')

        self.stdout.write(self.style.SUCCESS('\nFake data muvaffaqiyatli qoshildi!\n'))
        self.stdout.write('  Admin: http://localhost:8000/admin/')
        self.stdout.write('  API:   http://localhost:8000/api/')
