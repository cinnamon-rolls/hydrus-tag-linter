const LOGGING = true;

export default class Component {
  /**
   * @param container probably a &lt;div&gt; or a &lt;ul&gt; or a &lt;table&gt; in the document
   * @param creatorFunc function(key) that returns an object, {elem, state} where elem is some element in the document and a state is something it can refer to later
   * @param updaterFunc function(key, elem, state) that gets the elem and state it created earlier and can modify it as it sees fit
   */
  constructor(container, creatorFunc) {
    this.container = container;
    this.creatorFunc = creatorFunc;

    this.children = {};

    if (typeof creatorFunc !== "function") {
      throw new Error("Expected a function for creatorFunc");
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
      fragment.appendChild(this.getChild(key));
    }

    this.container.innerHTML = null;
    this.container.appendChild(fragment);

    return this;
  }
}
