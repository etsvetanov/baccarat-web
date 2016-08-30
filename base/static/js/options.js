function update_preview() {
    console.log('update_preview() is called!')
    // TODO: get base_row values from the server
    var base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26];
    var sb = $('id_starting_bet_input').val();
    var mplier = $('id_step_input').val();

    for(var j=0; j < 3; j++) {
        var tr = $('table_level_' + j);
        tr.children('td').each(function(i) {
            var cell_value = base_row[i] * sb * Math.pow(mplier, j);
            this.val(cell_value);
        })

    }
};

$(document).ready(function() {
    $('.preview').on("onchange", update_preview);
});