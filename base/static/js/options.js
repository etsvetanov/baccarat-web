function update_preview() {
    console.log('update_preview() is called!')
    // TODO: get base_row values from the server
    var base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26];
    var sb = $('#id_starting_bet').val();
    var mplier = $('#id_step').val();

    for(var j=0; j < 3; j++) {
        var tr = $('#table_level_' + (j + 1));
        tr.children('td').each(function(i) {
            var cell_value = base_row[i] * sb * Math.pow(mplier, j);
            this.innerText = cell_value.toFixed(1);
        })

    }
};

function increment() {
    var input_id = $(this).attr('data-target');
    var input = $(input_id);
    var step = Number(input.attr('step'));
    var value = Number(input.val());
    var new_value = value + step;
    var max = input.attr('max');

    input.val(new_value > max ? value : Number(new_value.toFixed(1)));

    input.trigger('input');
};

function decrement() {
    var input_id = $(this).attr('data-target');
    var input = $(input_id);
    var step = input.attr('step');
    var value = input.val();
    var new_value = parseFloat(value) - parseFloat(step);
    var min = input.attr('min');

    input.val(new_value < min ? value : Number(new_value.toFixed(1)));
    input.trigger('input');
};


$(document).ready(function() {
    $('.preview').on('input', update_preview);
    update_preview();

    $('.incr').on('click', increment);
    $('.decr').on('click', decrement);
});