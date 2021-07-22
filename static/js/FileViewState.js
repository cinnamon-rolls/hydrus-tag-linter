"use strict";

import TagList from "/static/js/TagList.js";
import ActionList from "/static/js/ActionList.js";

import { httpPostJson } from "/static/js/http_helper.js";
import { getTagsFromMetadata } from "/static/js/tags.js";
import { getFileMetadata } from "/static/js/api.js";
import { renderEmbedElement } from "/static/js/file_embeds.js";
import {
  getRuleInfo,
  getRuleFiles,
  getRuleExemptions,
} from "/static/js/rules.js";
import { getAllKnownTagsFromMetadata } from "./tags.js";

const PARAM_FILE_ID = "file";

export const QUEUE_RULE = "rule";
export const QUEUE_EXEMPTIONS = "rule exemptions";

export default class FileViewState {
  constructor() {
    this.actionList = new ActionList("actions_container", this);
    this.tagList = new TagList("tags_container");
    this.fileEmbedContainer = document.getElementById("file_embed_container");
    this.elemDirectDownload = document.getElementById("direct_download");
    this.elemFileTitle = document.getElementById("file_title");
    this.elemRuleHeader = document.getElementById("rule_header");
    this.elemRuleNote = document.getElementById("rule_note");
    this.elemRuleContainer = document.getElementById("rule_container");
    this.elemRulePageLink = document.getElementById("rule_page_link");

    this.pendingMetadataRedownload = true;
    this.pendingFileQueueRedownload = true;

    this.pendingFileId = null;
    this.fileId = null;
    this.fileMetadata = null;
    this.fileTags = [];

    this.pendingRuleName = null;
    this.ruleName = null;
    this.ruleInfo = null;
    this.currentRuleActions = null;

    this.fileQueue = null;
    this.fileQueuePosition = 0;
    this.fileQueueStrategy = null;

    this.pendingTagService = null;
    this.tagService = null;

    this.useRuleExemptions = false;
  }

  getFileId() {
    return this.fileId;
  }

  getFileTitle() {
    var fileId = this.getFileId();
    if (fileId == null) {
      return null;
    }
    return "File #" + this.getFileId();
  }

  getFileMetadata() {
    return this.fileMetadata;
  }

  getFileLocation() {
    var metadata = this.getFileMetadata();
    if (metadata != null) {
      if (metadata.is_trashed) {
        return "trash";
      } else if (metadata.is_inbox) {
        return "inbox";
      } else {
        return "archive";
      }
    }
    return "unknown";
  }

  getFileTags() {
    return getTagsFromMetadata(this.getFileMetadata(), this.getTagService());
  }

  getFileAllKnownTags() {
    return getAllKnownTagsFromMetadata(this.getFileMetadata());
  }

  getFileHasTag(tag) {
    return this.getFileAllKnownTags().indexOf(tag) != -1;
  }

  getFileIsExempt() {
    var ruleInfo = this.getRuleInfo();
    if (ruleInfo == null) {
      return false;
    }
    var exemptTag = ruleInfo.exempt_tag;
    if (exemptTag == null) {
      return false;
    }
    return this.getFileHasTag(exemptTag);
  }

  getRuleName() {
    return this.ruleName;
  }

  getRuleInfo() {
    return this.ruleInfo;
  }

  getRuleNote() {
    var ruleInfo = this.getRuleInfo();
    if (ruleInfo == null) {
      return "(No rule)";
    }
    var note = ruleInfo.note;
    if (note == null) {
      return "(No note)";
    }
    return note;
  }

  getRulePage() {
    return "/rules/" + ruleName;
  }

  getTagService() {
    return this.tagService;
  }

  getFileQueueStrategy() {
    return this.fileQueueStrategy;
  }

  setFileId(fileId) {
    this.pendingFileId = fileId;
  }

  setRuleName(ruleName) {
    this.pendingRuleName = ruleName;
  }

  setTagService(serviceName) {
    this.pendingTagService = serviceName;
  }

  setFileQueueStrategy(strategy) {
    if (strategy !== this.fileQueueStrategy) {
      this.fileQueueStrategy = strategy;
      this.pendingFileQueueRedownload = true;
    }
  }

  async refresh() {
    var tagServiceChanged = false;
    var fileIdChanged = false;
    var ruleNameChanged = false;
    var fileMetadataChanged = false;
    var fileQueueChanged = false;

    if (
      this.pendingTagService != null &&
      this.pendingTagService !== this.tagService
    ) {
      this.tagService = this.pendingTagService;
      tagServiceChanged = true;
    }
    this.pendingTagService = null;

    if (
      this.pendingRuleName != null &&
      this.pendingRuleName !== this.ruleName
    ) {
      this.ruleName = this.pendingRuleName;
      ruleNameChanged = true;
    }
    this.pendingRuleName = null;

    if (this.pendingFileId != null && this.pendingFileId !== this.fileId) {
      this.fileId = this.pendingFileId;
      fileIdChanged = true;
    }
    this.pendingFileId = null;

    if (fileIdChanged || this.pendingMetadataRedownload) {
      this.fileMetadata = await getFileMetadata(this.fileId, true);
      fileMetadataChanged = true;
      this.pendingMetadataRedownload = false;
    }

    if (fileIdChanged) {
      // update the url in case the user refreshes the page
      let params = new URLSearchParams(window.location.search);
      params.set(PARAM_FILE_ID, this.fileId + "");
      window.history.replaceState(null, null, "/file?" + params.toString());
    }

    if (fileMetadataChanged) {
      // update file's title
      this.elemFileTitle.textContent = this.getFileTitle();

      // update direct download link
      this.elemDirectDownload.innerHTML =
        "<span>Direct Download (<code>" +
        this.fileMetadata.mime +
        "</code>)</span>";
      this.elemDirectDownload.href = "/files/full/" + this.fileId;

      // update hash display
      var metadata = this.getFileMetadata();
      var hash = metadata.hash || "?";
      document.getElementById("hash_container").innerText = hash;
    }

    if (fileMetadataChanged || tagServiceChanged) {
      this.tagList.setTags(this.getFileTags());
    }

    if (ruleNameChanged) {
      this.ruleInfo = await getRuleInfo(this.ruleName);

      // hide or show rule container
      if (this.ruleName != null) {
        this.elemRuleContainer.classList.remove("noshow");

        // update link to rule page
        this.elemRulePageLink.href = "/rules/" + this.ruleName;

        this.elemRuleHeader.innerText = "Rule: " + this.ruleName;
        this.elemRuleHeader.style = "";

        this.elemRuleNote.innerText = this.getRuleNote();
      } else {
        this.elemRuleContainer.classList.add("noshow");
      }
    }

    if (fileIdChanged) {
      // update embed
      let fileEmbedElem = renderEmbedElement(this.getFileMetadata());
      this.fileEmbedContainer.innerHTML = null;
      this.fileEmbedContainer.appendChild(fileEmbedElem);
    }

    if (this.pendingFileQueueRedownload || ruleNameChanged) {
      // download the queue
      this.fileQueue = await this.downloadFileQueue();

      // update position in queue
      if (this.fileQueue != null) {
        this.fileQueuePosition = this.fileQueue.indexOf(this.fileId);
        console.log(
          "File queue is " +
            this.fileQueue.length +
            " elements long, we are at index " +
            this.fileQueuePosition
        );
      } else {
        this.fileQueuePosition = -1;
      }

      this.pendingFileQueueRedownload = false;
    }

    if (fileMetadataChanged || ruleNameChanged) {
      await this.actionList.refresh();
    }
  }

  async downloadFileQueue() {
    console.log("downloading file queue...");

    switch (this.fileQueueStrategy) {
      case null:
        return null;
      case QUEUE_RULE:
        return await getRuleFiles(this.ruleName);
      case QUEUE_EXEMPTIONS:
        return await getRuleExemptions(this.ruleName);
      default:
        throw Error(
          "Unknown strategy: '" +
            this.fileQueueStrategy +
            "' (" +
            typeof this.fileQueueStrategy +
            ")"
        );
    }
  }

  renderRulePageLink() {
    var ruleLinkElem = document.createElement("a");
    ruleLinkElem.innerText = "(Rule Page)";
    ruleLinkElem.href = "/rules/" + encodeURI(ruleName);
    return ruleLinkElem;
  }

  moveInFileQueue(motion) {
    if (
      this.fileQueue == null ||
      motion == null ||
      motion == 0 ||
      this.fileQueue.length == 0
    ) {
      return;
    }

    if (this.fileQueuePosition == null || this.fileQueuePosition == -1) {
      this.setFileQueuePosition(0);
    } else {
      this.setFileQueuePosition(this.fileQueuePosition + motion);
    }
  }

  async setFileQueuePosition(position) {
    if (position >= this.fileQueue.length) {
      position = 0;
    } else if (position < 0) {
      position = this.fileQueue.length - 1;
    }

    this.fileQueuePosition = position;
    this.setFileId(this.fileQueue[position]);
    await this.refresh();
  }

  async onShortcut(shortcut) {
    if (shortcut == "shift+r") {
      this.pendingMetadataRedownload = true;
      this.pendingFileQueueRedownload = true;
      await this.refresh();
      return true;
    }

    var actionName = this.actionList.getActionNameFromShortcut(shortcut);
    if (actionName != null) {
      return await this.onAction(actionName);
    }
  }

  /** Returns true if there is a matching action */
  async onAction(actionName) {
    if (actionName == null) {
      return false;
    }

    var actionInfo = this.actionList.getActionInfo(actionName);

    if (actionInfo == null) {
      console.log("no action for: " + actionName, this.fileActions);
      return false;
    }

    this.runAction(actionInfo);
  }

  async runAction(actionInfo) {
    var archetype = actionInfo.archetype;
    var actionName = actionInfo.name;
    var hints = actionInfo.hints;

    if (typeof archetype !== "string") {
      throw Error("not a string: " + archetype);
    }

    var promise;

    switch (archetype.trim().toLowerCase()) {
      case "noop":
        promise = null;
        break;
      case "move_to_trash":
        promise = this.actionMoveToTrash(hints);
        break;
      case "move_to_inbox":
        promise = this.actionMoveToInbox(hints);
        break;
      case "move_to_archive":
        promise = this.actionMoveToArchive(hints);
        break;
      case "quick_add_tag":
        promise = this.actionQuickAddOrDeleteTag(true, hints);
        break;
      case "quick_delete_tag":
        promise = this.actionQuickAddOrDeleteTag(false, hints);
        break;
      case "quick_delete_tag":
        promise = this.actionQuickAddOrDeleteTag(null, hints);
        break;
      case "change_tags":
        promise = this.actionChangeTags(hints);
        break;
      case "move":
        promise = this.actionMoveInQueue(hints);
        break;
      case "mark_as_exempt":
        promise = this.actionMarkAsExempt(hints);
        break;
      case "unmark_as_exempt":
        promise = this.actionUnmarkAsExempt(hints);
        break;
      default:
        throw Error("archetype doesn't exist: " + archetype);
    }

    var viewState = this;

    if (promise == null) {
      promise = Promise.resolve(null);
    }

    promise
      .then((x) => {
        if (actionInfo.resolves) {
          viewState.moveInFileQueue(1);
        }
      })
      .catch((err) => {
        console.error(err);
        alert(
          "Execution of '" +
            actionName +
            "' failed: " +
            err +
            ". Please open the console, expand the error, and screenshot as much as you can. Thank you :)"
        );
      });
  }

  async changeTags(addTags, rmTags) {
    return await httpPostJson("/api/files/change_tags", {
      tag_service: this.getTagService(),
      file_ids: this.getFileId(),
      add_tags: addTags,
      rm_tags: rmTags,
    })
      .then(this.redownloadFileMetadata.bind(this))
      .catch((e) => {
        alert(
          "Failed to change tags: " +
            e +
            ", please check the console, expand the error, and screenshot as much as you can."
        );
        console.error(e);
      });
  }

  async redownloadFileMetadata() {
    this.pendingMetadataRedownload = true;
    await this.refresh();
  }

  actionMoveToTrash() {
    return httpPostJson("/api/files/move_to_trash", {
      file_ids: this.getFileId(),
    }).then(this.redownloadFileMetadata.bind(this));
  }

  actionMoveToInbox() {
    return httpPostJson("/api/files/move_to_inbox", {
      file_ids: this.getFileId(),
    }).then(this.redownloadFileMetadata.bind(this));
  }

  actionMoveToArchive() {
    return httpPostJson("/api/files/move_to_archive", {
      file_ids: this.getFileId(),
    }).then(this.redownloadFileMetadata.bind(this));
  }

  actionQuickAddOrDeleteTag(add, hints) {
    if (hints == null) {
      hints = {};
    }

    if (add == null) {
      if (hints.prompt_add == null) {
        throw new Error("add or remove not specified :(");
      }
      add = !!hints.prompt_add;
    }

    if (add) {
      var message =
        "Please enter a tag to add to the file. The tag will be added to '" +
        this.getTagService() +
        "'";
    } else {
      var message =
        "Please enter a tag to remove from the file. The tag will be removed from '" +
        this.getTagService() +
        "'";
    }

    var defaultTag = hints.default_tag != null ? hints.default_tag + "" : "";

    var tag = prompt(message, defaultTag);

    if (tag != null && tag != "") {
      var addTags = [];
      var rmTags = [];

      if (add) {
        addTags.push(tag);
      } else {
        rmTags.push(tag);
      }

      if (hints.add_tags != null) {
        addTags = addTags.concat(hints.add_tags);
      }
      if (hints.rm_tags != null) {
        rmTags = rmTags.concat(hints.rm_tags);
      }

      return this.changeTags(addTags, rmTags);
    }
  }

  actionChangeTags(hints) {
    return this.changeTags(hints.add_tags, hints.rm_tags);
  }

  actionMoveInQueue(hints) {
    let movement = hints.movement || 1;
    return this.moveInFileQueue(movement);
  }

  actionMarkAsExempt() {
    var rule = this.getRuleInfo();
    if (rule != null) {
      return this.changeTags([rule.exempt_tag], null);
    } else {
      alert(
        "cannot mark as an exception because there is no rule in the current context"
      );
    }
  }

  actionUnmarkAsExempt() {
    var rule = this.getRuleInfo();
    if (rule != null) {
      return this.changeTags(null, [rule.exempt_tag]);
    } else {
      alert(
        "cannot unmark as an exception because there is no rule in the current context"
      );
    }
  }
}
