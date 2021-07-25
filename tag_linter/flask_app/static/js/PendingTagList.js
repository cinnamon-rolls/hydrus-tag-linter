import TagList from "./TagList.js";

export default class PendingTagList extends TagList {
  constructor(container) {
    super(container);
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

  getTags() {
    return this.tags;
  }
}
