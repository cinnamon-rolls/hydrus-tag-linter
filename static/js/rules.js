import ApiCache from "./apiCache.js";
import { httpGetJson } from "./http_helper.js";

const RULE_INFO_CACHE = new ApiCache(async (name) =>
  httpGetJson("/api/rules/get_info?name=" + name)
);

const RULE_FILES_CACHE = new ApiCache(async (name) =>
  httpGetJson("/api/rules/get_files?name=" + name)
);

const RULE_EXEMPTIONS_CACHE = new ApiCache(
  async (name) => await httpGetJson("/api/rules/get_exemptions?name=" + name)
);

export async function getRuleInfo(ruleName) {
  return RULE_INFO_CACHE.get(ruleName);
}

export async function getRuleFiles(ruleName) {
  return RULE_FILES_CACHE.get(ruleName);
}

export async function getRuleFileCount(ruleName) {
  return (await getRuleFiles(ruleName)).length;
}

export async function getRuleExemptions(ruleName) {
  return RULE_EXEMPTIONS_CACHE.get(ruleName);
}

export async function getRuleNames() {
  return await httpGetJson("/api/rules/get_rule_names");
}
