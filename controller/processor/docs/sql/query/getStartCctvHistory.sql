
        SELECT id.*
        FROM
          (
          SELECT MAX(illegal_data_seq) AS max_seq
          FROM illegal_data
          WHERE count = 1 AND illegal_data_seq < 820
          
          GROUP BY cctv_id
          ) sub
        JOIN illegal_data id
        ON id.illegal_data_seq = sub.max_seq
        WHERE id.cctv_id = 'aaaa'