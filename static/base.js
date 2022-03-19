"use strict"

var modal
var hasAfterRequestBeenCalled = false


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

async function getCardThatShouldBeDeleted(e) {
  const requestor = e.target
  const inputBoardFromId = requestor.querySelector("[name=board_from]")
  const inputCardId = requestor.querySelector("[name=card_id]")
  const boardId = inputBoardFromId.getAttribute("value")
  const cardId = inputCardId.getAttribute("value")
  return document.querySelector(`[data-parent="${boardId}"][data-card="${cardId}"]`)
}

async function deleteTheCard(node) {
  node.remove()
}

document.addEventListener("DOMContentLoaded", () => {
  modal = new bootstrap.Modal(document.getElementById("modal"))
})


document.addEventListener("htmx:afterSwap", e => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()
  } else {
    modal.hide()
  }
  document.addEventListener("htmx:beforeSwap", e => {
    if (e.detail.requestConfig.verb === "post" && e.detail.target.id === "dialog") {
        // handle on edit + add
        if (e.detail.xhr.status === 204) {
          modal.hide()
          e.detail.shouldSwap = false
          removeEmptyContentContainer()
        } else {
          renewModal()
        }
    } else if (e.detail.requestConfig.verb === "post" 
              && e.detail.xhr.status === 200
              && ["card", "board", "workspace"].includes(e.detail.target.id.split("-")[0])
    ) {
      // handle on delete, always close modal and render message with status code 200
      modal.hide()
      e.detail.shouldSwap = true
    } 
  })
  
  document.addEventListener("htmx:afterRequest", async e => {
    if (e.detail.requestConfig.verb === "post" 
      && e.detail.xhr.status === 200
      && e.detail.target.id.split("-")[0] === "cardcontainer") {
        // handle moving card
        // using async to solve this callback invoked twice
        await deleteTheCard(await getCardThatShouldBeDeleted(e))
      }
  })
  
  document.addEventListener("hidden.bs.modal", () => {
    const dialog = document.querySelector("#dialog")
    dialog.innerHTML = ""
  })

 document.querySelector("body").addEventListener("messagePushed", e => {
    console.log("message has been pushed", e.detail)
    e.stopImmediatePropagation();
  })
})


