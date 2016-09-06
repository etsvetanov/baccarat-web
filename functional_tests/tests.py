from django.test import LiveServerTestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

from django.contrib.auth.models import User
import unittest


class NewVisitorTest(StaticLiveServerTestCase):
    options_form_elements = ('id_bet_column',
                             'id_index_column',
                             'id_level_column',
                             'id_net_column',
                             'id_partner_column',
                             'id_play_column',
                             'id_result_column',
                             'id_debt_column')

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'httpL//' + arg.split('=')[1]
                return
            super().setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        try:
            self.browser.refresh()
            self.browser.quit()
        except ConnectionResetError:
            print('Browser was closed!')

    def test_can_open_page(self):
        self.browser.get(self.server_url)

        self.assertIn('Baccarat', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Baccarat', header_text)

        # ----
        play_button = self.browser.find_element_by_id('play_button_id')
        self.assertEqual(play_button.text, 'Play')
        self.assertTrue(play_button.get_attribute('href').endswith('/play'))
        # play_button.click()

        # ----
        options_button = self.browser.find_element_by_id('id_options_button')
        self.assertEqual(options_button.text, 'Options')
        self.assertTrue(options_button.get_attribute('href').endswith('/options'))
        # ----
        simulate_button = self.browser.find_element_by_id('id_simulate_button')
        self.assertEqual(simulate_button.text, 'Simulate')
        self.assertTrue(play_button.get_attribute('href').endswith('/simulate'))

    def test_play_page(self):
        self.browser.get(self.server_url + '/play')

        self.assertIn('Play Baccarat', self.browser.title)
        stats_table = self.browser.find_element_by_id('id_stats_table')

    def test_options_page(self):
        john = User(username='john')
        john.save()
        self.browser.get(self.server_url + '/options')

        self.assertIn('Session options', self.browser.title)

        form = self.browser.find_element_by_id('id_options_form')
        self.assertEqual(form.get_attribute('method'), 'post')

        step_input = self.browser.find_element_by_id('id_step')
        pair_num_input = self.browser.find_element_by_id('id_pairs')
        starting_bet_input = self.browser.find_element_by_id('id_starting_bet')
        column_bet = self.browser.find_element_by_id('id_bet_column')
        column_index = self.browser.find_element_by_id('id_index_column')
        column_level = self.browser.find_element_by_id('id_level_column')
        column_net = self.browser.find_element_by_id('id_net_column')
        column_partner = self.browser.find_element_by_id('id_partner_column')
        column_play = self.browser.find_element_by_id('id_play_column')
        column_result = self.browser.find_element_by_id('id_result_column')
        column_debt = self.browser.find_element_by_id('id_debt_column')

        real_player_rows = self.browser.find_element_by_id('id_real_player_rows')
        virtual_player_rows = self.browser.find_element_by_id('id_virtual_player_rows')


        preview_table = self.browser.find_element_by_id('id_preview_table')

        submit_button = self.browser.find_element_by_id('id_submit_button')

    @override_settings(DEBUG=True)
    def test_options_layout_and_styling(self):
        user = User(username='john')
        user.save()
        self.browser.get(self.server_url + '/options')
        self.browser.set_window_size(1024, 768)

        form_elements = [self.browser.find_element_by_id(id)
                         for id in self.options_form_elements]

        for i in range(len(form_elements) - 1):
            self.assertTrue(form_elements[i].location['y'] < form_elements[i+1].location['y'])

    def test_simulate_page(self):
        self.browser.get(self.server_url + '/simulate')

        round_info_table = self.browser.find_element_by_id('id_round_info')



# we don't need 'main' since we are using the Django test runner to launch the FT
# if __name__ == '__main__':
#     unittest.main()
