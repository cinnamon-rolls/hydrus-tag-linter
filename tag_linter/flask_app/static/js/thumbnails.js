function getThumbnailUrl(fileId) {
  return "/files/thumbnail/" + fileId;
}

function getFileUrl(fileId, galleryOptions = {}) {
  var ret = "/file?file=" + fileId;

  if (galleryOptions.ruleName) {
    ret += "&rule=" + encodeURI(galleryOptions.ruleName);
  }
  if (galleryOptions.exemptions) {
    ret += "&exemptions=true";
  }

  return ret;
}

export function renderThumbnail(fileId, galleryOptions = {}) {
  const fileHref = getFileUrl(fileId, galleryOptions);

  var anchor = document.createElement("a");
  // weird workaround to cope with quirky html rendering
  anchor.style += "font-size: 0;";
  anchor.href = fileHref;

  var container = document.createElement("div");
  container.className += " thumbnail";
  anchor.appendChild(container);

  var img = document.createElement("img");
  img.src = getThumbnailUrl(fileId);
  container.appendChild(img);

  return anchor;
}
