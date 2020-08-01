function search(e, url) {
    document.getElementsByClassName()
    const data = {

    }
    fetch(url, param)
        .then(data=>{return data.json()})
        .then(res=>{console.log(res)})
        .catch(error=>console.log(error))
}


$(document).on('click', '.search-bar', function(e){
    e.preventDefault();
    search(e, url);
    return false;
});
