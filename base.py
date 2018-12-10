import requests
import re


def mission(id, passwd):
    ses = requests.session()
    pat = '<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />'
    response = ses.get('http://202.195.102.32')
    response.encoding = 'utf8'

    VIEWSTATE = re.compile(pat).findall(response.text)[0]

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ('
                             'KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

    data = {
        'UserName': id,
        'Password': passwd,
        '__VIEWSTATE': VIEWSTATE,
        'getpassword': ''
    }

    ses.post('http://202.195.102.32/login_gh.aspx', headers=headers, data=data)

    response = ses.get('http://202.195.102.32/web_xsxk/web_xs_xk_cjcx_fzjh.aspx')
    VIEWSTATE = re.compile(pat).findall(response.text)[0]

    data = {
        '__EVENTTARGET': 'LinkButton1',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': VIEWSTATE
    }

    ses.post('http://202.195.102.32/web_xsxk/web_xs_xk_cjcx_fzjh.aspx', headers=headers, data=data)
    response = ses.get('http://202.195.102.32/web_jxpj/jxpj_xspj.aspx')

    pat_s = 'input name="Txtxsxx" type="text" value="(.*?)"'
    pat_x = 'input name="Txtcxxq" type="text" value="(.*?)"'
    state = re.compile(pat_s).findall(response.text)[0]
    xq = re.compile(pat_x).findall(response.text)[0]

    print(xq, ' ', state)

    VIEWSTATE = re.compile(pat).findall(response.text)[0]
    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__EVENTTARGET': 'LBView1',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTARGUMENT': '',
        'Txtxsxx': state,
        'Txtcxxq': xq
    }

    xk_url = 'http://202.195.102.32/web_jxpj/jxpj_xspj.aspx?xsxh=' + id + '&xkxq=' + xq + '&xkfs=&dm=0007-001'

    response = ses.post(xk_url, data=data)
    response.encoding = 'utf8'

    pat_c = "__doPostBack.'GVpjkc','(.*?)'.."
    data['__EVENTTARGET'] = 'GVpjkc'
    all_course = re.compile(pat_c).findall(response.text)

    td = data.copy()
    td['__EVENTTARGET'] = ''
    td['__EVENTARGUMENT'] = ''
    td['DDztpj'] = '很好'

    for i in range(2, 22):
        if i < 10:
            k = 'GVpjzb$ctl0' + str(i) + '$RaBxz'
        else:
            k = 'GVpjzb$ctl' + str(i) + '$RaBxz'
        td[k] = '100'

    td['GVpjzb$ctl21$RaBxz'] = 80

    for cs in all_course:
        data['__EVENTARGUMENT'] = cs
        response = ses.post(
            xk_url,
            data=data)
        response.encoding = 'utf8'

        ttd = td.copy()

        pat_a = '<input name="(.*?)" type="text" value="(.*?)" readonly="readonly"'
        atr = re.compile(pat_a).findall(response.text)
        # print(atr)
        for item in atr:
            ttd[item[0]] = item[1]

        ttd['__VIEWSTATE'] = re.compile(pat).findall(response.text)[0]

        ttd['BTjc'] = '检查结果'
        ses.post(xk_url, data=ttd)
        ttd.pop('BTjc')
        ttd['BTbc'] = '保存结果'
        ttd['__VIEWSTATE'] = re.compile(pat).findall(response.text)[0]
        ses.post(xk_url, data=ttd)

    favourite_url = 'http://202.195.102.32/web_jxpj/jxpj_zxajs.aspx?xsxh=' + id + '&xkxq=' + xq + '&xkfs=&dm=0007-005'
    response = ses.get(favourite_url, data=data)
    response.encoding = 'utf8'

    ttd = td.copy()
    ttd['__VIEWSTATE'] = re.compile(pat).findall(response.text)[0]
    ttd['__EVENTTARGET'] = "GVpjkc"
    ttd['__EVENTARGUMENT'] = "Select$0"
    ttd['ScriptManager1'] = "UpdatePanel1|GVpjkc"
    ttd['__VIEWSTATEENCRYPTED'] = ""

    ses.post(favourite_url, data=ttd)
