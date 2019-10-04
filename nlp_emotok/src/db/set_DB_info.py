import pymysql

#에러 문자 디비
def get_sms_db():
    host_n = '35.236.167.247'
    user_n = 'root'
    pass_n = 'rojaroja'
    db_n = 'fail_over'
    conn = pymysql.connect(host=host_n, user=user_n, password=pass_n, db=db_n, charset='utf8')
    return conn
