# pip install mysql-connector-python -i https://pypi.tuna.tsinghua.edu.cn/simple
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            charset='utf8',
            password=password,
            database=database
        )
        self.mycursor = self.mydb.cursor()

    # 检查表是否存在
    def table_exists(self, table_name):
        self.mycursor.execute("SHOW TABLES LIKE %s", (table_name,))
        return self.mycursor.fetchone()

    # 创建新表
    def create_table(self, table_name, columns):
        if not self.table_exists(table_name):
            create_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
            self.mycursor.execute(create_query)
            self.mydb.commit()
            print(f"表 '{table_name}' 创建成功.")
        else:
            print(f"表 '{table_name}' 已存在，无需创建.")

    # 插入数据
    def insert_data(self, table_name, columns, values, num_rows=1, allow_duplicates=False):
        if self.table_exists(table_name):
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s' for _ in values])
            insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            try:
                total_rows_inserted = 0
                for _ in range(num_rows):
                    if not allow_duplicates and self.check_duplicate_data(table_name, columns, values):
                        print("不允许插入重复数据.")
                        continue

                    # 将values转换为元组形式传递给execute方法
                    self.mycursor.execute(insert_query, tuple(values))
                    total_rows_inserted += 1
                
                self.mydb.commit()
                print(f"{total_rows_inserted} 条记录成功插入到表 '{table_name}' 中.")
            except mysql.connector.Error as err:
                print(f"插入数据时发生错误: {err}")
        else:
            print(f"表 '{table_name}' 不存在，无法插入记录.")


    # 检查是否存在重复数据
    def check_duplicate_data(self, table_name, columns, values):
        select_query = f"SELECT * FROM {table_name} WHERE {' AND '.join([f'{col}=%s' for col in columns])}"
        
        self.mycursor.execute(select_query, values)
        result = self.mycursor.fetchone()
        
        return result is not None


    # 删除表
    def drop_table(self, table_name):
        if self.table_exists(table_name):
            drop_query = f"DROP TABLE {table_name}"
            self.mycursor.execute(drop_query)
            print(f"表 '{table_name}' 已删除.")
        else:
            print(f"表 '{table_name}' 不存在，无需删除.")


    # 删除符合条件的记录
    def delete_record(self, table_name, condition):
        if self.table_exists(table_name):
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            self.mycursor.execute(delete_query)
            self.mydb.commit()
            print(f"已从表 '{table_name}' 中删除符合条件 '{condition}' 的记录.")
        else:
            print(f"表 '{table_name}' 不存在，无法删除记录.")


    # 添加新字段
    def add_column(self, table_name, column_name, column_type):
        if self.table_exists(table_name):
            alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            try:
                self.mycursor.execute(alter_query)
                print(f"成功向表 '{table_name}' 中添加字段 '{column_name}'.")
            except mysql.connector.Error as err:
                print(f"添加字段时发生错误: {err}")
        else:
            print(f"表 '{table_name}' 不存在，无法添加字段.")


    # 删除字段
    def drop_column(self, table_name, column_name):
        if self.table_exists(table_name):
            alter_query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            try:
                self.mycursor.execute(alter_query)
                print(f"成功从表 '{table_name}' 中删除字段 '{column_name}'.")
            except mysql.connector.Error as err:
                print(f"删除字段时发生错误: {err}")
        else:
            print(f"表 '{table_name}' 不存在，无法删除字段.")


    # 关闭数据库连接
    def close_connection(self):
        self.mycursor.close()
        self.mydb.close()


    # 查询记录
    def select_data(self, table_name, columns=None, condition=None):
        if self.table_exists(table_name):
            if columns:
                columns_str = ', '.join(columns)
            else:
                columns_str = '*'

            select_query = f"SELECT {columns_str} FROM {table_name}"
            if condition:
                select_query += f" WHERE {condition}"

            self.mycursor.execute(select_query)
            result = self.mycursor.fetchall()
            if result:
                for row in result:
                    print(row)
            else:
                print("未找到符合条件的记录.")
        else:
            print(f"表 '{table_name}' 不存在，无法查询记录.")


# 使用DatabaseManager类的示例
# 服务器地址,用户名,密码,数据库名(这里用做测试)
db_manager = DatabaseManager("mysql服务器的ip或者域名", "账号", "密码", "数据库名称")

# 以下是增删改查的演示
# 新建表
# db_manager.create_table('dlzc', [
#     'user_name VARCHAR(255)',
#     'pwd VARCHAR(20)',
#     'phone VARCHAR(20)',
#     'email VARCHAR(255)'
# ])

# 删除表
# db_manager.drop_table('test')

# 插入数据
# num_rows=设置插入条数, allow_duplicates=是否插入重复的数据,默认插入1条并且不重复
# db_manager.insert_data('test', ['user_name', 'phone', 'email', 'pwd'], ['test', '999', 'test@gmail.com', '888666'])

# 删除记录
# db_manager.delete_record('test', "user_name = '2'")

# 添加新字段
# db_manager.add_column('test', 'age', 'VARCHAR(20)')

# 删除字段
# db_manager.drop_column('test', 'age')

# 查询表中所有记录
# db_manager.select_data('test')
            
# 根据条件查询指定列
# db_manager.select_data('test', columns=['user_name', 'phone', 'email', 'pwd'], condition="user_name='Edward'")
    
# 关闭连接
db_manager.close_connection()