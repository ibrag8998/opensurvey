(function ($) {
  function initialiseCKEditor(parentElement) {
    var $textareas = (typeof parentElement  === 'undefined')
      ? $('textarea[data-type=ckeditortype]')
      : $(parentElement).find('textarea[data-type=ckeditortype]')

    $textareas.each(function () {
      if (this.getAttribute('data-processed') === '0' && this.id.indexOf('__prefix__') === -1) {
        this.setAttribute('data-processed', '1');
        var ext = JSON.parse(this.getAttribute('data-external-plugin-resources'));
        for (var j = 0; j < ext.length; ++j) {
          CKEDITOR.plugins.addExternal(ext[j][0], ext[j][1], ext[j][2]);
        }
        var editor = CKEDITOR.instances[this.id];
        if (editor) {
          editor.destroy(true);
        }
        CKEDITOR.replace(this.id, JSON.parse(this.getAttribute('data-config')));
      }
    });
  }

  function destroyCKeditor(parentElement) {
    var $textareas = (typeof parentElement  === 'undefined')
      ? $('textarea[data-type=ckeditortype]')
      : $(parentElement).find('textarea[data-type=ckeditortype]')

    $textareas.each(function () {
      try {
        CKEDITOR.instances[this.id] && CKEDITOR.instances[this.id].destroy();
        this.setAttribute("data-processed", "0");
      } catch (err) {
        console.log(this, err);
        /* intentionally left empty */
      }
    })
  }

  var dragObserver = new MutationObserver((mutations) => {
    mutations.forEach(mu => {
      var oldClassList = mu.oldValue.split(' ');
      var newClassList = mu.target.classList.value.split(' ');
      // Caught drag start
      if ($(newClassList).not(oldClassList).get()[0] === 'djn-item-dragging') {
        destroyCKeditor(mu.target);
      }
      // Caught drag end
      if ($(oldClassList).not(newClassList).get()[0] === 'djn-item-dragging') {
        initialiseCKEditor(mu.target);
      }
    });
  });

  function observeSort(el) {
    dragObserver.observe(el, {
      attributes: true,
      attributeOldValue: true,
      attributeFilter: ['class']
    })
  }

  $(document).ready(function () {
    $('.djn-item').each(function () {
      observeSort(this);
    })
    $(document).on('formset:added', function (event, row) {
      initialiseCKEditor(row[0]);
      observeSort(row[0]);
    })
  });
}(django.jQuery));
