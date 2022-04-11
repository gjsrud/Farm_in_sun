from flask import Flask,render_template,request,jsonify
from ml import predict_lang,trans_lang

app = Flask(__name__)

@app.route('/')
def home():
    #SSR수행시 값을 전달하는 방법
    return render_template('index.html',userName="사용자명")

# flask 고급 주제에서 blueprint를 적용해 업무별로 나누고 prefix 적용

@app.route('/service/ml', methods=['GET','POST'])
def ml():    
    if request.method == 'GET':
        return render_template('ml.html', userName="사용자명")
    else:
        # 1. 클라이언트가 보낸 데이터 획득
        msg=request.form.get('msg')
        print(msg)
        # 2. 예측 처리함수에 데이터 넣어서 호출
        # y_pred : ['en']
        y_pred=predict_lang(msg)
        print(y_pred)
        # 3. 결과를 받아서
        res = {
            'code':1,
            'na':y_pred[0] if y_pred else '예측오류'
        }
        return jsonify(res)

@app.route('/service/ml/trans', methods=['POST'])
def trans():
    # 클라이언트가 보낸 데이터 획득
    s_code = request.form.get('s_code')
    msg    = request.form.get('msg')
    # 번역
    data   = trans_lang( msg, s_code )
    return jsonify({
        'code': 1,
        'msg' : data
    })


if __name__=='__main__':
    app.run(debug=True)
    #app.run()