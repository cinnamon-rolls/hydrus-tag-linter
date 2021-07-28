import TagList from "./TagList.js";

export default class PendingTagList extends TagList {
  constructor(container) {
    super(container, x => this.toggleTag(x, false, true));
    this.tags = [];
  }

  toggleTag(tag, allowAdd = true, allowRemove = true) {
    if (typeof tag !== "string") {
      throw Error("Not a string: " + typeof tag + ", " + tag);
    }

    var inputArray = tag.split("\n");

    for (let input of inputArray) {
      input = input.trim().toLowerCase();

      // check if not empty
      if (input) {
        let index = this.tags.indexOf(input);
        if (index == -1) {
          if (allowAdd) {
            this.tags.push(input);
          }
        } else {
          if (allowRemove) {
            this.tags.splice(index, 1);
          }
        }
      }
    }

    this.setTags(this.tags);
  }

  setTags(tags) {
    this.tags = tags;
    super.setTags(tags);
  }

  getTags() {
    return this.tags;
  }

  listenToInput(inputElemName) {
    var inputElem = document.getElementById(inputElemName);

    if (inputElem == null) {
      console.error("Could not find element: " + inputElemName);
      return;
    }

    var actualThis = this;

    inputElem.addEventListener("keyup", function (e) {
      if (e.key === "Enter" || e.keyCode === 13) {
        var inputString = inputElem.value;
        inputElem.value = "";
        actualThis.toggleTag(inputString);
      }
    });
  }
}
