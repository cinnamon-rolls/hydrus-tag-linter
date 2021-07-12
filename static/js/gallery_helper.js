function copy(obj) {
  var ret = {};
  for (var key in obj) {
    ret[key] = obj[key];
  }
  return ret;
}

function createThumbnail(id, options = {}) {
  id_uri = encodeURI(id);

  href = "/file?file=" + id_uri;

  if (options.ruleName) {
    href += "&rule=" + encodeURI(options.ruleName);
  }

  var anchor = document.createElement("a");
  anchor.style += "font-size: 0;";
  anchor.href = href;

  var container = document.createElement("div");
  container.className += " thumbnail";

  var img = document.createElement("img");
  img.src = "/files/thumbnail/" + id_uri;

  anchor.appendChild(container);
  container.appendChild(img);

  return anchor;
}

function createGallery(files, options = {}) {
  galleryElemID = options.galleryElemID || "gallery";
  page = options.page || 1;
  filesPerPage = options.filesPerPage || 24;

  console.log("Setting up gallery starting at page " + page + " with " + filesPerPage + " files per page");

  var target = document.getElementById(galleryElemID);
  if (target == null) {
    console.log("Cannot find element: " + galleryElemID);
    return;
  }

  target.innerHTML = "";

  if (files == null || files.length == 0) {
    var e = document.createElement("p");
    e.innerText = "Nobody home...";
    target.appendChild(e);
    return;
  }

  var thumbnails = document.createElement("div");
  thumbnails.className += "thumbnails_container";
  target.appendChild(thumbnails);

  var startIndex = (page - 1) * filesPerPage;

  var filesAdded = 0;
  for (var i = startIndex; i < files.length && filesAdded < filesPerPage; i++) {
    var thumbnail = createThumbnail(files[i], options);
    thumbnails.appendChild(thumbnail);

    filesAdded++;
  }

  var pagination = document.createElement("div");
  pagination.className += "pagination";
  target.appendChild(pagination);

  var pages = files.length / filesPerPage;

  function getPaginationClick(pageIndex) {
    var newOptions = copy(options);
    newOptions.page = pageIndex + 1;
    return function () {
      createGallery(files, newOptions);
    };
  }

  for (var pageIndex = 0; pageIndex < pages; pageIndex++) {
    var pageButton = document.createElement("button");
    pageButton.innerText = pageIndex + 1 + "";
    pageButton.onclick = getPaginationClick(pageIndex);
    pagination.appendChild(pageButton);
  }
}
