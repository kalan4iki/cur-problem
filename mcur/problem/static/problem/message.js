function viewmessage(title, mes, status) {
    if (status === 0) {
        toastr["success"](mes, title);
    } else {
        toastr["error"]('Код ошибки' + status, 'Ошибка выполнения')
    }
}

function viewmessage2(title, mes, status) {
    Swal.fire(
      title,
      mes,
      status
    )
}
