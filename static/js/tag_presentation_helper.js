// depends on async_helper.js

// future versions maybe download automagically from client api
var tagPresentation = {
  default: "#72A0C1", // undefined namespace
  namespaces: {
    "": "#006FFA", // no namespaced
    character: "#00AA00",
    creator: "#AA0000",
    meta: "#000000",
    person: "#008000",
    series: "#AA00AA",
    studio: "#800000",
    system: "#996515"
  }
};

/** Given a namespace name as a string, get the color in css */
function getNamespaceColor(namespace) {
  var ret = tagPresentation.namespaces[namespace];
  if (ret == null) {
    ret = tagPresentation.namespaces[""];
  }
  return ret;
}

/** Given a tag as a string, get the color in css */
function getTagColor(tag) {
  var parts = tag.split(":", 2);
  if (parts.length < 2) {
    return tagPresentation.default;
  } else {
    return getNamespaceColor(parts[0]);
  }
}

function createTagElement(tag) {
  var e = document.createElement("span")
  e.innerText = tag
  e.style += "color=" + getTagColor(tag) + ";"
  return e
}