import MongoClient from "mongodb";

// This means that only one connection is created per transaction
export transaction function (next) {
  MongoClient.connect("mongodb://localhost:27017/feedlark", (err, db) => {

    // Error should be null/undefined normally
    if (err) throw err;

    next(db);

    db.close();
  });
}

export findOne function (db, collection, selector, cb) {

  // Mongo's findOne is deprecated. Recommended to use find().limit(1)
  db.collection(collection).find(selector).limit(1).toArray((err, data) => {

    if (err) throw err;

    return cb(data[0]);
  });
}

export create function (db, collection, data, cb) {
  db.collection(collection).insertOne(data, (err, data) => {

    if (err) throw err;

    return cb();
  });
}

export update function (db, collection, selector, data, cb) {
  db.collection(collection).updateOne(selector, {$set: data}, (err, data) => {

    if (err) throw err;

    return cb();
  });
}

export remove function (db, collection, selector, cb) {
  db.collection(collection).removeOne(selector, (err, data) => {

    if (err) throw err;

    return cb();
  });
}