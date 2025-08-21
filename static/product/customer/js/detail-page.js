// Simpan file ini di: static/customer/js/detail-page.js

document.addEventListener('DOMContentLoaded', function () {
    // Inisialisasi fungsionalitas tab dari Bootstrap
    var triggerTabList = [].slice.call(document.querySelectorAll('#v-pills-tab a'))
    triggerTabList.forEach(function (triggerEl) {
        var tabTrigger = new bootstrap.Tab(triggerEl)

        triggerEl.addEventListener('click', function (event) {
            event.preventDefault()
            tabTrigger.show()
        })
    })
});
