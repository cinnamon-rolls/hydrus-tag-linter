import Component from "./Component.js";

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

function defaultTagOnClick(tagName) {
  var url = "/search?search=" + JSON.stringify(tagName);
  window.open(url, "_blank");
}

export default class TagList extends Component {
  constructor(container, tagClickFunc) {
    super(container, (x) => this.renderTagListItem(x));
    this.container.classList.add("tag_list");
    this.tagClickFunc = tagClickFunc;
  }

  setTags(tags) {
    if (tags == null) {
      tags = [];
    }
    tags.sort(compareTags);
    this.reorder(tags);
  }

  getTagClickFunc() {
    var ret = this.tagClickFunc;
    if (ret == null) {
      return defaultTagOnClick;
    }
    return ret;
  }

  renderTagAnchor(tag) {
    var e = document.createElement("button");
    e.innerText = tag;
    e.style = "color:" + getTagColor(tag) + ";";
    e.className += "anchorbutton tag_anchor";

    e.onclick = () => this.getTagClickFunc()(tag);

    return e;
  }

  renderTagListItem(tag) {
    var li = document.createElement("li");
    li.appendChild(this.renderTagAnchor(tag));
    return li;
  }
}
