import { httpGetJson } from "./http_helper.js";

export async function destroy(options) {
  var confirmed = options.confirmed;

  var tagName = options.tagName;
  var tagService = options.tagService;
  var inbox = options.inbox;
  var archive = options.archive;

  var allJunkTagsMode = options.allJunkTags;
  var namespaceMode = options.namespaceMode;

  if (!inbox && !archive) {
    alert("If inbox and archive are both disabled, then nothing happens");
    return;
  }

  if (!allJunkTagsMode) {
    if (typeof tagName !== "string") {
      throw new Error("tag name is not a string it is a " + typeof tagName);
    }
    if (tagName != null) {
      tagName = tagName.trim().toLowerCase();
    }
    if (tagName == null || tagName === "") {
      if (namespaceMode) {
        alert("Namespace mode is not specified");
      } else {
        alert("Tag name is not specified");
      }
      return;
    }
  }

  if (tagService == null) {
    throw new Error("tag service not specified");
  }

  if (!confirmed) {
    confirmed = window.confirm(
      "Are you sure? This will automatically remove tags on the service '" +
        tagService +
        "' from files in bulk. You should only proceed if you have a backup or are otherwise prepared for unforeseen consequences."
    );
  }

  if (!confirmed) {
    return;
  }

  var params = new URLSearchParams();
  params.set("read_tag_service", tagService);
  params.set("write_tag_service", tagService);
  params.set("inbox", inbox);
  params.set("archive", archive);
  params.set("namespace_mode", namespaceMode)

  if (tagName != null) {
    params.set("tags", JSON.stringify(tagName));
  }

  var url = "/api";

  if (options.allJunkTags) {
    url += "/junk_tags/search_and_destroy?";
  } else {
    url += "/tags/search_and_destroy?";
  }

  url += params.toString();

  return await httpGetJson(url)
    .then((x) => {
      console.log(x);
      alert("Done, removals: " + x.removals);
    })
    .catch((x) => {
      console.error(x);
      alert(
        "The command failed. Please open the console and screenshot as much as possible, thank you"
      );
    });
}
