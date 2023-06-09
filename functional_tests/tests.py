import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
	'''Тест нового посетителя'''
	def setUp(self):
		'''установка'''
		options = Options()
		options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
		self.browser = webdriver.Firefox(options=options)
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		'''демонтаж'''
		# self.browser.refresh()
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		'''ожидать строку в таблице списка'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def	test_can_start_a_list_and_retrieve_it_later(self):
		'''тест: можно начать список и получить его позже'''
		# Эдит слышала про крутон новое онлайн-приложение со списком неотложных дел
		# Она решает оценить его домашнюю страницу
		self.browser.get(self.live_server_url)

		# Она видит что заголовок и шапка страницы говорят о списказ неотложных дел
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# Ей сразу же предлагается ввести элемент списка
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# Она набирает в текстовом поле "Купить павлиньи перья" (её хобби - вязание рыболовных мушек)
		inputbox.send_keys('Купить павлиньи перья')

		# Когда она нажимает enter, страница обновляется, и теперь страница содержит "1: Купить павлиньи перья" в качестве элемента списка
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		# Текстовое поле по-прежнему приглашает её добавить ещё один элемент
		# Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Сделать мушку из павлиньих перьев')
		inputbox.send_keys(Keys.ENTER)


		# Страница снова обновляется и теперь показывет оба элемента её списка
		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# self.assertTrue(any(row.text == '1: Купить павлиньи перья' for row in rows),
		# 				f"Новый элемент списка не появился в таблице.Содержимым было: {table.text}")
		# self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])
		# self.assertIn('2: Сделать мушку из павлиньих перьев', [row.text for row in rows])
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')
		self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

		#Эдит интересно, запомнит ли сайт её список. Далее она видит,
		# что сайт сгенерировал для неё уникальный URL-адрес - об этом выводится
		# небольшой текст с объяснениями
		# self.fail('Закончить тест!')
		# Она посещает этот URL-адрес - её списое по-прежнему там

		# Удовлетворенная, она снова ложится спать

	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''Тест: многочисленные пользователи могут начать списки по разным url'''

		#Эдит начинает новый список
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Купить павлиньи перья')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		# Она замечает, что её список имеет уникальный URL - адрес
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Теперь новый пользователь, Френсис, приходит на сайт

		# Мы мспользуем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
		# информация от Эдит не прошла через данные cookie и пр.
		self.browser.quit()
		options = Options()
		options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
		self.browser = webdriver.Firefox(options=options)

		# Френсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиньи перья', page_text)
		self.assertNotIn('Сделать мушку', page_text)

		# Френсис начинает новый список, вводя новый элемент. Он менее
		# интересен, чем список Эдит...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Купить молоко')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить молоко')

		# Френсис получает уникальный URL - адрес
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Опять-таки, нет ни следа от списка Эдит
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиньи перья', page_text)
		self.assertIn('Купить молоко', page_text)

	def test_layout_and_styling(self):
		'''Тест макета и стилевого оформления'''
		# Эдит открывает домашнюю страницу
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# Он замечает что поле ввода аккуратно центрировано
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width']/2,
			512,
			delta=10
		)

		#Она начинает новый список и видит, что поле ввода там тоже аккуратно центрировано
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

		# Удовлетворенные, они оба ложатся спать




# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')
 
