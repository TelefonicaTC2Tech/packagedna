$(document).ready(function(){
    $("#select_pkg").on("change", function(){
    	var divvalue = $(this).val(); 
        console.log(divvalue);
        if(divvalue == 0){
            $("div.dinamic_div").show();
        } else {
            $("div.dinamic_div").hide();
            $("#"+divvalue).show();
        }
    });
});