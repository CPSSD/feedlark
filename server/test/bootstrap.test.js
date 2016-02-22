var sails = require('sails');

before(function(done) {
  this.timeout(30000);

  sails.lift({
    log: {
      level: "silent"
    },
    models: {
      connection: 'test',
      migrate: 'drop'
    }
  }, function(err, server) {
    if (err) return done(err);
    done(err);
  });
});

after(function(done) {
  // here you can clear fixtures, etc.
  sails.lower(done);
});