(function ($) {
  // Only for stacked inlines
  $(document).ready(function () {
    $('div.inline-group div.inline-related:not(.tabular)').each(function () {
      fs = $(this).find('fieldset').not('.djn-fieldset')
      il = $(this).find('.inline-group')
      h3 = $(this).find('h3:first')

      // Don't collapse if fieldset contains errors
      if (fs.find('div').hasClass('errors') || $(this).hasClass('empty-form')) {
        fs.addClass('stacked_collapse');
        h3.prepend('<a class="stacked_collapse-toggle" href="#">(' + gettext('Hide') + ')</a> ');
      } else {
        h3.prepend('<a class="stacked_collapse-toggle" href="#">(' + gettext('Show') + ')</a> ');
        fs.addClass('stacked_collapse collapsed');
        il.hide();
      }

      // Add toggle link
      h3.find('a.stacked_collapse-toggle').bind("click", function () {
        fs = $(this).parent('h3').nextAll('fieldset');
        il = fs.nextAll('div.inline-group');
        if (!fs.hasClass('collapsed')) {
          fs.addClass('collapsed');
          il.hide()
          $(this).html('(' + gettext('Show') + ')');
        } else {
          fs.removeClass('collapsed');
          il.show();
          $(this).html('(' + gettext('Hide') + ')');
        }
      }).removeAttr('href').css('cursor', 'pointer');
    });
  });
}(django.jQuery));
