var APP_DATA = {}

const KEY_SHOWS = 'existing_shows';
const KEY_MOVIES = 'existing_movies';

const CUSTOM_OPT = "Custom";

function getRadioValue(name) {
    var ele = document.getElementsByName(name);
    var value = null

    for (i = 0; i < ele.length; i++) {
        if (ele[i].checked)
            value = ele[i].value
    }

    return value
}

// Populate the 'media select' dropdown w/ the passed through list of options
function setupMediaSelect(options) {
    var nameSelect = document.getElementById("media_name");
    // "Custom" is always at the top of the list
    var innerHTML = "<option>" + CUSTOM_OPT + "</option>";

    for (const opt of options) {
        innerHTML += "<option>" + opt + "</option>";
    }

    nameSelect.innerHTML = innerHTML;
}

// Initialize the App / assign the APP_DATA
function initializeApp(app_data) {
    APP_DATA = app_data

    document.addEventListener('DOMContentLoaded', function() {
        setupMediaSelect(APP_DATA[KEY_SHOWS]);
    });
}

function handleMediaNameChange() {
    var mediaNameSel = document.getElementById('media_name');

    if (mediaNameSel.value != CUSTOM_OPT) {
        document.getElementById('div_custom_name').classList.add('hidden');
    } else {
        document.getElementById('div_custom_name').classList.remove('hidden');
    }
}

function handleTypeChanged() {
    var typeValue = getRadioValue('type');

    // Hide 'Season' input based on movie/tv selected, and populate dropdown options
    if (typeValue == 'tv') {
        document.getElementById('div_season').classList.remove('hidden');
        setupMediaSelect(APP_DATA['existing_shows']);
    } else {
        document.getElementById('div_season').classList.add('hidden');
        setupMediaSelect(APP_DATA['existing_movies']);
    }

    handleMediaNameChange()
}