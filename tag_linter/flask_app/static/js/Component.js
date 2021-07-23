const LOGGING = false;

export default class Component {
  constructor(container, creatorFunc, updateFunc) {
    if (typeof container === "string") {
      container = document.getElementById(container);
    }
    this.container = container;
    this.creatorFunc = creatorFunc;
    this.updateFunc = updateFunc;

    this.children = {};

    if (!(container instanceof Node)) {
      throw new Error(
        "Not a Node: " + container + " (" + typeof container + ")"
      );
    }
    if (typeof creatorFunc !== "function") {
      throw new Error("Expected a function for creatorFunc");
    }
    if (updateFunc != null && typeof updateFunc !== "function") {
      throw new Error("Expected a function for updateFunc, or null/undefined");
    }
  }

  /** Removes the element from the document and clears the entry to null */
  removeChild(key) {
    var child = this.children[key + ""];
    if (child != null) {
      child.remove();
      this.children[child] = null;
    }
  }

  keepOnly(keepKeys) {
    for (let key of Object.keys(this.children)) {
      if (keepKeys.indexOf(key) !== -1) {
        this.removeChild(key);
      }
    }
  }

  getChild(key) {
    key = key + "";

    var child = this.children[key];

    if (child == null) {
      if (LOGGING) {
        console.log("COMPONENT: invoking creator func for '" + key + "'");
      }
      child = this.creatorFunc(key);
      this.children[key] = child;
    }

    return child;
  }

  reorder(keyOrder) {
    this.keepOnly(keyOrder);

    var fragment = document.createDocumentFragment();

    for (let key of keyOrder) {
      let elem = this.getChild(key);

      if (this.updateFunc != null) {
        this.updateFunc(key, elem);
      }

      if (elem != null) {
        if (elem instanceof Node) {
          fragment.append(elem);
        } else {
          console.error("not a Node: " + elem + " (" + typeof elem + ")");
        }
      }
    }

    this.container.innerHTML = null;
    this.container.appendChild(fragment);

    return this;
  }
}
