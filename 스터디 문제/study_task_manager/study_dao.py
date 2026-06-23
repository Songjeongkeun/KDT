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
        self.db = MySQLdb.connect(
            host='localhost', user='apple', password='1111', db='study_manager', charset='utf8')

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
                (SELECT COUNT(*) 
                FROM tasks 
                WHERE subject_id = %s)
                AS task_count,
                (SELECT COUNT(*)
                FROM study_plans 
                WHERE subject_id = %s)
                AS plan_count,
                (SELECT COUNT(*)
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
        # print("test")
        try:
            sql = """
                INSERT INTO tasks (subject_id, title, content, priority, due_date)
                VALUES (%s, %s, %s, %s, %s)
            """

            data = (task.subject_id, task.title, task.content,
                    task.priority, task.due_date)

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
                SELECT
                    t.task_id,
                    t.subject_id,
                    s.subject_name,
                    t.title,
                    t.content,
                    t.priority,
                    t.status,
                    t.due_date,
                    t.created_at
                FROM tasks t
                JOIN subjects s ON t.subject_id = s.subject_id
                ORDER BY t.task_id
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

            sql = f"""
                SELECT
                    t.task_id,
                    t.subject_id,
                    s.subject_name,
                    t.title,
                    t.content,
                    t.priority
                    t.status,
                    t.due_date,
                    t.created_at
                FROM tasks t
                JOIN subjects s ON t.subject_id = s.subject_id
                {where_sql}
                ORDER BY t.task_id
            """
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def search_tasks(self, keyword):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                SELECT
                    t.task_id,
                    t.subject_id,
                    s.subject_name,
                    t.title,
                    t.content,
                    t.priority,
                    t.status,
                    t.due_date,
                    t.created_at
                FROM tasks t
                JOIN subjects s ON t.subject_id = s.subject_id
                WHERE (t.title LIKE CONCAT('%%', %s, '%%')
                OR (t.content LIKE CONCAT('%%', %s, '%%'))
                ORDER BY t.task_id
                """
            data = (keyword, keyword)
            cur.execute(sql, data)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()
            
    def get_task_by_id(self, task_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            sql = """
                SELECT
                    task_id,
                    title,
                    content,
                    priority,
                    status,
                    due_date,
                    created_at
                FROM tasks 
                WHERE task_id = '%s'               
            """
            
            data = (task_id,)
            cur.execute(sql, data)
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()
            
    def update_task(self, task, task_id):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """
                UPDATE tasks
                SET title = %s,
                    content = %s,
                    priority = %s,
                    due_date = %s
                WHRER task_id = %s
            """
            
            data = (task.title, task.content, task.priority, task.due_date, task_id)
            
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        
        except Exception:
            self.db.rollback()
            raise
        
        finally:
            cur.close()
            self.disconnect()
            
    def complete_task(self, task_id):
        self.connect()
        cur = self.db.cursor()
        
        try:
            sql = """
                UPDATE tasks 
                SET status = '완료'
                WHERE task_id = %s
            """
            data = (task_id,)
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()
        
            
             