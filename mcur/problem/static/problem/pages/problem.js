var url = '/problem/'

// Операция "отправить на обновление
$('#naobn').click(function () {
  var CSRFtoken = jQuery("[name=csrfmiddlewaretoken]").val(),
      pk = $( this ).attr('nomdobr'),
      action = $( this ).attr('action'),
      posting = $.post( url + pk, {csrfmiddlewaretoken: CSRFtoken, pk: pk, action: action}, onAjaxSuccess);
});

// Пустая операция


// Операция "удаление назначения"
$('.delterm').click(function () {
  var CSRFtoken = jQuery("[name=csrfmiddlewaretoken]").val(),
      pk = $( this ).attr('pkterm'),
      nomdobr = $( this ).attr('nomdobr'),
      action = $( this ).attr('action'),
      posting = $.post( url + nomdobr, {csrfmiddlewaretoken: CSRFtoken, action: action, pk: pk}, onAjaxSuccess);
});

// Операция "утверждение назначений"
$('.termapprove').click(function () {
  var CSRFtoken = jQuery("[name=csrfmiddlewaretoken]").val(),
      pk = $( this ).attr('pkterm'),
      nomdobr = $( this ).attr('nomdobr'),
      action = $( this ).attr('action'),
      posting = $.post( url + nomdobr, {csrfmiddlewaretoken: CSRFtoken, action: action, pk: pk}, onAjaxSuccess);
});

// Операция "изменение назначения"
$('.btneditdate').click(function () {
  var but = $( this ),
      pk = but.attr('id'),
      nomdobr = but.attr('nomdobr'),
      action = but.attr('action'),
      CSRFtoken = $('input[name=csrfmiddlewaretoken]').val(),
      posting = $.post( url + nomdobr, {csrfmiddlewaretoken: CSRFtoken, view: true, pk:pk, action: action, nomdobr: nomdobr});
      posting.done(function (datas) {
          var modalka = $('#modal-changedate'),
              a = modalka.find('input[id="id_date_new"]'),
              but = modalka.find('button[type="submit"]');
          but.attr('id', pk);
          a.attr('value', datas['content']['date']);
          modalka.modal('show')
      })
});

$('#changedate').submit(function (event) {
  event.preventDefault();
  var $form = $( this ),
      pk = $form.find('button[type="submit"]').attr('id'),
      nomdobr = $form.attr('nomdobr'),
      action = $form.attr('action'),
      date = $form.find('input[id="id_date_new"]').val(),
      CSRFtoken = $('input[name=csrfmiddlewaretoken]').val(),
      posting = $.post( url + nomdobr, {csrfmiddlewaretoken: CSRFtoken, pk:pk, date:date, change: true, action: action, nomdobr: nomdobr});
  posting.done(function (datas) {
      var modalka = $('#modal-changedate');
      modalka.modal('hide');
      onAjaxSuccess(datas);
  })
});

// Операция "назначение ТУ"
$('#tyform').submit(function (event) {
  event.preventDefault();
  var $form = $( this ),
      name = $form.find('select[name="name"]').val(),
      pk = $form.attr('nomdobr'),
      action = $form.attr('action'),
      CSRFtoken = $('input[name=csrfmiddlewaretoken]').val(),
      posting = $.post( url+pk, {csrfmiddlewaretoken: CSRFtoken, name: name, pk: pk, action: action}, onAjaxSuccess);
  $('#modal-ty').modal('hide');
});

// Операция "подготовка pdf"


// Операция "добавление назначения"
$('#termform').submit(function (event) {
  event.preventDefault();
  var $form = $( this ),
      date = $form.find('input[name="date"]').val(),
      sele1 = $form.find('select[name="org"]').val(),
      sele2 = $form.find('select[name="curat"]').val(),
      sele3 = $form.find('select[name="curatuser"]').val(),
      text = $form.find('textarea[name="desck"]').val(),
      further = $form.find('input[name="further"]').prop('checked'),
      furtherdate = $form.find('input[name="furtherdate"]').val(),
      CSRFtoken = $('input[name=csrfmiddlewaretoken]').val(),
      pk = $form.attr('nomdobr'),
      action = $form.attr('action'),
      posting = $.post( url + pk, {csrfmiddlewaretoken: CSRFtoken, date: date, org: sele1, curat:sele2, curatuser:sele3, desck:text, further:further, furtherdate:furtherdate, pk: pk, action: action}, onAjaxSuccess);
  $('#modal-addterm').modal('hide');
});



$(document).ready(function () {
  var fd = $('#id_furtherdate');
  fd.attr('readonly', true);
  fd.attr('type', 'date');
});

$('#id_further').change(function () {
  var cb = $( this );
  if(this.checked) {
     cb.parents("div[class='row']").find('#id_furtherdate').attr('readonly', false)
  } else {
     cb.parents("div[class='row']").find('#id_furtherdate').attr('readonly', true)
  }
});

function onAjaxSuccess(data)
{
  if (data['status'] === 0) {
      Swal.fire({
          title: data['title'],
          text: data['message'],
          icon: 'success',
          onClose: reloadModal
      })

  } else {
      Swal.fire(
          data['title'],
          data['message'],
          'error'
      )
  }
}

function reloadModal() {
  location.reload()
}
