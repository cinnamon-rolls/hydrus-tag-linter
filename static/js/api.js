import { httpGetJson } from "./http_helper.js";
import ApiCache from "./ApiCache.js";

const FILE_METADATA_CACHE = new ApiCache(
  async (fileId) =>
    await httpGetJson("/api/files/get_metadata?file_id=" + fileId)
);

export async function getFileMetadata(fileId, force = false) {
  return FILE_METADATA_CACHE.get(fileId, force);
}

export async function getServices() {
  return await httpGetJson("/api/services/get_services");
}

export async function getServerInfo() {
  return httpGetJson("api/server/get_info");
}

export async function getRuleNames() {
  return httpGetJson("api/rules/get_all_names");
}

export async function getRuleInfo(name) {
  return await httpGetJson("api/rules/get_info?name=" + name);
}

export async function getRuleFiles(name) {
  return await httpGetJson("api/rules/get_files?name=" + name);
}
