/**
 * streams
 *
 * @description :: Displays feeds from the G2G Database
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/g2g.md
 */

const getFeeds = require("../models/stream").getFeeds;
const user = require("../controllers/users");
const userModel = require("../models/user");
const _ = require("lodash");

// Stream listing
module.exports = {
  index: (req, res) => {

    // This Lo-Dash function is lovely
    var page_length = _.toSafeInteger(req.query.page_length);
    if (page_length <= 0) {
      page_length = req.session.page_length; // Use the user's default instead
    }

    var page = _.toSafeInteger(req.query.page); // defaults to 0 if undefined
    // Sort out the filters
    var keywords = [];
    if (typeof req.query.keywords != "undefined" && req.query.keywords.length > 1) {
      keywords = req.query.keywords.split(" ").map(val => val.toLowerCase());
    }

    getFeeds(req.session.username, feeds => {

      // Filter the feeds
      var filtered_feeds = feeds.filter((feed, index, src) => {
        // Match with the filters
        return (typeof req.query.source == "undefined" || req.query.source.length < 1 || feed.feed == req.query.source) &&
               (keywords.length < 1 || keywords.every(val => feed.name.toLowerCase().includes(val)));
      });

      // Make sure the page number is less than the max available feeds
      while (page > filtered_feeds / page_length) page -= 1;

      // Take a page worth of feeds
      var pageinated_feeds = _.slice(filtered_feeds, page*page_length, (page+1)*page_length);

      var next_page = page + 1;
      if (next_page * page_length > filtered_feeds.length) next_page = 0;

      res.status(200).render("stream_index", {
        feeds: pageinated_feeds,
        page: page,
        next_page: next_page,
        page_length: page_length,
        subscribed_feeds: req.session.subscribed_feeds || {},
        keywords: req.query.keywords || "",
        source: req.query.source || ""
      });
    });

  },

  plaintext: (req, res) => {
    res.type('.txt');

    // This Lo-Dash function is lovely
    var page_length = _.toSafeInteger(req.query.page_length);
    if (page_length <= 0) {
      page_length = req.session.page_length; // Use the user's default instead
    }

    var page = _.toSafeInteger(req.query.page);
    var username = req.query.username;
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
