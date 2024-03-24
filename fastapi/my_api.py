# pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
from fastapi import FastAPI
import uvicorn
import my_db_console

# 获取FastAPI的实例
app = FastAPI()

# 添加路径操作装饰器和路径操作函数
@app.get("/")
def demo():
    return {"key": "value"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}

# 添加注册接口
@app.get("/register")
async def register(user_name: str, phone: str, age: int, email: str):
    if my_db_console.insert_zhuce(user_name, phone, age, email) == 200:
        return {"msg": "注册成功"}
    else:
        return {"msg": "注册失败"}

# 为了避免热重载你可以将reload内的参数设置为False,测试的时候建议True
if __name__ == '__main__':
    uvicorn.run(app='my_api:app', host="127.0.0.1", port=8010, reload=True)
