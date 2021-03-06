from django.http import HttpRequest
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from base.forms import OptionsForm
from base.views import home_page, play_page, options, simulate
from base.models import Round, Options
from django.contrib.auth.models import User

# 1. unit tests should not test constants but logic, flow control, and configuration
# 2. refactor only when unit tests are passing
# 3. when refactoring, work on either the code or the tests, but not both at once


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base/home.html')
        # request = HttpRequest()
        # response = home_page(request)
        # expected_html = render_to_string('base/home.html')
        # self.assertEqual(response.content.decode(), expected_html)


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
    def setUp(self):
        temp_user = User(username='john')
        temp_user.save()

    def test_options_page_uses_options_form(self):

        response = self.client.get('/options')
        self.assertIsInstance(response.context['form'], OptionsForm)

    def test_saving_and_retrieving_items(self):
        # this should skip 'id' and 'user' fields
        fields = [field.name for field in Options._meta.fields if field.name not in ('id', 'user')]

        david_options = Options()
        david_user = User(username='David')
        david_user.save()
        david_attributes = (2, 100, 1, False, True, True, True, True, True, True, True, True, False)
        for attr, option in zip(fields, david_attributes):
            setattr(david_options, attr, option)
        david_options.user = david_user
        david_options.save()

        derek_user = User(username='Derek')
        derek_user.save()
        derek_attributes = (3, 300, 2, True, True, True, True, True, True, True, False, False, True)
        derek_options = Options()
        for attr, option in zip(fields, derek_attributes):
            setattr(derek_options, attr, option)
        derek_options.user = derek_user
        derek_options.save()

        saved_options = Options.objects.all()
        self.assertEqual(saved_options.count(), 2)

        david_options_saved = saved_options[0]
        derek_options_saved = saved_options[1]

        self.assertEqual([getattr(david_options, attr) for attr in fields],
                         [getattr(david_options_saved, attr) for attr in fields])
        self.assertEqual([getattr(derek_options, attr) for attr in fields],
                         [getattr(derek_options_saved, attr) for attr in fields])


class SimulatePageTest(TestCase):
    def test_simulate_url_resolves_to_options_page_view(self):
        found = resolve('/simulate')
        self.assertEqual(found.func, simulate)

    def test_simulate_page_contains_heading(self):
        response = self.client.get('/simulate')
        self.assertIn('Simulation', response.content.decode())

    def test_simulate_page_uses_simulate_template(self):
        response = self.client.get('/simulate')
        self.assertTemplateUsed(response, 'base/simulate.html')


class OptionsPageTest(TestCase):
    def test_options_url_resolves_to_options_page_view(self):
        found = resolve('/options')
        self.assertEqual(found.func, options)

    def test_options_page_contains_heading(self):
        temp_user = User(username='john')
        temp_user.save()

        request = HttpRequest()
        response = options(request)
        self.assertIn('Session options', response.content.decode())

    def test_uses_options_template(self):
        temp_user = User(username='john')
        temp_user.save()

        response = self.client.get('/options')
        self.assertTemplateUsed(response, 'base/options.html')

    def test_options_page_can_save_a_POST_request(self):
        temp_user = User(username='john')
        temp_user.save()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['step'] = 3
        request.POST['pairs'] = 4
        request.POST['starting_bet'] = 5
        request.POST['bet_column'] = 'on'
        request.POST['level_column'] = 'on'
        request.POST['net_column'] = 'on'
        request.POST['partner_column'] = 'on'
        request.POST['real_player_rows'] = 'on'

        response = options(request)

        self.assertEqual(Options.objects.count(), 1)
        new_options = Options.objects.first()
        self.assertEqual(new_options.real_player_rows, True)
        self.assertEqual(new_options.step, 3)
        self.assertEqual(new_options.pairs, 4)
        self.assertEqual(new_options.starting_bet, 5)

    def test_options_page_redirects_after_POST(self):
        temp_user = User(username='john')
        temp_user.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['step'] = 3
        request.POST['pairs'] = 3
        request.POST['starting_bet'] = 3


        response = options(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')






