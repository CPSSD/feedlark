/**
 * bookmarks.js
 *
 * @description :: Generic model for bookmarks of all users on the site
 * @docs        :: https://github.com/CPSSD/feedlark/blob/master/doc/db/bookmark.md
 */

const dbFuncs = require("../middleware/db");

module.exports = {

  addBookmark: (username, url, named, date, feed, cb) => {

    dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, user => {
      var bookmarks;

      var newBookmark = {
          "feed": feed,
          "name": named,
          "link": url,
          "date": date
      };

      if (!user){
        dbFuncs.transaction(db => dbFuncs.insert(db, "bookmark", {
          username: username,
          bookmarks: [newBookmark]
          }, cb));
      } else {
        bookmarks = user.bookmarks;
        // Check if the user has already bookmarked this article
        for (var i = 0; i < bookmarks.length; i++) {
          if (bookmarks[i].link == url){
            return cb();
          }
        }
        // Append and update
        bookmarks.push(newBookmark);
        dbFuncs.update(
          db,
          "bookmark",
          {username: username},
          {bookmarks: bookmarks},
          _ => cb(bookmarks)
        );
      }
      }));
  },

  removeBookmark: (username, url, cb) => {

    dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, user => {
      var index;
      // Check if the user is already subscribed to this feed
      for (var i = 0; i <= user.bookmarks.length; i++) {
        if (user.bookmarks[i].link == url){
          index = i;
          break;
        } else if (i == user.bookmarks.length -1){
          return cb();
        }
      }

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
    dbFuncs.transaction(db => dbFuncs.findOne(db, "bookmark", {username: username}, data => {

      if (!data){
        dbFuncs.transaction(db => dbFuncs.insert(db, "bookmark", {
          username: username,
          bookmarks: []
        }, cb));
    } else {
        cb(data.bookmarks)
    }
    }));
  }
};
