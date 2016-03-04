var dbFuncs = require("../middleware/db");
var port = 3000;

function removeTestUser(done) {
  dbFuncs.transaction(db => dbFuncs.remove(db, "user", {username: "rmss"}, done));
  done();
}

describe('app', function () {

  // Remove rmss from the database before and after
  before (removeTestUser);

  after(removeTestUser);
});
