const wrap = require('express-async-wrap');
const Q = require('q');
let multer = require('multer'); // express에 multer모듈 적용 (for 파일업로드)

let BU = require('base-util-jh').baseUtil;
let DU = require('base-util-jh').domUtil;

let BiModule = require('../models/BiModule.js');

module.exports = function (app) {
  const initSetter = app.get('initSetter');
  const biModule = new BiModule(initSetter.dbInfo);

  // server middleware
  app.use(function (req, res, next) {
    // req.locals = DU.makeBaseHtml(req, 1);
    next();
  });


  // cctv monitoring 제공 주소
  app.get('/', wrap(async(req, res) => {
    BU.CLI('? what')
    let cctv_id = req.query.cctv_id ? req.query.cctv_id : '';

    // let cctvList = await biModule.getTable('cctv_info', '', '', true)
    let cctvList = await biModule.getCctvStatus()
    let selectCctv = _.findWhere(cctvList, {
      cctv_id: cctv_id
    })
    selectCctv = _.isEmpty(selectCctv) ? _.first(cctvList) : selectCctv;





    BU.CLI(selectCctv)


    // let dailyPowerReport = await biModule.getDailyPowerReport();
    // let moduleStatus = await biModule.getTable('v_photovoltaic_status');
    // let inverterDataList = await biModule.getTable('v_inverter_status');


    // req.locals.dailyPowerReport = dailyPowerReport;
    // req.locals.moduleStatus = moduleStatus;
    // req.locals.powerGenerationInfo = powerGenerationInfo;

    return res.render('./main/cctv.html', req.locals)
  }));


  // 정기적으로 cctv Processor에서 http get 방식으로 데이터를 보내옴
  app.get('/cctv_status_receiver', wrap(async(req, res) => {
    return res.send()
  }));

  // cctv에서 polling 방식으로 데이터를 가져가는 주소
  app.get('/check_commander', wrap(async(req, res) => {
    return res.send()
  }));

  // cctv에서 image를 post 방식으로 보내오는 주소
  app.post('/image_receiver', wrap(async(req, res) => {
    upload(req, res)
      .then(function (file) {
        console.trace(file)
        return res.json(file);
      })
      .catch(function (err) {
        console.error('err', err)
        return res.status(500).send(err);
      });
    return res.send()
  }));

  var upload = function (req, res) {
    var deferred = Q.defer();
    var storage = multer.diskStorage({
      // 서버에 저장할 폴더
      destination: function (req, file, cb) {
        cb(null, 'public/image/illegal/');
      },

      // 서버에 저장할 파일 명
      filename: function (req, file, cb) {
        console.log('file', file)
        file.uploadedFile = {
          name: req.params.filename,
          ext: 'png'
          // ext: file.mimetype.split('/')[1]
        };
        console.log('file.uploadeddedFile.ext', file.uploadedFile.name + '.' + file.uploadedFile.ext)
        cb(null, file.uploadedFile.name + '.' + file.uploadedFile.ext);
      }
    });

    var upload = multer({
      storage: storage
    }).single('image');
    upload(req, res, function (err) {
      if (err) {
        deferred.reject();
      } else deferred.resolve(req.file);
    });
    return deferred.promise;
  };


  // cctv에서 polling 방식으로 데이터를 가져가는 주소
  app.get('/test_dummy_inserter', wrap(async(req, res) => {
    let cctvList = await biModule.getTable('cctv_info')

    let insertList = [];

    cctvList.forEach(cctvInfo => {
      // 20개씩 집어넣음
      let count = 0;
      for (let i = 0; i < 20; i++) {
        let addObj = {
          cctv_id: cctvInfo.cctv_id,
          count: 0,
          status: 'reset',
          img: ''
        }
        // TEST 대충 데이터 넣음
        let rValue = _.random(0, 100);
        if (rValue < 5) {
          addObj.count = count = 0;
          addObj.img = 'reset';
        } else if (rValue < 10) {
          addObj.count = count = 1;
          addObj.status = 'new';
          addObj.img = 'new';
        } else {
          addObj.count = ++count;
          addObj.status = 'continue';
          addObj.img = 'continue';
        }
        insertList.push(addObj)
      }
    });
    let resSetTables = await biModule.setTables('illegal_data', insertList)
    return res.status(200).send(resSetTables)

  }));


  // 예외처리
  app.use(wrap(async(err, req, res, next) => {
    BU.CLI('Err', err)
    res.status(500).send(err);
  }));


}