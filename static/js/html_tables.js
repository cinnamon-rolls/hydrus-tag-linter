export function defaultRenderStrategy(
  data,
  elemType = null,
  elemId = null,
  elemClass = null
) {
  // if the thing is already rendered as a document element, we return it unchanged
  if (data instanceof Node) {
    return data;
  }

  if (elemType == null) {
    if (typeof data === "number") {
      elemType = "code";
    } else {
      elemType = "span";
    }
  }
  try {
    var span = document.createElement(elemType);
  } catch (e) {
    throw new Error(
      "Failed to create text element of type '" + elemType + "'",
      e
    );
  }
  span.innerText = data + "";
  if (elemId != null) {
    span.id = elemId;
  }
  if (elemClass != null) {
    span.className = elemClass;
  }
  return span;
}

export async function renderTr(row, renderFuncs) {
  if (renderFuncs == null) {
    renderFuncs = [];
  }

  var tr = document.createElement("tr");

  for (let i = 0; i < row.length; i++) {
    let thingToRender = row[i];

    let renderFunc = null;

    if (renderFuncs.length > i) {
      renderFunc = renderFuncs[i];
    }
    if (typeof renderFunc === "string") {
      let elemType = renderFunc;
      renderFunc = (data) => defaultRenderStrategy(data, elemType);
    } else if (renderFunc == null) {
      renderFunc = defaultRenderStrategy;
    }

    let td = document.createElement("td");
    let rendered = await renderFunc(thingToRender);
    if (rendered != null) {
      td.appendChild(rendered);
    }
    tr.appendChild(td);
  }

  return tr;
}

export async function renderRows(tbody, data, renderFuncs) {
  if (tbody == null) {
    throw new Error("Body is null");
  }

  if (renderFuncs == null) {
    renderFuncs = [];
  }

  var fragment = document.createDocumentFragment();

  for (var i = 0; i < data.length; i++) {
    fragment.appendChild(await renderTr(data[i], renderFuncs));
  }

  tbody.innerHTML = null;
  tbody.appendChild(fragment);
}
