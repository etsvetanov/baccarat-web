from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.utils import flatatt


class SpinInputWidget(widgets.Input):
    input_type = 'number'

    def render(self, name, value, min_value=None, max_value=None, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            final_attrs['value'] = force_text(self.format_value(value))

        widget_string = '<div class="form-group">' \
                        '   <label for="id_{name}"> {label_text} </label>' \
                        '   <div class="input-group input-group-lg>' \
                        '       <span class="input-group-btn">' \
                        '           <button type="button" class="btn btn-primary decr"' \
                        'data-target="#id_{name}"> - </button>' \
                        '       </span>' \
                        '       <input{attrs} />' \
                        '       <span class"input-group-btn">' \
                        '           <button type="button" class="btn btn-primary incr" data-target="#id_{name}"> + </button>' \
                        '       </span>' \
                        '   </div>' \
                        '</div>' \

        return format_html(widget_string,
                           name=name,
                           label_text=name.replace('_', ' ').capitalize(),
                           attrs=flatatt(final_attrs))


