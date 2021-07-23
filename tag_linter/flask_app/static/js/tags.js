import { getFileMetadata, getServices } from "./api.js";
import ApiCache from "./ApiCache.js";

const TAG_SERVICE_CACHE = new ApiCache(fetchTagServices);

export const STATUS_CURRENT = "0";
export const STATUS_PENDING = "1";
export const STATUS_DELETED = "2";
export const STATUS_PETITIONED = "3";

const TAG_SERVICE_CATEGORIES = [
  "local_tags",
  "tag_repositories",
  "all_known_tags",
];

var allKnownTagsServiceName;

async function fetchTagServices() {
  var services = await getServices();
  var ret = [];

  for (let category of TAG_SERVICE_CATEGORIES) {
    for (let service of services[category] || []) {
      let serviceObj = Object.assign({}, service);
      serviceObj.category = category;

      if (serviceObj.category.replace("_", " ") == service.name) {
        serviceObj.userString = service.name;
      } else {
        serviceObj.userString = service.name + " (" + service.category + ")";
      }

      ret.push(serviceObj);
    }
  }

  return ret;
}

export async function getTagServices() {
  return await TAG_SERVICE_CACHE.get("singleton");
}

async function getAllKnownTagsServiceName() {
  if (allKnownTagsServiceName != null) {
    return allKnownTagsServiceName;
  }

  var services = await getServices();

  var allKnownTagsServices = services["all_known_tags"];
  if (allKnownTagsServices != null && allKnownTagsServices.length > 0) {
    allKnownTagsServiceName = allKnownTagsServices[0].name;
    return allKnownTagsServiceName;
  }

  console.error("What? You don't have an all_known_tags service???");
  return null;
}

export async function getAllKnownTags(
  fileId,
  status = STATUS_CURRENT,
  display = true
) {
  return await getTags(
    fileId,
    await getAllKnownTagsServiceName(),
    status,
    display
  );
}

export async function getTags(
  fileId,
  serviceName,
  status = STATUS_CURRENT,
  display = true
) {
  var metadata = await getFileMetadata(fileId);
  return getTagsFromMetadata(metadata, serviceName, status, display);
}

export function getTagsFromMetadata(
  metadata,
  serviceName,
  status = STATUS_CURRENT,
  display = true
) {
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

export function getAllKnownTagsFromMetadata(
  metadata,
  status = STATUS_CURRENT,
  display = true
) {
  return getTagsFromMetadata(metadata, "all known tags", status, display);
}
