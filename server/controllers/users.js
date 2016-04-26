/**
 * users
 *
 * @description :: Server-side logic for managing users.
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

const fs = require("fs");
const _ = require("lodash");
const crypto = require("crypto");
const bcrypt = require("bcrypt-nodejs");
const dbFuncs = require("../middleware/db");
const userModel = require("../models/user");
const streamModel = require("../models/stream");
const recaptcha = require("express-recaptcha");
var tokens = {secret_key: "nope", site_key: "bees"}
if (fs.existsSync("../script/captcha_tokens.js")) {
  tokens = require("../../script/captcha_tokens");
}

module.exports = {
  // Login processing
  login: (req, res) => {

    // Load request vars & verify
    var email = req.body.email;
    var password = req.body.password;
    if (!_.isString(email) || !_.isString(password)) return res.status(400).render("login", {err: "Invalid email/password combination."});

    // Get the user's details from the DB
    userModel.findByEmail(email, user => {

      // Is the user name valid? (DB query returns nothing if not)
      if (typeof user == "undefined") return res.status(400).render("login", {err: "Invalid email/password combination."});

        // Check their password
        bcrypt.compare(password, user.password, (err, valid) => {
          if (!valid) return res.status(400).render("login", {err: "Invalid email/password combination."});

          // Set session vars and redirect
          req.session.username = user.username;
          req.session.subscribed_feeds = user.subscribed_feeds;
          req.session.verified = user.verified;
          req.session.msg = "Successfully logged in.";
          return res.redirect(302, "/");
        });
    });
  },

  // Logout processing
  logout: (req, res) => {
    req.session.destroy();
    res.status(200).render("logout");
  },

  // Signup processing
  signup: (req, res) => {

    // captcha setup
    recaptcha.init(tokens.site_key, tokens.secret_key);

    // Import things & load request vars
    var email = req.body.email;
    var password = req.body.password;
    var username = req.body.username;
    var captcha_html = recaptcha.render();

    // Check if anything actually needs to be done (initial viewing of signup page)
    if (req.method == "GET") return res.status(200).render("signup", {captcha: captcha_html});

    // Verify these details
    if (!_.isString(email) || !_.isString(password) || !_.isString(username)) return res.status(400).render("signup", {err: "Invalid input data.", captcha: captcha_html});
    if (email.length < 5) return res.status(400).render("signup", {err: "Email Address too short.", captcha: captcha_html});
    if (password.length < 8) return res.status(400).render("signup", {err: "Password too short.", captcha: captcha_html});
    if (username.length < 4) return res.status(400).render("signup", {err: "Username too short.", captcha: captcha_html});

    // Check the captcha
    // NodeJS is async hell
    recaptcha.verify(req, err => {
      if (err && process.env.ENVIRONMENT == "PRODUCTION") return res.status(400).render("signup", {err: "Captcha error: " + recaptcha.error, captcha: captcha_html});

      // Check the user doesn't already exist
      userModel.exists(username, email, data => {
        if (data) return res.status(400).render("signup", {err: "Email/Username already taken.", captcha: captcha_html});

        // Generate a verification token
        crypto.randomBytes(32, (err, buf) => {
          if (err) return res.status(500).render("signup", {err: "Failed to generate verification token:" + err, captcha: captcha_html});
          var token = buf.toString("hex");

          // Add new user to the database
          userModel.create(username, email, password, token, _ => {

            // Send verification email
            if (process.env.ENVIRONMENT == "PRODUCTION") {
              res.mailer.send(
                "email_verify",
                {
                  to: email,
                  subject: "Feedlark - Activate your account",
                  token: token
                },
                err => {
                  if (err) return res.status(500).render("signup", {err: "Failed to send activation email: " + err, captcha: captcha_html});

                  // Send to verify ask page
                  req.session.username = username;
                  req.session.verified = token;
                  return res.redirect(302, "/user");
                }
              );
            } else {
              req.session.username = username;
              req.session.verified = true;
              return res.redirect(302, "/user");
            }
          });
        });
      });
    });
  },

  // Email verification
  // This is setup in a way that you can activate your account
  // from your phone without logging in again.
  verify: (req, res) => {
    if (typeof req.params.token == "undefined") return res.status(400).render("error", {message: "Missing token", error: {status: "", stack: ""}});

    userModel.findByToken(req.params.token, user => {
      if (!user) return res.status(400).render("error", {message: "Invalid token/Already activated", error: {status: "", stack: ""}});

      userModel.verify(req.params.token, _ => {

        if (typeof req.session != "undefined") {
          req.session.verified = true;
        }
        return res.status(200).render("verify_success");
      });
    });
  },

  // Render the user profile
  profile: (req, res) => {
    userModel.findByUsername(req.session.username, user => {
      res.status(200).render("profile", {
        user: user
      });
    });
  },

  addToken: (req, res) => {
    const username = req.session.username;
    // TODO: add per token permissions

    // Get the user's details from the DB
    crypto.randomBytes(32, (err, buf) => {
      if (err) return res.status(400).render("/user", {err: "Oops, something broke."});
      const token = buf.toString('hex');
      userModel.addToken(username, token, status => {

        if (typeof status == "undefined" || status == "err") {
          return res.redirect(400 , "/user");
        }
        else {
          return res.redirect(302, "/user");
        }
      });
    });
  },

  removeToken: (req, res) => {
    const username = req.session.username;
    const token = req.query.token;
    // TODO: add per token permissions
    userModel.removeToken(username, token, (data) => {
      return res.redirect(302, "/user");
    });
  },

  listTokens: (req, res) => {
    const username = req.session.username;
    userModel.findByUsername(username, user => {
      if ( user ) {
        if (user.tokens) {
          return res.status(200).send(user.tokens);
        }
        else {
          res.status(403).end();
        }
      }
      else {
        res.status(403).end();
      }
    });
  },

  validToken: (req, res, next) => {
    const username = req.query.username;
    const token = req.query.token;
    userModel.findByUsername(username, user => {
      if ( user ) {
        if (user.tokens[token]) {
          next();
        }
        else {
          res.status(403).end();
        }
      }
      else {
        res.status(403).end();
      }
    });
  },

  sendSummaries: (req, res) => {

    // One transaction to rule them all
    dbFuncs.transaction(db => {
      userModel.getSummaryUsers(db, users => {

        if (users.length == 0) return res.status(304).send("No users");

        for (var i = 0; i < users.length; i++) {
          var user = users[i];

          streamModel.getFeedsNoTransaction(db, user.username, feeds => {

            // Assume the last summary was sent at (now - summaryInterval)
            // Summary interval is in hours, time is created in milliseconds
            var oldest_date = new Date(Date.now() - user.summaryInterval * 3600000);

            // Filter feeds accordingly
            var filtered_feeds = feeds.filter((feed, index, src) => {
              return feed.pub_date > oldest_date;
            });

            if (filtered_feeds.length > 0) {

              // Pick the best feeds to send
              // Prioritizes one from each feed source
              var cherrypicked_feeds = [];
              var sources_covered = [];
              for (i = 0; i < filtered_feeds.length; i++) {
                var feed = filtered_feeds[i];

                // Put articles from new sources at the top
                if (sources_covered.indexOf(feed.feed) == -1) {
                  cherrypicked_feeds.unshift(feed);
                  sources_covered.push(feed.feed);

                // Otherwise append them to cherrypicked_feeds
                } else {
                  cherrypicked_feeds.push(feed);
                }
              }

              // Only send 6
              // while (cherrypicked_feeds.length > 6) cherrypicked_feeds.pop();

              // Update the nextSummary value of this user
              dbFuncs.update(db, "user", {username: user.username}, {nextSummary: new Date(Date.now() + user.summaryInterval * 3600000)}, _ => {

                res.render(
                  "email_summary",
                  {
                    to: email,
                    subject: "Feedlark - Your Daily Roundup",
                    feeds: cherrypicked_feeds
                  }
                );

                // Don't send the email if we're not in production
                if (process.env.ENVIRONMENT != "PRODUCTION") return res.send("Skipped " + i + "/" + users.length + ": Not in production.");

                // Send email
                // res.mailer.send(
                //   "email_summary",
                //   {
                //     to: email,
                //     subject: "Feedlark - Your Daily Roundup",
                //     feeds: cherrypicked_feeds
                //   },
                //   err => {
                //     if (err) return res.send("Failed to send email " + i + "/" + users.length);
                //     return res.send("Email sent " + i + "/" + users.length);
                //   }
                // );
              });
            }
          });
        }
      });
    });
  }
};
