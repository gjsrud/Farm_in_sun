'''
    1. ml 모델, 레이블 파일 을 로드
        - 시스템이 가동하면 1회만 로드할것인가?
        - 매 요청이 들어올때마다 로드할것이가?
    2. 말뭉치 -> 모델이 예측할수 있게 전처리 함수
    3. 전처리된 데이터를 넣어서 예측하고 결과를 돌려주는 함수    
'''
import joblib
import os
import re
import sys
import urllib.request
import json
# 로드
def initML():
    # joblib.dump()로 만든 파일이 오류가 있을 수 있으므로(생성,다운로드,이동과정중),
    # 파일자체가 문제없음을 사전체크
    
    # 경로이슈
    label_path = os.getcwd() + '/ml/label.lb'
    model_path = os.getcwd() + '/ml/lang_detected.ml'
    print( label_path )
    print( model_path )
    if os.path.exists( label_path ) or os.path.exists( model_path ):
        # 엔트리 포인트(프로그램 시작점) 기준 경로를 체크
        # 프로젝트 루트를 기점으로 경로를 체크
        labels = joblib.load( label_path )
        print( labels )
        clf    = joblib.load( model_path )
        print( '모델로드' )
        return clf, labels
    return None, None

# 전처리
def input_data_preprocessing(ori_src):    
    cnts = [0]*26
    # 단어별 빈도 계산    
    # 2. 입력 데이터를 소문자 처리
    text    = ori_src.lower()

    # 3. 읽은 내용을 가지고 알파벳 소문자만 남긴다
    p       = re.compile('[^a-z]*')
    text_re = p.sub('', text)
    
    # 4. 알파벳 a-z까지 각각 빈도를 카운트 한다(생략)
    STD_INX = ord('a')
    for word in text_re:
        cnts[ ord(word) - STD_INX ] += 1
    total_count = sum(cnts)
    cnts_norm_softmax = list( map( lambda x: x/total_count , cnts) )

    return [ cnts_norm_softmax ]

# 예측
def predict_lang( ori_src ):
    # 실습 (5분)
    # 모델로드
    clf, labels = initML()
    if clf: # 모델이 존재하면 처리
        print( '모델로드 성공' )
        # 전처리된데이터를 입력
        X = input_data_preprocessing( ori_src )
        print( '전처리', X )
        # 예측 
        y_pred = clf.predict( X )
        print( '예측', y_pred )
        # -> 레이블에 대입 -> 결과 리턴
        return y_pred
    else:
        print( '모델로드 실패' )
        return None
    

# 번역(파파고 api 활용)
def trans_lang(ori_src,src_lang_code,target_lang_code='ko'):
    Client_ID='8Zre9a7JgrD3_rriHP2m'
    Client_Secret='2MYivoeMuf'
    '''
    curl "https://openapi.naver.com/v1/papago/n2mt" \
-H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
-H "X-Naver-Client-Id: 8Zre9a7JgrD3_rriHP2m" \
-H "X-Naver-Client-Secret: 2MYivoeMuf" \
-d "source=ko&target=en&text=만나서 반갑습니다." -v
    '''

    client_id = "8Zre9a7JgrD3_rriHP2m" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "2MYivoeMuf" # 개발자센터에서 발급받은 Client Secret 값
    encText         = urllib.parse.quote( ori_src.strip() )
    data            = f"source={src_lang_code}&target={target_lang_code}&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    
    # 번역 요청 객체 획득
    request = urllib.request.Request(url)
    # 헤더추가
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    # 통신 응답코드 획득
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode() 
    if(rescode==200): # 정상통신
        # 응답결과를 얻는다
        #response_body = response.read()
        # 인코딩 처리
        #msg=response_body.decode('utf-8')
                # 응답데이터 구현
        tmp=json.load(response)
        return tmp['message']['result']['translatedText']
    else:
        print("Error code:"+rescode)
        # 번역실패
        return ori_src
    pass

if __name__ == '__main__':
    # initML()
    # # 테스트 코드 삽입
    # print(
    #     input_data_preprocessing( '''
    #         Many Americans are surprised to see they have not prepared as well as they had hoped for retirement when they finally get ready to call it quits. The bad news is, you’ll probably have to make some realistic assumptions of what your retirement will look like. If you’ve lived primarily paycheck to paycheck in your working years, that may continue to feel the case in your retirement.
    #     ''' )
    # )
    print( predict_lang('''
      Kumusta magandang umaga. Kumain ka na ba? Nagugutom ako. Gusto kong kumain ng masarap na bacon.
    ''') )
    pass