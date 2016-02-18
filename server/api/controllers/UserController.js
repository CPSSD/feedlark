/**
 * UserController
 *
 * @description :: Server-side logic for managing users
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

  /**
   * `UserController.login()`
   */
  login: function (req, res) {
    var bcrypt = require('bcrypt-nodejs');
    var email = req.param('email');
    var password = req.param('entry_password');
    User.findOne({
      email: email
    })
    .exec(function (err, user) {
      if (err) return res.negotiate(err);

      // define a function so we don't repeat ourselves
      var invalid = function(req, res) {
        if (req.wantsJSON) {
          return res.badRequest('Invalid username/password combination.');
        }
        return res.view("login", {});
      };

      if (!user) {
        return invalid(req, res);
      }
      bcrypt.compare(password, user.password, function(err, valid) {
        if (valid) {
          req.session.authenticated = user.email;
          if (req.wantsJSON) {
            return res.ok("Login successful");
          }
          return res.redirect("/");
        } else {
          return invalid(req, res);
        }
      });
    });
  },


  /**
   * `UserController.logout()`
   *
   * @description :: Logout, don't bother checking if they're logged in
   */
  logout: function (req, res) {
    req.session.authenticated = null;
		if (req.wantsJSON) {
      return res.ok('Logged out! See you next time :)');
    }
		return res.redirect('/');
  },


  /**
   * `UserController.signup()`
   */
  signup: function (req, res) {
    var password = req.param('entry_password');
    var bcrypt = require('bcrypt-nodejs');
    bcrypt.hash(password, null, null, function(err, hash) {
      if (err) return res.negotiate(err);
      User.create({
        username: req.param('username'),
        email: req.param('email'),
        subscribed_feeds: [],
        password: hash
      })
      .exec(function (err, user) {
        if (err) {
          console.log(err);
          // Redirect to signup page
          return res.view('signup', {});
        }
        req.session.authenticated = user.email;
        if (req.wantsJSON) {
          return res.ok('Signup successful! Horray!');
        }
        return res.view('profile', {});
      });
    });
  },

  /**
   * `UserController.addfeed()`
   */
  addfeed: function (req, res) {
    var feeds_to_add = req.param('feeds');
    User.findOne({
     'email': req.session.authenticated
    })
    .exec( function (err, user) {
       if (err) return res.negotiate(err);
       if (user) {
        for (var feed in feeds_to_add){
         user.subscribed_feeds.push(feeds_to_add[feed]);
        }
        user.save( function(err, s){
          if (err) return res.negotiate(err);
        });
       }

      if (req.wantsJSON) {
        return res.ok('Feeds added successfully');
      }
      return res.redirect('/');
    });
  }
};
