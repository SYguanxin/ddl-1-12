from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:csm.zhinai.123@localhost/PYTODO'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    ifdone = db.Column(db.Boolean, db.ForeignKey("done.id"), default=False)
    insert_time = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.func.now())
    ddl = db.Column(db.TIMESTAMP(True))
    href = db.Column(db.String(100), server_default="http://127.0.0.1:5000/items/")

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Done(db.Model):
    id = db.Column(db.Boolean, primary_key=True)
    items = db.relationship('Item', lazy='dynamic')


@app.before_first_request
def init_db():
    db.create_all()
    if Done.query.first() is not None: return
    subdone = Done(id=False)
    done = Done(id=True)
    db.session.add_all([subdone, done])
    db.session.commit()


# 增
@app.route("/items", methods=["POST"])
def add():
    js = request.get_json()
    item = Item(title=js['title'], body=js['body'], ddl=js['ddl'])
    db.session.add(item)
    db.session.flush()
    item.href += str(item.id)
    db.session.commit()
    item = Item.query.order_by(Item.id.desc()).first().to_json()
    return {
        "code": 200,
        "msg": "增加成功",
        "data": {
            "items": [item],
        }
    }


# 删
@app.route("/items", methods=["DELETE"])
def delete():
    del_code = request.args.get('del_code').lower()
    if del_code in ["true", "false", "all"]:
        if del_code == "true":
            ifdone = Done.query.get_or_404(True)
            items = ifdone.items
        elif del_code == "false":
            ifdone = Done.query.get_or_404(False)
            items = ifdone.items
        elif del_code == "all":
            items = Item.query.all()
        for item in items:
            db.session.delete(item)
        db.session.commit()
        return {
            "code": 200,
            "msg": "删除成功",
            "data": {}
        }
    else:
        return {
            "code": 406,
            "msg": "请输入del_code",
            "data": {}
        }


# 删<id>
@app.route("/items/<int:id>", methods=["DELETE"])
def id_delete(id=None):
    item = Item.query.get(id)
    if item is None:
        return {
            "code": 404,
            "msg": "资源不存在id=%s" % id
        }
    db.session.delete(item)
    db.session.commit()
    return {
        "code": 200,
        "msg": "删除成功title=%s" % item.title,
        "data": {}
    }


# 改
@app.route("/items", methods=["PUT"])
def update():
    code = request.args.get('code').lower()
    if code == "true":
        ifdone = Done.query.get_or_404(True)
        items = ifdone.items.all()
        done_code = "0"
    elif code == "false":
        ifdone = Done.query.get_or_404(False)
        items = ifdone.items.all()
        done_code = "1"
    else:
        return {
            "code": 406,
            "msg": "请输入正确的code"
        }
    for i in range(len(items)):
        items[i].ifdone ^= True
    db.session.commit()
    return redirect(url_for('loading', ifdone=done_code))


# 改<id>
@app.route("/items/<int:id>", methods=["PUT"])
def id_update(id=None):
    item = Item.query.get(id)
    if item is None:
        return {
            "code": 404,
            "msg": "未找到数据id=%s" % id
        }
    item.ifdone ^= True
    db.session.commit()
    return redirect(url_for('id_loading', id=id))


# 查
@app.route("/items", methods=["GET"])
def loading():
    page = request.args.get('page')
    ifdone = request.args.get('ifdone')
    sch = request.args.get('sch')

    if page is None:
        page = 1
    else:
        page = int(page)
    if ifdone is not None:
        ifdone = bool(int(ifdone))
        ifdone = Done.query.get_or_404(ifdone)
        items_ = ifdone.items.paginate(page=page, per_page=10)
        result_count = items_.total
        items_ = items_.items
        items = []
        for i in range(len(items_)):
            items.append(items_[i].to_json())
        msg = "查询ifdone=%s" % ifdone.id
    elif sch is not None:
        items = Item.query.filter(Item.body.contains(sch)).order_by(Item.id.asc()) \
            .paginate(page=page, per_page=10)
        result_count = items.total
        items = items.items
        for i in range(len(items)):
            items[i] = items[i].to_json()
        msg = "关键词查询sch=%s" % sch
    else:
        items = Item.query.order_by(Item.id.asc()).paginate(page=page, per_page=10)
        result_count = items.total
        items = items.items
        for i in range(len(items)):
            items[i] = items[i].to_json()
        msg = "查询全部"
    if not items:
        return {
            "code": 404,
            "msg": "未查找到数据",
        }
    return {
        "code": 200,
        "msg": msg,
        "data": {
            "items": items,
            "page": page,
            "total_result": result_count
        }
    }


# 查<id>
@app.route("/items/<int:id>", methods=["GET"])
def id_loading(id=None):
    item = Item.query.get(id)
    if item is not None:
        item = item.to_json()
        items = [item]
    else:
        items = []
    msg = "查询id=%s" % id
    if not items:
        return {
            "code": 404,
            "msg": "未查找到数据id=%s" % id,
        }
    return {
        "code": 200,
        "msg": msg,
        "data": {
            "items": items,
        }
    }


app.run()
