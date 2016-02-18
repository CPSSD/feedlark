
var assert = require('assert');
var request = require('supertest');

describe('UserModel', function() {
  describe('#signup()', function() {
    it('should check signup function', function (done) {
      var user_details = {
        username: "rms",
        email: "rms@gnu.org",
        entry_password: "gnuisnotlinux"
      };
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send(user_details)
        .expect(200)
        .expect("Signup successful! Horray!");
      done();
    });
  });
});
