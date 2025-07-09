from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from minilibrary.models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para la biblioteca'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        User = get_user_model()

        # Limpia datos previos
        self.stdout.write(self.style.WARNING('Eliminando datos previos...'))
        Recommendation.objects.all().delete()
        Loan.objects.all().delete()
        Review.objects.all().delete()
        BookDetail.objects.all().delete()
        Book.objects.all().delete()
        Genre.objects.all().delete()
        Author.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Usuarios
        self.stdout.write(self.style.SUCCESS('Creando usuarios...'))
        users = [User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password='password123'
        ) for _ in range(10)]

        # Autores
        self.stdout.write(self.style.SUCCESS('Creando autores...'))
        authors = [Author.objects.create(
            name=fake.name(),
            birth_date=fake.date_of_birth(minimum_age=30, maximum_age=85)
        ) for _ in range(10)]

        # Géneros
        self.stdout.write(self.style.SUCCESS('Creando géneros...'))
        genres = [Genre.objects.create(
            name=fake.unique.word().capitalize()
        ) for _ in range(6)]

        # Libros y detalles
        self.stdout.write(self.style.SUCCESS('Creando libros y detalles...'))
        books = []
        for _ in range(20):
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                publication_date=fake.date_between(start_date='-30y', end_date='today'),
                author=random.choice(authors),
                pages=random.randint(100, 900),
                isbn=fake.isbn13()
            )
            # Asigna géneros aleatorios
            book.genres.set(random.sample(genres, random.randint(1, 3)))
            # Detalle del libro
            BookDetail.objects.create(
                summary=fake.paragraph(nb_sentences=4),
                cover_url=fake.image_url(),
                language=random.choice(['Español', 'Inglés', 'Francés', 'Alemán']),
                book=book
            )
            books.append(book)

        # Recomendaciones
        self.stdout.write(self.style.SUCCESS('Creando recomendaciones...'))
        for book in books:
            for _ in range(random.randint(1, 4)):
                user = random.choice(users)
                try:
                    Recommendation.objects.create(
                        user=user,
                        book=book,
                        note=fake.sentence(nb_words=10)
                    )
                except:
                    continue  # Evita duplicados por unique_together

        # Reseñas
        self.stdout.write(self.style.SUCCESS('Creando reseñas...'))
        for _ in range(50):
            Review.objects.create(
                user=random.choice(users),
                book=random.choice(books),
                rating=random.randint(1, 5),
                text=fake.paragraph(nb_sentences=3)
            )

        # Préstamos
        self.stdout.write(self.style.SUCCESS('Creando préstamos...'))
        for _ in range(30):
            is_returned = random.choice([True, False])
            Loan.objects.create(
                user=random.choice(users),
                book=random.choice(books),
                return_date=fake.date_time_this_year() if is_returned else None,
                is_returned=is_returned
            )

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada con datos ficticios!'))
