SQL_LOCKS = """
SELECT C.SECONDS_IN_WAIT AS TEMPO,
       C.SID,
       A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID AS SESSIONID,
       C.MACHINE AS MAQUINA,
       A.OS_USER_NAME AS USUARIO,
       A.ORACLE_USERNAME AS ORACLEDB,
       TO_CHAR(WM_CONCAT(B.OBJECT_NAME)) AS OBJETOS,
       B.OBJECT_TYPE AS OBJETOTIPO,
       C.PROCESS AS PROCESSO,
       C.INST_ID AS RAC,
       C.SQL_ADDRESS,
       C.PREV_SQL_ID,
       COUNT(1) AS QTD_LOCKED
  FROM SYS.GV_$LOCKED_OBJECT A,
       SYS.ALL_OBJECTS B,
       SYS.GV_$SESSION C
 WHERE A.OBJECT_ID = B.OBJECT_ID
   AND A.INST_ID = C.INST_ID
   AND C.SID = A.SESSION_ID
   AND C.SECONDS_IN_WAIT >= %s
 GROUP BY C.SECONDS_IN_WAIT,
          C.SID,
          A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID,
          C.MACHINE,
          A.OS_USER_NAME,
          A.ORACLE_USERNAME,
          B.OBJECT_TYPE,
          C.PROCESS,
          C.INST_ID,
          C.SQL_ADDRESS,
          C.PREV_SQL_ID
 ORDER BY SECONDS_IN_WAIT DESC, 5 DESC
"""