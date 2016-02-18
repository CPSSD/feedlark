var sails = require('sails');

before(function(done) {
  this.timeout(10000);

  sails.lift({
    log: {
      level: "verbose"
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
