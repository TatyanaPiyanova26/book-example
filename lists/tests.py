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

    def test_can_save_a_POST_request(self):
        '''Тест: можно сохранить post-запрос'''
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_Post(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/один-единственный-список-в-мире/')

        # self.assertIn('A new list item', response.content.decode())
        # self.assertTemplateUsed(response, 'home.html')

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


    def test_only_saves_items_when_nessasary(self):
        '''Тест: сохраняет элементы, только когда нужно'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):
    '''Тест представления списка'''
    def test_uses_home_template(self):
        '''Тест: использует шаблон списка'''
        response = self.client.get('/lists/один-единственный-список-в-мире/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        '''Тест: отображаются все элементы списка'''
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/один-единственный-список-в-мире/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
