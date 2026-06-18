import MySQLdb
from db import get_connection


class StudyDAO:
    def __init__(self):
        self.db = None

    def connect(self):
        if MySQLdb is None:
            raise RuntimeError(
                "mysqlclient가 설치되지 않았습니다. "
                "'python -m pip install mysqlclient'를 실행하세요."
            )

        self.db = get_connection()

    def disconnect(self):
        if self.db:
            self.db.close()

    def add_subject(self, subject):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into subjects (subject_name, description)
                values (%s, %s)
            """
            result = cur.execute(sql, (subject.subject_name, subject.description))
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
                select subject_id, subject_name, description, created_at
                from subjects
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
                select subject_id, subject_name, description, created_at
                from subjects
                where subject_id = %s
            """
            cur.execute(sql, (subject_id,))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def delete_subject(self, subject_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from subjects where subject_id = %s"
            result = cur.execute(sql, (subject_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def count_subject_links(self, subject_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    (select count(*) from tasks where subject_id = %s) as task_count,
                    (select count(*) from study_plans where subject_id = %s) as plan_count,
                    (select count(*) from study_logs where subject_id = %s) as log_count
            """
            cur.execute(sql, (subject_id, subject_id, subject_id))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def add_task(self, task):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into tasks
                    (subject_id, title, content, priority, due_date)
                values
                    (%s, %s, %s, %s, %s)
            """
            data = (
                task.subject_id,
                task.title,
                task.content,
                task.priority,
                task.due_date,
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

    def get_task_by_id(self, task_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    task_id,
                    subject_id,
                    title,
                    content,
                    priority,
                    status,
                    due_date,
                    created_at
                from tasks
                where task_id = %s
            """
            cur.execute(sql, (task_id,))
            return cur.fetchone()
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
            if priority:
                conditions.append("t.priority = %s")
                params.append(priority)
            if status:
                conditions.append("t.status = %s")
                params.append(status)

            where_sql = ""
            if conditions:
                where_sql = "where " + " and ".join(conditions)

            sql = f"""
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
                {where_sql}
                order by t.task_id
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
                where (t.title like concat('%%', %s, '%%')
                or t.content like concat('%%', %s, '%%'))
                order by t.task_id
            """
            cur.execute(sql, (keyword, keyword))
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def update_task(self, task, task_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                update tasks
                set title = %s,
                    content = %s,
                    priority = %s,
                    due_date = %s
                where task_id = %s
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
            sql = "update tasks set status = '완료' where task_id = %s"
            result = cur.execute(sql, (task_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def delete_task(self, task_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from tasks where task_id = %s"
            result = cur.execute(sql, (task_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def add_plan(self, plan):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into study_plans
                    (subject_id, plan_title, plan_date, start_time, end_time, memo)
                values
                    (%s, %s, %s, %s, %s, %s)
            """
            data = (
                plan.subject_id,
                plan.plan_title,
                plan.plan_date,
                plan.start_time,
                plan.end_time,
                plan.memo,
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

    def get_plans(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    p.plan_id,
                    p.subject_id,
                    s.subject_name,
                    p.plan_title,
                    p.plan_date,
                    p.start_time,
                    p.end_time,
                    p.memo,
                    p.created_at
                from study_plans p
                join subjects s on p.subject_id = s.subject_id
                order by p.plan_date, p.plan_id
            """
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def get_plan_by_id(self, plan_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = "select plan_id from study_plans where plan_id = %s"
            cur.execute(sql, (plan_id,))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def delete_plan(self, plan_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from study_plans where plan_id = %s"
            result = cur.execute(sql, (plan_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def add_log(self, log):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into study_logs
                    (subject_id, study_date, study_time, content)
                values
                    (%s, %s, %s, %s)
            """
            data = (log.subject_id, log.study_date, log.study_time, log.content)
            result = cur.execute(sql, data)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def get_logs(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    l.log_id,
                    l.subject_id,
                    s.subject_name,
                    l.study_date,
                    l.study_time,
                    l.content,
                    l.created_at
                from study_logs l
                join subjects s on l.subject_id = s.subject_id
                order by l.study_date desc, l.log_id desc
            """
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def get_log_by_id(self, log_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = "select log_id from study_logs where log_id = %s"
            cur.execute(sql, (log_id,))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def delete_log(self, log_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from study_logs where log_id = %s"
            result = cur.execute(sql, (log_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def add_memo(self, memo):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = """
                insert into task_memos (task_id, memo)
                values (%s, %s)
            """
            result = cur.execute(sql, (memo.task_id, memo.memo))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def get_memos(self, task_id=None):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            where_sql = ""
            params = ()

            if task_id is not None:
                where_sql = "where m.task_id = %s"
                params = (task_id,)

            sql = f"""
                select
                    m.memo_id,
                    m.task_id,
                    t.title,
                    m.memo,
                    m.created_at
                from task_memos m
                join tasks t on m.task_id = t.task_id
                {where_sql}
                order by m.memo_id
            """
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()
            self.disconnect()

    def get_memo_by_id(self, memo_id):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = "select memo_id from task_memos where memo_id = %s"
            cur.execute(sql, (memo_id,))
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()

    def delete_memo(self, memo_id):
        self.connect()
        cur = self.db.cursor()

        try:
            sql = "delete from task_memos where memo_id = %s"
            result = cur.execute(sql, (memo_id,))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()
            self.disconnect()

    def get_summary(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        try:
            sql = """
                select
                    (select count(*) from subjects) as subject_count,
                    (select count(*) from tasks) as task_count,
                    (select count(*) from tasks where status = '완료') as done_count,
                    (select count(*) from tasks where status = '대기') as waiting_count,
                    (select count(*) from study_plans) as plan_count,
                    (select count(*) from study_logs) as log_count,
                    (select ifnull(sum(study_time), 0) from study_logs) as total_time,
                    (select count(*) from task_memos) as memo_count
            """
            cur.execute(sql)
            return cur.fetchone()
        finally:
            cur.close()
            self.disconnect()
