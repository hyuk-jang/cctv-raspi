
SELECT id.*
 FROM	
	(
	SELECT MAX(illegal_data_seq) AS max_seq
	 FROM illegal_data
	WHERE count = 15
	GROUP BY cctv_id
		
	) sub
JOIN illegal_data id
	ON id.illegal_data_seq = sub.max_seq

 	


