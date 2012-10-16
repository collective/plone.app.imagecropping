
if (jQuery) {

    function clearCoords() {
        $('#coords input').val('');
        $('#h').css({color:'red'});
        window.setTimeout(function(){
            $('#h').css({color:'inherit'});
        },500);
    };

    function doChange(c) {
        // show coords
        $('#x1').val(c.x);
        $('#y1').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);

        // render thumbnail
        /*
        rx = c.w / 100;
        ry = c.h / 100;
        prev_node = $('#preview-' + $("#scalename").val());
        console.log(prev_node);
        cropbox_img = $('img.cropbox');
        thumb_img = $('<img />');
        thumb_img.attr('src', cropbox_img.attr('src'));
        prev_node.html(thumb_img);
        $("img", prev_node).css({
            width: Math.round(rx * cropbox_img.attr('width')) + 'px',
            height: Math.round(ry * cropbox_img.attr('height')) + 'px',
            marginLeft: '-' + Math.round(rx * c.x) + 'px',
            marginTop: '-' + Math.round(ry * c.y) + 'px'
        });
        */
    };

    function option_change(option) {

        var config = jQuery.parseJSON(option.attr('data-jcrop_config')),
            scale_name = option.attr('data-scale_name'),
            jcrop_config = {
                onChange: doChange,
                onSelect: doChange,
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
        // TODO: preview of actual scale
        //$('ul.scales a').prepOverlay({subtype: 'image'});
        option_change($('ul.scales li.selected'));
        $('ul.scales').scrollTop($('ul.scales li.selected').scrollTop());
    });
}
