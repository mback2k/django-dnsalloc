/*
jQuery.fn.extend({
  htmlToggle: function(html) {
    if (!$.trim($(this).html())) {
      $(this).hide();
    }
    if (!$.trim(html)) {
      $(this).slideUp('slow');
    } else if ($(this).is(':hidden')) {
      $(this).html(html).slideDown('slow');
    } else {
      if ($.trim($(this).text()) != $.trim($(html).formatDatetime().text())) {
        $(this).fadeOut('slow', function() {
          $(this).html(html).formatDatetime().fadeIn('slow');
        });
      }
    }
  }
});
$(document).ready(function() {
  if ($.support.htmlSerialize) {
    $('a.toggle').live('click', function(event) {
      $.ajax({
        owner: this,
        url: this.href,
        dataType: 'html',
        beforeSend: function (XMLHttpRequest, textStatus) {
          if ($(this.owner).find('img')) {
            $(this.owner).attr('src', $(this.owner).find('img').attr('src'));
            $(this.owner).find('img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/loading.gif');
          }
        },
        success: function(data, textStatus) {
          $('#base').html($(data).find('#base').html());
          $('#upper').htmlToggle($(data).find('#upper').html());
          $('#lower').htmlToggle($(data).find('#lower').html());
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          if ($(this.owner).find('img')) {
            $(this.owner).attr('title', textStatus);
            $(this.owner).find('img').attr('alt', textStatus);
            $(this.owner).find('img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/exclamation.png');
          } else {
            $(this.owner).attr('title', textStatus);
            $(this.owner).html(textStatus);
          }
        }
      });
      event.preventDefault();
      return false;
    });
    $('a.delete').live('click', function(event) {
      if (window.confirm('Continue this operation?')) {
        $.ajax({
          owner: this,
          url: this.href,
          dataType: 'html',
          beforeSend: function (XMLHttpRequest, textStatus) {
            $(this.owner).find('img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/loading.gif');
          },
          success: function(data, textStatus) {
            $(this.owner).parent().parent().fadeOut('slow');
            $('#upper').htmlToggle($(data).find('#upper').html());
            $('#lower').htmlToggle($(data).find('#lower').html());
          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
            $(this.owner).attr('title', textStatus);
            $(this.owner).find('img').attr('alt', textStatus);
            $(this.owner).find('img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/exclamation.png');
          }
        });
      }
      event.preventDefault();
      return false;
    });
    $('form').live('submit', function(event) {
      $.ajax({
        owner: this,
        url: this.action,
        type: this.method.toUpperCase(),
        dataType: 'html',
        data: $(this).serialize(),
        beforeSend: function (XMLHttpRequest, textStatus) {
          $(this.owner).find('legend img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/loading.gif');
          $(this.owner).find('input').each(function(i) {
            $(this).attr('disabled', 'disabled');
          });
        },
        success: function(data, textStatus) {
          $('#upper').htmlToggle($(data).find('#upper').html());
          $('#lower').htmlToggle($(data).find('#lower').html());
          $('#base').html($(data).find('#base').html());
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          $(this.owner).find('legend img').attr('src', site_data.settings.MEDIA_URL+'dnsalloc/icons/exclamation.png');
        }
      });
      event.preventDefault();
      return false;
    });
  }
});
*/
