from django.http import HttpRequest
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from base.views import home_page, play_page
from base.models import Round

# 1. unit tests should not test constants but logic, flow control, and configuration
# 2. refactor only when unit tests are passing
# 3. when refactoring, work on either the code or the tests, but not both at once


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('base/home.html')
        self.assertEqual(response.content.decode(), expected_html)


class PlayPageTest(TestCase):
    def test_play_url_resolves_to_play_page_view(self):
        found = resolve('/play')
        self.assertEqual(found.func, play_page)

    def test_play_page_returns_correctly_html(self):
        request = HttpRequest()
        response = play_page(request)
        self.assertIn('A new table item', response.content.decode())
        expected_html = render_to_string(
            'base/play.html',
            {'new_item_text': 'A new table item'})
        self.assertEqual(response.content.decode(), expected_html)


class PlayerModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_round = Round()
        first_round.number = 1
        first_round.save()

        second_round = Round()
        second_round.number = 2
        second_round.save()

        saved_rounds = Round.objects.all()
        self.assertEqual(saved_rounds.count(), 2)

        first_round_saved = saved_rounds[0]
        second_round_saved = saved_rounds[1]
        self.assertEqual(first_round_saved.number, 1)
        self.assertEqual(second_round_saved.number, 2)


