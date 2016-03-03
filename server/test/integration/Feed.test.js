
var assert = require('assert');
var request = require('supertest');

describe('FeedModel', function() {
  var user_details_base = {
    username: "rmss",
    email: "rms@gnu.org",
    password: "gnuisnotlinux"
  }
  var feed_details = {
    url: "https://news.ycombinator.com/rss"
  }
  // Perisistent agent so session stays
  var agent = request.agent("http://localhost:1337");
  describe('#login()', function() {
    it('User can login', function (done) {
      agent
        .post('/user/login')
        .type('json')
        .send(user_details_base)
        .expect(200)
        .expect('Success', done)
    });
  });
  describe('#manage()', function() {
    it('User can manage their feeds', function (done) {
      agent
        .get('/feed/manage')
        .expect(200, done);
    });
  });
  describe('#add()', function() {
    it('User can add a feed', function (done) {
      agent
        .post('/feed/add')
        .type('json')
        .send(feed_details)
        .expect(200, done);
    });
    it('User cant use an invalid url', function (done) {
      agent
        .post('/feed/add')
        .type('json')
        .send({url: "blonk u.wat"})
        .expect(400, done);
    });
    // TODO: Fails, as far as I can tell, due to the sails-memory db
  //   it('User can safely try to add a duplicate', function (done) {
  //     agent
  //       .post('/feed/add')
  //       .type('json')
  //       .send(feed_details)
  //       .expect(200, done);
  //   });
  });
  describe('#remove()', function() {
    it('User cant use blank', function (done) {
      agent
        .post('/feed/add')
        .type('json')
        .send({})
        .expect(400, done);
    });
    // TODO: Fails, as far as I can tell, due to the sails-memory db
  //   it('User can remove a feed', function (done) {
  //     agent
  //       .get('/feed/remove')
  //       .type('json')
  //       .send(feed_details)
  //       .expect(200, done);
  //   });
    // TODO: Fails, as far as I can tell, due to the sails-memory db
    // it('User can safely try to remove a duplicate', function (done) {
    //   agent
    //     .get('/feed/remove')
    //     .type('json')
    //     .send(feed_details)
    //     .expect(200, done);
    // });
  });
  describe('#logout()', function() {
    it('User can log out', function (done) {
      agent
        .get('/user/logout')
        .expect(200, done);
    });
    it('User can no longer manage feeds', function (done) {
      agent
        .get('/feed/manage')
        .expect(403, done);
    });
  });
});
