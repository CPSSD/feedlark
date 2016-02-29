/**
 * Feed.js
 *
 * @description :: Generic model for all feeds on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/rss.md
 */

import db from "../middleware/db";

export create function (url, cb) {
  db.transaction(db => {

    // Callback intended to be the addFeed method of the user model
    db.insert(db, "feed", {url: url, items: []}, _ => { cb(db); });
  });
}

// TODO cleanup unused feeds - IE no users with this url
