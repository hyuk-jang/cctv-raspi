SELECT o.*
FROM `Persons` o                    # 'o' from 'oldest person in group'
  LEFT JOIN `Persons` b             # 'b' from 'bigger age'
      ON o.Group = b.Group AND o.Age < b.Age
WHERE b.Age is NULL                 # bigger age not found