/**
 * users
 *
 * @description :: Server-side logic for managing users.
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

const _ = require("lodash");
const crypto = require("crypto");
const bcrypt = require("bcrypt-nodejs");
const userModel = require("../models/user");
const Recaptcha = require("recaptcha").Recaptcha;
const captcha_tokens = require("../../script/captcha_tokens");

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
          return res.redirect(302, "/user");
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

    // Captcha setup
    var data = {
      remoteip:  req.connection.remoteAddress,
      challenge: req.body.recaptcha_challenge_field,
      response:  req.body.recaptcha_response_field
    };
    var captcha = new Recaptcha(captcha_tokens.public_key, captcha_tokens.private_key, data);
    var captcha_html = captcha.toHTML();

    // Check if anything actually needs to be done (initial viewing of signup page)
    if (req.method == "GET") return res.status(200).render("signup", {captcha: captcha_html});

    // Import things & load request vars
    var email = req.body.email;
    var password = req.body.password;
    var username = req.body.username;

    // Verify these details
    if (!_.isString(email) || !_.isString(password) || !_.isString(username)) return res.status(400).render("signup", {err: "Invalid input data."});
    if (email.length < 5) return res.status(400).render("signup", {err: "Email Address too short.", captcha: captcha_html});
    if (password.length < 8) return res.status(400).render("signup", {err: "Password too short.", captcha: captcha_html});
    if (username.length < 4) return res.status(400).render("signup", {err: "Username too short.", captcha: captcha_html});


    captcha.verify((success, error_code) => {
      if (!success && process.env.ENVIRONMENT == "PRODUCTION") return res.status(400).render("signup", {captcha: captcha_html});

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
                  subject: "Activate your account",
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
  }

};
