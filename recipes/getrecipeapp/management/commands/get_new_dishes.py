import bs4
import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from getrecipeapp.models import Category, Complexity, Tag, Dishes
import os
from django.conf import settings
from tqdm import tqdm

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36'}


class Recipe:

    def __init__(self, rec: bs4.element.Tag):
        self.recipe = rec

    def get_title(self) -> str:
        """Возвращает заголовок рецепта"""
        return self.recipe.find('div', class_='title_shortstory border-bottom') \
            .find('h3').text

    def get_link_title(self) -> str:
        """Возвращает ссылку на рецепт"""
        return self.recipe.find('div', class_='title_shortstory border-bottom') \
            .find('a')['href']

    def get_tags(self) -> list:
        """Возвращает теги блюда"""  # .get('href')
        return [tag.text for tag in
                self.recipe.find('span', {'itemprop': 'recipeCategory'}).findAll('a', class_='povar_col')]

    def get_time(self) -> str:
        """Возвращает время приготовления"""
        try:
            return self.recipe.find('div', class_='ingr_bg').findAll('span')[1].text
        except Exception:
            return ''

    def get_complexity(self) -> str:
        """Возвращает уровень сложности приготовления"""
        try:
            return self.recipe.find('div', class_='ingr_bg').findAll('span')[2].next_sibling.strip()
        except Exception:
            return ''

    def get_calories(self) -> str:
        """Возвращает калорийность блюда"""
        try:
            return self.recipe.find('div', class_='ingr_bg').findAll('span')[4].nextSibling.strip()
        except Exception:
            return ''

    def get_rating(self) -> str:
        """Возвращает рейтинг блюда в виде процентов. К примеру 40% это 2 звезды, 100% - 5 звезды"""
        return self.recipe.find('li', class_='current-rating').text

    def get_image(self):
        """Скачивает картинку в МАЛЕНЬКОМ разрешении и возвращает путь к картинке на диске"""
        url = self.recipe.find('div', class_='recepiesimg').find('img').get('src')
        resp = requests.get(url)
        img_file = os.path.join(settings.MEDIA_ROOT, 'images_small', url.split('/')[-1])
        if not os.path.exists(img_file):
            with open(img_file, 'wb') as img:
                img.write(resp.content)
            return os.path.join('images_small', url.split('/')[-1])
        else:
            return os.path.join('images_small', url.split('/')[-1])

    def get_image_full(self):
        """Скачивает картинку в ВЫСОКОМ разрешении и возвращает путь к картинке на диске"""
        url = self.recipe.find('div', {'id': 'fullstory'}).find('div', class_='centr').find('img').get('src')
        resp = requests.get(url)
        img_file = os.path.join(settings.MEDIA_ROOT, 'images_full', url.split('/')[-1])
        if not os.path.exists(img_file):
            with open(img_file, 'wb') as img:
                img.write(resp.content)
            return os.path.join('images_full', url.split('/')[-1])
        else:
            return os.path.join('images_full', url.split('/')[-1])

    def get_description(self) -> str:
        """Возвращает описание блюда"""
        return self.recipe.find('div', class_='param').find('p').text

    def get_full_description(self) -> str:
        """Возвращает полное описание блюда"""
        return self.recipe.find('p', {'itemprop': 'description'}).text

    def get_nutrition(self) -> str:
        """Возвращает пищевую ценность одной порции"""
        return str(self.recipe.find('div', {"itemprop": "nutrition"}))

    def get_ingredients_clr(self) -> str:
        """Возвращает ингридиенты к рецепту"""
        return str(self.recipe.find('div', class_='ingredients clr'))

    def get_instructions(self) -> str:
        """Возвращает пошаговый алгоритм приготовления блюда по рецепту"""
        return str(self.recipe.find('div', class_='instructions'))


def get_total_pages(url):
    """Вернуть кол-во страниц"""
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return int(soup.find('div', class_='navigation').findAll('a')[-1].text)  # узнаем номер послед. стр


class Command(BaseCommand):

    def handle(self, *args, **options):
        URL = f'https://grandkulinar.ru/recepies/zdorovoe-pitanie/nizkokalorijnye-blyuda/page/{1}/'
        total_pages = get_total_pages(URL)
        print('Всего страниц: ', total_pages)
        print('-' * 30)

        for page in range(1, total_pages + 1):
            URL = f'https://grandkulinar.ru/recepies/zdorovoe-pitanie/nizkokalorijnye-blyuda/page/{page}/'
            response = requests.get(url=URL, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            # блок всех блюд на странице
            body_recipes = soup.find('div', {'id': 'dle-content'}).findAll('div', class_='shortstory')

            # добавление категорий в бд для дальнейшего изъятия в результирующую табл.
            category_name = soup.find('h1', class_='titlecat').text
            try:
                Category.objects.create(name=category_name)
            except:
                pass

            # пробегаемся по всем рецептам
            for recipe in tqdm(body_recipes, f'Обработка страницы: {page}'):
                obj_r = Recipe(recipe)  # текущий рецепт

                # извлекаются теги из исх. рецепта и добавл в бд
                tags = obj_r.get_tags()
                for tag in tags:
                    try:
                        Tag.objects.create(name=tag)
                    except Exception:
                        pass

                # извлекается категория сложности приготовления блюда из исх рецепта и добавл в бд
                complexity = obj_r.get_complexity()
                try:
                    Complexity.objects.create(name=complexity)
                except Exception:
                    pass

                # извкл. остальные атрибуты
                title = obj_r.get_title()
                rating = obj_r.get_rating()
                time = obj_r.get_time()
                calories = obj_r.get_calories()
                description = obj_r.get_description()
                image = obj_r.get_image()
                link = obj_r.get_link_title()

                # переход по ссылке для получения доп. инф.
                link_resp = requests.get(url=link, headers=headers)
                link_soup = BeautifulSoup(link_resp.text, 'lxml')
                link_recipe = Recipe(link_soup)
                # получение доп. инф
                image_full = link_recipe.get_image_full()
                description_full = link_recipe.get_full_description()
                nutrition = link_recipe.get_nutrition()
                ingredients_clr = link_recipe.get_ingredients_clr()
                instructions = link_recipe.get_instructions()


                # добавл. в бд
                try:
                    tmp_dishes = Dishes.objects.create(title=title,
                                                       category=Category.objects.get(name=category_name),
                                                       complexity=Complexity.objects.get(name=complexity),
                                                       timeprocess=time,
                                                       calories=calories,
                                                       rating=rating,
                                                       description=description,
                                                       image=image,
                                                       link=link,
                                                       image_full=image_full,
                                                       description_full=description_full,
                                                       nutrition=nutrition,
                                                       ingredients_clr=ingredients_clr,
                                                       instructions=instructions)

                    for tag in tags:
                        tmp_tag = Tag.objects.filter(name=tag).values_list('id', flat=True)
                        if tmp_tag.count() == 1:
                            tmp_dishes.tags.add(tmp_tag[0])
                except Exception as er:
                    pass