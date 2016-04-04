const MongoClient = require("mongodb");

if (process.env.ENVIRONMENT == "PRODUCTION") {
  var MongoURL = "mongodb://feedlark:hackmeplz@127.0.0.1:9001/feedlark"
}
else {
  var MongoURL = "mongodb://127.0.0.1:9001/feedlark"
}

module.exports = {
  // This means that only one connection is created per transaction
  transaction: (next) => {
    MongoClient.connect(MongoURL, (err, db) => {
      // Error should be null/undefined normally
      if (err) throw err;

      next(db);
    });
  },

  findOne: (db, collection, selector, cb) => {

    // Mongo's findOne is deprecated. Recommended to use find().limit(1)
    db.collection(collection).find(selector).limit(1).toArray((err, data) => {

      if (err) {
        console.log("oops");
        throw err;
      }

      return cb(data[0]);
    });
  },

  insert: (db, collection, data, cb) => {
    db.collection(collection).insertOne(data, (err, data) => {

      if (err) throw err;

      return cb();
    });
  },

  update: (db, collection, selector, data, cb) => {
    db.collection(collection).updateOne(selector, {$set: data}, (err, data) => {
      if (err) throw err;

      return cb(data);
    });
  },

  remove: (db, collection, selector, cb) => {
    db.collection(collection).removeOne(selector, (err, data) => {

      if (err) throw err;

      return cb();
    });
  }
};
