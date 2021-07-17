function newClient(resolve, reject) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState == 4) {
      var status = xmlHttp.status;
      if (status >= 200 && status <= 299) {
        resolve(xmlHttp.responseText);
      } else {
        reject(xmlHttp.responseText);
      }
    }
  };
  xmlHttp.onerror = reject;
  return xmlHttp;
}

async function httpGet(url) {
  return new Promise((resolve, reject) => {
    var xmlHttp = newClient(resolve, reject);
    xmlHttp.open("GET", url, true);
    console.log("GET", url);
    xmlHttp.send();
  });
}

async function httpGetJson(url) {
  return httpGet(url).then(JSON.parse);
}

async function httpPostJson(url, body) {
  return new Promise((resolve, reject) => {
    var xmlHttp = newClient(resolve, reject);
    xmlHttp.open("POST", url, true);
    console.log("POST", url);
    xmlHttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    xmlHttp.send(JSON.stringify(body));
  });
}

export { httpGet, httpGetJson, httpPostJson };
