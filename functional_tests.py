from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import unittest

class NewVisitorTest(unittest.TestCase):
	'''Тест нового посетителя'''
	
	def setUp(self):
		'''установка'''
		options = Options()
		options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
		self.browser = webdriver.Firefox(options=options)

	
	def tearDown(self):
		'''демонтаж'''
		self.browser.quit()

	def	test_can_start_a_list_and_retrieve_it_later(self):
		'''тест: можно начать список и получить его позже'''
		# Эдит слышала про крутон новое онлайн-приложение со списком неотложных дел
		# Она решает оценить его домашнюю страницу
		self.browser.get('http://localhost:8000')

		# Она видит что заголовок и шапка страницы говорят о списказ неотложных дел
		self.assertIn('To-Do', self.browser.title)
		self.fail('Закончить тест!')

		# Ей сразу же предлагается ввести элемент списка

		# Она набирает в текстовом поле "Купить павлиньи перья" (её хобби - вязание рыболовных мушек)

		# Когда она нажимает enter, страница обновляется, и теперь страница содержит "1: Купить павлиньи перья" в качестве элемента списка

		# Текстовое поле по-прежнему приглашает её добавить ещё один элемент
		# Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)

		# Страница снова обновляется и теперь показывет оба элемента её списка

		#Эдит интересно, запомнит ли сайт её список. Далее она видит, что сайт сгенерировал для неё уникальный URL-адрес - об этом выводится 		небольшой текст с объяснениями

		# Она посещает этот URL-адрес - её списое по-прежнему там

		# Удовлетворенная, она снова ложится спать

if __name__ == '__main__':
	unittest.main(warnings='ignore')
 
