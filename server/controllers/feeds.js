/**
 * feeds
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

const userModel = require("../models/user");
const feedModel = require("../models/feed");
const _ = require("lodash");
const gearman = require("../middleware/gearman");

module.exports = {

  index: (req, res) => {

    // Get all subscribed feeds from the db
    userModel.findByUsername(req.session.username, (data) => {
      return res.status(200).render("feeds_index", {subscribed_feeds: data.subscribed_feeds});
    });
  },

  add: (req, res) => {

    if (!_.isString(req.body.url) || !_.isArray(req.body.url.match(/https?:\/\/[^\/]+/g))) {
      req.session.msg = "Invalid URL provided";
      return res.redirect(302, "/feeds");
    }
    var url = req.body.url.toLowerCase();

    // Add to feed DB
    // I'm doing this a weird way so it only makes one DB connection
    feedModel.create(url, db => {

      // Add to current user
      userModel.addFeed(db, req.session.username, url, subscribed_feeds => {
        // Call gearman
        gearman.startJob('update-single-feed', {"url":url}, undefined, () => {});

        // Return to feed manager page
        req.session.msg = "Successfully added feed!";
        req.session.subscribed_feeds = subscribed_feeds;
        return res.redirect(302, "/feeds");
      });
    });
  },

  remove: (req, res) => {

    // Only need to remove from user, for now
    // TODO clean up no longer relevant feeds from the feed collection

    if (!_.isString(req.query.url) || !_.isArray(req.query.url.match(/https?:\/\/[^\/]+/g))) {
      req.session.msg = "Invalid URL provided";
      return res.redirect(302, "/feeds");
    }
    var url = req.query.url.toLowerCase();

    userModel.removeFeed(req.session.username, url, subscribed_feeds => {

      // Return to feed manager page
      req.session.msg = "Successfully removed feed!";
      req.session.subscribed_feeds = subscribed_feeds;
      return res.redirect(302, "/feeds");
    });
  },

  like: (req, res) => {
	res.type(".txt");

	if (!_.isString(req.query.url) || !_.isArray(req.query.url.match(/https?:\/\/[^\/]+/g))) {
	  return res.status(200).send("Invalid URL provided, oops!");
	}
	var url = req.query.url.toLowerCase();
	var jobData = {
	  "username": req.session.username,
	  "feed_url": req.query.feed.toLowerCase(),
	  "article_url": url,
	  "positive_opinion": true
  	};

    // Call gearman
	try{
      gearman.startJob('update-user-model', jobData, undefined, () => {
		  return res.status(200).send("Showing interest in " + url);
	  });
  	} catch(err){ console.log(err); }
  },

  dislike: (req, res) => {
	res.type(".txt");
    if (!_.isString(req.query.url) || !_.isArray(req.query.url.match(/https?:\/\/[^\/]+/g))) {
	  return res.status(200).send("Invalid URL provided, oops!");
    }

    var url = req.query.url.toLowerCase();
    var jobData = {
      "username": req.session.username,
      "feed_url": req.query.feed.toLowerCase(),
      "article_url": url,
      "positive_opinion": false
    };

    // Call gearman
	try {
      gearman.startJob('update-user-model', jobData, undefined, () => {
		  return res.status(200).send("Showing disinterest in " + url);
	  });
  	} catch(err){ console.log(err); }

  }
};
