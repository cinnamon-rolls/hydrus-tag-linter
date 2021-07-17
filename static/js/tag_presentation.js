var rule_namespaces = ["linter rule:", "linter exempt:"];

// future versions maybe download automagically from client api
var tagPresentation = {
  default: "#72A0C1", // undefined namespace
  namespaces: {
    "": "#006FFA", // no namespace
    character: "#00AA00",
    creator: "#AA0000",
    meta: "#AAAAAA",
    person: "#008000",
    series: "#AA00AA",
    studio: "#800000",
    system: "#996515",
    "linter rule": "#AA8000",
    "linter exempt": "#AA8000",
  },
};

/** Given a namespace name as a string, get the color in css */
function getNamespaceColor(namespace) {
  var ret = tagPresentation.namespaces[namespace];
  if (ret == null) {
    ret = tagPresentation.default;
  }
  return ret;
}

/** Given a tag as a string, get the color in css */
function getTagColor(tag) {
  var parts = tag.split(":", 2);
  if (parts.length < 2) {
    return tagPresentation.namespaces[""];
  } else {
    return getNamespaceColor(parts[0]);
  }
}

function createTagAnchor(tag) {
  var e = document.createElement("a");
  e.innerText = tag;
  e.style = "color:" + getTagColor(tag) + ";";
  e.className += "tag_anchor";

  var match = null;
  for (var i = 0; i < rule_namespaces.length && match == null; i++) {
    if (tag.startsWith(rule_namespaces[i])) {
      match = rule_namespaces[i];
    }
  }

  if (match != null) {
    e.href = "/rules/" + encodeURI(tag.substring(match.length));
  } else {
    var search = encodeURI('"' + tag + '"');
    e.href = "/search?search=" + search;
  }
  return e;
}

function createTagListItem(tag) {
  var li = document.createElement("li");
  li.appendChild(createTagAnchor(tag));
  return li;
}

function createTagList(tags) {
  tags.sort(compareTags);
  var ul = document.createElement("ul");
  ul.className += "tag_list";
  for (var i = 0; i < tags.length; i++) {
    ul.appendChild(createTagListItem(tags[i]));
  }
  return ul;
}

/** Sorts tags based on namespace and then text */
function compareTags(tag1, tag2) {
  var b1 = tag1.includes(":");
  var b2 = tag2.includes(":");
  if (b1 && !b2) {
    return -1;
  } else if (!b1 && b2) {
    return 1;
  } else if (b1 && b2) {
    return tag1.split(":", 2)[0].localeCompare(tag2.split(":", 2)[0]);
  } else {
    return tag1.localeCompare(tag2);
  }
}

export { createTagList };
