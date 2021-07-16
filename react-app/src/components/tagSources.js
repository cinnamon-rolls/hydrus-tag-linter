function statusString(status) {
  status = status + "";
  switch (status) {
    case "0":
      return "current";
    case "1":
      return "pending";
    case "2":
      return "deleted";
    case "3":
      return "petitioned";
    default:
      return "unknown (" + status + ")";
  }
}

function createSource(hydrus_statuses_to_tags) {
  var ret = {};

  for (var status of Object.keys(hydrus_statuses_to_tags)) {
    var myStatus = statusString(status);
    ret[myStatus] = hydrus_statuses_to_tags[status];
  }

  return {};
}

function getAllSourcesFromMetadata(metadata) {
  if (metadata == null) {
    return {};
  }
  var ret = {};

  var sntstdt = metadata["service_names_to_statuses_to_display_tags"];
  if (sntstdt != null) {
    for (var service_name of Object.keys(sntstdt)) {
      var sourceName = service_name + " (display)";
      ret[sourceName] = createSource(sntstdt[service_name]);
    }
  }

  var sntstt = metadata["service_names_to_statuses_to_tags"];
  if (sntstt != null) {
    for (service_name of Object.keys(sntstt)) {
      sourceName = service_name + " (raw)";
      ret[sourceName] = createSource(sntstdt[service_name]);
    }
  }

  return ret;
}

module.exports = {
  getAllSourcesFromMetadata,
};
