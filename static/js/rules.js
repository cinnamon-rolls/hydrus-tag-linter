import ApiCache from "./ApiCache.js";
import { httpGetJson } from "./http_helper.js";

const RULE_INFO_CACHE = new ApiCache(async (name) =>
  httpGetJson("/api/rules/get_info?name=" + name)
);

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

export async function getRuleInfo(ruleName) {
  return RULE_INFO_CACHE.get(ruleName);
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

export async function getRuleNames() {
  return await httpGetJson("/api/rules/get_rule_names");
}
