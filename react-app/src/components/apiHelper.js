var baseURL = process.env.REACT_APP_API_BASE_URL || "/api/";

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
  return fetchJson("server/get_info");
}

async function getRuleNames() {
  return fetchJson("rules/get_all_names");
}

async function getRuleInfo(name) {
  return await fetchJson("rules/get_info?name=" + name);
}

async function getRuleFiles(name) {
  return await fetchJson("rules/get_files?name=" + name);
}

module.exports = {
  getUrl,
  fetchJson,
  getServerInfo,
  getRuleNames,
  getRuleInfo,
  getRuleFiles,
};
