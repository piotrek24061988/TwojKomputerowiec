var userAuth = userAuthenticated
var updateBtns1 = document.getElementsByClassName('update-cart1');
var updateBtns2 = document.getElementsByClassName('update-cart2');
var orderBtn1 = document.getElementsByClassName('process-order1');
var orderBtn2 = document.getElementsByClassName('process-order2');

for(var i = 0; i < updateBtns1.length; i++) {
    updateBtns1[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId: " + productId  + ", userAuthenticated: " +  userAuth);

        if(userAuth == 'True') {
            console.log("user authenticated do nothing");
        } else {
            console.log("user not authenticated");
            addCookieItem(productId, action);
        }
    })
}

for(var i = 0; i < updateBtns2.length; i++) {
    updateBtns2[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId: " + productId  + ", userAuthenticated: " +  userAuth);

        if(userAuth == 'True') {
            updateUserBin(productId, action);
        } else {
            console.log("user not authenticated");
            addCookieItem(productId, action);
        }
    })
}

for(var i = 0; i < orderBtn1.length; i++) {
    orderBtn1[i].addEventListener('click', function(){
        var orderId = this.dataset.order;
        var action = this.dataset.action;
        console.log("orderId: " + orderId + ", action: " + action);

        if(userAuth == 'True') {
            console.log("user authenticated do nothing");
        } else {
            console.log("user not authenticated");
            processOrder(999, 'order');//niezalogowany uzytkownik
        }
    })
}

for(var i = 0; i < orderBtn2.length; i++) {
    orderBtn2[i].addEventListener('click', function(){
        var orderId = this.dataset.order;
        var action = this.dataset.action;
        console.log("orderId: " + orderId + ", action: " + action);

        if(userAuth == 'True') {
            processOrder(orderId, action);
        } else {
            console.log("user not authenticated");
            processOrder(999, 'order');//niezalogowany uzytkownik
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
    console.log("processing order");
    console.log("csrftoken:" + csrftoken);
    var brakDanych = Boolean(false);
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
    if(form.adres && form.adres.value){
        FormData.adres = form.adres.value;
    } else {
        brakDanych = true;
    }
    if(form.miasto && form.miasto.value){
        FormData.miasto = form.miasto.value;
    } else {
        brakDanych = true;
    }
    if(form.kod && form.kod.value) {
        FormData.kod = form.kod.value;
    } else {
        brakDanych = true;
    }
    if(form.numer && form.numer.value){
        FormData.numer = form.numer.value;
    } else {
        brakDanych = true;
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
        console.log("promise done")
        console.log(data)
        if(brakDanych) {
          console.log("cookies not cleared missing data")
        } else {
            console.log("cookies cleared")
            cart = {}
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        }
        location.reload(true)
        alert("zamówienie zrealizowane")
        window.location.href = '/sklep'
    }, reason => {
        console.log("promise not done")
        console.error(reason)
    })
}