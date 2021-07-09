async function asyncPrompt(promptText, defaultValue) {
  return new Promise((resolve, reject) => {
    ret = prompt(promptText, defaultValue);
    if (ret != null) {
      resolve(ret);
    } else {
      reject("User provided no input");
    }
  });
}

async function asyncAlert(promptText) {
  return new Promise(resolve => {
    alert(promptText);
    resolve();
  });
}

async function asyncConfirm(promptText) {
  return new Promise(resolve => {
    if (confirm(promptText)) {
      resolve();
    } else {
      reject("User did not confirm");
    }
  });
}

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
    xmlHttp.send(); // no body for GET
  });
}

async function httpGETJSON(url) {
  return httpGET(url).then(JSON.parse);
}