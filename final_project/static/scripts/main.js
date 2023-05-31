$(document).ready(function () {
    $('.list-item').click(function () {
        itemID = $(this).attr('id');
        info = $('#info-' + itemID).text()
        price = $('#price-' + itemID).text().replace('$', '')
        type = $('#type-' + itemID).val()

        $('#update-info').val(info)
        $('#update-price').val(parseInt(price))
        $('#record-id').val(itemID)

        if (type == 0) {
            $('#update-income').attr('checked', false);
            $('#update-expense').attr('checked', true);
        } else {
            $('#update-income').attr('checked', true);
            $('#update-expense').attr('checked', false);
        }
    });

    $('#calendar').on('selectDate', function (event, newDate) {
        location.href = "/update_date?date=" + newDate;
    });
});

function validation() {
    pwd = $('#pwd').val()
    pwdConfirm = $('#pwdConfirm').val()
    if (pwd != '' && pwdConfirm != '') {
        if (pwd === pwdConfirm) {
            return true;
        }
    }
    $('.login-failed').text('請輸入相同密碼');
    return false;
}

function sendDateToFlask(date) {
    fetch('/update_date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'date': date })
    })
        .then(response => response.json())
        .then(data => {
            // 在这里处理来自 Flask 的响应数据，根据需要进行页面转跳或其他操作
            console.log(data);
        })
        .catch(error => {
            console.error(error);
            // 处理错误
        });
}