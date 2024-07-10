import pymysql as mysql
from pymysql.cursors import DictCursor


class SQLConnect:

    def __init__(self, tpz, host, port, db, user, password):
        self.tpz = tpz
        self.host = host
        self.port = int(port)
        self.db = db
        self.user = user
        self.pwd = password
        self.conn = None

    def connect(self):
        """得到连接信息"""
        if self.tpz == "mysql":
            self.conn = mysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, port=self.port,
                                      cursorclass=DictCursor, charset='utf8')
        else:
            raise RuntimeError("不支持的数据库类型")
        cur = self.conn.cursor()
        if not cur:
            raise RuntimeError("连接数据库失败")
        else:
            return cur

    def query(self, sql):
        """执行查询语句"""
        cur = self.connect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList[0] if len(resList) == 1 else resList

    def exec(self, sql):
        """执行非查询语句"""
        cur = self.connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
