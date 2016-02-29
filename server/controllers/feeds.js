/**
 * feeds
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

import { addFeed, removeFeed } from "../models/user";
import { create, remove } from "../models/feed";

export add function (req, res) {

  // TODO sanitise url
  let url = req.body.url.toLowerCase();

  // Add to feed DB
  // I'm doing this a weird way so it only makes one DB connection
  create(url, db => {

    // Add to current user
    addFeed(db, req.session.username, url, _ => {

      // Return to feed manager page
      req.session.msg = "Successfully added feed!";
      return res.redirect(200, "/feeds");
    });
  });
}

export remove function (req, res) {

  // Only need to remove from user, for now
  // TODO clean up no longer relevant feeds from the feed collection

  // TODO sanitise url
  let url = req.params.url.toLowerCase();

  removeFeed(url, req.session.username, url, _ => {

    // Return to feed manager page
    req.session.msg = "Successfully removed feed!";
    return res.redirect(200, "/feeds");
  });
}
