function themThuoc(id, ten, gia, ghi_chu){
    event.preventDefault()

    fetch('/api/add-thuoc', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'ten': ten,
            'gia': gia,
            'ghi_chu': ghi_chu
        }),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById('demThuoc')
        counter.innerText = data.tong_so_luong
        var soluong = document.getElementById('soluong'+(id))
        soluong.innerText -= 1

    }).catch(function(err) {
        console.error(err)
    })
}


function themtoathuoc(){
    fetch('/api/themtoathuoc', {
    method: "post"

    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
        if (data.status === 200)
            location.reload()
    }).catch(function(err) {
        console.error(err)
    })
}



//$(document).ready(function () {
//    function themtoathuoc() {
//        $.ajax({
//            url: '/api/themtoathuoc',
//            type: "POST",
//            success: function(res) {
//                alert(res);
//            },
//            error: function(res) {
//                alert(res);
//            }
//        });
//    }
//});