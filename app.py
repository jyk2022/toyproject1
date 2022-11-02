from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, timezone, datetime
import certifi
import requests
import uuid

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "guhaejo-secret"
now = datetime.now()
ca = certifi.where()

# JWT config
jwt = JWTManager(app)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_CSRF_IN_COOKIES'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)

# JWT without authorization
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for('login_page'))

# DB information
client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.guhaejo

# Crawling config
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://news.daum.net/digital/#1', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/home')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    print(current_user)
    if not current_user:
        return redirect(url_for('login_page'))

    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=["POST"])
def login():
    user_email = request.form['email_give']
    user_password = request.form['password_give']

    user = db.user.find_one({'email': user_email})

    if user is None:
        return jsonify({'msg': "이메일이 존재하지 않습니다."});
    if check_password_hash(user['password'], user_password) is False:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.'});

    access_token = create_access_token(identity=user['email'])
    refresh_token = create_refresh_token(identity=user['email'])

    response = jsonify({'flag': 1})

    # Save tokens into cookie storage
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200

@app.route("/signup", methods=["POST"])
def sign_up():
    nickname_receive = request.form['nickname_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    confirm_password_receive = request.form['confirm_password_give']

    print(nickname_receive, email_receive, password_receive)
    # Validation
    if nickname_receive == "":
        return jsonify({'msg': '닉네임을 입력해주세요'})
    elif password_receive == "":
        return jsonify({'msg': '비밀번호를 입력해주세요'})
    elif email_receive == "":
        return jsonify({'msg': '이메일을 입력해주세요'})

    if password_receive != confirm_password_receive:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다'})

    check_dup_email = db.user.find_one({'email': email_receive})
    if check_dup_email is None:
        doc = {
            'nickname': nickname_receive,
            'email': email_receive,
            'password': generate_password_hash(password_receive)
        }
        db.user.insert_one(doc)
    elif check_dup_email['email'] == email_receive:
        return jsonify({'msg': '이미 가입된 이메일 입니다.'})

    return jsonify({'flag': 1})

@app.route("/guhaejo", methods=["GET"])
def board_get():
    board_list = list(db.article.find({}, {'_id': False}))
    return jsonify({'board_list': board_list})

@app.route("/guhaejo/news", methods=["GET"])
def news_get():
    news = soup.select('body > div.container-doc.cont-category > main > section > div.main-sub > div.box_g.box_news_major > ul > li')
    news_list = []
    for new in news:
        news_title = new.select_one('strong > a').text
        news_url = new.select_one('strong > a')['href']
        news_company = new.select_one('strong > span').text
        doc={
            'url': news_url,
            'title' : news_title,
            'company' : news_company}
        news_list.append(doc)
    return jsonify({'news_list': news_list})

@app.route("/guhaejo/todos", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']
    id_receive = request.form['id_give']

    todo_list = list(db.todos.find({},{'_id':False}))
    num = uuid.uuid4().hex
    doc = {
        'num':num,
        'todo':todo_receive,
        'id': id_receive,
        'done': 0
    }
    db.todos.insert_one(doc)
    return jsonify('msg',"등록 완료")

@app.route("/guhaejo/todos/done", methods=["POST"])
def todo_done():
    num_receive = request.form['num_give']
    done_receive = request.form['done_give']
    if int(done_receive) == 0:
        db.todos.update_one({'num': num_receive}, {'$set': {'done': 1}})
        return jsonify({'msg': '완료!'})
    else:
        db.todos.update_one({'num': num_receive}, {'$set': {'done': 0}})
        return jsonify({'msg': '다시!'})

@app.route("/guhaejo/todos", methods=["GET"])
def todo_get():
    todo_list = list(db.todos.find({},{'_id':False}))
    return jsonify({'todos': todo_list})

@app.route("/guhaejo/todos/delete", methods=["POST"])
def todo_delete():
    num_receive = request.form['num_give']
    db.todos.delete_one({'num': num_receive})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/guhaejo/review", methods=["GET"])
def web_reivews_get():
    img_list = ['https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhyundai_autoever-logo.4ac170ea.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fyeogi-logo.8550ea49.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fkbbank-logo.cc16ad1a.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fjinhak-logo.7b03c373.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fmegazonecloud-logo.5c1b17fe.png&w=2048&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ffinda-logo.2b20b042.png&w=256&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhana-logo.4da14aa2.png&w=1920&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbalaan-logo.ced9ed54.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcafe24-logo.92bd253e.png&w=384&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fnewploy-logo.5ca6c380.png&w=3840&q=75',
                ]
    url = 'https://hanghae99.spartacodingclub.kr'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    reviews = soup.select('#__next > section > section.css-1pxpne5 > div > div.css-1y4ubqo > div.css-1ldg707')
    reviews_list = []
    for review in reviews:
        a = review.select_one('h3')
        if a is not None:
            title = review.select_one('h3').text
            company = review.select_one('p').text
            comment = review.select_one('p:last-child').text
            review_obj = {'title':title, 'company':company, 'comment':comment}
            reviews_list.append(review_obj)
    return jsonify({'reviews' : reviews_list, 'imgList': img_list})

@app.route("/guhaejo/view-count", methods=["POST"])
def view_count_post():
    post_num_receive = request.form['post_num']
    view_count_receive = request.form['view_count']
    db.article.update_one({'post_num': int(post_num_receive)},{'$set':{'view_count': int(view_count_receive)}})
    return jsonify('msg',"view-count+1 완료")

@app.route('/article')
def article():
    return render_template('article.html')

@app.route("/article/post", methods=["POST"])
def web_article_post():
    title_receive = request.form['title_give']
    name_receive = request.form['name_give']
    tag_receive = request.form['tag_give']
    content_receive = request.form['content_give']
    article_list = list(db.article.find({},{'_id':False}))
    count = len(article_list) + 1
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    view_count = 0
    comment_count = 0

    doc ={
        'title':title_receive,
        'nickname':name_receive,
        'tag':tag_receive,
        'content':content_receive,
        'post_num': count,
        'time':current_time,
        'view_count': view_count,
        'comment_count': comment_count
    }

    db.article.insert_one(doc)
    return jsonify({'msg': '등록완료!'})

@app.route("/article", methods=["GET"])
def web_article_get():
    return jsonify({'articles': 'GET 연결 완료!'})

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "로그아웃 하였습니다."})
    unset_jwt_cookies(response)
    return response

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)