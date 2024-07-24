function lap_phieu_kham(benh_nhan_id){
    event.preventDefault()

    fetch('/api/phieukhambenh', {
        method: 'post',
        body: JSON.stringify({
            'benh_nhan_id': benh_nhan_id,
        }),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
    }).catch(function(err) {
        console.error(err)
    })
}