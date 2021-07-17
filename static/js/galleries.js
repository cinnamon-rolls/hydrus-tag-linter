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

function renderNobodyHome() {
  var e = document.createElement("p");
  e.innerText = "Nobody home...";
  return e;
}

function renderThumbnail(fileId, galleryOptions = {}) {
  const fileHref = getFileUrl(fileId, galleryOptions);

  var anchor = document.createElement("a");
  // weird workaround to cope with quirky rendering
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

function renderPaginationButton(
  currentPage,
  page,
  textOverride,
  buttonCallback
) {
  const text = textOverride || page + "";

  var ret;

  if (currentPage !== page) {
    ret = document.createElement("button");
    ret.className += "pagination_entry anchorbutton";
    ret.innerText = text;
    if (buttonCallback != null) {
      ret.onclick = () => buttonCallback(page);
    }
  } else {
    ret = document.createElement("b");
    ret.className += "pagination_entry";
    ret.innerText = text;
  }

  return ret;
}

function renderPagination(totalFiles, filesPerPage, rerender, galleryOptions) {
  if (galleryOptions == null) {
    galleryOptions = {};
  }

  const currentPage = galleryOptions.page || 1;
  const firstPage = 1;
  const lastPage = Math.ceil(totalFiles / filesPerPage);

  var pagination = document.createElement("div");
  pagination.className += "pagination";

  if (currentPage !== firstPage) {
    pagination.appendChild(
      renderPaginationButton(currentPage, firstPage, "<<", rerender)
    );
  }

  var padding = galleryOptions.paginationButtonsAroundCurrent || 3;
  var buttonsStart = Math.max(firstPage, currentPage - padding);
  var buttonsEnd = Math.min(lastPage + 1, currentPage + padding + 1);

  for (var i = buttonsStart; i < buttonsEnd; i++) {
    pagination.appendChild(
      renderPaginationButton(currentPage, i, null, rerender)
    );
  }

  if (currentPage !== lastPage && lastPage !== firstPage) {
    pagination.appendChild(
      renderPaginationButton(currentPage, lastPage, ">>", rerender)
    );
  }

  return pagination;
}

function renderGallery(fileIds, galleryOptions = {}) {
  const galleryElemID = galleryOptions.galleryElemID || "gallery";
  const page = galleryOptions.page || 1;
  const filesPerPage = galleryOptions.filesPerPage || 24;

  const rerender = (newPage) => {
    var newOptions = Object.assign({}, galleryOptions);
    newOptions.page = newPage;
    renderGallery(fileIds, newOptions);
  };

  console.log(
    "Setting up gallery starting on page " +
      page +
      " with " +
      filesPerPage +
      " files per page"
  );

  const target = document.getElementById(galleryElemID);
  if (target == null) {
    console.log("Cannot find element: " + galleryElemID);
    return;
  }

  target.innerHTML = "";

  if (fileIds == null || fileIds.length == 0) {
    target.appendChild(renderNobodyHome());
    return;
  }

  var thumbnailsContainer = document.createElement("div");
  thumbnailsContainer.className += "thumbnails_container";
  target.appendChild(thumbnailsContainer);

  var startIndex = (page - 1) * filesPerPage;

  var filesAdded = 0;
  for (
    let i = startIndex;
    i < fileIds.length && filesAdded < filesPerPage;
    i++
  ) {
    var thumbnail = renderThumbnail(fileIds[i], galleryOptions);
    thumbnailsContainer.appendChild(thumbnail);
    filesAdded++;
  }

  target.appendChild(
    renderPagination(fileIds.length, filesPerPage, rerender, galleryOptions)
  );
}

export { renderGallery };
