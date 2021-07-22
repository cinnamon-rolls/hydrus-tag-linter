import ApiCache from "./ApiCache.js";
import { httpGetJson } from "./http_helper.js";

const GLOBAL_FILE_ACTIONS_CACHE = new ApiCache(async () => {
  return await httpGetJson("/api/server/get_global_file_actions");
});

export async function getGlobalFileActions() {
  return await GLOBAL_FILE_ACTIONS_CACHE.get("singleton");
}
