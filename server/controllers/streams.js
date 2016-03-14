/**
 * streams
 *
 * @description :: Displays feeds from the G2G Database
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

const getFeeds = require("../models/stream").getFeeds;
const _ = require("lodash");

// Stream listing
module.exports = {
  index: (req, res) => {

    // Get & verify the page length & number
    // This Lo-Dash function is lovely
    var page_length = _.toSafeInteger(req.query.page_length);
    if (page_length <= 0) {
      page_length = 20; // Default Page Length = 20
    }
    var page = _.toSafeInteger(req.query.page); // defaults to 0 if undefined

    getFeeds(req.session.username, feeds => {

      // Get a page worth of feeds
      var pageinated_feeds = _.slice(feeds, page*page_length, (page+1)*page_length);
      var next_page = page + 1;
      if ((page + 1) * page_length > feeds.length) next_page = 0;

      res.status(200).render("stream_index", {
        feeds: pageinated_feeds,
        page: page,
        next_page: next_page,
        page_length: page_length
      });
    });
  },

  plaintext: (req, res) => {
    var page_length = _.toSafeInteger(req.query.page_length);
    if (page_length <= 0) {
      page_length = 20; // Default Page Length = 20
    }
    var page = _.toSafeInteger(req.query.page);


    var username = req.query.username;
    res.type('.txt');

    getFeeds(username, feeds => {

      var pageinated_feeds = _.slice(feeds, page*page_length, (page+1)*page_length);
      var next_page = page + 1;
      if ((page + 1) * page_length > feeds.length) next_page = 0;

      res.status(200).render("stream_plaintext", {
        feeds: pageinated_feeds,
        page: page,
        next_page: next_page,
        page_length: page_length
      });
    });
  }
};
