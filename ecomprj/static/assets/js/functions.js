console.log("Working Fine");

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
    $(".filter-checkbox").on("click", function(){
        console.log("A check box has been clicked!");

        let filter_object = {}

        $(".filter-checkbox:checked").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            console.log("Filter value is:", filter_value);
            console.log("Filter key is:", filter_key);

            if(!filter_object[filter_key]) {
                filter_object[filter_key] = [];
            }

            filter_object[filter_key].push(filter_value);
        });

        console.log("Filter objects are:", filter_object);

        $.ajax({
            url : "/filter-products",
            data : filter_object,
            dataType: "json",
            beforeSend : function(){
                console.log("Trying to Filter Products......");
            },
            success : function(response){
                console.log(response);
                console.log("Data Filtered Successfully!");
                $("#filtered-products").html(response.data)
                console.log("Done!");
            }
        })
    });
});