from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Book, Genre, Author


def create_genres():
    genres = [
        "Thriller",
        "Romance",
        "Mystery",
        "Fantasy",
        "Biography",
        "History",
        "Horror",
        "Adventure",
        "Drama",
        "Comedy",
        "Action",
        "Non-fiction",
        "Self-Help",
        "Science",
        "Poetry",
        "Classic",
        "Fiction",
        "Philosophy",
        "Religion",
        "Business",
        "Politics",
        "Psychology",
        "Health",
        "Cooking",
        "Sports",
        "Technology",
        "Education",
        "Parenting",
        "Mythology",
        "Children's",
        "Fantasy Adventure",
        "Memoir",
        "Autobiography",
        "Short Stories",
        "Dystopian",
    ]

    created_genres = []

    # Create each genre
    for genre_name in genres:
        genre, created = Genre.objects.get_or_create(genre_name=genre_name)
        created_genres.append(genre)

    return created_genres


def create_authors():
    author_names = [
        "William Shakespeare",
        "Jane Austen",
        "Charles Dickens",
        "Mark Twain",
        "F. Scott Fitzgerald",
        "George Orwell",
        "Ernest Hemingway",
        "J.K. Rowling",
        "Gabriel García Márquez",
        "Leo Tolstoy",
        "Harper Lee",
        "Agatha Christie",
        "J.R.R. Tolkien",
        "Virginia Woolf",
        "Toni Morrison",
        "Franz Kafka",
        "Albert Camus",
        "Emily Brontë",
        "John Steinbeck",
        "Oscar Wilde",
        "George Bernard Shaw",
        "Maya Angelou",
        "Arthur Conan Doyle",
        "Victor Hugo",
        "H.G. Wells",
    ]

    created_authors = []

    # Create each author
    for author_name in author_names:
        author, created = Author.objects.get_or_create(author_name=author_name)
        created_authors.append(author)

    return created_authors


def create_owners():
    fake = Faker()
    created_owners = []

    # Creating three book owners
    for _ in range(3):
        owner = get_user_model().objects.create_user(
            email=fake.unique.email(), password=fake.password()
        )
        created_owners.append(owner)

    return created_owners


class Command(BaseCommand):
    help = "Create books"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of books to create")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs["count"]
        genres = create_genres()
        authors = create_authors()
        owners = create_owners()

        for _ in range(count):
            book = Book.objects.create(
                title=fake.catch_phrase(),
                owner_id=fake.random_element(elements=[owner.id for owner in owners]),
                ISBN=fake.unique.isbn10(),
                description=fake.paragraph(),
                condition=fake.random_element(elements=("Brand New", "Used")),
                retrieval_location=fake.address(),
            )
            book.genre.add(fake.random_element(elements=genres))
            book.author.add(fake.random_element(elements=authors))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} books."))
