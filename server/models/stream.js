/**
 * stream
 *
 * @description :: Basic model for referencing the Good-to-Go aggregated feeds
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

const dbFuncs = require("../middleware/db");

// Gets all the feeds of the current user
module.exports = {
  getFeeds: (username, cb) => {
    dbFuncs.transaction(db => dbFuncs.findOne(db, "g2g", {username: username}, data => cb(data.feeds)));
  }
};
