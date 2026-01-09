import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from .config import DATABASE_PATH


class DatabaseManager:
    """SQLite数据库管理器"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',  -- pending, approved, rejected
                    approved_at TIMESTAMP NULL,
                    approved_by INTEGER NULL,
                    rejected_at TIMESTAMP NULL,
                    rejected_by INTEGER NULL,
                    notes TEXT
                )
            ''')



            conn.commit()

    def approve_user(self, telegram_id: int, approved_by: int, notes: str = None) -> bool:
        """同意用户加入群组"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                from datetime import datetime
                cursor.execute('''
                    UPDATE users
                    SET status = 'approved', approved_at = ?, approved_by = ?, notes = ?
                    WHERE telegram_id = ?
                ''', (datetime.now(), approved_by, notes, telegram_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"同意用户失败: {e}")
            return False

    def reject_user(self, telegram_id: int, rejected_by: int, notes: str = None) -> bool:
        """拒绝用户加入群组"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                from datetime import datetime
                cursor.execute('''
                    UPDATE users
                    SET status = 'rejected', rejected_at = ?, rejected_by = ?, notes = ?
                    WHERE telegram_id = ?
                ''', (datetime.now(), rejected_by, notes, telegram_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"拒绝用户失败: {e}")
            return False

    def get_user_status(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """获取用户状态"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT status, approved_at, approved_by, rejected_at, rejected_by, notes
                    FROM users
                    WHERE telegram_id = ?
                ''', (telegram_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        'status': row[0],
                        'approved_at': row[1],
                        'approved_by': row[2],
                        'rejected_at': row[3],
                        'rejected_by': row[4],
                        'notes': row[5]
                    }
                return None
        except sqlite3.Error as e:
            print(f"获取用户状态失败: {e}")
            return None

    def get_pending_users(self) -> List[Dict[str, Any]]:
        """获取待审核用户列表"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT telegram_id, username, first_name, last_name, joined_at, notes
                    FROM users
                    WHERE status = 'pending'
                    ORDER BY joined_at DESC
                ''')
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"获取待审核用户失败: {e}")
            return []

    def get_approved_users(self) -> List[Dict[str, Any]]:
        """获取已同意用户列表"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT u.telegram_id, u.username, u.first_name, u.last_name,
                           u.approved_at, u.approved_by, a.username as admin_username, u.notes
                    FROM users u
                    LEFT JOIN users a ON u.approved_by = a.telegram_id
                    WHERE u.status = 'approved'
                    ORDER BY u.approved_at DESC
                ''')
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"获取已同意用户失败: {e}")
            return []

    def is_user_approved(self, telegram_id: int) -> bool:
        """检查用户是否已同意"""
        status_info = self.get_user_status(telegram_id)
        return status_info and status_info['status'] == 'approved'

    def create_user(self, telegram_id: int, username: str = None,
                   first_name: str = None, last_name: str = None) -> bool:
        """创建新用户"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO users
                    (telegram_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (telegram_id, username, first_name, last_name))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"创建用户失败: {e}")
            return False

    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, row))
                return None
        except sqlite3.Error as e:
            print(f"获取用户信息失败: {e}")
            return None

    # ========== 管理员管理方法 ==========
        """创建订单"""
        try:
            from datetime import datetime, timedelta
            expire_at = datetime.now() + timedelta(minutes=expire_minutes)

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO orders
                    (telegram_user_id, out_trade_no, payment_type, amount, expire_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (telegram_user_id, out_trade_no, payment_type, amount, expire_at.isoformat()))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"创建订单失败: {e}")
            return False


    # ========== 统计方法 ==========

    def get_users_count(self) -> int:
        """获取总用户数量"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM users')
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"获取用户数量失败: {e}")
            return 0
