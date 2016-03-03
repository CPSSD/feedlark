/**
 * streams
 *
 * @description :: Displays feeds from the G2G Database
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

const getFeeds = require("../models/stream").getFeeds;

// Stream listing
module.exports = {
  index: (req, res) => {
    getFeeds(req.session.username, feeds => res.render("stream_index", {feeds: feeds}));
  }
};
