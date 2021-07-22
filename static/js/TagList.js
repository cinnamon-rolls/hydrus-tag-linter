import Component from "./Component.js";

var rule_namespaces = ["linter rule:", "linter exempt:"];

const DEFAULT_TAG_PRESENTATION = {
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

function getTagPresentation() {
  // in the future this might be an API call
  return DEFAULT_TAG_PRESENTATION;
}

/** Given a namespace name as a string, get the color in css */
function getNamespaceColor(namespace) {
  var ret = getTagPresentation().namespaces[namespace];
  if (ret == null) {
    ret = getTagPresentation().default;
  }
  return ret;
}

/** Given a tag as a string, get the color in css */
function getTagColor(tag) {
  var parts = tag.split(":", 2);
  if (parts.length < 2) {
    return getTagPresentation().namespaces[""];
  } else {
    return getNamespaceColor(parts[0]);
  }
}

function renderTagAnchor(tag) {
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
    e.href = "/rule?uid=" + tag.substring(match.length);
  } else {
    var search = encodeURI('"' + tag + '"');
    e.href = "/search?search=" + search;
  }
  return e;
}

function renderTagListItem(tag) {
  var li = document.createElement("li");
  li.appendChild(renderTagAnchor(tag));
  return li;
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

export default class TagList extends Component {
  constructor(container) {
    super(container, renderTagListItem);
    this.container.classList.add("tag_list");
  }

  setTags(tags) {
    if (tags == null) {
      tags = [];
    }
    tags.sort(compareTags);
    this.reorder(tags);
  }

  refreshTags() {
    this.setTagList(getTags());
  }
}
