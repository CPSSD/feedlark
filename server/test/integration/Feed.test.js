const app = require("../../app");
const assert = require('assert');
const request = require('supertest');

describe('FeedModel', _ => {
  var user_details_base = {
    username: "rmss",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  }
  var feed_details = {
    url: "https://news.ycombinator.com/rss"
  }
  // Perisistent agent so session stays
  var agent = request.agent(app);
  describe('#login()', _ => {
    it('User can login', done => {
      agent
        .post('/user/login')
        .type('form')
        .send(user_details_base)
        .expect(302, done);
    });
  });
  describe('#manage()', _ => {
    it('User can manage their feeds', done => {
      agent
        .get('/feeds')
        .expect(200, done);
    });
  });
  describe('#add()', _ => {
    it('User can add a feed', done => {
      agent
        .post('/feeds/add')
        .type('form')
        .send(feed_details)
        .expect(302, done);
    });
    it('User cant use an invalid url', done => {
      agent
        .post('/feeds/add')
        .type('form')
        .send({url: "blonk u.wat"})
        .expect(302, done);
    });
    // Make sure it works by querying the DB and checking for 2 of the same thing
    it('User can safely try to add a duplicate', done => {
      agent
        .post('/feeds/add')
        .type('form')
        .send(feed_details)
        .expect(302, done);
    });
  });
  describe('#remove()', _ => {
    it('User cant use blank', done => {
      agent
        .post('/feeds/add')
        .type('form')
        .send({})
        .expect(302 , done);
    });
    it('User can remove a feed', done => {
      agent
        .get('/feeds/remove')
        .type('form')
        .send(feed_details)
        .expect(302, done);
    });
    it('User can safely try to remove a duplicate', done => {
      agent
        .get('/feeds/remove')
        .type('form')
        .send(feed_details)
        .expect(302, done);
    });
  });
  describe('#logout()', _ => {
    it('User can log out', done => {
      agent
        .get('/user/logout')
        .expect(200, done);
    });
    it('User can no longer manage feeds', done => {
      agent
        .get('/feeds')
        .expect(302, done);
    });
  });
});
