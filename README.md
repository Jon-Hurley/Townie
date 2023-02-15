# Townie
Code repository for the app Townie.


I recommend you use Visual Studio. It has good github integration and is a pretty light code editor with lots of extensions!

If you do not have Node installed, download it here: https://nodejs.org/en/

To get svelte working:

cd townie
npm install
npm run dev <- starts the frontend

Source: https://svelte.dev

To get django working:

cd backend

pip install pipenv

pipenv shell

pipenv install django

cd townie_project

python manage.py runserver <- runs the server

NOTE: when you make a change in models or otherwise, you have to run:
python manage.py makemigrations <- ensure that there are no warnings or errors in this stage before migrating. 

python manage.py migrate

Source: https://www.ginkgobioworks.com/2021/02/04/creating-a-rest-api-using-django-rest-framework/