const express = require('express');
const app = express();

app.get('/', (req, res) => {
  let count = req.query.count || null;
  let cctv_id = req.query.cctv_id || null;
  let etc = req.query.etc || null;

  res.json({
    msg: 'Hello World',
    count,
    cctv_id,
    etc
  });
  //  send('Hello /')
})

app.get('/processor', (req, res) => {
  res.json('good job /')
})

app.listen(3333, () => {
  console.log('Server is listen : 3333');
})