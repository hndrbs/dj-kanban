"use strict"

let modal;

const CONSTANTS = {
  swapTypeAttribute: "data-swap-type",
  swapTargetAttribute: "data-swap-target"
}

function clearMessage(id){
  let baseDelay = 10000
  const incrementDelay = 1500
  const messageWrapper = document.getElementById(id)
  const alerts = messageWrapper.querySelectorAll(".alert")

  Array.from(alerts).forEach((alert, idx) => {
    baseDelay += incrementDelay * idx
    htmx.remove(alert, baseDelay)

    if (idx + 1 === alerts.length) {
      setTimeout(() => messageWrapper.remove(), baseDelay + 3000)
    }
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
    // handle on edit + add
    if (e.detail.requestConfig.verb === "post" && e.detail.target === "dialog") {
        if (e.detail.xhr.status === 204) {
          modal.hide()
          e.detail.shouldSwap = false
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
