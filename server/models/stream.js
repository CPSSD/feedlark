/**
 * stream
 *
 * @description :: Basic model for referencing the Good-to-Go aggregated feeds
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

import {transaction, findOne} from "../middleware/db";

// Gets all the feeds of the current user
export getFeeds function (username, cb) {
  transaction(db => findOne(db, "g2g", {"username": username}, data => cb(data.feeds)));
}
