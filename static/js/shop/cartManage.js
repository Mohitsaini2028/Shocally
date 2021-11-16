
console.log("index");
console.log(cartJson);

function CheckingUser(){
console.log("chala")
  if(null==document.getElementById('AuthUser'))  //if user is authenticated then this function will work otherwise not
  {

    loginButton=document.getElementById('userLogin');
    loginButton.click();
    return false;
  }
   else{
     return true;
   }
}




  if(document.getElementById('AuthUser'))
  {

    if (cartJson==0) {
      // if (localStorage.getItem('cart') == null) {
        var cart = {};
      }
      else {
        cart = cartJson;
        // cart = JSON.parse(localStorage.getItem('cart'));
        console.log("cart  ",cart);
        updateCart(cart);
      }

  }

  // If the add to cart button is clicked, add/increment the item
  //$('.cart').click(function() {

      $('.divpr').on('click', 'button.cart', function(e){
        console.log("chaala ki lab da fire")
        if(CheckingUser())
        {
          var idstr = this.id.toString();
          if (cart[idstr] != undefined) {
              qty = cart[idstr][0] + 1;
          } else {
              qty = 1;
              name = document.getElementById('name'+idstr).innerHTML;
              price = document.getElementById('price'+idstr).innerHTML;
              console.log(price);
              cart[idstr] = [qty, name, parseFloat(price)];
              console.log("cart price - ",cart[idstr][2])
          }
          updateCart(cart);

              cartForm=document.getElementById('cartForm');
              $('#cartData').val(JSON.stringify(cart));
              console.log("cart ki value bhai ",$('#cartData').val())
              e.preventDefault();

              $.ajax({
                  type:'POST',
                  url:'/shop/cart/',
                  data:{
                        cartData:$('#cartData').val(),
                        user:$('#user').val(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                      },
                      success:function(data){

                      }
              });

        }

  });


  //Add Popover to cart
  // $('#popcart').popover();
  updatePopover(cart);

  // function updatePopover(cart) {
  //
  //   if(document.getElementById('AuthUser'))
  //   {
  //
  //     console.log('We are inside updatePopover');
  //     var popStr = "";
  //     popStr = popStr + "<h5> Cart for your items in my shopping cart </h5><div class='mx-2 my-2'>";
  //     var i = 1;
  //     for (var item in cart) {
  //       if (Object.keys(cart).length >0)
  //       {
  //         // popStr = popStr + "<b>" + i + "</b>. ";
  //         // popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 19) + "... Qty: " + cart[item][0] + '<br>';
  //         // i = i + 1;
  //
  //         popStr = popStr + "<b>" + i + "</b>. ";
  //         popStr = popStr + cart[item][1].slice(0, 19) + "... Qty: " + cart[item][0] + '<br>';
  //         i = i + 1;
  //       }
  //       else{
  //         popStr = "<h5> You haven't Cart any item </h5><div class='mx-2 my-2'>";
  //       }
  //
  //     }
  //
  //     // popStr = popStr + "</div> <a href='/shop/checkout'><button class='btn btn-primary' id ='checkout'>Checkout</button></a><button class='btn btn-primary' onclick='clearCart()' id ='clearCart'>Clear Cart</button>"
  //     popStr = popStr + "</div> <a href='/shop/checkout' class='btn btn-primary'>Checkout</a>"+ "<a  class='btn btn-primary mx-2' onclick='clearCart()' id ='clearCart'>Clear Cart</a>"
  //     var dp=new DOMParser();
  //     var doc=dp.parseFromString(popStr,'text/html');
  //     // alert(doc.documentElement.outerHTML);
  //     document.getElementById('popcart').setAttribute('data-content', popStr);
  //     // document.getElementById('popcart').setAttribute('data-content',doc.documentElement.outerHTML );
  //     // $('#popcart').popover('show');
  //     var $j=jQuery.noConflict();
  //     $j(document).ready(function(){
  //     //
  //       $j('[data-toggle="popover"]').popover();
  //     });
  //
  //   }
  // }

  //
  // $("#clearCart").click(function(e){
  //   clearCart();
  //
  //   cartForm=document.getElementById('cartForm');
  //   $('#cartData').val(JSON.stringify(cart));
  //   e.preventDefault();
  //
  //   $.ajax({
  //       type:'POST',
  //       url:'/shop/cart/',
  //       data:{
  //             cartData:$('#cartData').val(),
  //             user:$('#user').val(),
  //             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
  //           },
  //           success:function(){
  //             alert("ok done");
  //           }
  //   });
  // });



  // function clearCart() {
  //     console.log("cart is clearing ")
  //     // cart = JSON.parse(localStorage.getItem('cart'));
  //     for (var item in cart) {
  //         document.getElementById('div' + item).innerHTML = '<button id="' + item + '" class="btn btn-primary cart">Add To Cart</button>'
  //     }
  //     localStorage.clear();
  //     cart = {};
  //     updateCart(cart);
  // }



  function updateCart(cart) {

      var sum = 0;
      for (var item in cart) {
          sum = sum + cart[item][0];
          if (document.getElementById('div' + item))
            document.getElementById('div' + item).innerHTML = "<button id='minus" + item + "' class='btn btn-primary minus'>-</button> <span id='val" + item + "''>" + cart[item][0] + "</span> <button id='plus" + item + "' class='btn btn-primary plus'> + </button>";

      }



      // localStorage.setItem('cart', JSON.stringify(cart));
      document.getElementById('cart').innerHTML = sum;
      console.log(cart);
      updatePopover(cart);

  }


  // If plus or minus button is clicked, change the cart as well as the display value
  $('.divpr').on("click", "button.minus", function(e) {


    if(CheckingUser())
    {

      a = this.id.slice(7, );
      cart['pr' + a][0] = cart['pr' + a][0] - 1;
      cart['pr' + a][0] = Math.max(0, cart['pr' + a][0]);
      if (cart['pr' + a][0] == 0){
          document.getElementById('divpr' + a).innerHTML = '<button id="pr'+a+'" class="btn btn-primary cart">Add to Cart</button>';
          delete cart['pr'+a];
      }
      else{
          document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
      }
      updateCart(cart);
      cartForm=document.getElementById('cartForm');

      // document.getElementById('cartData').value=cart;
      $('#cartData').val(JSON.stringify(cart));

    e.preventDefault();

    $.ajax({
        type:'POST',
        url:'/shop/cart/',
        data:{
              cartData:$('#cartData').val(),
              user:$('#user').val(),
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){

            }
    });

  }

  });

  $('.divpr').on("click", "button.plus", function(e) {

    if(CheckingUser())
    {

      a = this.id.slice(6, );
      cart['pr' + a][0] = cart['pr' + a][0] + 1;
      document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
      updateCart(cart);


        cartForm=document.getElementById('cartForm');
        $('#cartData').val(JSON.stringify(cart));
        e.preventDefault();

        $.ajax({
            type:'POST',
            url:'/shop/cart/',
            data:{
                  cartData:$('#cartData').val(),
                  user:$('#user').val(),
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(){
                  
                }
        });
    }
  });
