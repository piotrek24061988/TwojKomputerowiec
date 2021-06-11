var userAuth = userAuthenticated
var updateBtns = document.getElementsByClassName('update-cart2');

for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId: " + productId + ", action: " + action + ", userAuthenticated: " +  userAuth);

        if(userAuth) {
            updateUserBin(productId, action)
        } else {
            console.log("user not authenticated - please log in");
        }
    })
}

function updateUserBin(productId, action) {
    console.log("user authenticated - sending data");
    console.log("csrftoken:" + csrftoken);

    url='';
    if(action == 'add') {
        url = '/dodajDoKosza/' + productId;
    }
    else if(action == 'increase') {
        url = '/zwiekszKosz/' + productId;
    }
    else if(action == 'decrease') {
        url = '/zmniejszKosz/' + productId;
    }

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'produkt_id': productId})
    })

    .then((data) => {
        location.reload()
    })
}