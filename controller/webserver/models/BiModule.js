const bmjh = require('base-model-jh');
const Promise = require('bluebird')
const BU = require('base-util-jh').baseUtil;

class BiModule extends bmjh.BM {
  constructor(dbInfo) {
    super(dbInfo);

  }

  /**
   * cctv 리스트와 현재 데이터를 가져옴
   */
  getCctvStatus() {
    let sql = `
        SELECT id.*
                , ci.name, ci.address
        FROM illegal_data AS id
        LEFT JOIN cctv_info AS ci
            ON id.cctv_id = ci.cctv_id
        WHERE illegal_data_seq IN (
            SELECT MAX(illegal_data_seq)
            FROM illegal_data
            GROUP BY cctv_id
            )
        `;

    return this.db.single(sql);
  }

  /**
   * cctv 대상의 최근 불법주차 내역을 가져옴
   * @param {String} cctv_id cctv Id
   * @return {Object} {startIllegalObj, endIllegalObj} 불법 주차 시작 사진, 불법 주차 종료 사진
   */
  async getCctvHistory(cctv_id) {
    let returnValue = {
      startIllegalObj: {},
      endIllegalObj: {}
    }
    let sql = `
        SELECT id.*
        FROM	
          (
          SELECT MAX(illegal_data_seq) AS max_seq
          FROM illegal_data
          WHERE count > 14
          GROUP BY cctv_id
          ) sub
        JOIN illegal_data id
        ON id.illegal_data_seq = sub.max_seq
        WHERE id.cctv_id = '${cctv_id}'
      `;
    // 최근 불법 종료 시점 지점 찾아오기
    let endIllegalCctvData = await this.db.single(sql);
 
    // 불법 주차 내역이 없다면 초기 선언 데이터 반환
    if (!endIllegalCctvData.length) {
      return returnValue;
    }

    returnValue.endIllegalObj = _.first(endIllegalCctvData)

    sql = `
        SELECT id.*
        FROM	
          (
          SELECT MAX(illegal_data_seq) AS max_seq
          FROM illegal_data
          WHERE count = 1 AND illegal_data_seq < ${returnValue.endIllegalObj.illegal_data_seq}
          GROUP BY cctv_id
          ) sub
        JOIN illegal_data id
        ON id.illegal_data_seq = sub.max_seq
        WHERE id.cctv_id = '${cctv_id}'
  `;
    // 최근 불법 종료 시점 지점 찾아오기
    let startIllegalCctvData = await this.db.single(sql);
    BU.CLI(startIllegalCctvData)
    returnValue.startIllegalObj = startIllegalCctvData.length ? _.first(startIllegalCctvData) : {}

    return returnValue;

  }




}
module.exports = BiModule;