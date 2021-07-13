async function httpGet(url) {
  return new Promise((resolve, reject) => {
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
    xmlHttp.open("GET", url, true);
    xmlHttp.onerror = reject;
    console.log("GET", url);
    xmlHttp.send(); // no body for GET
  });
}

async function httpGetJson(url) {
  return httpGet(url).then(JSON.parse);
}

async function httpPostJson(url, body) {
  return new Promise((resolve, reject) => {
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
    xmlHttp.open("POST", url, true);
    xmlHttp.onerror = reject;
    xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    console.log("POST", url);
    xmlHttp.send(JSON.stringify(body));
  });
}
