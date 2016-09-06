from django.test import TestCase
from base.forms import OptionsForm


class OptionsFormTest(TestCase):
    def test_form_renders_inputs(self):
        form = OptionsForm()
        self.assertIn('class="form-control preview centered_input"', str(form['starting_bet']))
        self.assertIn('class="form-control preview centered_input"', str(form['step']))
        self.assertIn('class="form-control preview centered_input"', str(form['pairs']))

    def test_form_renders_checkboxes(self):
        form = OptionsForm()
        self.assertIn('name="bet_column" type="checkbox"', str(form['bet_column']))