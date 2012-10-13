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
        var origWidth = option.attr('data-origWidth');
        var origHeight = option.attr('data-origHeight');
        var minWidth = option.attr('data-minWidth');
        var minHeight = option.attr('data-minHeight');
        var ratioWidth = option.attr('data-ratioWidth');
        var ratioHeight = option.attr('data-ratioHeight');

        var imageURL = option.attr('data-imageURL');
        $('#coords img.cropbox').attr('src', imageURL);
        $('#coords img.cropbox').width(origWidth);
        $('#coords img.cropbox').height(origHeight);


        var field = option.val().split('-')[0];
        $('#field').val(field);
        var scaleName = option.val().split('-')[1];
        $('#scalename').val(scaleName);

        var jcrop_api = $('#coords img.cropbox').data('Jcrop');
        if (jcrop_api != undefined) {
            jcrop_api.destroy();
        }

        $('#coords img.cropbox').Jcrop({
            allowResize: true,
            allowMove: true,
            onChange: showCoords,
            onSelect: showCoords,
            onRelease: clearCoords,
            trueSize: [origWidth, origHeight],
            boxWidth: 900,
            boxHeight: 0,
            setSelect: [0,0, minWidth, minHeight],
            aspectRatio: ratioWidth/ratioHeight,
            minSize: [minWidth,minHeight]
        });
    }

    $(document).ready(function() {
        $('#image-select').change( function(){
            option_change($('option:selected',this));
        });
        option_change($('#image-select option:selected'));

    });
}
