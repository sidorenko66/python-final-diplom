FROM python:3.9
COPY ./requirements.txt ./requirements.txt
# Установка рабочей директории, откуда выполняются команды внутри контейнера.
# WORKDIR /stocks_products
# Запустить команду внутри образа, установка зависимостей.
RUN pip install -r requirements.txt
COPY . .
# Добавить мета-информацию к образу для открытия порта к прослушиванию.
EXPOSE 8000
WORKDIR /orders
# RUN python manage.py makemigrations
# RUN python manage.py makemigrations backend
RUN python manage.py migrate

CMD python manage.py runserver