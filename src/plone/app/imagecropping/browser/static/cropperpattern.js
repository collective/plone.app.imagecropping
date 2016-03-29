require([
    'pat-base',
    'jquery',
    'plone_app_imagecropping_cropper' // defines itself as jq plugin: Cropper
], function(Base, $) {
  'use strict';
  var ImageCropper = Base.extend({
    name: 'image-cropper',
    trigger: '.pat-image-cropper',
    parser: 'mockup',
    while_reset: false,
    while_init: true,
    while_saving: false,
    _changed: false,
    defaults: {
      identifier: null,
      fieldname: null,
      saveurl: null,
      authenticator: null,
      scale: null,
      preview: null,
      is_cropped: null,
      view_mode: 3,
      aspect_ratio: 16 / 9,
      currrent_x: null,
      currrent_y: null,
      currrent_w: null,
      currrent_h: null,
      true_width: null,
      true_height: null,
    },
    update_badges: function() {
      if (this.while_saving) {
        this.$badge_saving.show();
        this.$button_save.prop('disabled', true);
        this.$button_reset.prop('disabled', true);
        this.$button_remove.prop('disabled', true);
        return;
      } else {
        this.$badge_saving.hide();
      }
      if (this.options.is_cropped) {
        this.$button_remove.prop('disabled', false);
        this.$badge_uncropped.hide();
        this.$badge_cropped.show();
      } else {
        this.$button_remove.prop('disabled', true);
        this.$badge_uncropped.show();
        this.$badge_cropped.hide();
      }
      if (this.crop_changed()) {
        this.$badge_changed.show();
        this.$button_save.prop('disabled', false);
        this.$button_reset.prop('disabled', false);
      } else {
        this.$badge_changed.hide();
        if (this.options.is_cropped) {
          this.$button_save.prop('disabled', true);
          this.$button_reset.prop('disabled', true);
        } else {
          this.$button_save.prop('disabled', false);
          this.$button_reset.prop('disabled', true);
        }
      }
    },
    crop_changed: function () {
      if (this.while_init || this.while_reset) {
        return false;
      }
      if (!$('.cropper-container', this.$image.parent()).is(':visible')) {
        return this._changed;
      }
      var current = this.$image.cropper('getData');
      var xc = (this.original_data.x -1) < current.x  && current.x < (this.original_data.x +1),
          yc = (this.original_data.y -1) < current.y  && current.y < (this.original_data.y +1),
          wc = (this.original_data.width -1) < current.width  && current.width < (this.original_data.width +1),
          hc = (this.original_data.height -1) < current.height  && current.height < (this.original_data.height +1);
      this._changed = !(xc && yc && wc && hc);
      return this._changed;
    },
    reset: function() {
      console.log('RESET');
      this.while_reset = true;
      this.cropper.setData(this.original_data);
      this.visualize_selected_area();
      this.while_reset = false;
      this.update_badges();
    },
    remove: function() {
      console.log('REMOVE');
      var self = this,
          postData = {
        remove: true,
        fieldname: this.options.fieldname,
        scale: this.options.scalename,
        _authenticator: this.options.authenticator
      };
      self.while_saving = true;
      self.update_badges();
      $.ajax(
        {
          url: this.options.saveurl,
          type: 'POST',
          data: postData,
          success: function(data, textStatus, jqXHR) {
            self.options.is_cropped = false;
            self.while_saving = false;
            self.update_badges();
         },
          error: function(jqXHR, textStatus, errorThrown) {
            self.while_saving = false;
            self.update_badges();
            alert(textStatus, errorThrown);
          }
        }
      );
    },
    save: function() {
      console.log('SAVE ' + this.identifier);
      var self = this,
          crop_data = this.$image.cropper('getData'),
          postData = {
            x: crop_data.x,
            y: crop_data.y,
            width: crop_data.width,
            height: crop_data.height,
            fieldname: this.options.fieldname,
            scale: this.options.scalename,
            _authenticator: this.options.authenticator
          };
      self.while_saving = true;
      self.update_badges();
      $.ajax(
        {
          url: this.options.saveurl,
          type: 'POST',
          data: postData,
          success: function(data, textStatus, jqXHR) {
            self.options.is_cropped = true;
            self._changed = false;
            self.original_data = $.extend({}, self.cropper.getData());
            self.while_saving = false;
            self.update_badges();
          },
          error: function(jqXHR, textStatus, errorThrown) {
            self.while_saving = false;
            self.update_badges();
            alert(textStatus, errorThrown);
          }
        }
      );

    },
    visualize_selected_area: function() {
      var crop_data = this.$image.cropper('getData');
      $('.cropx', self.$el).text(Math.round(crop_data.x));
      $('.cropy', self.$el).text(Math.round(crop_data.y));
      $('.cropw', self.$el).text(Math.round(crop_data.width));
      $('.croph', self.$el).text(Math.round(crop_data.height));
    },
    notify_visible: function() {
      this.while_reset = true;
      this.cropper.resize();
      if (this.options.is_cropped && !this.crop_changed()) {
        console.log('set to orig');
        this.cropper.setData(this.original_data);
        this.visualize_selected_area();
      }
      this.while_reset = false;
    },
    limit_minimum_cropping_size: function() {
      var current = this.$image.cropper('getData'),
          newbox = {};
      if (current.width <  this.options.target_width ||
          current.height <  this.options.target_height) {
        newbox.width = this.options.target_width;
        newbox.height = this.options.target_height;
        if (current.x + this.options.target_width > this.options.true_width) {
          newbox.x = this.options.true_width - this.options.target_width;
        } else {
          newbox.x = current.x;
        }
        if (current.y + this.options.target_height > this.options.true_height) {
          newbox.y = this.options.true_height - this.options.target_height;
        } else {
          newbox.y = current.y;
        }
        newbox.rotate = current.rotate;
        newbox.scaleX = current.scaleX;
        newbox.scaleY = current.scaleY;
        this.while_reset = true;
        this.cropper.setData(newbox);
        this.while_reset = false;
      }
    },
    init: function() {
      var self = this,
          area_inactive = self.$el.parent().hasClass('inactive'),
          sel_select = '#select-' + self.options.identifier,
          sel_cropper = '#croppingarea-' + self.options.identifier,
          sel_form = '#croppingarea-' + self.options.identifier;
      self.identifier = self.options.identifier;
      self.$image = $('img.main-image', self.$el);
      self.$badge_cropped = $(sel_select + ' .label.cropped');
      self.$badge_uncropped = $(sel_select + ' .label.uncropped');
      self.$badge_changed = $(sel_select + ' .label.changed');
      self.$badge_saving = $(sel_select + ' .label.saving');
      self.$button_save = $(sel_form + ' button.save');
      self.$button_remove = $(sel_form + ' button.remove');
      self.$button_reset = $(sel_form + ' button.reset');
      self.$button_save_all = $('button.save-all');

      // we need to make coords floats
      self.options.current_x = parseFloat(self.options.current_x);
      self.options.current_y = parseFloat(self.options.current_y);
      self.options.current_w = parseFloat(self.options.current_w);
      self.options.current_h = parseFloat(self.options.current_h);
      self.options.true_width = parseFloat(self.options.true_width);
      self.options.true_height = parseFloat(self.options.true_height);
      self.options.target_width = parseFloat(self.options.target_width);
      self.options.target_height = parseFloat(self.options.target_height);
      self.options.is_cropped = self.options.is_cropped == "True" ? true : false;

      // the scale we came in with from server side
      self.original_data = {
        // x: 100,
        // y: 100,
        // width: 1024,
        // height: 768,
        x: this.options.current_x,
        y: this.options.current_y,
        width: this.options.current_w,
        height: this.options.current_h,
        rotate: 0,
        scaleX: 1,
        scaleY: 1,
      };

      // hide badges
      self.update_badges();

      // bind buttons
      self.$button_reset.click(function() {self.reset();});
      self.$button_remove.click(function() {self.remove();});
      self.$button_save.click(function() {self.save();});
      self.$button_save_all.on(
        'click',
        {identifier: self.identifier},
        function(event) {
          if (self.crop_changed()) {
            self.save();
          }
        }
      );

      // configure and init cropper
      var configuration = {
          preview: self.options.preview,
          data: self.original_data,  // for some reasons these are not respected
          autoCrop: true,
          autoCropArea: 1,
          aspectRatio: parseFloat(self.options.aspect_ratio),
          viewMode: self.options.view_mode,
          restore: false,
          crop: function(e) {
            if (self.while_init || self.while_reset) {
              return;
            }
            self.limit_minimum_cropping_size();
            self.update_badges();
            self.visualize_selected_area();
          },
          built: function () {
            self.reset();
            self.while_init = false;
          }
        };
      self.$image.cropper(configuration);
      self.cropper = self.$image.data('cropper');
      self.$image.on(
        'CROPPERPATTERN.VISIBLE',
        function() {
          self.notify_visible();
        }
      );
    }
  });
  return ImageCropper;
});
