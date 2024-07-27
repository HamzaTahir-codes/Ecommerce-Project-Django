console.log("Working Fine");

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method : $(this).attr("method"),

        url : $(this).attr("action"),

        datatype : "json",

        success: function(res){
            console.log("Comment Saved To Db.....");

            if(res.bool == true)
            {
                $("#review-res").html("Review Added Successfully!")
                $(".hide-comment-form").hide()
                $(".add-review").hide() 
            }
        }
    })
})