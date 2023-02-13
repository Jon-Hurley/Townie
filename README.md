# Townie
Code repository for the app Townie.

To get svelte working:

npm create svelte@latest myapp
cd myapp
npm install
npm run dev

To get django working:

cd django-townie

pip install pipenv

pipenv shell

pipenv install django

cd backend

python manage.py migrate

python manage.py runserver