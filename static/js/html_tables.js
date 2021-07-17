export function renderDataAsText(
  data,
  elemType = null,
  elemId = null,
  elemClass = null
) {
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
    let renderFunc = null;
    if (renderFuncs.length > i) {
      renderFunc = renderFuncs[i];
    }
    if (typeof renderFunc === "string") {
      renderFunc = (data) => renderDataAsText(data);
    }
    if (renderFunc == null) {
      renderFunc = renderDataAsText;
    }

    let td = document.createElement("td");
    let rendered = await renderFunc(row[i]);
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

  var rows = [];

  for (var i = 0; i < data.length; i++) {
    rows.push(await renderTr(data[i], renderFuncs));
  }

  tbody.innerHTML = "";

  for (let row of rows) {
    tbody.appendChild(row);
  }
}
