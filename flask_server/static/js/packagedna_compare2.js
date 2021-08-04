$(document).ready(function(){
    
    $("div.dinamic_div").hide();
    $("div.compare_div").hide();
    
    var messageDiv = $("#alert_message");

    $("#select_cmp").on("click", function(){
        //console.log('click')
        if( ($("#select_pkg1").val() != "0") && ($("#select_pkg2").val() != "0") ) {
            if( $("#select_pkg1").val() != $("#select_pkg2").val() ) {
              
                //console.log($('#select_pkg1 option:selected').val());
                $("div.dinamic_div").hide();
                $("#grp_pkg1 #" + $('#select_pkg1 option:selected').val()).show();
                
                $("div.compare_div").hide();
                //console.log($('#select_pkg2 option:selected').val());
                $("#grp_pkg2 #" + $('#select_pkg2 option:selected').val()).show();
                
            } else {
                messageDiv.show().html('Select different versions!');
                setTimeout(function(){ messageDiv.hide().html('');}, 2000); 
                $("div.dinamic_div").hide();
                $("div.compare_div").hide();
            }
        } else {
            messageDiv.show().html('You need select version to compare!'); 
            setTimeout(function(){ messageDiv.hide().html('');}, 2000); 
            $("div.dinamic_div").hide();
            $("div.compare_div").hide();
        }
    });
    
});