function clearMessage(){
  let baseDelay = 10000
  let incrementDelay = 1500
  let arrayOfAlerts = [].slice.call(document.querySelectorAll(".alert"))

  arrayOfAlerts.forEach((alert, idx) => {
    setTimeout(() => {
      alert.remove()
    }, baseDelay + (incrementDelay * idx))
  })
}


function fetchForm(url) {
  htmx
    .ajax("GET", url, { target: "#modal_container" })
    .then(() => toggleModal("modal_form"))
}



function toggleModal(modalId) {
  var myModal = bootstrap.Modal.getOrCreateInstance(document.getElementById(modalId), {
    keyboard: false
  })
  myModal.show()
}


function setListenerFetchModalForm() {
  const buttons = document.querySelectorAll("[data-todo=fetchForm]")
  
  Array.from(buttons).forEach((button) => {
    const url = button.getAttribute("data-url")
    const id = "#" + button.id
    htmx.on(id, "click", () => fetchForm(url))
  })
}

document.addEventListener("DOMContentLoaded", function() {
  setListenerFetchModalForm()
})
