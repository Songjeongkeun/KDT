# online_store_dao.py
import MySQLdb

from db import get_connect

class OnlineStoreDAO:
    def __init__(self):
        self.db = None
        
    def connect(self):
        self.db = get_connect()
        
    def disconnect(self):
        if self.db:
            self.db.close()
            
    def find_membership(self, keyword):
        # keyword = username or email
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT username, email
                FROM member
                WHERE username = %s
                OR email = %s
            """
            
            data = (keyword, keyword)
            cur.execute(sql, data)
            return cur.fetchone()
        
        finally:
            cur.close()
            self.disconnect()
            
    def insert_membership(self, membership):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """
                INSERT INTO member (username, password, name, email)
                VALUES (%s, %s, %s, %s)
            """
            
            data = (membership.username, membership.password, membership.name, membership.email)
            
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        
        except Exception:
            self.db.rollback()
            raise
            
        finally:
            cur.close()
            self.disconnect()
        
    def login(self, username, password):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT id, name
                FROM member
                WHERE username = %s
                AND password = %s
            """
            data = (username, password)
            cur.execute(sql, data)
            return cur.fetchone()
        
        finally:
            cur.close()
            self.disconnect()
        
    def get_product_list(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT id, name, price, stock
                FROM product
                ORDER BY id
            """
            cur.execute(sql)
            return cur.fetchall()
        
        finally:
            cur.close()
            self.disconnect()    
            
    def search_product_list(self, keyword):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT id, name, price, stock
                FROM product
                WHERE name
                LIKE CONCAT("%%", %s, "%%")
                ORDER BY id
            """
            data = (keyword,)
            cur.execute(sql, data)
            return cur.fetchall()
        
        finally:
            cur.close()
            self.disconnect()
            
    def find_product(self, product_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT stock, price
                FROM product
                WHERE id = %s
            """
            
            data = (product_id,)
            cur.execute(sql, data)
            return cur.fetchone()
        
        finally:
            cur.close()
            self.disconnect()
            
    def create_order(self, order_header, item):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            order_header_sql = """
                INSERT INTO order_header (member_id, total_price, status)
                VALUES (%s, %s, %s)
            """   
            order_header_data = (order_header.member_id, order_header.total_price, order_header.status)
            
            cur.execute(order_header_sql, order_header_data) 
            order_id = cur.lastrowid

            order_item_sql = """
                INSERT INTO order_item (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            order_item_data = (order_id, item.product_id, item.quantity, item.price)
            
            cur.execute(order_item_sql, order_item_data)
            
            update_stock_sql = """
                UPDATE product
                SET stock = stock - %s
                WHERE id = %s
            """        
            update_stock_data = (item.quantity, item.product_id)
            
            cur.execute(update_stock_sql, update_stock_data)
            
            self.db.commit()
            return order_id
        except Exception:
            self.db.rollback()
            raise
        
        finally:
            cur.close()
            self.disconnect()
            
    def select_order_list(self, member_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT id, total_price, status, created_at
                FROM order_header
                WHERE member_id = %s
                ORDER BY id
            """
            data = (member_id,)
            cur.execute(sql, data)
            return cur.fetchall()
        
        finally:
            cur.close()
            self.disconnect()
    
    def select_order_header(self, order_id, member_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT
                    oh.id AS id,
                    oh.member_id,
                    oh.total_price,
                    oh.status,
                    oh.created_at,
                    pr.name AS product_name,
                    oi.quantity,
                    oi.price,
                    p.id AS payment_id,
                    p.method,
                    p.paid_amount,
                    p.paid_at
                FROM order_header AS oh
                INNER JOIN order_item AS oi
                ON oh.id = oi.order_id
                INNER JOIN product AS pr
                ON oi.product_id = pr.id
                LEFT JOIN payment AS p
                ON oh.id = p.order_id
                WHERE oh.id = %s AND oh.member_id = %s     
            """
            data = (order_id, member_id)
            cur.execute(sql, data)
            return cur.fetchone()
        
        finally:
            cur.close()
            self.disconnect()

    def select_ready_order_list(self, member_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                SELECT id, total_price, status, created_at
                FROM order_header
                WHERE member_id = %s
                AND status = 'ready'
                ORDER BY id
            """
            data = (member_id,)
            cur.execute(sql, data)
            return cur.fetchall()

        finally:
            cur.close()
            self.disconnect()

    def pay_order(self, payment):
        self.connect()
        cur = self.db.cursor()

        try:
            pay_sql = """
                INSERT INTO payment (order_id, method, paid_amount)
                VALUES (%s, %s, %s)
            """
            pay_data = (payment.order_id, payment.method, payment.paid_amount)
            cur.execute(pay_sql, pay_data)

            order_sql = """
                UPDATE order_header
                SET status = 'paid'
                WHERE id = %s
                AND status = 'ready'
            """
            order_data = (payment.order_id,)
            cur.execute(order_sql, order_data)

            self.db.commit()
            
        except Exception:
            self.db.rollback()
            raise

        finally:
            cur.close()
            self.disconnect()
        
