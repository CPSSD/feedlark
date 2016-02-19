
var assert = require('assert');
var request = require('supertest');

describe('UserModel', function() {
  var user_details = {
    username: "rms",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  };
  var cookie;
  describe('#signup()', function() {
    it('should check signup functionality', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send(user_details)
        .expect(200)
        .expect("Signup successful! Horray!", done);
    });
    it('should check users cant signup twice', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('json')
        .send(user_details)
        .expect(400, done);
    });
  });
  describe('#login()', function() {
    it('should check login functionality', function (done) {
      request(sails.hooks.http.app)
        .post('/user/login')
        .type('json')
        .send(user_details)
        .expect(200)
        .expect("Login successful")
        .end(function (err, res) {
          if (err) done(err);
          cookie = res.headers['set-cookie'];
          done();
        });
    });
  });
  describe('#addfeed()', function() {
    it('should check user can add feed', function (done) {
      request(sails.hooks.http.app)
        .post('/user/addfeed')
        .type('json')
        .set('cookie', cookie)
        .send('{"feeds": ["https://www.reddit.com/r/linux/.rss"]}')
        .expect(200, done);
    });
  });
});
