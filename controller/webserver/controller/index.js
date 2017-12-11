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
    req.locals = {};
    next();
  });


  function convertColor(obj){
    let color = '';
    let msg = '';
    if(obj.count == 0){
      color = 'gre'
      msg = 'Normal'
    } else if(obj.count < 15){
      color = 'yel'
      msg = 'Monitoring'
    } else if(obj.count < 30){
      color = 'red'
      msg = 'Warning'
    } else {
      color = 'bla'
      msg = 'Illegal'
    }
    obj.color = color;
    obj.msg = msg;
    
    return obj;
  }

  function convertMeasureDateToStr(obj, keyName){
    // TEST 임시 지정 
    keyName = keyName ? 'write_date' : 'write_date';
    if(obj[keyName] == null || obj[keyName] === ''){
      keyName = 'write_date';
    }
    // keyName = keyName ? keyName : 'writedate';
    return obj['measure_date'] = obj[keyName] instanceof Date ? BU.convertDateToText(obj[keyName], '', 5) : '';    
  }

  
  function upload (req, res) {
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

  // cctv monitoring 제공 주소
  app.get('/', wrap(async(req, res) => {
    BU.CLI('index')
    let cctv_id = req.query.cctv_id ? req.query.cctv_id : '';

    let cctvList = await biModule.getCctvStatus()
    cctvList = _.map(cctvList, cctvInfo => {
      convertMeasureDateToStr(cctvInfo, 'measure_date')
      convertColor(cctvInfo);
      return cctvInfo;
    })
    // BU.CLI(cctvList)
    let selectedCctvInfo = _.findWhere(cctvList, {
      cctv_id: cctv_id
    })
    selectedCctvInfo = _.isEmpty(selectedCctvInfo) ? _.first(cctvList) : selectedCctvInfo;
    convertMeasureDateToStr(selectedCctvInfo, 'measure_date')
    convertColor(selectedCctvInfo)
    // BU.CLI(selectedCctvInfo)
    let selectedCctvHistory =  await biModule.getCctvHistory(selectedCctvInfo.cctv_id);
    // BU.CLI(selectedCctvHistory)
    selectedCctvHistory = _.each(selectedCctvHistory, his => {
      if(_.isEmpty(his)){
        return;
      }
      convertMeasureDateToStr(his, 'measure_date')
    })
    // BU.CLI(selectedCctvHistory)

    req.locals.currDate = BU.convertDateToText(new Date(), 'kor', 4)
    req.locals.cctvList = cctvList;
    req.locals.selectedCctvInfo = selectedCctvInfo;
    req.locals.selectedCctvHistory = selectedCctvHistory;

    return res.render('./main/cctv.html', req.locals)
  }));


  // 정기적으로 cctv Processor에서 http get 방식으로 데이터를 보내옴
  app.get('/cctv_status_receiver', wrap(async(req, res) => {
    BU.CLI('cctv_status_receiver', req.query)
    let cctv_id = req.query.cctv_id || null;
    let count = req.query.count || null;
    let img = req.query.img || null;
    let measure_date = req.query.measure_date || null;
    BU.CLI(measure_date)
    measure_date = measure_date.replace('_', ' ');

    // BU.CLI(measure_date)

    let reqQuery = {
      cctv_id,
      count,
      img,
      measure_date
    }
    // BU.CLI(reqQuery)

    let result = await biModule.setTable('illegal_data', reqQuery)

    return res.status(200).send(result)
  }));

  // cctv에서 polling 방식으로 데이터를 가져가는 주소
  app.get('/check_commander', wrap(async(req, res) => {
    return res.send()
  }));

  // cctv에서 image를 post 방식으로 보내오는 주소
  app.post('/image_receiver/:filename', wrap(async(req, res) => {
    BU.CLI('image_receiver')
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
        if (rValue < 20) {
          addObj.count = count = 0;
          addObj.img = 'reset';
        } else if (rValue < 40) {
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
