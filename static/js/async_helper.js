async function httpGET(url) {
  return new Promise((resolve, reject) => {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
      if (xmlHttp.readyState == 4) {
        var status = xmlHttp.status;
        if (status >= 200 && status <= 200) {
          resolve(xmlHttp.responseText);
        } else {
          reject(xmlHttp.responseText);
        }
      }
    };
    xmlHttp.open("GET", url, true);
    console.log('GET', url)
    xmlHttp.send(); // no body for GET
  });
}

async function httpGETJSON(url) {
  return httpGET(url).then(JSON.parse);
}
