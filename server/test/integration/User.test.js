
var assert = require('assert');
var request = require('supertest');

describe('UserModel', function() {
  var user_details_base = {
    username: "rmss",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  }
  var user_details_dupe_email = {
    username: "heyzeus",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  }
  var user_details_dupe_uname = {
    username: "rmss",
    email: "rekt@gnu.org",
    password: "gnuisnotlinux"
  }
  // Perisistent agent so session stays
  var agent = request.agent("http://localhost:1337");
  describe('#signup()', function() {
    it('User must provide username', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send({
          username: "",
          email: "rekt@gnu.org",
          password: "gnuisnotlinux"
        })
        .expect(400, done);
    });
    it('User must provide email', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send({
          username: "rmss",
          email: "r@gn",
          password: "gnuisnotlinux"
        })
        .expect(400, done);
    });
    it('User must provide good password', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send({
          username: "rmss",
          email: "rms@gnu.org",
          password: "w4t"
        })
        .expect(400, done);
    });
    it('User can sign up', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('form')
        .send(user_details_base)
        .expect(200)
        .expect('Success', done);
    });
    it('User cant reuse email', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('json')
        .send(user_details_dupe_email)
        .expect(400, done);
    });
    it('User cant reuse username', function (done) {
      request(sails.hooks.http.app)
        .post('/user/signup')
        .type('json')
        .send(user_details_dupe_uname)
        .expect(400, done);
    });
  });
  describe('#login()', function() {
    it('User cant login with invalid password', function (done) {
      agent
        .post('/user/login')
        .type('json')
        .send({
		  username: "rmss",
		  email: "rms@gnu.org",
		  password: "gnu1snotlinux"
		})
        .expect(400, done);
    });
    it('User cant login with invalid email', function (done) {
      agent
        .post('/user/login')
        .type('json')
        .send(user_details_dupe_uname)
        .expect(400, done);
    });
    it('User can login', function (done) {
      agent
        .post('/user/login')
        .type('json')
        .send(user_details_base)
        .expect(200)
        .expect("Success", done)
    });
  });
  describe('#profile()', function() {
    it('User can view profile', function (done) {
      agent
        .get('/user/profile')
        .expect(200, done);
    });
    it('User can log out', function (done) {
      agent
        .get('/user/logout')
        .expect(200, done);
    });
    it('User cant view profile when logged out', function (done) {
      agent
        .get('/user/profile')
        .expect(403, done);
    });
  });
});
