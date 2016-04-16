/**
 * feeds
 *
 * @description :: Server-side logic for managing bookmarks
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

const bookmarkModel = require("../models/bookmark");
const _ = require("lodash");

module.exports = {
  bookmarks: (req, res) => {

    // Get & verify the page length & number
    // This Lo-Dash function is lovely
    var page_length = _.toSafeInteger(req.query.page_length);
    if (page_length <= 0) {
      page_length = 20; // Default Page Length = 20
    }
    var page = _.toSafeInteger(req.query.page); // defaults to 0 if undefined

    // Sort out the filters
    var keywords = [];
    if (typeof req.query.keywords != "undefined" && req.query.keywords.length > 1) {
      keywords = req.query.keywords.split(" ").map(val => val.toLowerCase());
    }

    bookmarkModel.getBookmarks(req.session.username, bookmarks => {

      // Filter the bookmarks
      var filtered_bookmarks = bookmarks.filter((feed, index, src) => {

        // Match with the filters
        return (typeof req.query.source == "undefined" || req.query.source.length < 1 || feed.feed == req.query.source) &&
               (keywords.length < 1 || keywords.every(val => feed.name.toLowerCase().includes(val)));
      });

      // Make sure the page number is less than the max available feeds
      while (page > filtered_bookmarks / page_length) page -= 1;

      // Take a page worth of bookmarks
      var pageinated_bookmarks = _.slice(filtered_bookmarks, page*page_length, (page+1)*page_length);

      var next_page = page + 1;
      if (next_page * page_length > filtered_bookmarks.length) next_page = 0;

      res.status(200).render("bookmark_index", {
        bookmarks: pageinated_bookmarks,
        page: page,
        next_page: next_page,
        page_length: page_length,
        subscribed_feeds: req.session.subscribed_feeds || {},
        keywords: req.query.keywords || "",
        source: req.query.source || ""
      });
    });
  },

  addbk: (req, res) => {
      if (! (_.isString(req.body.url)) ) {
        return res.status(403).send("Invalid URL provided, oops!");
      }
    var url = req.body.url;
    var named = req.body.named;
    var date = req.body.date;
    var feed = req.body.feed;


    // Add to current user
    bookmarkModel.addBookmark(req.session.username, url, named, date, feed, bookmarks => {
      // Post message to stream
      req.session.bookmarks = bookmarks;
      return res.status(200).send("Added to your Bookmarks");
    });
  },

  removebk: (req, res) => {

    // Only need to remove from user, for now
    // TODO clean up no longer relevant feeds from the feed collection

    if (! (_.isString(req.body.url)) ) {
      return res.status(403).send("Invalid URL provided, oops!");
    }
    var url = req.body.url.toLowerCase();

    bookmarkModel.removeBookmark(req.session.username, url, bookmarks => {
      // Post message to stream
      req.session.bookmarks = bookmarks;
      return res.status(200).send("Bookmark removed");
    });
  }
};
