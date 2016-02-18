
var assert = require('assert');
var request = require('supertest');

describe('UserModel', function() {
  var user_details = {
    username: "rms",
    email: "rms@gnu.org",
    entry_password: "gnuisnotlinux"
  };
  describe('#signup()', function() {
    it('should check signup functionality', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send(user_details)
        .expect(200)
        .expect("Signup successful! Horray!");
      done();
    });
  });
  describe('#signup()', function() {
    it('should check users cant signup twice', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send(user_details)
        .expect(400);
      done();
    });
  });
  describe('#login()', function() {
    it('should check login in UserController', function (done) {
      request(sails.hooks.http.app)
        .post('/user/login')
        .type('form')
        .send(user_details)
        .expect(200);
      done();
    });
  });
});
