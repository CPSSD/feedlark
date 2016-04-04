/**
 * user.js
 *
 * @description :: Generic model for all users on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

const dbFuncs = require("../middleware/db");

function encrypt(password, cb) {
  var bcrypt = require("bcrypt-nodejs");

  bcrypt.hash(password, null, null, (err, res) => {

    if (err) return cb(err);

    return cb(res);
  });
}

module.exports = {

  // Gets user details
  findByEmail: (email, cb) => {
    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {email: email}, cb));
  },

  findByUsername: (username, cb) => {
    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {username: username}, cb));
  },

  // Returns a user if one exists
  exists: (username, email, cb) => {
    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {"$or": [{username: username}, {email: email}]}, cb));
  },

  create: (username, email, password, cb) => {

    // Encrypt the password first
    encrypt(password, new_password => dbFuncs.transaction(db => dbFuncs.insert(db, "user", {
      username: username,
      email: email,
      password: new_password,
      subscribed_feeds: []

    // Also create the blank entry in g2g
    }, _ => dbFuncs.insert(db, "g2g", {
      username: username,
      feeds: []
    }, cb))));
  },

  addFeed: (db, username, url, cb) => {

    dbFuncs.findOne(db, "user", {username: username}, user => {

      // Check if the user is already subscribed to this feed
      if (user.subscribed_feeds.indexOf(url) > -1) return cb();

      // Append and update
      user.subscribed_feeds.push(url);
      dbFuncs.update(
        db,
        "user",
        {username: username},
        {subscribed_feeds: user.subscribed_feeds},
        _ => cb(user.subscribed_feeds)
      );
    });
  },

  removeFeed: (username, url, cb) => {

    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {username: username}, user => {

      // Check if the user is already subscribed to this feed
      var index = user.subscribed_feeds.indexOf(url);
      if (index == -1) return cb();

      // Append and update
      user.subscribed_feeds.splice(index, 1);
      dbFuncs.update(
        db,
        "user",
        {username: username},
        {subscribed_feeds: user.subscribed_feeds},
        _ => cb(user.subscribed_feeds)
      );
    }));
  },

  addToken: (username, token, cb) => {
    if (!token || !username) {
      return cb();
    }
    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {username: username}, user => {

      // TODO Add and render error message
      if (!user.tokens) {
        user.tokens = {};
      }
      user.tokens[token] = true;


      // TODO: check for max tokens
      dbFuncs.update(
        db,
        "user",
        {username: username},
        {tokens: user.tokens},
        cb
      );
    }));
  },

  removeToken: (username, token, cb) => {
    dbFuncs.transaction(db => dbFuncs.findOne(db, "user", {username: username}, user => {
      if (typeof user.tokens != "undefined") {
        delete user.tokens[token];
      }
      dbFuncs.update(
        db,
        "user",
        {username: username},
        {tokens: user.tokens},
        cb
      );
    }));
  },

};
