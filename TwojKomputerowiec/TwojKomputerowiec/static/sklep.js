var userAuth = userAuthenticated
var updateBtns = document.getElementsByClassName('update-cart2');
var orderBtn = document.getElementsByClassName('process-order');

for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId: " + productId  + ", userAuthenticated: " +  userAuth);

        if(userAuth) {
            updateUserBin(productId, action);
        } else {
            console.log("user not authenticated - please log in");
        }
    })
}

for(var i = 0; i < orderBtn.length; i++) {
    orderBtn[i].addEventListener('click', function(){
        var orderId = this.dataset.order;
        var action = this.dataset.action;
        console.log("orderId: " + orderId + ", action: " + action);

        if(userAuth) {
            processOrder(orderId, action);
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

function processOrder(orderId, action) {
    console.log("user authenticated - processing order");
    console.log("csrftoken:" + csrftoken);
    var form = document.getElementById('orderForm');
    var FormData = {
        'platnosc': null,
        'uwagi': null,
        'adres': null,
        'miasto': null,
        'kod': null,
        'numer': null,
    }

    console.log("platnosc:" + form.platnosc.value);
    FormData.platnosc = form.platnosc.value;
    console.log("uwagi:" + form.uwagi.value);
    FormData.uwagi = form.uwagi.value;
    if(form.adres){
        FormData.adres = form.adres.value;
    }
    if(form.miasto){
        FormData.miasto = form.miasto.value;
    }
    if(form.kod) {
        FormData.kod = form.kod.value;
    }
    if(form.numer){
        FormData.numer = form.numer.value;
    }

    console.log("FormData", FormData);

    url='';
    if(action == 'order') {
        url = '/procesujZamowienie/' + orderId;
    }

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'order_id': orderId})
    })

    //.then((data) => {
    //    location.reload()
    //})
}