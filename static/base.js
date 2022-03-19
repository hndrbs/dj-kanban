"use strict"

var modal

function clearMessage(id){
  let baseDelay = 10000
  const incrementDelay = 1500
  const messageWrapper = document.getElementById(id)
  const alerts = messageWrapper.querySelectorAll(".alert")

  alerts.forEach((alert, idx) => {
    // conditional to handle just in case messages already removed manually
    if (messageWrapper) {
      baseDelay += incrementDelay * idx
      htmx.remove(alert, baseDelay)

      if (idx + 1 === alerts.length) {
        setTimeout(() => messageWrapper.remove(), baseDelay + 3000)
      }
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