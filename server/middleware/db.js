const MongoClient = require("mongodb");

module.exports = {
  // This means that only one connection is created per transaction
  transaction: (next) => {
    MongoClient.connect("mongodb://localhost:27017/feedlark", (err, db) => {

      // Error should be null/undefined normally
      if (err) throw err;

      next(db);

      db.close();
    });
  },

  findOne: (db, collection, selector, cb) => {

    // Mongo's findOne is deprecated. Recommended to use find().limit(1)
    db.collection(collection).find(selector).limit(1).toArray((err, data) => {

      if (err) throw err;

      return cb(data[0]);
    });
  },

  create: (db, collection, data, cb) => {
    db.collection(collection).insertOne(data, (err, data) => {

      if (err) throw err;

      return cb();
    });
  },

  update: (db, collection, selector, data, cb) => {
    db.collection(collection).updateOne(selector, {$set: data}, (err, data) => {

      if (err) throw err;

      return cb();
    });
  },

  remove: (db, collection, selector, cb) => {
    db.collection(collection).removeOne(selector, (err, data) => {

      if (err) throw err;

      return cb();
    });
  }
}