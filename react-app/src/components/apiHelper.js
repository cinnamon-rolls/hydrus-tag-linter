var baseURL = process.env.REACT_APP_API_BASE_URL || "/";

console.log("API Base URL: " + baseURL);

/**
 * Given a path as a string, puts the API's base URL in front of it
 */
function getUrl(path) {
  return baseURL + path;
}

async function fetchJson(path) {
  var url = getUrl(path);
  return fetch(url)
    .then((x) => x.json())
    .catch((x) => {
      console.log("Error parsing JSON from '" + url + "'", x);
      return null;
    });
}

async function getServerInfo() {
  return fetchJson("api/server/get_info");
}

async function getRuleNames() {
  return fetchJson("api/rules/get_all_names");
}

async function getRuleInfo(name) {
  return await fetchJson("api/rules/get_info?name=" + name);
}

async function getRuleFiles(name) {
  return await fetchJson("api/rules/get_files?name=" + name);
}

async function getFileMetadata(fileIDs) {
  return await fetchJson("api/files/get_metadata?file_id=" + fileIDs);
}

async function getServices() {
  return await fetchJson("api/services/get_services");
}

function getThumbnailUrl(fileID) {
  return getUrl("files/thumbnail/" + fileID);
}

function getFileUrl(fileID) {
  return getUrl("files/full/" + fileID);
}

module.exports = {
  getUrl,
  fetchJson,
  getServerInfo,
  getRuleNames,
  getRuleInfo,
  getRuleFiles,
  getFileMetadata,
  getServices,
  getThumbnailUrl,
  getFileUrl,
};
