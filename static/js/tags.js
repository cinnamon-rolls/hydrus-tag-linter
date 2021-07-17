import { getFileMetadata, getServices } from "./api.js";

export const STATUS_CURRENT = "0";
export const STATUS_PENDING = "1";
export const STATUS_DELETED = "2";
export const STATUS_PETITIONED = "3";

const TAG_SERVICE_CATEGORIES = [
  "local_tags",
  "tag_repositories",
  "all_known_tags",
];

export async function getTagServices() {
  var services = getServices();
  var ret = [];

  for (category of TAG_SERVICE_CATEGORIES) {
    for (service of services[category] || []) {
      let serviceObj = Object.assign({}, service);
      serviceObj.category = category;

      if (service.category.replace("_", " ") == service.name) {
        serviceObj.userString = service.name;
      } else {
        serviceObj.userString = service.name + " (" + service.category + ")";
      }

      ret.push(serviceObj);
    }
  }

  return ret;
}

export async function getTags(
  fileId,
  serviceName,
  status = STATUS_CURRENT,
  display = true
) {
  var metadata = await getFileMetadata(fileId);

  var lookup = display
    ? "service_names_to_statuses_to_display_tags"
    : "service_names_to_statuses_to_tags";

  // very defensive against null values because i've been burned by unexpected
  // nulls related to this api path too many times

  var serviceNamesToStatusesToTags = metadata[lookup];
  if (serviceNamesToStatusesToTags == null) {
    return [];
  }

  var statusesToTags = serviceNamesToStatusesToTags[serviceName];
  if (statusesToTags == null) {
    return [];
  }

  var tags = statusesToTags[status];
  if (tags == null) {
    return [];
  }

  return tags;
}
