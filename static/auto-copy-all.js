// go through each hash block and add a copy all button

window.addEventListener("load", function () {
  function getCopyFunc(elem) {
    return function (e) {
      navigator.clipboard.writeText(elem.innerText);
    };
  }

  console.log("Automagically adding 'copy all' buttons...");

  var elements = document.body.getElementsByTagName("div");

  for (var i = 0; i < elements.length; i++) {
    var div = elements[i];
    var codeID = div.id + "_code";
    var code = document.getElementById(codeID);

    if (code != null) {
      var btn = document.createElement("button");
      btn.innerText = "Copy All";

      btn.onclick = getCopyFunc(code);

      div.appendChild(btn);
    }
  }
});
