/**
 * users
 *
 * @description :: Server-side logic for managing users.
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

import express from "express";
import { compare, hash } from "bcrypt-nodejs";
import { isAuthed } from "../middleware/auth";
import { findByEmail, exists, create } from "../models/user";

const app = express();

app.route("/user")

  // Profile page
  .get("/profile", isAuthed, (req, res) => { res.render("profile"); })

  // Login form
  .get("/login", (req, res) => {

    // Go to profile page if user is already logged in
    if (typeof req.session.username != "undefined") return res.redirect(200, "/user/profile");

    return res.render("login");
  })

  // Login processing
  .post("/login", (req, res) => {

    // Load request vars & verify
    let email = req.body.email;
    let password = req.body.password;
    if (!_.isString(email) || !_.isString(password)) return res.status(400).render("login", {err: "Invalid email/password combination."});

    // Get the user's details from the DB
    findByEmail(email, user => {

      // Is the user name valid? (DB query returns nothing if not)
      if (typeof user == "undefined") return res.status(400).render("login", {err: "Invalid email/password combination."});

        // Check their password
        bcrypt.compare(password, user.password, function(err, valid) {
          if (!valid) return res.status(400).render("login", {err: "Invalid email/password combination."});

          // Set session vars and redirect
          // TODO Setup session
          req.session.username = user.username;
          req.session.msg = "Successfully logged in.";
          return res.redirect(200, "/user/profile");
        });
    });
  })

  // Logout processing
  .all("/logout", (req, res) => {
    // TODO Destroy the session
    res.render("logout");
  })

  // Signup page
  .get("/signup", (req, res) => { res.render("signup") })

  // Signup processing
  .post("/signup", (req, res) => {

    // Import things & load request vars
    let email = req.body.email;
    let password = req.body.password;
    let username = req.body.username;

    // Verify these details
    if (!_.isString(email) || !_.isString(password) || !_.isString(username)) return res.status(400).render("signup", {err: "Invalid input data"});
    if (email.length < 5) return res.status(400).render("signup", {err: "Email Address too short."});
    if (password.length < 8) return res.status(400).render("signup", {err: "Password too short."});
    if (username.length < 4) return res.status(400).render("signup", {err: "Username too short."});

    // Add new user to the database
    // TODO Create blank g2g entry
    create(username, email, password, _ => {

      // Log the user in
      // TODO Setup session
      req.session.username = username;
      req.session.msg = "Signup successful. Welcome!";
      return redirect(req, res, "/user/profile");
    });
  });
