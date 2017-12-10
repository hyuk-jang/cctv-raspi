const BU = require('base-util-jh').baseUtil;
const _ = require('underscore');

const config = require('./config')

global.BU = BU;
global._ = _;


let app = require('./config/app.js')(config.dbInfo);

app.set('initSetter', config);

require('./controller')(app);


  // TEST
  app.listen(config.serverInfo.port, (req, res) => {
    console.log('Controller Server is Running', config.serverInfo.port);
  });