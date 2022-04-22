import bs4
import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from getrecipeapp.models import Category, Complexity, Tag, Dishes

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

    def get_image(self) -> str:
        """Возвзращает ссылку в виде строки на картинку"""
        return self.recipe.find('div', class_='recepiesimg').find('img').get('src')

    def get_description(self) -> str:
        """Возвращает описание блюда"""
        return self.recipe.find('div', class_='param').find('p').text


class Command(BaseCommand):

    def handle(self, *args, **options):
        page = 1
        total_pages = 9999
        while page <= total_pages:  # пробегаемся по всем страницам
            URL = f'https://grandkulinar.ru/recepies/zdorovoe-pitanie/nizkokalorijnye-blyuda/page/{page}/'
            response = requests.get(url=URL)
            soup = BeautifulSoup(response.text, 'lxml')
            total_pages = int(soup.find('div', class_='navigation').findAll('a')[-1].text)  # узнаем номер послед. стр

            # блок всех блюд на странице
            body_recipes = soup.find('div', {'id': 'dle-content'}).findAll('div', class_='shortstory')

            # добавление категорий в бд для дальнейшего изъятия в результирующую табл.
            category_name = soup.find('h1', class_='titlecat').text
            try:
                Category.objects.create(name=category_name)
            except:
                pass

            # пробегаемся по всем рецептам
            for recipe in body_recipes:
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

                # добавл. в бд
                try:
                    tmp_dishes = Dishes.objects.create(title=title,
                                                       category=Category.objects.get(name=category_name),
                                                       complexity=Complexity.objects.get(name=complexity),
                                                       timeprocess=time,
                                                       calories=calories,
                                                       rating=rating,
                                                       description=description,
                                                       image=image)

                    for tag in tags:
                        tmp_tag = Tag.objects.filter(name=tag).values_list('id', flat=True)
                        if tmp_tag.count() == 1:
                            tmp_dishes.tags.add(tmp_tag[0])
                except Exception as er:
                    pass

            # переход на следю стр.
            page += 1