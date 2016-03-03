var http = require('http');
var app  = require(__dirname + '/../app.js');
var port = 3000;

describe('app', function () {

  before (function (done) {

    // Launch sequence extracted from bin/www
    app.set('port', port);
    var server = http.createServer(app);
    server.listen(port);
    server.on('error', done);
    server.on('listening', _ => {
      console.log("Succesfully started test server");
      done();
    });
  });

  after(function (done) {
    app.close();
  });
});