const bmjh = require('base-model-jh');
const Promise = require('bluebird')
const BU = require('base-util-jh').baseUtil;

class BiModule extends bmjh.BM {
    constructor(dbInfo) {
        super(dbInfo);

    }

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




}
module.exports = BiModule;