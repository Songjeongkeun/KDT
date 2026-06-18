CREATE DATABASE IF NOT EXISTS study_manager;

USE study_manager;

DROP TABLE IF EXISTS task_memos;
DROP TABLE IF EXISTS study_logs;
DROP TABLE IF EXISTS study_plans;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS subjects;

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    priority VARCHAR(10) DEFAULT '보통',
    status VARCHAR(10) DEFAULT '대기',
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tasks_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE RESTRICT
);

CREATE TABLE study_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    plan_title VARCHAR(100) NOT NULL,
    plan_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    memo VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_study_plans_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE RESTRICT
);

CREATE TABLE study_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    study_date DATE NOT NULL,
    study_time INT DEFAULT 0,
    content VARCHAR(300) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_study_logs_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE RESTRICT
);

CREATE TABLE task_memos (
    memo_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    memo VARCHAR(300) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_task_memos_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id)
        ON DELETE CASCADE
);
