( function ( doc, win ) {

    var new_button,
        show = true;

    /**
     * @author GCardona
     * @function to execute once DOM has loaded.
     */
    function on_ready() {
        new_button = doc.getElementById('show-new');
        new_log_div = doc.getElementById('newlog-form');
        _setButtonBehaviour();
    }

    /**
     * @author GCardona
     * @function that sets the show button behaviour.
     */
    function _setButtonBehaviour() {
        new_button.addEventListener('click', _toggleNewLog, true);
    }

    /**
     * @author GCardona
     * @function that toggles the visibility of the actual form
     */
    function _toggleNewLog() {

        if (show) {
            new_log_div.className =
                new_log_div.className.replace(/\s*hidden/, '');
            new_button.innerHTML = 'Cancel';
        }
        else {
            new_log_div.className += ' hidden';
            new_button.innerHTML = 'New Log';
        }
        show = !show;
    }

    console.log('javascript loaded!');
    doc.addEventListener('DOMContentLoaded', on_ready, false);

} (document, window) );
