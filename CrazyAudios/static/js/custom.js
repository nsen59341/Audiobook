$(document).ready(function() {

    $(".del-mul-btn").attr('disabled', true);

    $("input[name=select_row]").on('click', function() {
        if($(this).is(':checked'))
        {
            var ids = $("#ids").val();
            if(ids.length!=0)
            {
                ids = ids+','+$(this).val();
            }
            else
            {
                ids += $(this).val();
            }
            $("#ids").val(ids);
            $(".del-mul-btn").attr('disabled', false);
        }
        else{
            var ids = $("#ids").val().split();
            ids.splice(ids.indexOf($(this).val()),1);
            if(ids.length==0)
            {
                $("#ids").val('');
                $(".del-mul-btn").attr('disabled', true);
            }
            else{
                $("#ids").val(ids);
            }
        }

    });

    $(".del-mul-btn").on('click', function() {
        $(".delete_files").submit();
    });

    $(".del-single-btn").on('click', function() {
        $("#ids").val($(this).data('id'));
        $(".delete_files").submit();
    });

});