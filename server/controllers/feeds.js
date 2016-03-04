/**
 * feeds
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

const userModel = require("../models/user");
const feedModel = require("../models/feed");

module.exports = {

  index: (req, res) => {

    // Get all subscribed feeds from the db
    userModel.findByUsername(req.session.username, (data) => {
      return res.status(200).render("feeds_index", {subscribed_feeds: data.subscribed_feeds});
    });
  },

  add: (req, res) => {

    // TODO sanitise url
    var url = req.body.url.toLowerCase();

    // Add to feed DB
    // I'm doing this a weird way so it only makes one DB connection
    feedModel.create(url, db => {

      // Add to current user
      userModel.addFeed(db, req.session.username, url, _ => {

        // Return to feed manager page
        req.session.msg = "Successfully added feed!";
        return res.redirect(302, "/feeds");
      });
    });
  },

  remove: (req, res) => {

    // Only need to remove from user, for now
    // TODO clean up no longer relevant feeds from the feed collection

    // TODO sanitise url
    var url = req.query.url.toLowerCase();

    userModel.removeFeed(req.session.username, url, _ => {

      // Return to feed manager page
      req.session.msg = "Successfully removed feed!";
      return res.redirect(302, "/feeds");
    });
  }
};
