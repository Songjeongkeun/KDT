import MySQLdb

class ContactsDAO:
    def __init__(self):
        self.db = None

    def connect(self):
        if MySQLdb is None:
            raise RuntimeError(
                "mysqlclient가 설치되지 않았습니다. "
                "'python -m pip install mysqlclient'를 실행하세요."
            )

        self.db = MySQLdb.connect(host='localhost', user='apple', password='1111', db='ai', charset='utf8')

    def disconnect(self):
        if self.db:
            self.db.close()

    def insert(self, contact):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into phonebook (name, phone, address)
                values (%s, %s, %s)
            """
            data = (contact.name, contact.phone, contact.address)
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def select_all(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select name, phone, address
                from phonebook
                order by name asc, phone asc
            """
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def search_all(self, keyword):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select name, phone, address
                from phonebook
                where (name like concat('%%', %s, '%%')
                or phone like concat('%%', %s, '%%'))
                order by name asc, phone asc
            """
            
            # select name, phone, address from phonebook where name or phone like concat('%%', %s, '%%')
            # cur.execute(sql)
            cur.execute(sql, (keyword, keyword))
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def search(self, phone):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select name, phone, address
                from phonebook
                where phone = %s
            """
            cur.execute(sql, (phone,))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def update(self, contact, old_phone):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                update phonebook
                set name = %s, phone = %s, address = %s
                where phone = %s
            """
            data = (
                contact.name,
                contact.phone,
                contact.address,
                old_phone,
            )
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def delete(self, phone):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from phonebook where phone = %s"
            result = cur.execute(sql, (phone,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()
