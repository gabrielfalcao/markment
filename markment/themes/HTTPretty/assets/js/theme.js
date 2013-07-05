(function($){$(function(){
    $(function(){
        $("a.toc-link").on("click", function(e){
            $("ul.toc li").removeClass("active");
            $(this).parents("li").addClass("active");
        });
    });
})})(jQuery);