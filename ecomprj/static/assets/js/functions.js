const months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

$("#commentForm").submit(function(e) {
    e.preventDefault();

    const dt = new Date();
    const time = dt.getUTCDate() + " " + months_list[dt.getUTCMonth()] + ", " + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        // dataType: "json",
        success: function(res) {
            console.log("Comment Saved To Db.....");

            // Log the response in JSON format
            // console.log("JSON Response: ", JSON.stringify(res));

            if (res.bool === true) {
                $("#review-res").html("Review Added Successfully!");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">';
                _html += '<div class="user justify-content-between d-flex">';
                _html += '<div class="thumb text-center">';
                _html += '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNvWDvQb_rCtRL-p_w329CtzHmfzfWP0FIw&s" alt="" />';
                _html += '<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>';
                _html += '</div>';

                _html += '<div class="desc">';
                _html += '<div class="d-flex justify-content-between mb-10">';
                _html += '<div class="d-flex align-items-center">';
                _html += '<span class="font-xs text-muted">'+ time +'</span>';
                _html += '</div>';

                for (let i = 1; i <= res.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>';
                }

                _html += '</div>';
                _html += '<p class="mb-10">'+ res.context.review +'</p>';

                _html += '</div>';
                _html += '</div>';
                _html += '</div>';

                $(".comment-list").prepend(_html);
            }
        }
    });
});

// $(document).ready(function(){
//     $(".filter-checkbox").on("click", function(){
//         console.log("A check box has been clicked!");

//         let filter_object = {}

//         $(".filter-checkbox").each(function(){
//             let filter_value = $(this).val()
//             let filter_key = $(this).data("filter")

//             console.log("Filter value is:", filter_value);
//             console.log("filter key is:", filter_key);

//             filter_object[filter_key] = Array.from(document.querySelectorAll("input[data-filter='" + filter_value + "']:checked")).map(function(element){
//                 return element.value
//             })
//         })
//         console.log("Filter objects are:", filter_object);
        // $.ajax({
        //     url : "/filter-products",
        //     data : filter_object,
        //     dataType: "json",
        //     beforeSend : function(){
        //         console.log("Trying to Filter Products......");
        //     },
        //     success : function(response){
        //         console.log(response);
        //         console.log("Data Filtered Successfully!");
        //         $("#filtered-products").html(response.data)
        //         console.log("Done!");
        //     }
        // })
//     })
// })

$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function() {
        console.log("A check box has been clicked!");
    
        let filter_object = {};
    
        let min_price = $("#min_price").val();
        let max_price = $("#max_price").val();
    
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
    
        $(".filter-checkbox:checked").each(function() {
            let filter_value = $(this).val();
            let filter_key = $(this).data("filter");
    
            console.log("Filter value is:", filter_value);
            console.log("Filter key is:", filter_key);
    
            if (!filter_object[filter_key]) {
                filter_object[filter_key] = [];
            }
    
            filter_object[filter_key].push(filter_value);
        });
    
        console.log("Filter objects are:", filter_object);
    
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: "json",
            beforeSend: function() {
                console.log("Trying to Filter Products...");
            },
            success: function(response) {
                console.log(response);
                console.log("Data Filtered Successfully!");
                $("#filtered-products").html(response.data);
                console.log("Done!");
            }
        });
    });
    
    $("#max_price").on("blur", function(){
        let min = $(this).attr("min")
        let max = $(this).attr("max")
        let cp = $(this).val()

        // console.log("Min value:", min);
        // console.log("Max value:", max);
        // console.log("Current value:", cp);

        if(cp < parseInt(min) || cp > parseInt(max)){
            // console.log("Error Occuredd!");

            min = Math.round(min * 100) / 100
            max = Math.round(max * 100) / 100

            // console.log("Min:", min);
            // console.log("Max:", max);

            alert("The Price Must be from $"+min +" and $"+ max)

            $(this).val(min)
            $("#range").val(min)

            $(this).focus()

            return false
        }
    })

    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let title = $(".product-title-" + index).val()
        let id = $(".product-id-" + index).val()
        let pid = $(".product-pid-" + index).val()
        let image = $(".product-image-" + index).val()
        let price = $(".current-product-price-" + index).text()
        
    
        console.log("Quantity", quantity);
        console.log("Title", title);
        console.log("id", id);
        console.log("Price", price);
        console.log("this is", this_val);
        console.log("PID", pid);
        console.log("Index", index);
        console.log("Image", image);
    
        $.ajax({
            url: "/add-to-cart",
            data : {
                'id' : id,
                'pid' : pid,
                'image' : image,
                'title' : title,
                'quantity' : quantity,
                'price' : price,
            },
            dataType : "json",
            beforeSend: function(){
                console.log("Adding product to Cart!!!");
            },
            success: function(res){
                this_val.html("✔")
                console.log("Product Added Successfully!!");
                $(".cart-items-count").text(res.totalCartItems)
            }
        })
    })

    $(".delete-product").on("click", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
    
        console.log("Product_id", product_id);
    
        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id,
            },
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalCartItems);
                $("#cart-list").html(response.data);
            }
        });
    });    

    $(".update-product").on("click", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".update-product-"+product_id).val();
    
        console.log("Product_id", product_id);
        console.log("Product_QTY", product_quantity);
    
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "product_quantity": product_quantity,
            },
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalCartItems);
                $("#cart-list").html(response.data);
            }
        });
    });
});

// Add to Cart Functionality for product-detail page
// $(".add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let title = $(".product-title").val()
//     let id = $(".product-id").val()
//     let price = $(".current-product-price").text()
//     let this_val = $(this)

//     console.log("Quantity", quantity);
//     console.log("Title", title);
//     console.log("id", id);
//     console.log("Price", price);
//     console.log("this is", this_val);

//     $.ajax({
//         url: "/add-to-cart",
//         data : {
//             'id' : id,
//             'title' : title,
//             'quantity' : quantity,
//             'price' : price,
//         },
//         dataType : "json",
//         beforeSend: function(){
//             console.log("Adding product to Cart!!!");
//         },
//         success: function(res){
//             this_val.html("Added to Cart!!")
//             console.log("Product Added Successfully!!");
//             $(".cart-items-count").text(res.totalCartItems)
//         }
//     })
// })

