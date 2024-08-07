$(document).ready(function(){

    $(document).on("click", ".make-default-address", function() {
        console.log("Button clicked");
        let id = $(this).attr("data-address-id");
        let element = $(this);

        console.log("Id is:", id);
        console.log("Element is:", element);

        $.ajax({
            url:"/make-default-address",
            data:{
                "id" : id,
            },
            dataType: "json",
            success:function(res){
                console.log("Address Made Default......");

                if(res.boolean == true){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                }
            }

        })
    });

    $(".add-to-wishlist").on("click", function(e) {
        e.preventDefault();
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);

        console.log("Product Id: ", product_id);

        $.ajax({
            url : "/add-to-wishlist",
            data : {
                "id" : product_id,
            },
            dataType : "json",
            beforeSend: function(){
                console.log("Adding to Wishlist.....")
            },
            success:function(res){
                this_val.html("✔");

                if(res.bool == true){
                    console.log("Added to Wishlist");
                }
            }
        })
    });

    $(".remove-from-wishlist").on("click", function(){
        console.log("Wishlist Button Clicked")
        let wish_id = $(this).attr("data-wishlist")
        let this_val = $(this)

        console.log("Wishlist id", wish_id);

        $.ajax({
            url : "/remove-from-wishlist",
            data : {
                'id' : wish_id,
            },
            dataType : "json",
            beforeSend : function(){
                console.log("Deleting from Wishlist.....");
            },
            success: function(res){
                $("#wish-list-rem").html(res.data);
            }
        })
    });

    $("#contact-form-ajax").on("submit",function(e){
        e.preventDefault()
        console.log("Button Clicked!");

        let full_name=$("#full_name").val()
        let email=$("#email").val()
        let phone=$("#phone").val()
        let subject=$("#subject").val()
        let message=$("#message").val()

        console.log("Full Name:", full_name);
        console.log("Email :", email);
        console.log("phone:", phone),
        console.log("subject:", subject);
        console.log("message:", message);

        $.ajax({
            url: "/ajax-contact-us",
            data : {
                "full_name" : full_name,
                "email" : email,
                "phone" : phone,
                "subject" : subject,
                "message" : message,
            },
            dataType : "json",
            beforeSend: function(){
                console.log("Sending Data to server!!!");
            },
            success : function(res){
                console.log("Data Sent Successfully!");
                $(".contact-form-p").hide()
                $(".ajax-form").hide()
                $(".message-text").html("Message Sent Successfully!")
            }
        })
    })
})