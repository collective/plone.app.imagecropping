//TODO: seting the ration is not working always right...

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

        var config = jQuery.parseJSON(option.attr('data-jcrop_config'));
        var jcrop_config = {
            onChange: showCoords,
            onSelect: showCoords,
            onRelease: clearCoords
        };
        jcrop_config.allowResize = config["allowResize"];
        jcrop_config.allowMove = config["allowMove"];
        jcrop_config.trueSize = config["trueSize"];
        jcrop_config.boxWidth = config["boxWidth"];
        jcrop_config.boxHeight = config["boxHeight"];
        jcrop_config.setSelect = config["setSelect"];
        jcrop_config.aspectRatio = config["aspectRatio"];
        jcrop_config.minSize = config["minSize"];
        jcrop_config.maxSize = config["maxSize"];

        $('#coords img.cropbox').attr('src', config["data-imageURL"]);
        $('#coords img.cropbox').width(config["origWidth"]);
        $('#coords img.cropbox').height(config["origHeight"]);

        var scaleName = option.val();
        $('#scalename').val(scaleName);

        var jcrop_api = $('#coords img.cropbox').data('Jcrop');
        if (jcrop_api != undefined) {
            jcrop_api.destroy();
        }

        $('#coords img.cropbox').Jcrop(jcrop_config);
    }

    $(document).ready(function() {
        $('#image-select').change( function(){
            option_change($('option:selected',this));
        });
        option_change($('#image-select option:selected'));

    });
}
