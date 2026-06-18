# study_dao.py
import MySQLdb

class StudyDAO:
    def __init__(self):
        self.db = None
        
    def connect(self):
        if MySQLdb is None:
            raise RuntimeError(
                "mysqlclient가 설치되지 않았습니다."
                "'python3 -m pip install mysqlclient를 실행하세요."
            )
        self.db = MySQLdb.connect(host='localhost', user='apple', password='1111', db='study_manager', charset='utf8')
        
    def disconnect(self):
        if self.db:
            self.db.close()
            
    def add_subject(self, subject):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """ 
                INSERT INTO subjects (subject_name, description)
                VALUES (%s, %s)
            """
            data = (subject.subject_name, subject.description)
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()
            
    def get_subjects(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT subject_id, subject_name, description, created_at
                FROM subjects
                order by subject_id
            """
            
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()
            
    def get_subject_by_id(self, subject_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT subject_id, subject_name, description, created_at
                FROM subjects
                WHERE subject_id = %s
            """
            data = (subject_id,)
            cur.execute(sql, data)
            return cur.fetchone()
        
        finally:
            cur.close()
            self.disconnect()
            
    def count_subject_links(self, subject_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                (SELECT count(*) 
                FROM tasks 
                WHERE subject_id = %s)
                AS task_count,
                (SELECT count(*)
                FROM study_plans 
                WHERE subject_id = %s)
                AS plan_count,
                (SELECT count(*)
                FROM study_logs
                WHERE subject_id = %s)
                AS log_count            
            """
            data = (subject_id, subject_id, subject_id)
            cur.execute(sql, data)
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()
            
    def delete_subject(self, subject_id):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """
                DELETE FORM subjects
                WHERE subject_id = "%s"
            """
            data = (subject_id, )
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()
    
            
    def add_task(self, task):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """
                INSERT INTO tasks (subject_id, title, content, priority, due_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            data = (task.subject_id, task.title, task.content, task.priority, task.due_date)
            
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        
        except Exception:
            self.db.rollback()
            raise
        
        finally:
            cur.close()
            self.disconnect()
            
    def get_tasks(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    t.task_id,
                    t.subject_id,
                    s.subject_name,
                    t.title,
                    t.content,
                    t.priority,
                    t.status,
                    t.due_date,
                    t.created_at
                from tasks t
                join subjects s on t.subject_id = s.subject_id
                order by t.task_id
            """
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()  
            
    def filter_tasks(self, subject_id=None, priority=None, status=None):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            conditions = []
            params = []
            
            if subject_id is not None:
                conditions.append("t.subject_id = %s")
                params.append(subject_id)
            
            if priority is not None:
                conditions.append("t.priority = %s")
                params.append(priority)
                
            if status:
                conditions.append("t.status = %s")
                params.append(status)
                
            where_sql = ""
            if conditions:
                where_sql = "WHERE " + " AND ".join(conditions)
                
            sql = """
                
            """
            