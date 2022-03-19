
document.addEventListener("DOMContentLoaded", () => {
  modal = new bootstrap.Modal(document.getElementById("modal"))
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
  
   document.querySelectorAll("div.message-wrapper")
    .forEach(node => node.addEventListener("messagePushed", e => {
      clearMessage(e.detail.messageId)
      e.stopImmediatePropagation();
    }))
  })
})

