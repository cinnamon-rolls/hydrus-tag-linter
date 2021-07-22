"use strict";

import { getGlobalFileActions } from "./actions.js";
import { getRuleActions } from "./rules.js";
import Component from "./Component.js";

const AUTO_SHORTCUTS = "qwertyuiop".split("");

const PFX_DIVIDER = "divider:";

const PFX_ACTION = "action:";
const PFX_GLOBAL_ACTION = PFX_ACTION + "global:";
const PFX_LOCAL_ACTION = PFX_ACTION + "local:";

const GLOBAL_ACTION_NAMES = [];

const actionInfoCache = {};

var downloadedGlobalActions = false;

function getActionInfo(key) {
  return actionInfoCache[key];
}

function setActionInfo(key, info) {
  actionInfoCache[key] = info;
}

async function downloadGlobalFileActions() {
  if (downloadedGlobalActions) {
    return;
  }
  var actions = await getGlobalFileActions();
  for (let action of actions) {
    let key = PFX_GLOBAL_ACTION + action.name;
    setActionInfo(key, action);
    GLOBAL_ACTION_NAMES.push(key);
  }
  downloadedGlobalActions = true;
  return GLOBAL_ACTION_NAMES;
}

function renderDivider(name) {
  var elem = document.createElement("br");
  return elem;
}

export default class ActionList extends Component {
  constructor(container, fileViewState) {
    super(
      container,
      (x) => this.renderElement(x),
      (a, b) => this.updateElement(a, b)
    );
    this.container.classList.add("action_list");
    this.fileViewState = fileViewState;

    this.fileActions = {};
    this.shortcutsToActionNames = {};
  }

  async refresh() {
    await downloadGlobalFileActions();

    if (this.fileViewState == null) {
      console.error("Can't do much without a parent FileViewState :(");
      return;
    }

    var names = [];
    names = names.concat(GLOBAL_ACTION_NAMES);

    var ruleName = this.fileViewState.getRuleName();
    if (ruleName != null) {
      let ruleActions = await getRuleActions(ruleName);

      if (ruleActions != null && ruleActions.length > 0) {
        names.push(PFX_DIVIDER + "1");

        for (let action of ruleActions) {
          let actionEffectiveName = PFX_LOCAL_ACTION + action.name;
          actionInfoCache[actionEffectiveName] = action;
          names.push(actionEffectiveName);
        }
      }
    }

    this.reorder(names);
  }

  renderElement(name) {
    if (name.startsWith(PFX_DIVIDER)) {
      return renderDivider(name);
    } else if (name.startsWith(PFX_ACTION)) {
      return this.renderAction(name);
    } else {
      console.error("What is this element name? '" + name + "'");
      return null;
    }
  }

  updateElement(name, elem) {
    if (name.startsWith(PFX_ACTION)) {
      this.updateAction(name, elem);
    }
  }

  renderAction(actionName) {
    var action = getActionInfo(actionName);

    if (action == null) {
      console.error(
        "Could not get action info for action '" + actionName + "'"
      );
      return null;
    }

    this.fileActions[action.name] = action;

    if (action.shortcut != null) {
      var shortcut = action.shortcut.trim().toLowerCase();

      if (shortcut == "auto") {
        shortcut = null;
        for (var i = 0; i < AUTO_SHORTCUTS.length && shortcut == null; i++) {
          let autoShortcut = AUTO_SHORTCUTS[i];
          if (this.shortcutsToActionNames[autoShortcut] == null) {
            shortcut = autoShortcut;
          }
        }
      }

      this.shortcutsToActionNames[shortcut] = action.name;
      action.shortcut = shortcut;
    }

    var elem = this.renderActionButton(action);

    return elem;
  }

  updateAction(actionName, elem) {
    var action = getActionInfo(actionName);

    if (action == null) {
      return;
    }

    var fileLocation = this.fileViewState.getFileLocation();

    var ruleInfo = this.fileViewState.getRuleInfo();
    var exempt = false;

    if (ruleInfo != null) {
      exempt = this.fileViewState.getFileIsExempt();
    }

    var hidden =
      action.hidden ||
      (action.hiddenIfInbox && fileLocation == "inbox") ||
      (action.hiddenIfArchive && fileLocation == "archive") ||
      (action.hiddenIfTrash && fileLocation == "trash") ||
      (action.hiddenIfNoRule && ruleInfo == null) ||
      (action.hiddenIfRule && ruleInfo != null) ||
      (action.hiddenIfExempt && exempt) ||
      (action.hiddenIfNotExempt && !exempt);

    if (hidden) {
      elem.classList.add("noshow");
    } else {
      elem.classList.remove("noshow");
    }
  }

  renderActionButton(action) {
    var span = document.createElement("span");
    var innerText = action.name;
    if (action.shortcut != null) {
      innerText += " (" + action.shortcut + ")";
    }
    span.innerText = innerText;
    span.className += "icon_left icon_left_" + action.icon;

    var actionFunc = (x) => this.fileViewState.onAction(x);

    var e = document.createElement("button");
    e.className = "anchorbutton action_button";
    e.appendChild(span);
    e.onclick = async function () {
      await actionFunc(action.name);
    };
    return e;
  }

  getActionInfo(actionName) {
    return this.fileActions[actionName];
  }

  getActionNameFromShortcut(shortcut) {
    return this.shortcutsToActionNames[shortcut];
  }
}
