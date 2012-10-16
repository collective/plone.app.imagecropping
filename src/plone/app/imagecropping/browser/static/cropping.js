
if (jQuery) {

    function clearCoords() {
        $('#coords input').val('');
        $('#h').css({color:'red'});
        window.setTimeout(function(){
            $('#h').css({color:'inherit'});
        },500);
    };

    function showCoords(c) {
        $('#x1').val(c.x);
        $('#y1').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);
    };

    function option_change(option) {

        var config = jQuery.parseJSON(option.attr('data-jcrop_config')),
            scale_name = option.attr('data-scale_name'),
            jcrop_config = {
                onChange: showCoords,
                onSelect: showCoords,
                onRelease: clearCoords
            };
        jQuery.extend(jcrop_config, config);

        $('#coords img.cropbox').attr('src', config["data-imageURL"]);
        $('#coords img.cropbox').width(config["origWidth"]);
        $('#coords img.cropbox').height(config["origHeight"]);
        $('#scalename').val(scale_name);

        var jcrop_api = $('#coords img.cropbox').data('Jcrop');
        if (jcrop_api != undefined) {
            jcrop_api.destroy();
        }

        $('#coords img.cropbox').Jcrop(jcrop_config);
    }

    $(function() {
        $('ul.scales li').click(function(e) {
            option_change($(this));
            $(this).addClass('selected').siblings().removeClass('selected');
        });
        $('ul.scales a').prepOverlay({subtype: 'image'});
        option_change($('ul.scales li.selected'));
    });
}
