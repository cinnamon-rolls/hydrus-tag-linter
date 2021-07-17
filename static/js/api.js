import { httpGetJson } from "./http_helper.js";

// will this get too big?
const metadataCache = {};

export async function getFileMetadata(fileId) {
  const cached = metadataCache[fileId + ""];
  if (cached != null) {
    return cached;
  }

  const metadata = await httpGetJson(
    "/api/files/get_metadata?file_id=" + fileId
  );
  metadataCache[fileId + ""] = metadata;
  return metadata;
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
