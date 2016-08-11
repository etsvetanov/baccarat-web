from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_open_page(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Baccarat', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Baccarat', header_text)

        play_button = self.browser.find_element_by_id('play_button_id')
        self.assertEqual(play_button.text, 'Play')
        self.assertTrue(play_button.get_attribute('href').endswith('/play'))
        play_button.click()

        self.fail("finish test")

    def test_play_page(self):
        self.browser.get('http://localhost:8000/play')

        self.assertIn('Play Baccarat', self.browser.title)
        stats_table = self.browser.find_element_by_id('id_stats_table')


if __name__ == '__main__':
    unittest.main()
