function someFunction(){
  let baseDelay = 10000
  let incrementDelay = 1500
  let arrayOfAlerts = [].slice.call(document.querySelectorAll(".alert"))

  arrayOfAlerts.forEach((alert, idx) => {
    setTimeout(() => {
      alert.remove()
    }, baseDelay + (incrementDelay * idx))
  })
}

someFunction()