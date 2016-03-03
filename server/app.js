const express = require('express');
const path = require('path');
const favicon = require('serve-favicon');
const logger = require('morgan');
const bodyParser = require('body-parser');

const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));

// express-session
//  https://github.com/expressjs/session
const session = require('express-session');
const MongoStore = require('connect-mongo')(session);

app.use(session({
  secret: 'g)o(r)ooodl2z8xh(5qan80517e%35dgh(_03+t%3&1*w$)t9)',
  resave: false,
  saveUninitialized: false,
  store: new MongoStore({ url: 'mongodb://localhost:27017/feedlark' })
}));

// Pass the session to each view as a local var
app.use('/', (req, res, next) => {
  res.locals.session = req.session;
  next();
});

// Load all the routing
app.use('/', require('./routes/routes'));

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
