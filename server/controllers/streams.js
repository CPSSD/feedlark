/**
 * streams
 *
 * @description :: Displays feeds from the G2G Database
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

const getFeeds = require("../models/stream").getFeeds;
const _ = require("lodash");
const page_length = 20;

// Stream listing
module.exports = {
  index: (req, res) => {

    // Get & verify the page number
    // This Lo-Dash function is lovely
    var page = _.toSafeInteger(req.params.page);

    getFeeds(req.session.username, feeds => {

      // Get a page worth of feeds
      var pageinated_feeds = [];
      for (var i = page * page_length; i <= (page + 1) * page_length && i < feeds.length; i++) {
        pageinated_feeds.push(feeds[i]);
      }

      // Work out the next page number now, because Lo-Dash sorted out the param already
      var next_page = page + 1;
      if ((page + 1) * page_length > feeds.length) next_page = 0;

      res.status(200).render("stream_index", {feeds: pageinated_feeds, page: next_page});
    });
  }
};
