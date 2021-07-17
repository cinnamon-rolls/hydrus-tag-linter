import { getFileMetadata } from "./api.js";
import { renderThumbnail } from "./thumbnails.js";

const classNameFullFile = "full_file";

/** Creates a source element, needed for some cases below */
function renderSourceElement(fileId, src, mime) {
  var source = document.createElement("source");
  source.src = src;
  source.type = mime;
  return source;
}

function renderAsImage(fileId, src, mime) {
  var e = document.createElement("img");
  e.src = src;
  e.className = classNameFullFile;
  return e;
}

function renderAsAudio(fileId, src, mime) {
  var e = document.createElement("audio");
  e.className = classNameFullFile;
  e.controls = true;
  e.appendChild(renderSourceElement(src, mime));
  return e;
}

function renderAsVideo(fileId, src, mime) {
  var e = document.createElement("video");
  e.className = classNameFullFile;
  e.controls = true;
  e.appendChild(renderSourceElement(src, mime));
  return e;
}

function renderAsUnknwon(fileId, src, mime) {
  var e = document.createElement("div");
  var span = document.createElement("span");
  span.innerText = "The MIME type of this file is not supported (yet?)";
  e.appendChild(span);
  e.appendChild(document.createElement("br"));
  e.appendChild(renderThumbnail(fileId));
  return e;
}

/** Creates an element to display the file in based on the mimetype */
export async function renderEmbedElement(fileId) {
  var metadata = await getFileMetadata(fileId);

  var mime = metadata.mime;
  var src = "/files/full/" + fileId;

  if (mime.startsWith("image")) {
    return renderAsImage(fileId, src, mime);
  } else if (mime.startsWith("audio")) {
    return renderAsAudio(fileId, src, mime);
  } else if (mime.startsWith("video")) {
    return renderAsVideo(fileId, src, mime);
  } else {
    return renderAsUnknwon(fileId, src, mime);
  }
}
