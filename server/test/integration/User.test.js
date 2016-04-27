const app = require("../../app");
const assert = require('assert');
const request = require('supertest');

describe('UserModel', _ => {
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
  var agent = request.agent(app);
  describe('#signup()', _ => {
    it('User must provide username', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send({
          username: "",
          email: "rekt@gnu.org",
          password: "gnuisnotlinux"
        })
        .expect(400, done);
    });
    it('User must provide email', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send({
          username: "rmss",
          email: "r@gn",
          password: "gnuisnotlinux"
        })
        .expect(400, done);
    });
    it('User must provide good password', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send({
          username: "rmss",
          email: "rms@gnu.org",
          password: "w4t"
        })
        .expect(400, done);
    });
    it('User can sign up', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send(user_details_base)
        .expect(302, done);
    });
    it('User cant reuse email', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send(user_details_dupe_email)
        .expect(400, done);
    });
    it('User cant reuse username', done => {
      agent
        .post('/user/signup')
        .type('form')
        .send(user_details_dupe_uname)
        .expect(400, done);
    });
  });
  describe('#login()', _ => {
    it('User cant login with invalid password', done => {
      agent
        .post('/user/login')
        .type('form')
        .send({
          username: "rmss",
          email: "rms@gnu.org",
          password: "gnu1snotlinux"
        })
        .expect(400, done);
    });
    it('User cant login with invalid email', done => {
      agent
        .post('/user/login')
        .type('form')
        .send(user_details_dupe_uname)
        .expect(400, done);
    });
    it('User can login', done => {
      agent
        .post('/user/login')
        .type('form')
        .send(user_details_base)
        .expect(302, done);
    });
  });
  describe('#profile()', _ => {
    it('User can view profile', done => {
      agent
        .get('/user')
        .expect(200, done);
    });
    it('User can change default page length', done => {
      agent
        .post('/user/change/defaults')
        .type('form')
        .send({
          'pageLength': "23"
        })
        .expect(200, done);
    });
    it('User can not set invalid default page length', done => {
      agent
        .post('/user/change/defaults')
        .type('form')
        .send({
          'pageLength': "400"
        })
        .expect(400, done);
    });
    it('User can log out', done => {
      agent
        .get('/user/logout')
        .expect(200, done);
    });
    it('User cant view profile when logged out', done => {
      agent
        .get('/user')
        .expect(302, done);
    });
  });
});
