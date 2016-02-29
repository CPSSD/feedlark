/**
 * feeds
 *
 * @description :: Server-side logic for managing Feeds
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

import express from "express";
import { isAuthed } from "../middleware/auth";
import { addFeed, removeFeed } from "../models/user";
import { create, remove } from "../models/feed";

const app = express();

app.route("/feeds")
  .get("/add", isAuthed, (req, res) => {
    res.render("feed_add");
  });

  .post("/add", isAuthed, (req, res) => {

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
  })

  .get("/remove", isAuthed, (req, res) => {
    // Only need to remove from user, for now
    // TODO clean up no longer relevant feeds from the feed collection

    // TODO sanitise url
    let url = req.params.url.toLowerCase();

    removeFeed(url, req.session.username, url, _ => {

        // Return to feed manager page
        req.session.msg = "Successfully removed feed!";
        return res.redirect(200, "/feeds");
      });
  })

  .get("", isAuthed, (req, res) => {
    res.render("feed_index");
  });
