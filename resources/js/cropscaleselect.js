import $ from "jquery";
import Base from "@patternslib/patternslib/src/core/base";
import logging from "@patternslib/patternslib/src/core/logging";

logging.setLevel("INFO");
const log = logging.getLogger("pat-imagecrop-scaleselect");

export default Base.extend({
    name: "imagecropsave",
    trigger: ".pat-imagecrop-scaleselect",
    parser: "mockup",

    // A shortcut for triggering custom events
    trigger_notify_visible: function ($cropperimg) {
        var e = $.Event("CROPPERPATTERN.VISIBLE");
        $cropperimg.trigger(e);
    },

    toggle_li: function (li) {
        var $li = $(li),
            $ul = $($li.parent());
        if ($li.hasClass("active")) {
            // ignore any active
            return;
        }
        // set prior active to inactive
        $("li.list-group-item.active", $ul).removeClass("active").addClass("inactive");

        // set clicked tab to active
        $li.removeClass("inactive").addClass("active");

        // activate/ deactivate cropping area
        var $new_area = $($($li.data("cropping-area"))),
            $areas = $($new_area.parent()),
            $old_area = $(".singlecroppingarea.active", $areas);

        $old_area.removeClass("active").addClass("inactive");

        $new_area.removeClass("inactive").addClass("active");

        // trigger repaint
        var $cropperimg = $("img.main-image", $new_area);
        this.trigger_notify_visible($cropperimg);
    },

    init: function () {
        import("../scss/cropscaleselect.scss");

        var self = this, tabEl = document.querySelector('a[data-bs-toggle="tab"]');
        tabEl.addEventListener('shown.bs.tab', function (event) {
            // trigger resize
            var $cropperimg = $('div.singlecroppingarea.active img.main-image', $fieldset);
            self.trigger_notify_visible($cropperimg);
        });
        $(".tab-pane", self.$el).each(function (findex) {
            var fieldset = this;
            $("li.list-group-item.scalable", $(fieldset)).each(function (lindex) {
                var li = this;
                $(li).on("click", function (e) {
                    self.toggle_li(li);
                });
            });
        });
    },

});
