$(document).ready(function(){
    
    var messageDiv = $("#alert_message");

    $("#select_cmp").on("click", function(){
        if( ($("#select_pkg1").val() != "0") && ($("#select_pkg2").val() != "0") ) {
            if( $("#select_pkg1").val() != $("#select_pkg2").val() ) {
                
                var formData = {
                    'select_pkg1': $("#select_pkg1").val(),
                    'select_pkg2': $("#select_pkg2").val(),
                };
                $.ajax({
                    url: "/compare_process",
                    type: "POST",
                    data: formData,
                    cache: false,
                    success: function(response) {

                        $("#divider").addClass('divider_thin');

                        $("div.dinamic_div").hide();
                        $("#grp_pkg1 #" + $('#select_pkg1 option:selected').val()).show();
                        
                        $("div.compare_div").hide();                        
                        $("#grp_pkg2 #" + $('#select_pkg2 option:selected').val()).show();
                        $("#cve_typo_details").show();

                        var info = response;

                        if( info['data']['changes_pkg']['chg_home_page'] == "1"){
                            $("#grp_pkg1 #chg_home_page").addClass("label_red");
                            $("#grp_pkg2 #chg_home_page").addClass("label_red");
                        } else {
                            $("#grp_pkg1 #chg_home_page").removeClass("label_red");
                            $("#grp_pkg2 #chg_home_page").removeClass("label_red");
                        }

                        if( info['data']['changes_pkg']['chg_author_email'] == "1"){
                            $("#grp_pkg1 #chg_author_email").addClass("label_red");
                            $("#grp_pkg2 #chg_author_email").addClass("label_red");
                        } else {
                            $("#grp_pkg1 #chg_author_email").removeClass("label_red");
                            $("#grp_pkg2 #chg_author_email").removeClass("label_red");
                        }

                        if( info['data']['changes_pkg']['chg_author'] == "1"){
                            $("#grp_pkg1 #chg_author").addClass("label_red");
                            $("#grp_pkg2 #chg_author").addClass("label_red");
                        } else {
                            $("#grp_pkg1 #chg_author").removeClass("label_red");
                            $("#grp_pkg2 #chg_author").removeClass("label_red");
                        }


                        var val1 = $("#select_pkg1").val().replace(".","-");
                        var val2 = $("#select_pkg2").val().replace(".","-");
                        var resultado = $("#grp_pkg1 #"+val1).find(".label_black");
                        var resultado2 = $("#grp_pkg2 #"+val2).find(".label_black");
                        let array_data = Object.entries(info['data']['changes_pkg']['chg_datac_urls']);

                        $.each(resultado, function (i) {
                                $.each (array_data, function (j) {

                                    if( array_data[j][0] == $(resultado[i]).text()){
                                        $(resultado[i]).addClass("label_red");
                                        $(resultado[i]).removeClass("label_black");
                                    }
                                });
                        });
                        
                        $.each(resultado2, function (k) {
                            $.each (array_data, function (l) {
                                
                                if( array_data[l][0] == $(resultado2[k]).text()){
                                    $(resultado2[k]).addClass("label_red");
                                    $(resultado2[k]).removeClass("label_black");
                                }
                            });
                        });

                        let array_ips = Object.entries(info['data']['changes_pkg']['chg_datac_ips']);

                        $.each(resultado, function (i) {
                                $.each (array_ips, function (j) {

                                    if( array_ips[j][0] == $(resultado[i]).text()){
                                        $(resultado[i]).addClass("label_red");
                                        $(resultado[i]).removeClass("label_black");
                                    }
                                });
                        });
                        
                        $.each(resultado2, function (k) {
                            $.each (array_ips, function (l) {
                                
                                if( array_ips[l][0] == $(resultado2[k]).text()){
                                    $(resultado2[k]).addClass("label_red");
                                    $(resultado2[k]).removeClass("label_black");
                                }
                            });
                        });


                        let array_emails = Object.entries(info['data']['changes_pkg']['chg_datac_emails']);

                        $.each(resultado, function (i) {
                                $.each (array_emails, function (j) {

                                    if( array_emails[j][0] == $(resultado[i]).text()){
                                        $(resultado[i]).addClass("label_red");
                                        $(resultado[i]).removeClass("label_black");
                                    }
                                });
                        });
                        
                        $.each(resultado2, function (k) {
                            $.each (array_ips, function (l) {
                                
                                if( array_emails[l][0] == $(resultado2[k]).text()){
                                    $(resultado2[k]).addClass("label_red");
                                    $(resultado2[k]).removeClass("label_black");
                                }
                            });
                        });


                        let array_hashes = Object.entries(info['data']['changes_pkg']['chg_datac_hash']);

                        $.each(resultado, function (i) {
                                $.each (array_hashes, function (j) {

                                    if( array_hashes[j][0] == $(resultado[i]).text()){
                                        $(resultado[i]).addClass("label_red");
                                        $(resultado[i]).removeClass("label_black");
                                    }
                                });
                        });

                        $.each(resultado2, function (k) {
                            $.each (array_hashes, function (l) {
                                
                                if( array_hashes[l][0] == $(resultado2[k]).text()){
                                    $(resultado2[k]).addClass("label_red");
                                    $(resultado2[k]).removeClass("label_black");
                                }
                            });
                        });

                        let array_filehashes = Object.entries(info['data']['changes_pkg']['chg_files_hashes']);

                        $.each(resultado, function (i) {
                            $.each (array_filehashes, function (j) {

                                if( array_filehashes[j][0] == $(resultado[i]).text()){
                                    $(resultado[i]).addClass("label_red");
                                    $(resultado[i]).removeClass("label_black");
                                }
                                });
                        });

                        $.each(resultado2, function (k) {
                            $.each (array_filehashes, function (l) {
                                
                                if( array_filehashes[l][0] == $(resultado2[k]).text()){
                                    $(resultado2[k]).addClass("label_red");
                                    $(resultado2[k]).removeClass("label_black");
                                }
                            });
                        });


                        
                    },
                });

            } else {
                messageDiv.show().html('<br/><br/>Select different versions!');
                setTimeout(function(){ messageDiv.hide().html('');}, 2000); 
                $("div.dinamic_div").hide();
                $("div.compare_div").hide();
                $("div.dinamic_div_details").hide();
            }
        } else {
            messageDiv.show().html('<br/><br/>You need select version to compare!'); 
            setTimeout(function(){ messageDiv.hide().html('');}, 2000); 
            $("div.dinamic_div").hide();
            $("div.compare_div").hide();
            $("div.dinamic_div_details").hide();
        }
    });


});