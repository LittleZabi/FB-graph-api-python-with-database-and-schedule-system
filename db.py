import sqlite3
from datetime import datetime


class SQL:
    def __init__(self):
        self.db = './database.db'
        self.con = sqlite3.connect(self.db)
        # self.createTable()
        self.table = 'posts'

    def createTable(self):
        sql = """
            CREATE TABLE posts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type CHAR(255) NOT NULL,
                source CHAR(1024) NOT NULL,
                caption CHAR(1024),
                post_on CHAR(255),
                posted TINYINT DEFAULT 0,
                post_id INTEGER,
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TINYINT DEFAULT 1
            )
            """

        k = self.con.execute(sql)
        return k

    def dropTable(self):
        sql = 'DROP TABLE posts'
        self.con.execute(sql)
        self.con.commit()

    def newPost(self, **args):
        sql = F'INSERT INTO {self.table}(type,source,caption,post_on) VALUES('
        i = 0
        for arg in args:
            if i == 0:
                sql += f"'{args[arg]}'"
            else:
                sql += f",'{args[arg]}'"
            i += 1
        sql += ');'
        j = self.con.execute(sql)
        self.con.commit()
        print('success')
        return 'success'

    def getPost(self, id):
        sql = f'SELECT * FROM {self.table} WHERE id = {id}'
        c = self.con.execute(sql)
        print(c)
        return c

    def close(self):
        self.con.close()

    def log(self, t):
        print(t)

    def delete(self, id):
        sql = f"DELETE FROM {self.table} WHERE id = {id}"
        self.con.execute(sql)
        self.con.commit()
        return 'success'

    def posted(self, id, post_id=0):
        print('update: ', id, post_id)
        try:
            post_id = int(post_id)
            sql = f"UPDATE {self.table} SET posted = 1, post_id = {post_id} WHERE id = {id}"
            self.con.execute(sql)
            self.con.commit()
            return 'success'
        except Exception as e:
            log(f'On posted Error: {e} \n Not Updated')

    def getAll(self):
        c = self.con.execute('SELECT * FROM posts').fetchall()
        return c

    def getDate(self, date=False):
        """
            get Date take date parameter if its false then its return today date
            Enter date format like dd/mm/yyyy
        """
        if date == False:
            return datetime.now().strftime("%Y/%m/%d 00:00:00")
        d = date.split('/')[0]
        m = date.split('/')[1]
        y = date.split('/')[2]
        return datetime(int(y), int(m), int(d))

    def getByDate(self, date):
        sql = f"SELECT * FROM posts WHERE datetime(posts.post_on) = '{date}' AND posted = 0"
        c = self.con.execute(sql)
        return c.fetchall()


if __name__ == '__main__':
    sql = SQL()
    # sql.dropTable()
    # sql.createTable()
    # post = sql.posted(1, 12322)
    # post = sql.getPost(1)
    posts = sql.getAll()
    for k in posts:
        print(k)
    # sql.delete(6)
    # print('-----------------------')
    # post = sql.getByDate(posts.getDate())
    # # print(post)
    # for k in post:
    #     print(k)
    # type_ = 'text'
    # source_ = 'hello world'
    # caption_ = ''
    # post_on_ = '2/2/2022'
    # sql.newPost(type=type_, source=source_,
    #             caption=caption_, post_on=post_on_)
