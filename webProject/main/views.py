from django.shortcuts import render
import pymysql
import pandas as pd
import numpy as np
import os,sys,glob
import time
from IPython.core.display import display, HTML

# Create your views here.
def index(request):
    print('yes')
    
    pd.set_option('display.max_rows',1000)

    #display(HTML("<style>.container { width:100% !important; }</style>"))

    conn = pymysql.connect(host = 'localhost',user='root',password = '0000')
    # maek cursor
    cur = conn.cursor()

    sql = '''
    SELECT *
    FROM amgnproject.real_certificate_final
    '''
    sql2 = '''
    SELECT *
    FROM amgnproject.usercertificate
    '''
    # 쿼리문 실행
    cur.execute(sql)
    # 데이터 로드
    data = cur.fetchall()

    cur.execute(sql2)
    user_data = cur.fetchall()
    # db 접속종료
    cur.close()
    conn.close()

    # Convert DB tuple to DataFrame
    df = pd.DataFrame(data, columns = ['Unknown','종목명','분야','기사명','평균연봉(만원)','응시자수(실기)','합격(실기)','합격률','연봉','난이도'])
    user = pd.DataFrame(user_data, columns = ['user_id','category','income','hard'])
    카테고리 = user.iloc[[-1]]['category'].values[0]
    연봉 = user.iloc[[-1]]['income'].values[0]
    난이도 = user.iloc[[-1]]['hard'].values[0]


    df['연봉1'] = np.where( (df['연봉'] =='2천만원대') , 1,
                np.where( (df['연봉'] =='3천초반대') , 2,
                np.where( (df['연봉'] =='3천중반대') , 3,
                np.where( (df['연봉'] =='3천후반대') , 4,
                np.where( (df['연봉'] =='4천초반대') , 5,
                np.where( (df['연봉'] =='4천중반대') , 6,
                np.where( (df['연봉'] =='4천후반대') , 7,
                np.where( (df['연봉'] =='5천초반대') , 8,
                np.where( (df['연봉'] =='5천중반대') , 9,
                np.where( (df['연봉'] =='5천후반대') , 10,
                np.where( (df['연봉'] =='6천초반대') , 11,
                np.where( (df['연봉'] =='6천중반대') , 12,'eror'))))))))))))

    df['난이도1'] = np.where( (df['난이도'] =='최하') , 1,
                np.where( (df['난이도'] =='하') , 2,
                np.where( (df['난이도'] =='중하') , 3,
                np.where( (df['난이도'] =='중') , 4,
                np.where( (df['난이도'] =='중상') , 5,
                np.where( (df['난이도'] =='상') , 6,
                np.where( (df['난이도'] =='최상') , 7,'error')))))))
                        
    df = df.drop(columns = 'Unknown')
    df = df.astype({'연봉1':'int', '난이도1':'int'})

    def 연봉변환기(income):
        if income =='2천만원대': return 1
        if income =='3천초반대': return 2
        if income =='3천중반대': return 3
        if income =='3천후반대': return 4
        if income =='4천초반대': return 5
        if income =='4천중반대': return 6
        if income =='4천후반대': return 7
        if income =='5천초반대': return 8
        if income =='5천중반대': return 9
        if income =='5천후반대': return 10
        if income =='6천초반대': return 11
        if income =='6천중반대': return 12



    def 난이도변환기(hard):
        if hard =='최하': return 1
        if hard =='하': return 2
        if hard =='중하': return 3
        if hard =='중': return 4
        if hard =='중상': return 5
        if hard =='상': return 6
        if hard =='최상': return 7


    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    show_feat = ['종목명','분야','기사명','연봉','난이도','합격률']
    def output1(input_df, category , money , possible):
        '''
        이용자가 희망분야, 희망연봉, 합격가능성을 모두 조회한 경우 추천하는 함수
        '''
        data = output2(input_df, category , money)
        result = output3(data , category , possible)
        return result
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    def output2(input_df , category, money):
        '''
        이용자가 희망분야, 희망연봉을 조회한 경우 추천하는 함수
        '''
        data = input_df[input_df.분야 == category]
        # 해당 분야에 희망연봉이 있는지 조회
        data_money = data[data.연봉 == money]
        if len(data_money) != 0:
            ## 해당 분야에 희망연봉 존재
            return data_money#[show_feat]

        else:
            ## 해당 분야에 희망연봉 존재하지 않음
            you_want = 연봉변환기(money)
            data_money_you_want = data[data['연봉1'] == find_nearest(list(map(int, data['연봉1'].tolist())),you_want)]
            return data_money_you_want#[show_feat]
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    def output3(input_df,category,possible):
        '''
        이용자가 희망분야, 희망난이도를 조회한 경우 추천하는 함수
        '''
        data = input_df[input_df.분야 == category]
        # 해당 분야에 희망난이도가 있는지 조회
        data_hard = data[data.난이도 == possible]
        if  len(data_hard) != 0:
            ## 해당 분야에 희망난이도 존재
            return data_hard
        else:
            ## 해당 분야에 희망연봉 존재하지 않음
            you_want = 난이도변환기(possible)
            data_hard_you_want = data[data['난이도1'] == find_nearest(list(map(int, data['난이도1'].tolist())), you_want)]
            return data_hard_you_want
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    def output4(input_df,category):
        data = df[df.분야 == category]
        return data
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    def output5(input_df , money , possible):
        data =  input_df[input_df.연봉 == money]
        # 해당 분야에 희망난이도가 있는지 조회
        data_hard = data[data.난이도 == possible]
        if  len(data_hard) != 0:
            ## 해당 분야에 희망난이도 존재
            return data_hard
        else:
            ## 해당 분야에 희망연봉 존재하지 않음
            you_want = 난이도변환기(possible)
            data_hard_you_want = data[data['난이도1'] == find_nearest(list(map(int, data['난이도1'].tolist())), you_want)]
            return data_hard_you_want
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    def output6(input_df,money):
        return input_df[input_df.연봉 == money]

    def output7(input_df,possible):
        return input_df[input_df.난이도 ==possible]

    def recommendation_ver2(input_df, category, money, possible):
        #print(category,money,possible)
        # case 1
        if ((category !='없음' )& (money!='없음') & (possible!='없음')):
            #print('output1')
            return output1(input_df, category, money, possible)
        # case 2
        elif ((category != '없음') & (money != '없음') & (possible == '없음')):
            #print('output2')
            return output2(input_df, category,money)
        # case 3
        elif ((category != '없음') &  (money == '없음') & (possible != '없음')):    
            #print('output3')
            return output3(input_df, category, possible)
        # case4
        elif ((category != '없음') & (money == '없음') & (possible == '없음')):    
            #print('output4')
            return output4(input_df, category)
        # case5
        elif ((category == '없음') & (money != '없음') & (possible != '없음')):    
            #print('output5')
            return output5(input_df, money, possible)
        # case6
        elif ((category == '없음') & (money != '없음') & (possible == '없음')):    
            #print('output6')
            return output6(input_df, money)
        # case7 
        elif ((category == '없음') & (money == '없음') & (possible != '없음')):    
            #print('output7')
            return output7(input_df, possible)
        else:
            return input_df
        
    feat = ['종목명','분야','기사명','연봉','난이도','합격률']

    result = recommendation_ver2(df, 카테고리,연봉,난이도)[feat]
    final = result.to_dict()
    cnt = 0
    for i in final['종목명'].values():
        cnt+=1
    mylist = [[''] * 6 for i in range(cnt)]
    tmp = 0
    for i in final['종목명'].values():
        mylist[tmp][0] = i
        tmp += 1
    tmp = 0
    for i in final['분야'].values():
        mylist[tmp][1] = i
        tmp += 1        
    tmp = 0
    for i in final['기사명'].values():
        mylist[tmp][2] = i
        tmp += 1
    tmp = 0
    for i in final['연봉'].values():
        mylist[tmp][3] = i
        tmp += 1  
    tmp = 0
    for i in final['난이도'].values():
        mylist[tmp][4] = i
        tmp += 1  
    tmp = 0
    for i in final['합격률'].values():
        mylist[tmp][5] = str(round(i*100,1)) + '%'
        tmp += 1 
    context = {'df': mylist}
    
    return render(request,'main/index.html', context)