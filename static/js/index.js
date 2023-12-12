function updateLabel(value) {
  var button = document.getElementById("button-set");
  button.innerText = "set " + value + "%";
}

window.addEventListener("DOMContentLoaded", (event) => {
  const rollo = document.getElementById("rollo");
  const touchBar = document.getElementById("touchBar");
  rolloMaxHeight = rollo.getBoundingClientRect().height;
  var serverAddress = window.location.host;
  var windowInputActive = false;
  var startX = 0;

  function changeRolloHeightStyle(value) {
    var rolloHeight = document.getElementById("rollo").clientHeight;
    var newHeight = rolloHeight - value;
    if (newHeight > rolloMaxHeight) {
      newHeight = rolloMaxHeight;
    }
    if (newHeight < 1) {
      newHeight = 15;
    }
    rollo.style.height = newHeight + "px";
  }

  rollo.addEventListener("pointerdown", (event) => {
    windowInputActive = true;
    startX = Math.round(event.clientY);
  });

  rollo.addEventListener("pointerup", (event) => {
    windowInputActive = false;
  });

  rollo.addEventListener("pointercancel", (event) => {
    windowInputActive = false;
  });

  rollo.addEventListener("mouseleave", (event) => {
    windowInputActive = false;
  });

  // TODO fix input delay
  rollo.addEventListener("pointermove", (event) => {
    if (event.pointerType != "mouse" || windowInputActive) {
      var styleChange = startX - Math.round(event.clientY);
      startX = Math.round(event.clientY);
      changeRolloHeightStyle(styleChange);
      updateLabel(getPercentageValueOfRollo());
    }
  });

  function getPercentageValueOfRollo() {
    var percentage =
      (100 / rolloMaxHeight) * document.getElementById("rollo").clientHeight;
    (percentage - 100) * -1;
    return (Math.round(percentage) - 100) * -1;
  }

  document.getElementById("button-set").onclick = () => setRollo();
  document.getElementById("button-0").onclick = () => setRolloPreset(0);
  document.getElementById("button-25").onclick = () => setRolloPreset(25);
  document.getElementById("button-50").onclick = () => setRolloPreset(50);
  document.getElementById("button-75").onclick = () => setRolloPreset(75);
  document.getElementById("button-100").onclick = () => setRolloPreset(100);

  function setRollo() {
    window.location.href =
      "http://" +
      serverAddress +
      "/api/setProcent/" +
      getPercentageValueOfRollo();
  }

  function setRolloPreset(presetValue) {
    window.location.href =
      "http://" + serverAddress + "/api/preset/" + presetValue;
  }
});
