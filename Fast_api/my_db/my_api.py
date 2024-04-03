# pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import my_db_console
import uvicorn

# 创建 FastAPI 应用
app = FastAPI()
# 设置允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 创建数据库管理器实例
db_manager = my_db_console.DatabaseManager("mysql服务器的ip或者域名", "账号", "密码", "数据库名称")

# 添加路径操作装饰器和路径操作函数
@app.get("/")
def demo():
    return {"key": "value"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}

# 处理注册请求的端点(这里的dlzc为你的表名)
@app.post("/register")
async def register(data: dict):
    try:
        # 将数据插入到数据库
        db_manager.insert_data('dlzc', list(data.keys()), list(data.values()))
        return {"msg": "注册成功"}
    except Exception as e:
        # 处理注册失败的情况
        raise HTTPException(status_code=500, detail="注册失败")


# 处理登录请求的端点
@app.post("/login")
async def login(data: dict):
    try:
        # 查询数据库中是否存在对应用户名和密码(这里的dlzc为你的表名)
        query = f"SELECT * FROM dlzc WHERE user_name = '{data['user_name']}' AND pwd = '{data['pwd']}'"
        db_manager.mycursor.execute(query)
        result = db_manager.mycursor.fetchone()

        if result:
            return {"msg": "登录成功"}
        else:
            # 若用户名或密码错误，则返回错误信息
            raise HTTPException(status_code=400, detail="用户名或密码错误")
        
    except Exception as e:
        # 处理服务器内部错误
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 当前端页面向这些端点发送请求时，它应该使用 POST 方法，而不是 GET 方法,使用 POST 方法是强制性的,如果前端页面向这些端点发送 GET 请求，FastAPI 会返回 405 Method Not Allowed 错误

# # get请求在FastApi中测试使用
# # 处理注册请求的端点
# @app.get("/register")
# async def register(user_name: str, pwd: str, phone: str, email: str):
#     try:
#         # 将数据插入到数据库(这里的dlzc为你的表名)
#         db_manager.insert_data('dlzc', ['user_name', 'phone', 'email', 'pwd'], [user_name, pwd, phone, email])
#         return {"msg": "注册成功"}
#     except Exception as e:
#         # 处理注册失败的情况
#         raise HTTPException(status_code=500, detail="注册失败")


# # 处理登录请求的端点
# @app.get("/login")
# async def login(user_name: str, pwd: str):
#     try:
#         # 查询数据库中是否存在对应用户名和密码(这里的dlzc为你的表名)
#         query = f"SELECT * FROM dlzc WHERE user_name = '{user_name}' AND pwd = '{pwd}'"
#         db_manager.mycursor.execute(query)
#         result = db_manager.mycursor.fetchone()

#         if result:
#             return {"msg": "登录成功"}
#         else:
#             # 若用户名或密码错误，则返回错误信息
#             raise HTTPException(status_code=400, detail="用户名或密码错误")
        
#     except Exception as e:
#         # 处理服务器内部错误
#         raise HTTPException(status_code=500, detail="内部服务器错误")

# 启动应用并运行在指定主机和端口
if __name__ == '__main__':
    # 自定义服务器的ip和端口号
    uvicorn.run(app='my_api:app', host="192.168.8.32", port=8010, reload=True)
    # 关闭数据库连接
    db_manager.close_connection()
