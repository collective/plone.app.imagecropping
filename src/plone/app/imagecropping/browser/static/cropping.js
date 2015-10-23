/*globals $:false */

var ImageCropping = {};

(function ($) {

    function PloneImageCropping() {
        'use strict';

        this.x1 = 0;
        this.y1 = 0;
        this.x2 = 0;
        this.y2 = 0;
        this.changed = false;

        this.i18n_message_ids = {
            confirm_discard_changes: "Your changes will be lost. Continue?"
        };

        this.clearCoords = function() {
            $('#coords input[hidden]').val('');
            $('#h').css({color:'red'});
            window.setTimeout(function(){
                $('#h').css({color:'inherit'});
            },500);
        };

        this.saveCoords = function() {
            this.x1 = parseFloat($("#x1").val());
            this.y1 = parseFloat($("#y1").val());
            this.x2 = parseFloat($("#x2").val());
            this.y2 = parseFloat($("#y2").val());
        };

        this.unsaved_changes = function() {
            if (this.changed) {
                return !confirm(this.i18n_message_ids.confirm_discard_changes);
            }
            return false;
        };

        this.option_change = function(option) {
            var obj = this;
            var protection_activated = 0;
            var config = jQuery.parseJSON(option.attr('data-jcrop_config'));
            var scale_name = option.attr('data-scale_name');
            var doChange = function(coord) {
                    if (protection_activated > 0) {
                        obj.changed = true;
                    }
                    // show coords
                    $('#x1').val(coord.x);
                    $('#y1').val(coord.y);
                    $('#x2').val(coord.x2);
                    $('#y2').val(coord.y2);
                };
            var jcrop_config = {
                    onChange: doChange,
                    onSelect: doChange,
                    onRelease: obj.clearCoords
                };
            jQuery.extend(jcrop_config, config);
            $('#coords img.cropbox').attr('src', config["data-imageURL"]);
            $('#coords img.cropbox').width(config.origWidth);
            $('#coords img.cropbox').height(config.origHeight);
            $('#scalename').val(scale_name);

            var jcrop_api = $('#coords img.cropbox').data('Jcrop');
            if (jcrop_api !== undefined) {
                jcrop_api.destroy();
            }

            $('#coords img.cropbox').Jcrop(jcrop_config);

            option.addClass('selected').siblings().removeClass('selected');

            /* quite hacky, but needed for at least chrome. */
            setTimeout(function(){
                protection_activated = true;
            }, 250);

        };

        this.init_editor = function() {
            var obj = this,
                scales = $('ul.scales li'),
                selected = $('ul.scales li.selected');

            if(scales.length) {
                if (selected.length===0) {
                    selected = $('ul.scales li:first');
                }
                var anchor = $(selected).children('a');
                scales.click(function(e) {
                    if(obj.unsaved_changes()) {
                        return false;
                    }
                    obj.option_change($(this));
                    obj.saveCoords();
                });
                obj.option_change($(selected));
                scales.scrollTop($(selected).scrollTop());
            }

            /* save initial coords to track changes */
           this.saveCoords();
        };
    }

    ImageCropping = PloneImageCropping;

})(jQuery);
