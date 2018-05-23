SQL_LOCKS = """
SELECT
  C.SECONDS_IN_WAIT AS SEGUNDOS,
  A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID AS SESSIONID,
  C.MACHINE AS MAQUINA,
  A.OS_USER_NAME AS USUARIO,
  A.ORACLE_USERNAME AS SCHEMA,
  B.OBJECT_NAME AS OBJETO,
  B.OBJECT_TYPE AS TIPO,
  C.INST_ID AS RAC,
  C.PREV_SQL_ID AS SQLID
FROM 
  SYS.GV_$LOCKED_OBJECT A,
  SYS.ALL_OBJECTS B,
  SYS.GV_$SESSION C
WHERE 
  A.OBJECT_ID = B.OBJECT_ID
  AND A.INST_ID = C.INST_ID
  AND C.SID = A.SESSION_ID
ORDER BY 1, 3, 4, 6
"""

SQL_SQLID = """
SELECT SQL_TEXT,
       SQL_FULLTEXT
  FROM SYS.GV_$SQL
 WHERE SQL_ID = %s
   AND INST_ID = %s
"""