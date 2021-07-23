import ApiCache from "./ApiCache.js";
import { httpGetJson } from "./http_helper.js";

const RULE_FILES_CACHE = new ApiCache(async (name) =>
  httpGetJson("/api/rules/get_files?name=" + name)
);

const RULE_FILES_COUNT_CACHE = new ApiCache(async (name) =>
  httpGetJson("/api/rules/get_files_count?name=" + name)
);

const RULE_EXEMPTIONS_CACHE = new ApiCache(
  async (name) => await httpGetJson("/api/rules/get_exemptions?name=" + name)
);

const RULE_EXEMPTIONS_COUNT_CACHE = new ApiCache(
  async (name) =>
    await httpGetJson("/api/rules/get_exemptions_count?name=" + name)
);

const RULE_ACTIONS_CACHE = new ApiCache(
  async (name) => await httpGetJson("/api/rules/get_actions?name=" + name)
);

export async function getRuleInfo(ruleName = null, options = {}) {
  var query = "?";
  if (ruleName != null) {
    query += "names=" + JSON.stringify(ruleName);
  } else {
    query += "all=true";
  }
  if (options.includeFileCount) {
    query += "&include_file_count=true";
  }
  if (options.includeExemptionCount) {
    query += "&include_exemption_count=true";
  }
  return httpGetJson("/api/rules/get_info" + query);
}

export async function getRuleFiles(ruleName) {
  return RULE_FILES_CACHE.get(ruleName);
}

export async function getRuleFileCount(ruleName) {
  return await RULE_FILES_COUNT_CACHE.get(ruleName);
}

export async function getRuleExemptions(ruleName) {
  return RULE_EXEMPTIONS_CACHE.get(ruleName);
}

export async function getRuleExemptionsCount(ruleName) {
  return RULE_EXEMPTIONS_COUNT_CACHE.get(ruleName);
}

export async function getRuleActions(ruleName) {
  return RULE_ACTIONS_CACHE.get(ruleName);
}

export async function getRuleNames() {
  return await httpGetJson("/api/rules/get_rule_names");
}
