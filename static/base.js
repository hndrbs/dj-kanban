"use strict"

let modal;

const CONSTANTS = {
  swapTypeAttribute: "data-swap-type",
  swapTargetAttribute: "data-swap-target"
}

function clearMessage(){
  const baseDelay = 10000
  const incrementDelay = 1500
  const alerts = document.querySelectorAll(".alert")

  Array.from(alerts).forEach((alert, idx) => {
    setTimeout(() => {
      alert.remove()
    }, baseDelay + (incrementDelay * idx))
  })
}


function removeEmptyContentContainer(){
  const emptyContentContainer = htmx.find("#empty")
  if (emptyContentContainer) htmx.remove(emptyContentContainer)
}

function renewModal() {
  modal.dispose()
  modal = new bootstrap.Modal(document.getElementById("modal"))
  modal.show()
}


document.addEventListener("DOMContentLoaded", () => {
  modal = new bootstrap.Modal(document.getElementById("modal"))
  
  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
      modal.show()
    }
  })

  
  htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.requestConfig.verb === "post") {
        if ([204, 200].includes(e.detail.xhr.status)) {
          modal.hide()
          e.detail.shouldSwap = (e.detail.target !== "dialog")
          removeEmptyContentContainer()
        } else {
          renewModal()
        }
    }
  })

  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })

})
