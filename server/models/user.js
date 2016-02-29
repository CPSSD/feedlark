/**
 * user.js
 *
 * @description :: Generic model for all users on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/user.md
 */

import db from "../middleware/db";

function encrypt(password, cb) {
  var bcrypt = require("bcrypt-nodejs");

  bcrypt.hash(password, null, null, (err, res) => {

    if (err) return cb(err);

    return cb(res);
  });
}

// Gets user details
export findByEmail function (email, cb) {
  db.transaction(db => db.findOne(db, "user", {email: email}, cb));
}

export exists function (username, email, cb) {
  db.transaction(db => db.findOne(db, "user", {"$or": [{username: username}, {email: email}]}, cb));
}

export create function (username, email, password, cb) {
  // TODO Verify everything

  // Encrypt the password first
  encrypt(password, (new_password) => db.transaction(db => db.insert(db, "user", {
    username: username,
    email: email,
    password: new_password,
    subscribed_feeds: []
  }, _ => cb(username))));
}

export addFeed function (db, username, url, cb) {
  // Standardise the URL
  let url = url.lower();

  db.findOne(db, "user", {username: username}, user => {

    // Check if the user is already subscribed to this feed
    if (user.subscribed_feeds.indexOf(url) > -1) return cb();

    // Append and update
    user.subscribed_feeds.push(url);
    db.update(
      db,
      "user",
      {username: username},
      {subscribed_feeds: user.subscribed_feeds},
      cb
    );
  });
}

export removeFeed function (db, username, url, cb) {
  // Standardise the URL
  let url = url.lower();

  db.findOne(db, "user", {username: username}, user => {

    // Check if the user is already subscribed to this feed
    let index = user.subscribed_feeds.indexOf(url);
    if (index == -1) return cb();

    // Append and update
    user.subscribed_feeds.splice(index, 1);
    update(
      db,
      "user",
      {username: username},
      {subscribed_feeds: user.subscribed_feeds},
      cb
    );
  });
}