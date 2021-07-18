const LOGGING = false;

export default class ApiCache {
  constructor(fetchFunc, timeInMemory = 10000) {
    this.fetchFunc = fetchFunc;
    this.timeInMemory = timeInMemory;
    this.memory = {};
    this.memoryTime = {};

    if (typeof fetchFunc !== "function") {
      throw new Error("Expected a nonnull async fetch function");
    }
    if (typeof timeInMemory !== "number") {
      throw new Error("Expected timeInMemory as a number in milliseconds");
    }
  }

  /** Fetches the response regardless of the state of memory, then saves it */
  async fetch(key) {
    if (LOGGING) {
      console.log("CACHE: fetch('" + key + "')");
    }
    var fetched = await this.fetchFunc(key);
    return this.save(key, fetched);
  }

  /** Gets the response from memory, or calls fetch() if its absent/expired */
  async get(key, force) {
    key = key + "";
    if (LOGGING) {
      console.log("CACHE: get('" + key + "', force=" + force + ")");
    }

    if (!force) {
      let recalled = this.recall(key);
      if (recalled != null) {
        return recalled;
      }
    }
    return await this.fetch(key);
  }

  /** Returns the remembered object if its saved and not expired, or null */
  recall(key) {
    if (LOGGING) {
      console.log("CACHE: recall('" + key + "')");
    }

    var now = new Date().getTime();
    var fetchedAt = this.memoryTime[key];

    var stillValid = false;
    if (fetchedAt != null) {
      var expiryTime = this.memoryTime[key] + this.timeInMemory;
      stillValid = expiryTime > now;
    }

    if (!stillValid) {
      if (LOGGING) {
        console.log(
          "CACHE: Gone stale! Expired " + (now - expiryTime) + "ms ago"
        );
      }
      return null;
    }
    return this.memory[key];
  }

  /** Overwrites the item at that cache */
  save(key, value, time) {
    if (time == null) {
      time = new Date().getTime();
    }
    this.memory[key] = value;
    this.memoryTime[key] = time;
    return value;
  }
}
