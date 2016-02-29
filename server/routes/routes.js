// All routing
// I've opted for a single file approach as this means that things
//  like express and the auth middleware aren't imported N times

import express from "express";
import { isAuthed } from "../middleware/auth";
import userController from "../controllers/users";
import feedController from "../controllers/feeds";
import streamController from "../controllers/streams";

// Router
module.exports = express().route("/")

  // Home/Index
  .get((req, res) => { res.render('index'); })

  // Stream
  .get("/stream", streamController.index)

// User pages

  // Profile
  .get("/user", isAuthed, (req, res) => { res.render("profile"); })

  // Logout
  .all("/user/logout", userController.logout)

  // Signup
  .get("/user/signup", (req, res) => { res.render("signup"); })

  // Login processing
  .post("/user/login", userController.login)

  // Login form
  .get("/user/login", (req, res) => {

    // Go to profile if user is already logged in
    if (typeof req.session.username != "undefined") return res.redirect(200, "/user/profile");

    res.render("login");
  })

// Feeds pages

  // List
  // TODO need to generate/get this list from the database
  .get("/feeds", isAuthed, (req, res) => { res.render("feed_index"); })

  // Add
  .get("/feeds/add", isAuthed, (req, res) => { res.render("feed_add"); })

  // Add processing
  .post("/feeds/add", isAuthed, feedController.add)

  // Remove processing
  // NOTE Last one needs the semicolon
  .get("/feeds/remove", isAuthed, feedController.remove);
