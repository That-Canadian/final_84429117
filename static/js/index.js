function hideCustomName(obj) {
    if (obj.value != 'custom') {
        document.getElementById('div_custom_name').classList.add('hidden');
    } else {
        document.getElementById('div_custom_name').classList.remove('hidden');
    }
}

function hideSeason() {
    if (document.getElementById('typeTV').checked) {
        document.getElementById('div_season').classList.remove('hidden');
    } else {
        document.getElementById('div_season').classList.add('hidden');
    }
}