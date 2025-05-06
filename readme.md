Платформа питомника включает в себя разделы:
- породы
- собаки
- пользователи
- отзывы

Виртуальное окружение используемое для проекта: venv

1) После настройки виртуального окружения установите зависимости из файла requirements.txt

```bash
  pip install -r requirements.txt
```

2) Заполните файл .env file согласно файла .env.sample

3) Создайте Базу Данных при помощи команды

```bash
  python manage.py ccdb
```

4) Создайте миграции при помощи команды

```bash
  python manage.py makemigrations
```

5) Примените созданные миграции при помощи команды

```bash
  python manage.py migrate
```

6) Выполните команду для создания пользователей

```bash
  python manage.py ccsu
```
7) Выполните команду для заполнения базы данных используя фикстуры

```bash
  python manage.py loaddata dogs.json
```

8) Выполните команду для запуска приложения

```bash
  python manage.py runserver
```

Модели используемые в проекте

Breeds с полями:

- name - название породы 

Dogs с полями:

- name - кличка собаки
- breed - порода собаки
- birth_date - дата рождения собаки
- owner - имя хозяина собаки (если есть)
- views - просмотры пользователями
- is_active - признак активности собаки по умолчанию True

Reviews с полями:

- title - заголовок отзыва
- content - содержимое отзыва
- created - дата создания отзыва
- author - почта автора отзыва

User с полями:

- email - электронная почта пользователя
- role - роль пользователя (ADMIN or MODERATOR or USER)
- first_name - имя пользователя (может быть пустым)
- last_name - фамилия пользователя (может быть пустым)
- phone - телефон пользователя (может быть пустым)
- telegram - телеграм пользователя (может быть пустым)
- is_active - признак активности пользователя по умолчанию True

Разрешения (Permissions)

- Реализованы кастомные разрешения для пользователя с ролью USER, MODERATOR, ADMIN
- перечислю

Пагинация

- Реализована пагинация ...

Views модели Breed (Порода)

- BreedsListView(показывает все породы собак)
- DogBreedSearchListView(поиск собак по породе)
- DogBreedListView(показывает собак выбранной породы)

Views модели Dogs (Собаки)

- DogListView(показывает активных собак)
- DogDeactivatedListView(показывает неактивных собак)
- DogSearchListView(поиск собаки по кличке)
- DogCreateView(добавление собаки)
- DogDetailView(вывод полной информации о собаке)
- DogUpdateView(изменение информации о собаке)
- DogDeleteView(удаление собаки)

Views модели Reviews (Отзывы)

- ReviewListview(показывает активные отзывы)
- ReviewDeactivatedListview(показывает неактивные отзывы)
- ReviewCreateView(создание отзыва)
- ReviewDetailView(вывод полной информации об отзыве)
- ReviewUpdateView(изменение отзыва)
- ReviewDeleteView(удаление отзыва)

Views модели User (Пользователи)

- UserRegisterView(регистрация пользователя)
- UserLoginView(реализация входа пользователя в аккаунт)
- UserProfileView(информация о пользователе)
- UserUpdateView(изменение информации о пользователе)
- UserPasswordChangeView(изменение пароля пользователя)
- UserLogoutView(выход из аккаунта пользователя)
- UserListView(список всех пользователей)
- UserDetailView(просмотр информации о пользователе)

