from django.http import HttpRequest
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from base.views import home_page, play_page, options
from base.models import Round, Options

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


class PlayViewTest(TestCase):
    def test_uses_play_template(self):
        response = self.client.get('/play')
        self.assertTemplateUsed(response, 'base/play.html')


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


class OptionsModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        OPTION_FIELDS = Options.OPTION_FIELDS

        david_options = Options()
        david_attributes = ('David', 2, 100, 1, False, True, True, True, True, True, True, True, 'ALL')
        for attr, option in zip(OPTION_FIELDS, david_attributes):
            setattr(david_options, attr, option)
        david_options.save()
        derek_attributes = ('Derek', 3, 300, 2, True, True, True, True, True, True, True, False, 'RP')

        derek_options = Options()
        for attr, option in zip(OPTION_FIELDS, derek_attributes):
            setattr(derek_options, attr, option)
        derek_options.save()

        saved_options = Options.objects.all()
        self.assertEqual(saved_options.count(), 2)

        david_options_saved = saved_options[0]
        derek_options_saved = saved_options[1]

        self.assertEqual([getattr(david_options, attr) for attr in OPTION_FIELDS],
                         [getattr(david_options_saved, attr) for attr in OPTION_FIELDS])
        self.assertEqual([getattr(derek_options, attr) for attr in OPTION_FIELDS],
                         [getattr(derek_options_saved, attr) for attr in OPTION_FIELDS])


class OptionsPageTest(TestCase):
    def test_options_url_resolves_to_options_page_view(self):
        found = resolve('/options')
        self.assertEqual(found.func, options)

    def test_options_page_returns_correct_html(self):
        request = HttpRequest()
        response = options(request)
        self.assertIn('Session options', response.content.decode())
        expected_html = render_to_string('base/options.html')

    def test_options_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['step'] = 3
        request.POST['pair_number'] = 3
        request.POST['starting_bet'] = 3
        request.POST['bet_column'] = 'on'
        request.POST['level_column'] = 'on'
        request.POST['net_column'] = 'on'
        request.POST['partner_column'] = 'on'
        request.POST['rows'] = 'VP'

        response = options(request)

        self.assertEqual(Options.objects.count(), 1)
        new_options = Options.objects.first()
        self.assertEqual(new_options.rows, 'VP')

    def test_options_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['step'] = 3
        request.POST['pair_number'] = 3
        request.POST['starting_bet'] = 3
        request.POST['bet_column'] = 'on'
        request.POST['level_column'] = 'on'
        request.POST['net_column'] = 'on'
        request.POST['partner_column'] = 'on'
        request.POST['rows'] = 'VP'

        response = options(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')






