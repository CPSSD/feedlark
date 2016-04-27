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
var tokens = {secret_key: "nope", site_key: "bees"};
if (fs.existsSync("../script/captcha_tokens.js")) {
  tokens = require("../../script/captcha_tokens");
}

// Used in sendSummaries
function processSummaryData(user, feeds) {

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
    while (cherrypicked_feeds.length > 6) cherrypicked_feeds.pop();

    // Update the nextSummary value of this user
    // Offset by two minutes so that they don't progressively become out of sync
    dbFuncs.update(db, "user", {username: user.username}, {nextSummary: new Date(Date.now() - 120000 + (user.summaryInterval) * 3600000)}, _ => {

      // Don't send the email if we're not in production
      if (process.env.ENVIRONMENT != "PRODUCTION") return res.send("Skipped " + j + "/" + users.length + ": Not in production.\n");

      // Send email
      res.mailer.send(
        "email_summary",
        {
          to: user.email,
          subject: "Feedlark - Your " + interval_eng[user.summaryInterval] + " Roundup",
          feeds: cherrypicked_feeds
        },
        err => {
          if (err) return res.send("Failed to send email " + j + "/" + users.length + "\n");
          return res.send("Email sent " + j + "/" + users.length + "\n");
        }
      );
    });
  }
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

  // Allow for password change
  changePassword: (req, res) => {

    // Load request vars & verify
    var username = req.session.username;
    var newPassword = req.body.newPassword;
    var oldPassword1 = req.body.oldPassword1;
    var newPassword2 = req.body.newPassword2;

    // Check validity of passwords
    if (newPassword.length < 8){
      req.session.msg = "New password is too short.";
      return res.redirect(302, "/user");
    }
    if (!_.isString(newPassword2) || !_.isString(oldPassword1) || !_.isString(newPassword)) {
      req.session.msg = "One of your Passwords is not a string";
      return res.redirect(302, "/user");
    }
    if (newPassword2 != newPassword) {
      req.session.msg = "Your new passwords did not match";
      return res.redirect(302, "/user");
    }

    // Get the user's details from the DB
    userModel.findByUsername(username, user => {

      // Is the user name valid? (DB query returns nothing if not)
      if (typeof user == "undefined") {
        req.session.msg = "Invalid username.";
        return res.redirect(302, "/user");
      }

      // Check their password
      bcrypt.compare(oldPassword1, user.password, (err, valid) => {
        if (!valid) {
          req.session.msg = "Your old password is incorrect.";
          return res.redirect(302, "/user");
        }
        // Change the password in the db
        userModel.updatePassword(user, newPassword, _ => {
          req.session.msg = "Successfully changed your password";
          return res.redirect(302, "/user");
        });
      });
    });
  },

  // Allow for password change
  changeEmail: (req, res) => {

    // Load request vars & verify
    var username = req.session.username;
    var newEmail = req.body.newEmail;
    var oldEmail = req.body.oldEmail;

    // Check validity of passwords
    if (newEmail.length < 5){
      req.session.msg = "Email address is too short.";
      return res.redirect(302, "/user");
    }
    if (!_.isString(newEmail)) {
      req.session.msg = "Your email is not a string";
      return res.redirect(302, "/user");
    }

    // Get the user's details from the DB
    userModel.findByUsername(username, user => {

      // Is the user name valid? (DB query returns nothing if not)
      if (typeof user == "undefined") {
        req.session.msg = "Invalid username.";
        return res.redirect(302, "/user");
      }
      if (user.email != oldEmail) {
        req.session.msg = "Incorrect current email.";
        return res.redirect(302, "/user");
      }
      crypto.randomBytes(32, (err, buf) => {
        if (err) return res.status(500).render("signup", {err: "Failed to generate verification token:" + err, captcha: captcha_html});
        var token = buf.toString("hex");

        if (process.env.ENVIRONMENT == "PRODUCTION") {
          res.mailer.send(
            "email_verify",
            {
              to: newEmail,
              subject: "Feedlark - Update your Email Address",
              token: token
            },
            err => {
              if (err) return res.status(500).render("signup", {err: "Failed to send activation email: " + err, captcha: captcha_html});
            }
          );
        } else {
          req.session.username = username;
          req.session.verified = true;
        }


        userModel.updateEmail(user.username, newEmail, token, _ => {
          req.session.msg = "Successfully changed your email. Please check it for the verification email.";
          return res.redirect(302, "/user");
        });
      });
    });
  },

  changeSummaryInterval: (req, res) => {
    // Changes to the options here need to be reflected on the profile page
    // Also down below in the sendSummaries function
    // Values are in hours
    var valid_intervals = {"off": 0, "daily": 24, "weekly": 168, "monthly": 5040};

    // Validation
    if (!req.body.summaryInterval || !valid_intervals[req.body.summaryInterval]) {
      req.session.msg = "Invalid summary interval.";
      return res.redirect(302, "/user");
    }

    // Update; error handling done in db middleware
    userModel.updateSummaryInterval(req.session.username, valid_intervals[req.body.summaryInterval], _ => {
      req.session.msg = "Successfully changed your summary interval.";
      return res.redirect(302, "/user");
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

  // Render the user profile tokens view
  profileTokens: (req, res) => {
    userModel.findByUsername(req.session.username, user => {
      res.status(200).render("profile_tokens", {
        user: user
      });
    });
  },

  addToken: (req, res) => {
    const username = req.session.username;
    // TODO: add per token permissions

    // Get the user's details from the DB
    crypto.randomBytes(32, (err, buf) => {
      if (err) return res.status(400).render("/user/tokens", {err: "Oops, something broke."});
      const token = buf.toString('hex');
      userModel.addToken(username, token, status => {

        if (typeof status == "undefined" || status == "err") {
          return res.redirect(400 , "/user/tokens");
        }
        else {
          return res.redirect(302, "/user/tokens");
        }
      });
    });
  },

  removeToken: (req, res) => {
    const username = req.session.username;
    const token = req.query.token;
    // TODO: add per token permissions
    userModel.removeToken(username, token, (data) => {
      return res.redirect(302, "/user/tokens");
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

    // Check the key
    if (req.params.key != process.env.SECRETKEY) {
      return res.status(403).send("Secret key doesn't match");
    }

    // One transaction to rule them all
    dbFuncs.transaction(db => {
      userModel.getSummaryUsers(db, users => {

        var interval_eng = {24: "Daily", 168: "Weekly", 5040: "Monthly"};

        if (users.length === 0) return res.status(200).send("No users");

        for (var j = 0; j < users.length; j++) {
          var user = users[j];

          streamModel.getFeedsNoTransaction(db, user.username, feeds => processSummaryData(user, feeds));
        }
      });
    });
  }
};
