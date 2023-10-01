<h1 align="center" id="title">Book Giveaway Service</h1>

<p id="description">Book giveaway is a service where people can give away books they no longer need or find books they want to read. Users can sign up list their available books or alternatively create offers to other book owners.</p>

  
  
<h2> Features</h2>

Here're some of the project's best features:

*   Users can list the books that they want to give away.
*   Users can also request books that they are interested in from owners.
*   Book owners can decide to whom they will give their books.
*   Books can be filtered by Genres Authors Book condition and availability.
*   Users will get notifications when book owner approves their request.
*   Users will also receive notifications if book owner rejects their request.


<h2>🛠️ Installation Steps:</h2>

<p>1. First clone the repository</p>

```
git clone repository
```

<p>2. Optionally create environment-variables.env file for environment variables and populate it with values such as "SECRET_KEY" "DEBUG" for Django and "NAME" "USER" "PASSWORD" for PostgreSQL</p>

```
touch environment-variables.env
```

<p>3. Start up docker containers</p>

```
docker compose up -d --build
```

<p>4. Create migrations</p>

```
docker compose exec django python3 manage.py migrate
```

<p>5. Run custom management command to create Users Books Genres and Book authors. This command takes a "count" argument which will determine how many books are created in total.</p>

```
docker compose exec django python3 manage.py create_books 50
```

<p>6. Run unit tests</p>

```
docker compose exec django python3 manage.py test
```

  


<h2>💻 Built with</h2>

Technologies used in the project:

*   Django
*   Django REST Framework
*   PostgreSQL
*   Docker
*   Docker Compose
*   Swagger

  
