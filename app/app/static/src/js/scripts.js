(function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

    $('input[name^="inputDogDOB"]').on('blur', function(){
        $('#calcDogAge').val(calc_age());
        return;
    })

    function calc_age(){
        var y = $('#inputDogDOBYear');
        var m = $('#inputDogDOBMonth');
        var d = $('#inputDogDOBDay');

        if ( (y.val().length === 0 ) || (m.val().length === 0) || (d.val().length === 0 ) ) {
            console.log("Not a valid Date")
        } else {
            var cd = moment();
            var dob = moment([y.val(),m.val()-1, d.val()]);
            var diff = cd.diff(dob, 'days')
            var dog_age = moment.duration(diff, 'days').format('M [Months], w [Weeks]')
            console.log(
                cd,
                dob,
                diff,
                moment.duration(diff, 'days').format('Y [Years], M [Months] w [Weeks]'));
            return dog_age;
        }
    }

    $('.ajax_update_btn').click(function(){
        var btn = $(this).html('<span class="spinner-grow text-muted"></span>');
        var command_id = btn.data('command-id');
        var dog_id = btn.data('dog-id');
        var action = btn.data('action')
        //var ch_avg = btn.parent().siblings('input').val();
        var post_url = window.location
        console.log(post_url)
        $.ajax({
            url: post_url,
            type: 'POST',
            data: {
                dog_id: dog_id,
                command_id: command_id,
                action: action
            },
            success: function(r){
                console.log(r)
                response_handler(r, btn)
            }
        })
    })
    function response_handler(val, btn){
        if (val) {
            btn.html('<span class="fa fa-check"></span>').toggleClass('btn-danger btn-success');
        } else {
            btn.html('<span class="fas fa-exclamation-triangle"></span>');
            console.err(val)
        }
    }

    $(document).ready(function(){

        $('input[type=radio]').on('change', function(){
           $('input:radio').each(function() {
              if($(this).is(':checked')) {
                // You have a checked radio button here...
                $(this).next().addClass('show')
              }
              else {
                // Or an unchecked one here...
                $(this).next().removeClass('show')
              }
            });

        });

        $('.age_calc').each(function(index, e){
            //dob = $(this).data('dob');
            //$(this).html(moment($(this).data('dob'), "YYYY-MM-DD").fromNow(true) + " old")
            var d = moment();
            var dob = moment($(this).data('dob'), "YYYY-MM-DD");
            var diff = d.diff(dob, 'days')
            $(this).html(moment.duration(diff, 'days').format('Y [Years], M [Months] w [Weeks]'))
        })
        $('.opn_training_modal').on('click', function(){
           var dog_id = $(this).data('dog-id');

           $.get("dog/" + dog_id, function(data) {
                var e = $('.modal-body .form-group[data-command-id]')
                $.each(e, function(){
                    var ce = $(this);
                    $.each(data, function(){
                        if ($(ce).data('command-id') == this.command_id){
                            ce.removeClass('d-none');
                        }
                    })
                })
            })
           $("#trainingModal").modal('show');
        });
        $('input[type=range]').on('change', function(){
            $(this).next().html(this.value)
        })
        $('#calcDogAge').val(calc_age());
    });
})(jQuery);

