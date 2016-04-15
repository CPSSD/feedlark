/**
 * bookmarks.js
 *
 * @description :: Generic model for bookmarks of all users on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/bookmark.md
 */

const dbFuncs = require("../middleware/db");

module.exports = {

  addBookmark: (username, url, name, pub_date, feed, cb) => {

    dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, user => {
      newBookmark = {
          "feed": feed,
          "name": name,
          "link":url,
          "pub_date": pub_date
      };

      // Check if the user has already bookmarked this article
      if (user.bookmarks.indexOf(url) > -1) return cb();

      // Append and update
      user.bookmarks.push(url);;
      dbFuncs.update(
        db,
        "bookmark",
        {username: username},
        {bookmarks: user.bookmarks},
        _ => cb(user.bookmarks)
      );
    }));
  },

  removeBookmark: (username, url, cb) => {

    dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, user => {
      oldBookmark = {
          "feed": feed,
          "name": name,
          "link":url,
          "pub_date": pub_date
      };
      // Check if the user is already subscribed to this feed
      var index = user.subscribed_feeds.indexOf(oldBookmark);
      if (index == -1) return cb();

      // Append and update
      user.bookmarks.splice(index, 1);
      dbFuncs.update(
        db,
        "bookmark",
        {username: username},
        {bookmarks: user.bookmarks},
        _ => cb(user.bookmarks)
      );
    }));
  },

  getBookmarks: (username,cb) => {
	dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, data => cb(data.feeds)));
  }

};
