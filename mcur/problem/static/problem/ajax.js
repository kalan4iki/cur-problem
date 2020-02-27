var domain = 'http://127.0.0.1:8000/'

window.onload = function() {
  var not = document.getElementById('notif')
  var not1 = document.getElementById('not1')
  var zapros = new XMLHttpRequest();
  zapros.onreadystatechange = function() {
    if (zapros.readyState == 4){
      if (zapros.status == 200){
        var data = JSON.parse(zapros.responseText)
        notif.innerHTML = data['kolvo']
        not1.innerHTML = '<i class="fas fa-envelope mr-2"></i> <b>' + data['kolvo'] + '</b> количество на согласовании';
      }
    }
  }

  function answerLoad() {
    zapros.open('GET', domain + 'api/answer/', true);
    zapros.send();
  }

  answerLoad();
}
