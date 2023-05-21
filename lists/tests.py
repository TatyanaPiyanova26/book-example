from django.test import TestCase
from django.urls import resolve

from lists.views import home_page

from lists.models import Item

#from views import home_page

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        '''Тест: использует домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_s_POST_reuest(self):
        '''Тест: можно сохранить post-запрос'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    def test_root_url_resolves_to_home_page_view(self):
        '''Тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''Тест: домашняя страницы возвращает правильный html'''

        response = self.client.get('/')
        html = response.content.decode('utf-8')
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    '''Тесст модели элемента списка'''
    def test_saving_and_retrieving_items(self):
        '''Тест сохранения и полечения элементов списка'''
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')