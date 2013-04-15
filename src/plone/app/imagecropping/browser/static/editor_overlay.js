(function($) {
    $(function() {
        $("a.croppingeditor").prepOverlay({
            subtype:'ajax',
            formselector:'#coords',
            closeselector:"input[name='form.button.Cancel']"
        });
        $(document).bind("formOverlayLoadSuccess", function() {
            imagecropping.init_editor();
        })
    })
})(jQuery);
