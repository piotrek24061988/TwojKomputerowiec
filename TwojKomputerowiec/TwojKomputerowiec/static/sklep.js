var userAuth = userAuthenticated
var updateBtns = document.getElementsByClassName('update-cart2');
var orderBtn = document.getElementsByClassName('process-order');

for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId: " + productId  + ", userAuthenticated: " +  userAuth);

        if(userAuth == 'True') {
            updateUserBin(productId, action);
        } else {
            console.log("user not authenticated - please log in");
            addCookieItem(productId, action);
        }
    })
}

for(var i = 0; i < orderBtn.length; i++) {
    orderBtn[i].addEventListener('click', function(){
        var orderId = this.dataset.order;
        var action = this.dataset.action;
        console.log("orderId: " + orderId + ", action: " + action);

        if(userAuth == 'True') {
            processOrder(orderId, action);
        } else {
            console.log("user not authenticated - please log in");
            processOrder(999, "order");//narazie tymczasowo

        }
    })
}

function addCookieItem(productId, action) {
    console.log("user not authenticated - sending data to cokies");

    if((action == 'add') || action == 'increase' ) {
        console.log("addCookieItem add action");
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
            console.log("addCookieItem add action new product in cart");
        } else {
            cart[productId]['quantity'] += 1;
            console.log("addCookieItem add action increased product in cart");
        }
    }

    if(action == 'decrease') {
        console.log("addCookieItem decrease action decrease product in cart");
        cart[productId]['quantity'] -= 1;

        if(cart[productId]['quantity'] <= 0) {
            console.log("addCookieItem decrease action remove product from cart");
            delete cart[productId];
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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

    FormData.platnosc = form.platnosc.value;
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
    console.log("orderId", orderId);

    url='';
    if(action == 'order') {
        url = '/procesujZamowienie/' + orderId;
    } else {
        console.log("zla akcja");
    }

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'order_id': orderId, 'form_data': FormData})
    })

    .then((data) => {
        cart = {}
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        location.reload()
    })
}