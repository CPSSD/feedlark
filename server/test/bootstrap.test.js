const MongoClient = require("mongodb");

function removeTestUser(done) {
  MongoClient.connect("mongodb://localhost:9001/feedlark", (err, db) => {
    if (err) throw err;

    db.collection("user").remove({"$or": [{username: "rmss"}, {username: "heyzeus"}]}, err => {
      if (err) throw err;

      db.collection("g2g").remove({"$or": [{username: "rmss"}, {username: "heyzeus"}]}, err => {
        if (err) throw err;

        db.close();
        console.log("Database cleaned");
        done();
      });
    });
  });
}

// Remove tests users from the database before and after
// Not inside a describe block, as per recommendations in Mocha's "Root-level hooks" documentation
// See https://mochajs.org/#hooks
before(removeTestUser);

after(removeTestUser);
