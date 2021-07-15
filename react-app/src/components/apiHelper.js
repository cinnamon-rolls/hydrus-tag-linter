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
    .then((x) => {
      console.log("GET from '" + url + "'", x);
      return x;
    })
    .then((x) => x.json())
    .catch((x) => {
      console.log("Error parsing JSON from '" + url + "'", x);
      return null;
    });
}

module.exports = {
  getUrl,
  fetchJson,
};
