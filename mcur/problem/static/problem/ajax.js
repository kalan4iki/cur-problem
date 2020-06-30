var urlbasic = '/api/answer/';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.onload = function() {
  var notif = $('#notif'),
      spannot = $('#spannot'),
      not1 = $('#not1'),
      not2 = $('#not2'),
      CSRFtoken = getCookie('csrftoken');
      post = $.post(urlbasic, {csrfmiddlewaretoken: CSRFtoken});
      post.done(function (dates) {
          notif.text(dates['kolvosogl'] + dates['kollno']);
          spannot.text(dates['kolvosogl'] + dates['kollno'] + ' Уведомлений');
          not1.empty();
          not2.empty();
          not1.append("<i class='fas fa-envelope mr-2'></i>" + dates['kollno'] + ' нераспределенных жалоб');
          not2.append('<i class="fas fa-envelope mr-2"></i>' + dates['kolvosogl'] + ' ответов на согласовании');
  });
};
