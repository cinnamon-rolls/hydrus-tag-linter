import React from "react";
import Loading from "./loading";
import AnchorButton from "./anchorButton";

var defaultTagPresentation = {
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

class FileTags extends React.Component {
  render() {
    var metadata = this.props.metadata;

    if (metadata == null || metadata === {}) {
      return <Loading />;
    }

    return this.renderTagUl(["hi", "hello:hello", "creator:your mo"]);
  }

  renderTagAnchor(tag) {
    return (
      <AnchorButton
        spanStyle={{ color: this.getTagColor(tag) }}
        buttonText={tag}
      ></AnchorButton>
    );
  }

  renderTagLi(tag) {
    return <li key={"li." + tag}>{this.renderTagAnchor(tag)}</li>;
  }

  renderTagUl(tags) {
    return (
      <ul className="tag_list">{tags.map((tag) => this.renderTagLi(tag))}</ul>
    );
  }

  getTagPresentation() {
    // future versions maybe download automagically from client api
    // in any case, this is not supported yet by Hydrus
    return defaultTagPresentation;
  }

  /** Given a namespace name as a string, get the color in css */
  getNamespaceColor(namespace) {
    var tagPresentation = this.getTagPresentation();
    var ret = tagPresentation.namespaces[namespace];
    if (ret == null) {
      ret = tagPresentation.default;
    }
    return ret;
  }

  /** Given a tag as a string, get the color in css */
  getTagColor(tag) {
    var tagPresentation = this.getTagPresentation();
    var parts = tag.split(":", 2);
    if (parts.length < 2) {
      return tagPresentation.namespaces[""];
    } else {
      return this.getNamespaceColor(parts[0]);
    }
  }
}

export default FileTags;
