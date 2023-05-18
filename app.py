from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@atlascluster.anrkcap.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

from bson.objectid import ObjectId

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/reviews", methods=["GET"])
def guestbook_get():
    all_member = list(db.members.find({},{'_id':False}))
    return jsonify({'result': all_member})

@app.route("/reviews", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    age_receive = request.form['age_give']
    mbti_receive = request.form['mbti_give']
    img_receive = request.form['img_give']
    email_receive = request.form['email_give']
    skill_receive = request.form['skill_give']
    pros_receive = request.form['pros_give']
    goal_receive = request.form['goal_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name' : name_receive,
        'age' : age_receive,
        'mbti' : mbti_receive,
        'img' : img_receive,
        'email' : email_receive,
        'skill' : skill_receive,
        'pros' : pros_receive,
        'goal' : goal_receive,
        'comment' : comment_receive
     }

    db.members.insert_one(doc)

    return jsonify({'msg': '저장완료'})


@app.route('/reviews/information')
def information():
   return render_template('information.html')

@app.route('/update_page')
def update_page():
    name = request.args.get('name')

    user = db.members.find_one({'name':name})

    return render_template('update.html',
                           name=user['name'], mbti=user['mbti'],
                            img=user['img'],email=user['email'],
                              skill=user['skill'], goal=user['goal'],
                                comment=user['comment'], pros=user['pros'],
                                  id=str(user['_id']), age=user['age'])

@app.route('/self_introduction_name')
def self_introduction():
    name = request.args.get('name')

    user = db.members.find_one({'name':name})

    return render_template('self_introduction_name.html',
                           id=str(user['_id']),name=user['name'],
                            age=user['age'],mbti=user['mbti'],
                              img=user['img'],email=user['email'],
                              skill=user['skill'], goal=user['goal'],
                                comment=user['comment'],pros=user['pros'] )

@app.route("/update", methods=["POST"])
def update():
     id_receive = str(request.form['id_give'])
     obj_id = ObjectId(id_receive)
     name_receive = str(request.form['name_give'])
     age_receive = str(request.form['age_give'])
     mbti_receive = str(request.form['mbti_give'])
     img_receive = str(request.form['img_give'])
     email_receive = str(request.form['email_give'])
     skill_receive = str(request.form['skill_give'])
     goal_receive = str(request.form['goal_give'])
     pros_receive = str(request.form['pros_give'])
     comment_receive = str(request.form['comment_give'])
     db.members.update_one({'_id':obj_id},{'$set':{'name':name_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'age':age_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'mbti':mbti_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'img':img_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'email':email_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'skill':skill_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'goal':goal_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'pros':pros_receive}})
     db.members.update_one({'_id':obj_id},{'$set':{'comment':comment_receive}})
     return jsonify({'msg': '저장완료'})

@app.route('/delete', methods=["POST"])
def delete():
    id_receive = str(request.form['id_give'])

    db.members.delete_one({'_id':ObjectId(id_receive)})

    return jsonify({'msg':'삭제 완료'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)