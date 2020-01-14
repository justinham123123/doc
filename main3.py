# A very simple Flask Hello World app for you to get started with...


from flask import Flask, render_template, request, make_response, redirect

import os
import json
import numpy as np
# import matplotlib.pyplot as plt
import datetime
import hashlib
# from cryptography.fernet import Fernet

import pdfkit
import jinja2
# import MySQLdb as mdb
import pymysql as mdb

# from flask_wkhtmltopdf import Wkhtmltopdf


db = None
cursor = None
dbname = "doc"
# ps = "sl400"
ps = ""

bc_table = None
balance_table = None
car_table = None
mf_table = None
rom_table = None


######### class & functions ########
class Patient:
    def __init__(self, id, name):
        self.id = id
        self.name = name


# def secu(code):
# 	key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
# 	cipher_suite = Fernet(key)
# 	ciphered_text = cipher_suite.encrypt(code)
# 	return ciphered_text

# def desecu(code):
# 	key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
# 	cipher_suite = Fernet(key)
# 	ciphered_text = cipher_suite.decrypt(code)
# 	return ciphered_text


def connDB():
    # conn = mdb.connect(host='justinham123123.mysql.pythonanywhere-services.com', user='justinham123123', passwd='31415926Qq', db='justinham123123$doc', port=3306)
    conn = mdb.connect("localhost", "root", "", dbname)
    # conn = mdb.connect("localhost", "root", "ma12345678", dbname)
    cursor = conn.cursor()
    return conn, cursor


class body_composition():
    def __init__(self):
        self.rm_dob = None
        self.rm_gender = None


'''
def draw_pie(count, rad_arr, cols, name):
	ax = plt.axes([0.025,0.025,0.95,0.95], polar=True)
	# ax = plt.axes([0.0,0.0,1.0,1.0], polar=False)

	theta = np.arange(0.0, 2*np.pi, 2*np.pi/count)
	width = 2*np.pi/count
	# printrad_arr, cols
	bars = plt.bar(theta, rad_arr, width=width, bottom=0.0)

	colors = []
	cc = 0
	for r,bar in zip(rad_arr, bars):
		cc += 1
		bar.set_facecolor(plt.cm.jet(cc*1.0/count))
		colors.append(plt.cm.jet(cc*1.0/count))
		# bar.set_alpha(1)

	# ax.set_xticklabels([])
	# ax.set_yticklabels([])
	ax.axes.get_xaxis().set_visible(False)
	ax.set_title(name)

	for x,y in zip(theta, cols):
		# printy
		ax.text(x,1.0, y, ha='center', va='bottom')

	# plt.savefig('static/polar_%s.png'%name,dpi=48)
	plt.show()
	return colors
'''


def set_zero(tar):
    if tar == "" or tar == None:
        return '0'
    else:
        return tar


# inc=1/0 --> inc++/--
def map_value(val, arr, inc):
    ## not tested
    if val == 0:
        return 0

    if arr == None or len(arr) == 0:
        # # print("missing map")
        return 0

    score = 99
    if inc == 1:
        for ele in arr:
            if val <= ele:
                break
            else:
                score -= 1
    elif inc == 0:
        for ele in arr:
            if val >= ele:
                break
            else:
                score -= 1
    return score


def map_value_range(val, arr):
    if val == 0:
        return 99

    score = 99
    for ele in arr:
        if val >= ele[0] and val <= ele[1]:
            break
        else:
            score -= 1

    return score


#### calculate result
def load_bc():
    names = []
    data = {"A1": None, "A2": None, "B6": None, "B8": None, "C1": None, "C2": None, "D1": None, "B4a": None,
            "B4b": None, "B7": None, "B9": None}
    my_dir = os.path.dirname(__file__)
    my_file = os.path.join(my_dir, "static/bc.csv")
    f = open(my_file, "r")
    # 	f = open("./static/bc.csv")
    tmp_dic = dict()
    tmp_row = ""

    for line in f:
        pre = 0
        eles = line.split(", ")
        if len(eles) == 0 or line[0] == '#':
            continue
        # break
        elif eles[0] in data.keys():
            if not tmp_row == "":
                data[tmp_row] = tmp_dic
                tmp_dic = dict()
            tmp_row = eles[0]
            continue
        else:
            arr = []
            title = eles[0]
            for ele in eles[1:]:
                if ele == "":
                    ele = pre - 0.001
                else:
                    pre = float(ele)
                arr.append(float(ele))
            tmp_dic[title] = arr
    if not tmp_row == "":
        data[tmp_row] = tmp_dic
    # tmp_dic.clear()
    f.close()
    return data


def check_table_bc(gender, age, bf, wthr, abf, bmi, data):
    bf_score = 0
    wthr_score = 0
    abf_score = 0
    bmi_score = 0
    wthr_score2 = 0
    wthr_score3 = 0
    if age < 20 or age >= 80:
        return [bf_score, wthr_score, abf_score, bmi_score]
    else:
        if gender == "male":
            bf_map = None
            wthr_map = None
            abf_map = None
            bmi_map = None
            if age >= 20 and age < 30:
                bf_map = data["A1"]["20-29"]
                wthr_map = data["B6"]["20-29"]
            elif age >= 30 and age < 40:
                bf_map = data["A1"]["30-39"]
                wthr_map = data["B6"]["30-39"]
            elif age >= 40 and age < 50:
                bf_map = data["A1"]["40-49"]
                wthr_map = data["B6"]["40-49"]
            elif age >= 50 and age < 60:
                bf_map = data["A1"]["50-59"]
                wthr_map = data["B6"]["50-59"]
            elif age >= 60 and age < 70:
                bf_map = data["A1"]["60-69"]
                wthr_map = data["B6"]["60-69"]
            elif age >= 70 and age < 80:
                bf_map = data["A1"]["70-79"]
                wthr_map = data["B6"]["70-79"]

            abf_map = data["C1"]["20-79"]
            abf_map_plus = data["C1"]["turn"]
            bmi_map = data["D1"]["18-79+"]

            bf_score = map_value(bf, bf_map, 1)
            wthr_score = map_value(wthr, wthr_map, 1)
            if abf >= 10:
                abf_score = map_value(abf, abf_map, 1)
            elif abf <= 8:
                abf_score = map_value(abf, abf_map_plus, 0)
            else:
                abf_score = 99
            bmi_score = map_value(bmi, bmi_map, 1)

            ## general age map
            wthr_map2 = wthr_map3 = None
            wthr_map2 = data["B4a"]["20-70"]
            wthr_map3 = data["B7"]["20-70"]
            wthr_score2 = map_value(wthr, wthr_map2, 0)
            wthr_score3 = map_value(wthr, wthr_map3, 1)

        elif gender == "female":
            bf_map = None
            wthr_map = None
            abf_map = None
            bmi_map = None
            if age >= 20 and age < 30:
                bf_map = data["A2"]["20-29"]
                wthr_map = data["B8"]["20-29"]
            elif age >= 30 and age < 40:
                bf_map = data["A2"]["30-39"]
                wthr_map = data["B8"]["30-39"]
            elif age >= 40 and age < 50:
                bf_map = data["A2"]["40-49"]
                wthr_map = data["B8"]["40-49"]
            elif age >= 50 and age < 60:
                bf_map = data["A2"]["50-59"]
                wthr_map = data["B8"]["50-59"]
            elif age >= 60 and age < 70:
                bf_map = data["A2"]["60-69"]
                wthr_map = data["B8"]["60-69"]
            elif age >= 70 and age < 80:
                bf_map = data["A2"]["70-79"]
                wthr_map = data["B8"]["70-79"]

            abf_map = data["C2"]["20-79"]
            bmi_map = data["D1"]["18-79+"]
            abf_map_plus = data["C2"]["turn"]

            bf_score = map_value(bf, bf_map, 1)
            wthr_score = map_value(wthr, wthr_map, 1)
            abf_score = map_value(abf, abf_map, 1)
            if abf >= 20:
                abf_score = map_value(abf, abf_map, 1)
            elif abf <= 14:
                abf_score = map_value(abf, abf_map_plus, 0)
            else:
                abf_score = 99
            bmi_score = map_value(bmi, bmi_map, 1)

            ## general age map
            wthr_map2 = wthr_map3 = None
            wthr_map2 = data["B4b"]["20-70"]
            wthr_map3 = data["B9"]["20-70"]
            wthr_score2 = map_value(wthr, wthr_map2, 0)
            wthr_score3 = map_value(wthr, wthr_map3, 1)

        wthr_score_t = (wthr_score + wthr_score2 + wthr_score3) / 3
        # # printwthr_score, wthr_score2, wthr_score3
        return [bf_score, wthr_score_t, abf_score, bmi_score]


def load_balance():
    names = []
    data = {"E1": None, "E2": None, "E3": None}
    my_dir = os.path.dirname(__file__)
    my_file = os.path.join(my_dir, "static/balance.csv")
    f = open(my_file, "r")
    # 	f = open("./static/balance.csv")
    tmp_dic = dict()
    tmp_row = ""
    for line in f:
        eles = line.split("; ")
        if len(eles) == 0 or line[0] == '#':
            continue
        # break
        elif eles[0] in data.keys():
            if not tmp_row == "":
                data[tmp_row] = tmp_dic
                tmp_dic = dict()
            tmp_row = eles[0]
            continue
        else:
            arr = []
            title = eles[0]
            for ele in eles[1:]:
                tar = None
                if "+" in ele:
                    tar = int(ele.split("+")[0])
                    s_e = [tar, 1000]
                elif ele == "":
                    s_e = [-1, 1]
                elif "," in ele:
                    num_list = ele.split(",")
                    s_e = [num_list[0], num_list[-1]]
                else:
                    tar = int(ele)
                    s_e = [tar, tar]
                arr.append(s_e)
            tmp_dic[title] = arr
    if not tmp_row == "":
        data[tmp_row] = tmp_dic
    # tmp_dic.clear()
    f.close()
    return data


def check_table_balance(gender, age, b_l, b_r, an_l, an_r, y_l, y_r, data):
    b_l_score = b_l_score2 = 0
    b_r_score = b_r_score2 = 0
    an_l_score = 0
    an_r_score = 0
    y_l_score = 0
    y_r_score = 0
    if age < 20 or age >= 70:
        return [b_l_score, b_r_score, an_l_score, an_r_score, y_l_score, y_r_score]
    else:
        if gender == "male":
            b_map = None
            b_map2 = None
            an_map = None
            y_map = None

            if age >= 20 and age < 30:
                b_map = data["E2"]["20-29"]
                b_map2 = data["E1"]["20-39"]
            elif age >= 30 and age < 40:
                b_map = data["E2"]["30-39"]
                b_map2 = data["E1"]["20-39"]
            elif age >= 40 and age < 50:
                b_map = data["E2"]["40-49"]
                b_map2 = data["E1"]["40-49"]
            elif age >= 50 and age < 55:
                b_map = data["E2"]["50-54"]
                b_map2 = data["E1"]["50-54"]
            elif age >= 55 and age < 60:
                b_map = data["E2"]["55-59"]
                b_map2 = data["E1"]["55-59"]
            elif age >= 60 and age < 65:
                b_map = data["E2"]["60-64"]
                b_map2 = data["E1"]["60-64"]
            elif age >= 65 and age < 70:
                b_map = data["E2"]["65-69"]
                b_map2 = data["E1"]["65-69"]

            b_l_score = map_value_range(b_l, b_map)
            b_l_score2 = map_value_range(b_l, b_map2)
            b_r_score = map_value_range(b_r, b_map)
            b_r_score2 = map_value_range(b_r, b_map2)
        ## an, y tbd

        elif gender == "female":
            b_map = None
            b_map2 = None
            an_map = None
            y_map = None

            if age >= 20 and age < 30:
                b_map = data["E3"]["20-29"]
                b_map2 = data["E1"]["20-39"]
            elif age >= 30 and age < 40:
                b_map = data["E3"]["30-39"]
                b_map2 = data["E1"]["20-39"]
            elif age >= 40 and age < 50:
                b_map = data["E3"]["40-49"]
                b_map2 = data["E1"]["40-49"]
            elif age >= 50 and age < 55:
                b_map = data["E3"]["50-54"]
                b_map2 = data["E1"]["50-54"]
            elif age >= 55 and age < 60:
                b_map = data["E3"]["55-59"]
                b_map2 = data["E1"]["55-59"]
            elif age >= 60 and age < 65:
                b_map = data["E3"]["60-64"]
                b_map2 = data["E1"]["60-64"]
            elif age >= 65 and age < 70:
                b_map = data["E3"]["65-69"]
                b_map2 = data["E1"]["65-69"]

            b_l_score = map_value_range(b_l, b_map)
            b_l_score2 = map_value_range(b_l, b_map2)
            b_r_score = map_value_range(b_r, b_map)
            b_r_score2 = map_value_range(b_r, b_map2)

        b_l_score_t = (b_l_score + b_l_score2) / 2
        b_r_score_t = (b_r_score + b_r_score2) / 2

        # # printwthr_score, wthr_score2, wthr_score3
        return [b_l_score_t, b_r_score_t, an_l_score, an_r_score, y_l_score, y_r_score]


#@app.before_request
#def before_user():
#    current_user = request.cookies.get('uname')
#    formname = request.form.get('uname')
#    if current_user or formname:
#        pass
#    else:
#        error = "Please Login"
#        return render_template('login.htmml', error=error)



# F1 down
def load_car():
    names = []
    data = {"F1": None, "F2": None, "F3": None, "F4": None, "G2": None}

    my_dir = os.path.dirname(__file__)
    my_file = os.path.join(my_dir, "static/car.csv")
    f = open(my_file, "r")

    tmp_dic = dict()
    tmp_row = ""
    for line in f:
        eles = line.split(", ")
        if len(eles) == 0 or line[0] == '#':
            continue
        # break
        elif eles[0] in data.keys():
            if not tmp_row == "":
                data[tmp_row] = tmp_dic
                tmp_dic = dict()
            tmp_row = eles[0]
            continue
        else:
            arr = []
            title = eles[0]
            left_tag = 0
            for ele in eles[1:]:
                tar = None
                if ele == "":
                    tar = left_tag - 0.001
                else:
                    tar = ele
                    left_tag = float(ele)
                arr.append(float(tar))
            tmp_dic[title] = arr
    if not tmp_row == "":
        data[tmp_row] = tmp_dic
    # tmp_dic.clear()
    f.close()
    return data


def check_table_car(gender, age, vo2max, hrr, data):
    vo2max_score = vo2max_score2 = 0
    hrr_score = 0
    if age < 20 or age >= 80:
        return [vo2max_score, hrr_score]
    else:
        if gender == "male":
            vo2max_map = None
            vo2max_map2 = None
            hrr_map = None

            if age >= 20 and age < 30:
                vo2max_map = data["F1"]["20-29"]
                vo2max_map2 = data["F2"]["20-29"]
            elif age >= 30 and age < 40:
                vo2max_map = data["F1"]["30-39"]
                vo2max_map2 = data["F2"]["30-39"]
            elif age >= 40 and age < 50:
                vo2max_map = data["F1"]["40-49"]
                vo2max_map2 = data["F2"]["40-49"]
            elif age >= 50 and age < 55:
                vo2max_map = data["F1"]["50-59"]
                vo2max_map2 = data["F2"]["50-59"]
            elif age >= 60 and age < 69:
                vo2max_map = data["F1"]["60-69"]
                vo2max_map2 = data["F2"]["60-69"]
            elif age >= 70 and age < 79:
                vo2max_map = data["F1"]["70-79"]
                vo2max_map2 = data["F2"]["70-79"]

            if age >= 20 and age < 70:
                hrr_map = data["G2"]["20-70"]
                hrr_score = map_value(hrr, hrr_map, 0)
            else:
                hrr_score = 0

            vo2max_score = map_value(vo2max, vo2max_map, 0)
            vo2max_score2 = map_value(vo2max, vo2max_map2, 0)
        # # printvo2max_score, "$$$"


        elif gender == "female":
            vo2max_map = None
            vo2max_map2 = None
            hrr_map = None

            if age >= 20 and age < 30:
                vo2max_map = data["F3"]["20-29"]
                vo2max_map2 = data["F4"]["20-29"]
            elif age >= 30 and age < 40:
                vo2max_map = data["F3"]["30-39"]
                vo2max_map2 = data["F4"]["30-39"]
            elif age >= 40 and age < 50:
                vo2max_map = data["F3"]["40-49"]
                vo2max_map2 = data["F4"]["40-49"]
            elif age >= 50 and age < 55:
                vo2max_map = data["F3"]["50-59"]
                vo2max_map2 = data["F4"]["50-59"]
            elif age >= 60 and age < 69:
                vo2max_map = data["F3"]["60-69"]
                vo2max_map2 = data["F4"]["60-69"]
            elif age >= 70 and age < 79:
                vo2max_map = data["F3"]["70-79"]
                vo2max_map2 = data["F4"]["70-79"]

            if age >= 20 and age < 70:
                hrr_map = data["G2"]["20-70"]
                hrr_score = map_value(hrr, hrr_map, 0)
            else:
                hrr_score = 0

            vo2max_score = map_value(vo2max, vo2max_map, 0)
            vo2max_score2 = map_value(vo2max, vo2max_map2, 0)

        # # printvo2max_map, vo2max, vo2max_score, "$$$"

        vo2max_score_t = (vo2max_score + vo2max_score2) / 2

        # # printwthr_score, wthr_score2, wthr_score3
        return [vo2max_score_t, hrr_score]


# h2,h4 down
def load_mf():
    names = []
    data = {"H2": None, "H4": None, "H1": None, "H3": None, "I1": None, "I4": None, "J1": None, "J2": None}

    my_dir = os.path.dirname(__file__)
    my_file = os.path.join(my_dir, "static/mf.csv")
    f = open(my_file, "r")

    tmp_dic = dict()
    tmp_row = ""
    for line in f:
        eles = line.split(", ")
        if len(eles) == 0 or line[0] == '#':
            continue
        # break
        elif eles[0] in data.keys():
            if not tmp_row == "":
                data[tmp_row] = tmp_dic
                tmp_dic = dict()
            tmp_row = eles[0]
            continue
        else:
            arr = []
            title = eles[0]
            left_tag = 0
            for ele in eles[1:]:
                tar = None
                if ele == "":
                    tar = left_tag - 0.001
                else:
                    tar = ele
                    left_tag = float(ele)
                arr.append(float(tar))
            tmp_dic[title] = arr
    if not tmp_row == "":
        data[tmp_row] = tmp_dic
    # tmp_dic.clear()
    f.close()
    return data


def check_table_mf(gender, age, pull, push, leg, grip_l, grip_r, grip, endurance, data):
    push_score = 0
    leg_score = 0
    pull_score = 0
    grip_l_score = 0
    grip_r_score = 0
    end_score = 0

    push_map = None
    leg_map = None
    grip_l_map = None
    grip_r_map = None
    end_map = None

    if gender == "male":
        if age < 20:
            push_map = data["H1"]["<20"]
            leg_map = data["H3"]["20-29"]
            grip_map = data["I1"]["15-19"]
        elif age >= 20 and age < 30:
            push_map = data["H1"]["20-29"]
            leg_map = data["H3"]["20-29"]
            grip_map = data["I1"]["20-29"]
            end_map = data["J1"]["20-29"]
        elif age >= 30 and age < 40:
            push_map = data["H1"]["30-39"]
            leg_map = data["H3"]["30-39"]
            grip_map = data["I1"]["30-39"]
            end_map = data["J1"]["30-39"]
        elif age >= 40 and age < 50:
            push_map = data["H1"]["40-49"]
            leg_map = data["H3"]["40-49"]
            grip_map = data["I1"]["40-49"]
            end_map = data["J1"]["40-49"]
        elif age >= 50 and age < 60:
            push_map = data["H1"]["50-59"]
            leg_map = data["H3"]["50-59"]
            grip_map = data["I1"]["50-59"]
            end_map = data["J1"]["50-59"]
        elif age >= 60:
            push_map = data["H1"]["60+"]
            leg_map = data["H3"]["60+"]
            grip_map = data["I1"]["60-69"]
            end_map = data["J1"]["60-69"]

    elif gender == "female":
        if age < 20:
            push_map = data["H2"]["<20"]
            grip_map = data["I4"]["15-19"]
        # leg_map = data["H4"]["<20"]
        elif age >= 20 and age < 30:
            push_map = data["H2"]["20-29"]
            leg_map = data["H4"]["20-29"]
            grip_map = data["I4"]["20-29"]
            end_map = data["J2"]["20-29"]
        elif age >= 30 and age < 40:
            push_map = data["H2"]["30-39"]
            leg_map = data["H4"]["30-39"]
            grip_map = data["I4"]["30-39"]
            end_map = data["J2"]["30-39"]
        elif age >= 40 and age < 50:
            push_map = data["H2"]["40-49"]
            leg_map = data["H4"]["40-49"]
            grip_map = data["I4"]["40-49"]
            end_map = data["J2"]["40-49"]
        elif age >= 50 and age < 60:
            push_map = data["H2"]["50-59"]
            leg_map = data["H4"]["50-59"]
            grip_map = data["I4"]["50-59"]
            end_map = data["J2"]["50-59"]
        elif age >= 60:
            push_map = data["H2"]["60+"]
            leg_map = data["H4"]["60+"]
            grip_map = data["I4"]["60-69"]
            end_map = data["J2"]["60-69"]

    push_score = leg_score = grip_l_score = grip_r_score = end_score = grip_score = 0

    if float(push) > 0:
        push_score = map_value(push, push_map, 0)
        pull_score = map_value(pull, push_map, 0)

    if float(leg) > 0:
        leg_score = map_value(leg, leg_map, 0)

    if float(grip_l) > 0:
        grip_l_score = map_value(grip_l, grip_map, 0)

    if float(grip_r) > 0:
        grip_r_score = map_value(grip_r, grip_map, 0)

    if float(grip) > 0:
        grip_score = map_value(grip, grip_map, 0)

    if float(endurance) > 0:
        end_score = map_value(endurance, end_map, 0)

    # # print(leg_map, leg, leg_score, "$")
    # # printpush_map
    # # printend_map

    return [pull_score, push_score, leg_score, grip_l_score, grip_r_score, grip_score, end_score]


def load_rom():
    names = []
    data = {"K1a": None, "K1b": None, "K1c": None, "K2a": None, "K2b": None, "K2c": None, "K3a": None, "K3b": None,
            "K4a": None, "K4b": None, "K4c": None, "K4d": None, "K5a": None, "K5b": None, "K5c": None, "K5d": None,
            "K6a": None, "K6b": None, "K7a": None, "K7b": None, "K8a": None, "K8b": None, "K8c": None}
    my_dir = os.path.dirname(__file__)
    my_file = os.path.join(my_dir, "static/rom.csv")
    f = open(my_file, "r")
    # 	f = open("./static/rom.csv")
    tmp_dic = dict()
    tmp_row = ""
    for line in f:
        eles = line.split(", ")
        if len(eles) == 0 or line[0] == '#':
            continue
        # break
        elif eles[0] in data.keys():
            if not tmp_row == "":
                data[tmp_row] = tmp_dic
                tmp_dic = dict()
            tmp_row = eles[0]
            continue
        else:
            arr = []
            title = eles[0]
            for ele in eles[1:]:
                arr.append(float(ele))
            tmp_dic[title] = arr
    if not tmp_row == "":
        data[tmp_row] = tmp_dic
    # tmp_dic.clear()
    f.close()
    return data


def check_table_rom(age, vals, data):
    # score_1a = score_1b = score_1c = 0
    # score_2a = score_2b = 0
    # score_3a = score_3b = 0
    # score_4a = score_4b = score_4c = score_4d = 0
    # score_5a = score_5b = score_5c = score_5d = 0
    # score_6a = score_6b = 0
    # score_7a = score_7b = 0
    # score_8a = score_8b = score_8c = 0
    scores = dict()
    scores['1a'] = scores['1ar'] = 0
    scores['1b'] = scores['1br'] = 0
    scores['1c'] = scores['1cr'] = 0
    scores['2a'] = scores['2ar'] = 0
    scores['2b'] = scores['2br'] = 0
    scores['3a'] = scores['3ar'] = 0
    scores['3b'] = scores['3br'] = 0
    scores['4a'] = scores['4ar'] = 0
    scores['4b'] = scores['4br'] = 0
    scores['4c'] = scores['4cr'] = 0
    scores['4d'] = scores['4dr'] = 0
    scores['5a'] = scores['5ar'] = 0
    scores['5b'] = scores['5br'] = 0
    scores['5c'] = scores['5cr'] = 0
    scores['5d'] = scores['5dr'] = 0
    scores['6a'] = scores['6ar'] = 0
    scores['6b'] = scores['6br'] = 0

    scores['7a'] = 0
    scores['7b'] = 0
    scores['8a'] = 0
    scores['8b'] = 0
    scores['8c'] = scores['8cr'] = 0

    if age < 20 or age > 70:
        return scores
    else:
        map_1a = data["K1a"]["20-70"]  # flel_h [r]
        map_1b = data["K1b"]["20-70"]  # hypl_h [r]
        map_1c = data["K1c"]["20-70"]  # abdl_h [r]
        map_2a = data["K2a"]["20-70"]  # flel_k [r]
        map_2b = data["K2b"]["20-70"]  # extl_k [r] {-}
        map_3a = data["K3a"]["20-70"]  # flel_a (dor_a) [r]
        map_3b = data["K3b"]["20-70"]  # extl_a (pf_a) [r]
        map_4a = data["K4a"]["20-70"]  # flel (s) [r]
        map_4b = data["K4b"]["20-70"]  # extl (s) [r]
        map_4c = data["K4c"]["20-70"]  # abdl (s) [r]
        map_4d = data["K4d"]["20-70"]  # lrl (s) [r]
        map_5a = data["K5a"]["20-70"]  # flel_e [r]
        map_5b = data["K5b"]["20-70"]  # extl_e [r] {-}
        map_5c = data["K5c"]["20-70"]  # prol_e [r]
        map_5d = data["K5d"]["20-70"]  # supl_e [r]
        map_6a = data["K6a"]["20-70"]  # flel_w [r]
        map_6b = data["K6b"]["20-70"]  # extl_w [r]
        map_7a = data["K7a"]["20-70"]  # fle (l)
        map_7b = data["K7b"]["20-70"]  # ext (l)
        map_8a = data["K8a"]["20-70"]  # fle_c
        map_8b = data["K8b"]["20-70"]  # ext_c
        map_8c = data["K8c"]["20-70"]  # lrl_c [r]

        scores["1a"] = map_value(vals[0][0], map_1a, 0) * 1.0 / 10
        scores["1b"] = map_value(vals[0][1], map_1b, 0) * 1.0 / 10
        scores["1c"] = map_value(vals[0][2], map_1c, 0) * 1.0 / 10
        scores["1ar"] = map_value(vals[0][3], map_1a, 0) * 1.0 / 10
        scores["1br"] = map_value(vals[0][4], map_1b, 0) * 1.0 / 10
        scores["1cr"] = map_value(vals[0][5], map_1c, 0) * 1.0 / 10

        scores['2a'] = map_value(vals[1][0], map_2a, 0) * 1.0 / 10
        scores['2b'] = map_value(vals[1][1], map_2b, 1) * 1.0 / 10
        scores['2ar'] = map_value(vals[1][2], map_2a, 0) * 1.0 / 10
        scores['2br'] = map_value(vals[1][3], map_2b, 1) * 1.0 / 10

        scores['3a'] = map_value(vals[2][0], map_3a, 0) * 1.0 / 10
        scores['3b'] = map_value(vals[2][1], map_3b, 0) * 1.0 / 10
        scores['3ar'] = map_value(vals[2][2], map_3a, 0) * 1.0 / 10
        scores['3br'] = map_value(vals[2][3], map_3b, 0) * 1.0 / 10

        scores['4a'] = map_value(vals[3][0], map_4a, 0) * 1.0 / 10
        scores['4b'] = map_value(vals[3][1], map_4b, 0) * 1.0 / 10
        scores['4c'] = map_value(vals[3][2], map_4c, 0) * 1.0 / 10
        scores['4d'] = map_value(vals[3][3], map_4d, 0) * 1.0 / 10
        scores['4ar'] = map_value(vals[3][4], map_4a, 0) * 1.0 / 10
        scores['4br'] = map_value(vals[3][5], map_4b, 0) * 1.0 / 10
        scores['4cr'] = map_value(vals[3][6], map_4c, 0) * 1.0 / 10
        scores['4dr'] = map_value(vals[3][7], map_4d, 0) * 1.0 / 10

        scores['5a'] = map_value(vals[4][0], map_5a, 0) * 1.0 / 10
        scores['5b'] = map_value(vals[4][1], map_5b, 1) * 1.0 / 10
        # # printmap_5b, vals[4][1], scores['5b'], "rom"

        scores['5c'] = map_value(vals[4][2], map_5c, 0) * 1.0 / 10
        scores['5d'] = map_value(vals[4][3], map_5d, 0) * 1.0 / 10
        scores['5ar'] = map_value(vals[4][4], map_5a, 0) * 1.0 / 10
        scores['5br'] = map_value(vals[4][5], map_5b, 1) * 1.0 / 10
        scores['5cr'] = map_value(vals[4][6], map_5c, 0) * 1.0 / 10
        scores['5dr'] = map_value(vals[4][7], map_5d, 0) * 1.0 / 10

        scores['6a'] = map_value(vals[5][0], map_6a, 0) * 1.0 / 10
        scores['6b'] = map_value(vals[5][1], map_6b, 0) * 1.0 / 10
        scores['6ar'] = map_value(vals[5][2], map_6a, 0) * 1.0 / 10
        scores['6br'] = map_value(vals[5][3], map_6b, 0) * 1.0 / 10

        scores['7a'] = map_value(vals[6][0], map_7a, 0) * 1.0 / 10
        scores['7b'] = map_value(vals[6][1], map_7b, 0) * 1.0 / 10

        scores['8a'] = map_value(vals[7][0], map_8a, 0) * 1.0 / 10
        scores['8b'] = map_value(vals[7][1], map_8b, 0) * 1.0 / 10
        scores['8c'] = map_value(vals[7][2], map_8c, 0) * 1.0 / 10
        scores['8cr'] = map_value(vals[7][3], map_8c, 0) * 1.0 / 10

        return scores


##### views ###
# app = Flask(__name__)
app = Flask(__name__)

@app.before_request
def before_user():
    current_user = request.cookies.get('uname')
    formname = request.form.get('uname')
    if str(request.url_rule)=="/basic_form":
        return render_template("bf.html")
    elif current_user or formname:
        pass
    else:
        error = 'Please Login'
        return render_template('login.html', error=error)


# wkhtmltopdf = Wkhtmltopdf(app)


@app.route("/")
def MainHandler():
    return redirect("/login_form")


@app.route("/login_form")
def LoginFormHandler():
    error = ""
    return render_template('login.html', error=error)


@app.route("/login", methods=["get", "post"])
def LoginHandler():
    uname = request.form.get("uname")
    passw = request.form.get("psw")
    # # printuname, passw
    error = ""
    db, cursor = connDB()

    comm = "select ps,fin,userType from User where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    # 	return "star"

    if len(res) == 0:
        # # print"user already exist"
        error = "user doesn't exist"
        return render_template('login.html', error=error)
    else:
        # return "ab"
        ps = res[0][0]
        # 		return "abc"
        fin = res[0][1]
        # if not desecu(ps) == passw:
        if not ps == passw:
            error = "wrong password"
            return render_template('login.html', error=error)
        else:
            if res[0][2] == "doctor":
                resp = redirect("/patient_list")
                resp.set_cookie('uname', uname, max_age=1800)
                return resp
            elif res[0][2] == "patient":
                resp = redirect("/report_list")
                resp.set_cookie('uname', uname, max_age=1800)
                return resp
            # resp = redirect("/result_m")
            # resp.set_cookie('uname', uname)
            # return resp


@app.route("/logout")
def LogoutHandler():
    resp = make_response(render_template('login.html', error="You have successfully logged out"))
    resp.delete_cookie('uname')
    # resp.set_cookie('uname', "")
    return resp


@app.route("/report_list")
def ReportListHandler():
    current_user = request.cookies.get('uname')
    db, cursor = connDB()
    comm = "select test_id, date from History where user='%s';" % current_user
    cursor.execute(comm)
    res3 = cursor.fetchall()
    count = 1
    report = []
    for ele in res3:
        report.append([count, ele[0], ele[1]])
        count += 1

    # # printpatient['test_list'], "**"

    return render_template("report_list.html", report=report, username=current_user)


@app.route("/patient_list")
def PatientListHandler():
    patients = []
    current_user = request.cookies.get('uname')
    db, cursor = connDB()
    comm = "select id,rname,email,dob,gender from User where userType='patient';"
    cursor.execute(comm)
    res = cursor.fetchall()
    for data in res:
        patient = dict()
        patient["id"] = data[0]
        patient["rname"] = data[1]
        patient["email"] = data[2]
        patient["dob"] = data[3]
        patient["mf"] = data[4]
        patient['test_list'] = []
        try:

            comm = "select test_id, date from History where user='%s';" % data[0]
            cursor.execute(comm)
            res3 = cursor.fetchall()
            count = 1
            for ele in res3:
                # # printele
                patient['test_list'].append([count, ele[0], ele[1]])
                count += 1

        # comm = "select gender,dob from BodyComposition where id='%s';"%data[0]
        # cursor.execute(comm)
        # res2 = cursor.fetchall()
        # patient["dob"] = res2[0][1]
        # patient["mf"] = res2[0][0]
        # # printpatient['test_list'], "**"
        except:
            pass
        patients.append(patient)
    return render_template("patient_list.html", patients=patients, username=current_user)


@app.route("/basic_form")
def BasicFormHandler():
    fr_doc = "f"
    try:
        fr_doc = request.args.get("fr_doc")
    except:
        pass
    # # printfr_doc

    user_dict = {}
    user_list = ["id", "ps", "rname", "email", "phone", "address", "postCode", "Country", "fin", "userType", "dob",
                 "gender", "age"]
    data = None

    if fr_doc == "t":
        for i in range(len(user_list)):
            user_dict[user_list[i]] = ""
        user_type = "doctor"
        return render_template('bf.html', fr_doc=fr_doc, username=user_type, userType=user_type, name="",
                               dict=user_dict, error="")

    else:

        uname = request.cookies.get('uname')
        # uname = request.form.get("uname")

        # if uname=="":
        if False:
            return redirect("/login")

        else:
            db, cursor = connDB()
            comm = "select * from User where id='%s';" % uname
            cursor.execute(comm)
            res = cursor.fetchall()

            if len(res) > 0:
                data = res[0]
                for i in range(len(user_list)):
                    if user_list[i] == "ps":
                        # user_dict[user_list[i]] = desecu(data[i])
                        user_dict[user_list[i]] = data[i]
                    else:
                        user_dict[user_list[i]] = data[i]
            else:
                for i in range(len(user_list)):
                    user_dict[user_list[i]] = ""

            user_type = user_dict["userType"]
            user_type = "doctor"
            return render_template('bf.html', fr_doc=fr_doc, username=user_type, userType=user_type, name=uname,
                                   dict=user_dict, error="")


@app.route("/basic_form_submit", methods=["get", "post"])
def BasicFormSubHandler():
    # uname = "Justin"
    uname = request.form.get("uname")
    passw1 = request.form.get("passw1")
    passw2 = request.form.get("passw2")

    rname = request.form.get("rname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    postCode = request.form.get("postCode")
    country = request.form.get("country")
    fin = request.form.get("fin")
    user_type = request.form.get("whor")
    dob = request.form.get("dob")
    age = request.form.get("age")
    gender = request.form.get("gender")
    # # printuser_type, "$$$"

    fr_doc = request.form.get("fr_doc")
    # # printfr_doc

    fin_sta = '0'
    if fin == '1':
        fin_sta = fin
    isnew = request.form.get("typ")

    user_dict = dict()
    data = None
    user_dict['ps'] = ''
    user_dict['rname'] = rname
    user_dict['email'] = email
    user_dict['phone'] = phone
    user_dict['address'] = address
    user_dict['postCode'] = postCode
    user_dict['Country'] = country
    user_dict['fin'] = fin
    user_dict['typ'] = isnew
    user_dict['userType'] = user_type
    user_dict['dob'] = dob
    user_dict['age'] = age
    user_dict['gender'] = gender

    # user_type = 'patient'
    # user_dict['userType'] = user_type

    db, cursor = connDB()
    comm = "select * from User where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:  ## update
        # # print"user already exist"
        if isnew == "new":
            error = "user exist"
            user_dict['id'] = ''
            return render_template('bf.html', fr_doc=fr_doc, userType=user_type, name=uname, dict=user_dict,
                                   error=error)

        elif isnew == "update":
            comm = "delete from User where id='%s';" % uname
            cursor.execute(comm)
            # comm = "insert into User values('%s', '%s', '%s', '%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');" % (uname, secu(passw1.encode()),
            # rname, email, phone, address, postCode, country, fin_sta, user_type, dob, gender, age)
            comm = "insert into User values('%s', '%s', '%s', '%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');" % (
            uname, passw1,
            rname, email, phone, address, postCode, country, fin_sta, user_type, dob, gender, age)

            cursor.execute(comm)
            db.commit()
            error = "successfully updated"
            return render_template('bf.html', fr_doc=fr_doc, userType=user_type, name=uname, dict=user_dict,
                                   error=error)

    elif not passw1 == passw2:
        error = "use same password"
        user_dict['id'] = ''
        return render_template('bf.html', fr_doc=fr_doc, userType=user_type, name=uname, dict=user_dict, error=error)


    else:  ## new
        # comm = "insert into User values('%s', '%s', '%s', '%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');" % (uname, secu(passw1.encode()),
        # 	rname, email, phone, address, postCode, country, fin_sta, user_type, dob, gender, age)
        comm = "insert into User values('%s', '%s', '%s', '%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');" % (
        uname, passw1,
        rname, email, phone, address, postCode, country, fin_sta, user_type, dob, gender, age)
        # # printcomm
        cursor.execute(comm)
        db.commit()
        # # printcomm

        if fr_doc == "t":
            return redirect("patient_list")
        else:

            # if user_type == "patient":
            #     # return "success"
            #     # ## login model
            #     # resp = make_response(redirect("/body_composition_form"))
            #     resp = make_response(redirect("/result_m"))
            #     resp.set_cookie('uname', uname)
            #     return resp
            # elif user_type == "doctor":
            if True:
                resp = make_response(redirect("/patient_list"))
                resp.set_cookie('uname', uname)
                return resp


@app.route("/general_form")
def GFormHandler():
    current_user = request.cookies.get('uname')
    uname = request.args.get("name")
    patient_name = ""

    bc_list = ["id", "weight", "rhr", "asis", "height", "bp"]
    bc_dict = dict()
    data = None
    db, cursor = connDB()
    comm = "select * from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()

    if len(res) > 0:
        data = res[0]
        for i in range(len(bc_list)):
            bc_dict[bc_list[i]] = data[i]
    else:
        for i in range(len(bc_list)):
            bc_dict[bc_list[i]] = ""

    comm = "select user,date from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    username = patient_name = res[0]
    bc_dict["td"] = res[1]
    # # printusername, bc_dict["td"], "##"

    states = []  ## 5 form statues + 1 basic statues
    forms = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion", "General"]
    for fname in forms:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    return render_template('general.html', pname=patient_name, states=states, username=current_user, name=uname,
                           dict=bc_dict)


@app.route("/general_form_submit", methods=["get", "post"])
def GFormSubmitHandler():
    current_user = request.cookies.get('uname')
    uname = request.form.get("Username")

    db, cursor = connDB()
    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    username = res[0]

    weight = request.form.get("weight")
    rhr = request.form.get("rhr")
    asis = request.form.get("asis")
    height = request.form.get("height")
    bp = request.form.get("bp")
    td = request.form.get("td")

    comm = "select * from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        comm = "delete from General where id='%s';" % uname
        cursor.execute(comm)

    comm = "insert into General values('%s','%s','%s','%s', '%s', '%s');" % (uname, weight, rhr, asis, height, bp)
    # # printcomm
    cursor.execute(comm)
    db.commit()

    comm = "update History set date='%s' where test_id='%s';" % (td, uname)
    # # printcomm
    cursor.execute(comm)
    db.commit()

    bc_dict = {"weight": weight, "rhr": rhr, "asis": asis, 'height': height, 'bp': bp}

    # return render_template('general.html', username=current_user, name=uname, dict=bc_dict)
    return redirect("general_form?name=%s" % uname)


@app.route("/body_composition_form")
def BCFormHandler():
    # uname = request.cookies.get('uname')
    current_user = request.cookies.get('uname')

    uname = request.args.get("name")

    bc_list = ["uname", "height", "weight", "bmi", "bp", "rhr", "neck", "chest", "waist", "abdomen", "armr", "arml",
               "forearmr", "forearml", "buttocks", "midthighr", "midthighl", "calfr", "calfl", "foot", "knee", "asis",
               "shoulder", "abdomen2", "triceps", "chest2", "midaxillary", "subscapular", "suprailiac", "thigh", "sum7",
               "sum31", "sum32", "bd1", "bd2", "bd3", "bf1", "bf2", "bf3", "bf", "fm", "lbm", "circumference", "wthr",
               "bmr", "act_level", "tdee", "hrm"]
    bc_dict = dict()
    data = None
    basic_list = ["dob", "age", "gender"]

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    userType = res[0]

    comm = "select * from BodyComposition where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()

    if len(res) > 0:
        data = res[0]
        for i in range(len(bc_list)):
            bc_dict[bc_list[i]] = data[i]
    else:
        for i in range(len(bc_list)):
            bc_dict[bc_list[i]] = ""

    comm = "select weight,rhr,asis from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        data = res[0]
        bc_dict["weight"] = data[0]
        bc_dict["rhr"] = data[1]
        bc_dict["asis"] = data[2]

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    username = res[0]

    comm = "select dob,age,gender from User where id='%s';" % username
    cursor.execute(comm)
    res = cursor.fetchone()
    for i in range(len(basic_list)):
        bc_dict[basic_list[i]] = res[i]

    comm = "select height,bp from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    bc_dict["height"] = res[0]
    bc_dict["bp"] = res[1]

    return render_template('body_composition.html', userType=userType, username=current_user, name=uname, dict=bc_dict)


@app.route("/body_composition_form_submit", methods=["get", "post"])
def BCFormSubHandler():
    # uname = request.cookies.get('uname')
    # uname = request.args.get("name")
    uname = request.form.get("Username")

    db, cursor = connDB()
    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    username = res[0]

    comm = "select dob,age,gender from User where id='%s';" % username
    cursor.execute(comm)
    res = cursor.fetchone()
    dob = res[0]
    age = res[1]
    gender = res[2]

    height = request.form.get("height")
    weight = request.form.get("weight")
    bmi = request.form.get("bmi")
    bp = request.form.get("bp")
    rhr = request.form.get("rhr")
    neck = request.form.get("neck")
    chest = request.form.get("chest")
    waist = request.form.get("waist")
    abdomen = request.form.get("abdomen")
    armr = request.form.get("armr")
    arml = request.form.get("arml")
    forearmr = request.form.get("forearmr")
    forearml = request.form.get("forearml")
    buttocks = request.form.get("buttocks")
    midthighr = request.form.get("midthighr")
    midthighl = request.form.get("midthighl")
    calfr = request.form.get("calfr")
    calfl = request.form.get("calfl")
    foot = request.form.get("foot")
    knee = request.form.get("knee")
    asis = request.form.get("asis")
    calfr = request.form.get("calfr")
    calfl = request.form.get("calfl")
    foot = request.form.get("foot")
    knee = request.form.get("knee")
    asis = request.form.get("asis")
    shoulder = request.form.get("shoulder")
    abdomen2 = request.form.get("abdomen2")
    triceps = request.form.get("triceps")
    chest2 = request.form.get("chest2")
    midaxillary = request.form.get("midaxillary")
    subscapular = request.form.get("subscapular")
    suprailiac = request.form.get("suprailiac")
    thigh = request.form.get("thigh")
    sum7 = request.form.get("sum7")

    height = set_zero(height)
    weight = set_zero(weight)
    bmi = set_zero(bmi)
    bp = set_zero(bp)
    rhr = set_zero(rhr)
    neck = set_zero(neck)
    chest = set_zero(chest)
    waist = set_zero(waist)
    abdomen = set_zero(abdomen)
    armr = set_zero(armr)
    arml = set_zero(arml)
    forearmr = set_zero(forearmr)
    forearml = set_zero(forearml)
    buttocks = set_zero(buttocks)
    midthighr = set_zero(midthighr)
    midthighl = set_zero(midthighl)
    calfr = set_zero(calfr)
    calfl = set_zero(calfl)
    foot = set_zero(foot)
    knee = set_zero(knee)
    asis = set_zero(asis)
    shoulder = set_zero(shoulder)
    abdomen2 = set_zero(abdomen2)
    triceps = set_zero(triceps)
    chest2 = set_zero(chest2)
    midaxillary = set_zero(midaxillary)
    subscapular = set_zero(subscapular)
    suprailiac = set_zero(suprailiac)
    thigh = set_zero(thigh)
    sum7 = set_zero(sum7)
    # age = set_zero(age)

    sum3m1 = request.form.get("sum3m1")
    sum3m2 = request.form.get("sum3m2")
    sum3f1 = request.form.get("sum3f1")
    sum3f2 = request.form.get("sum3f2")
    sum3m1 = set_zero(sum3m1)
    sum3m2 = set_zero(sum3m2)
    sum3f1 = set_zero(sum3f1)
    sum3f2 = set_zero(sum3f2)
    sum31 = sum3m1
    sum32 = sum3m2
    if gender == "female":
        sum31 = sum3f1
        sum32 = sum3f2

    bd1m = request.form.get("bd1m")
    bd2m = request.form.get("bd2m")
    bd3m = request.form.get("bd3m")
    bd1f = request.form.get("bd1f")
    bd2f = request.form.get("bd2f")
    bd3f = request.form.get("bd3f")
    bd1m = set_zero(bd1m)
    bd2m = set_zero(bd2m)
    bd3m = set_zero(bd3m)
    bd1f = set_zero(bd1f)
    bd2f = set_zero(bd2f)
    bd3f = set_zero(bd3f)
    bd1 = bd1m
    bd2 = bd2m
    bd3 = bd3m
    if gender == "female":
        bd1 = bd1f
        bd2 = bd2f
        bd3 = bd3f

    bf1m = request.form.get("bf1m")
    bf2m = request.form.get("bf2m")
    bf3m = request.form.get("bf3m")
    bf1f = request.form.get("bf1f")
    bf2f = request.form.get("bf2f")
    bf3f = request.form.get("bf3f")
    bf1m = set_zero(bf1m)
    bf2m = set_zero(bf2m)
    bf3m = set_zero(bf3m)
    bf1f = set_zero(bf1f)
    bf2f = set_zero(bf2f)
    bf3f = set_zero(bf3f)
    bf1 = bf1m
    bf2 = bf2m
    bf3 = bf3m
    # # printbf1f, "####"

    if gender == "female":
        bf1 = bf1f
        bf2 = bf2f
        bf3 = bf3f

    bfm = request.form.get("bfm")
    bff = request.form.get("bff")
    bfm = set_zero(bfm)
    bff = set_zero(bff)
    bf = bfm
    if gender == "female":
        bf = bff

    fm = request.form.get("fm")
    lbm = request.form.get("lbm")
    circumference = request.form.get("circumference")
    wthr = request.form.get("wthr")
    bmr = request.form.get("bmr")
    act_level = request.form.get("act_level")
    tdee = request.form.get("tdee")
    hrm = request.form.get("hrm")

    fm = set_zero(fm)
    lbm = set_zero(lbm)
    circumference = set_zero(circumference)
    wthr = set_zero(wthr)
    bmr = set_zero(bmr)
    act_level = set_zero(act_level)
    tdee = set_zero(tdee)
    hrm = set_zero(hrm)

    # # printuname, dob, gender, height, weight, bmi, bp, rhr, neck, chest, waist, abdomen, armr, arml, forearmr, forearml, buttocks, midthighr, midthighl, calfr, calfl, foot, knee, asis, shoulder, abdomen2, triceps, chest2, midaxillary, subscapular, suprailiac, thigh, sum7, sum31, sum32, bd1, bd2, bd3, bf1, bf2,bf3,bf,fm,lbm,circumference,wthr,bmr,act_level,tdee
    # # print"----"

    # # print"rec", cs2, cs3
    # id, dob, gender, height, weight, bmi, bp, rhr, neck, chest, waist, abdomen, armr, arml, forearmr, forearml, buttocks, midthighr, midthighl, calfr, calfl, foot, knee, asis, shoulder, abdomen2, triceps, chest2, midaxillary, subscapular, suprailiac, thigh, sum7, sum31, sum32, bd1, bd2, bd3, bf1, bf2,bf3,bf,fm,lbm,circumference,wthr,bmr,act_level,tdee

    db, cursor = connDB()
    comm = "select * from BodyComposition where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        # # print"user already exist"
        # return "user exist"
        comm = "delete from BodyComposition where id='%s';" % uname
        cursor.execute(comm)

    # else:
    comm = "insert into BodyComposition values('%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'\
	,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s');" % (uname, height, weight, bmi, bp, rhr, neck, chest, waist,
                    abdomen, armr, arml, forearmr, forearml, buttocks, midthighr, midthighl,
                    calfr, calfl, foot, knee, asis, shoulder, abdomen2, triceps, chest2,
                    midaxillary, subscapular, suprailiac, thigh, sum7, sum31, sum32,
                    bd1, bd2, bd3, bf1, bf2, bf3, bf, fm, lbm, circumference, wthr,
                    bmr, act_level, tdee, hrm)

    # # printcomm #48 vs 49 ?
    cursor.execute(comm)
    db.commit()

    # return render_template('body_composition.html', name="justin")
    # return "success"
    return redirect("/general_form?name=%s" % uname)


# return render_template('body_composition.html', name="justin")


@app.route("/balance_form")
def BFormHandler():
    current_user = request.cookies.get('uname')
    # uname = request.cookies.get('uname')
    uname = request.args.get("name")
    # username = request.form.get("username")
    asis = None

    balance_list = ["uname", "ft", "dls", "dlsp", "lf", "lsls", "lts", "lslsp", "ltsp", "rf", "rsls", "rts", "rslsp",
                    "rtsp", "tf", "lbb", "lk2t", "lh", "lrb", "lfs", "cs", "rbb", "rk2t", "rh", "rrb", "rfs", "cs2",
                    "lat1", "lat2", "lat3", "laas", "larrd", "lacrd", "lpt1", "lpt2", "lpt3", "lpas", "lprrd", "lpcrd",
                    "lpt21", "lpt22", "lpt23", "lpas2", "lprrd2", "lpcrd2", "cs3", "rat1", "rat2", "rat3", "raas",
                    "rarrd", "racrd", "rpt1", "rpt2", "rpt3", "rpas", "rprrd", "rpcrd", "rpt21", "rpt22", "rpt23",
                    "rpas2", "rprrd2", "rpcrd2", "cs4", "lkup", "rkup"]
    balance_dict = dict()
    data = None

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    userType = res[0]

    comm = "select asis from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) == 0:
        # # print"user already exist"
        # return "fill Body Composition form first!"
        return render_template('warning.html', test_id=uname)

    else:
        asis = res[0][0]
        comm = "select * from Balance where id='%s';" % uname
        cursor.execute(comm)
        res = cursor.fetchall()

        if len(res) > 0:
            data = res[0]
            for i in range(len(balance_list)):
                balance_dict[balance_list[i]] = data[i]
        else:
            for i in range(len(balance_list)):
                balance_dict[balance_list[i]] = ""

    return render_template('balance.html', userType=userType, username=current_user, name=uname, asis=asis,
                           dict=balance_dict)


@app.route("/balance_form_submit", methods=["get", "post"])
def BFormSubHandler():
    # uname = request.cookies.get('uname')
    # uname = request.args.get("name")
    uname = request.form.get("Username")

    ft = request.form.get("ft")
    dls = request.form.get("dls")
    dlsp = request.form.get("dlsp")
    lf = request.form.get("lf")
    lsls = request.form.get("lsls")
    lts = request.form.get("lts")
    lslsp = request.form.get("lslsp")
    ltsp = request.form.get("ltsp")
    rf = request.form.get("rf")
    rsls = request.form.get("rsls")
    rts = request.form.get("rts")
    rslsp = request.form.get("rslsp")
    rtsp = request.form.get("rtsp")
    tf = request.form.get("tf")
    lbb = request.form.get("lbb")
    lk2t = request.form.get("lk2t")
    lh = request.form.get("lh")
    lrb = request.form.get("lrb")
    lfs = request.form.get("lfs")
    cs = request.form.get("cs")
    rbb = request.form.get("rbb")
    rk2t = request.form.get("rk2t")
    rh = request.form.get("rh")
    rrb = request.form.get("rrb")
    rfs = request.form.get("rfs")
    cs2 = request.form.get("cs2")
    lat1 = request.form.get("lat1")
    lat2 = request.form.get("lat2")
    lat3 = request.form.get("lat3")
    laas = request.form.get("laas")
    larrd = request.form.get("larrd")
    lacrd = request.form.get("lacrd")
    lpt1 = request.form.get("lpt1")
    lpt2 = request.form.get("lpt2")
    lpt3 = request.form.get("lpt3")
    lpas = request.form.get("lpas")
    lprrd = request.form.get("lprrd")
    lpcrd = request.form.get("lpcrd")
    lpt21 = request.form.get("lpt21")
    lpt22 = request.form.get("lpt22")
    lpt23 = request.form.get("lpt23")
    lpas2 = request.form.get("lpas2")
    lprrd2 = request.form.get("lprrd2")
    lpcrd2 = request.form.get("lpcrd2")
    cs3 = request.form.get("cs3")
    rat1 = request.form.get("rat1")
    rat2 = request.form.get("rat2")
    rat3 = request.form.get("rat3")
    raas = request.form.get("raas")
    rarrd = request.form.get("rarrd")
    racrd = request.form.get("racrd")
    rpt1 = request.form.get("rpt1")
    rpt2 = request.form.get("rpt2")
    rpt3 = request.form.get("rpt3")
    rpas = request.form.get("rpas")
    rprrd = request.form.get("rprrd")
    rpcrd = request.form.get("rpcrd")
    rpt21 = request.form.get("rpt21")
    rpt22 = request.form.get("rpt22")
    rpt23 = request.form.get("rpt23")
    rpas2 = request.form.get("rpas2")
    rprrd2 = request.form.get("rprrd2")
    rpcrd2 = request.form.get("rpcrd2")
    cs4 = request.form.get("cs4")
    lkup = request.form.get("lkup")
    rkup = request.form.get("rkup")

    ft = set_zero(ft)
    dls = set_zero(dls)
    dlsp = set_zero(dlsp)
    lf = set_zero(lf)
    lsls = set_zero(lsls)
    lts = set_zero(lts)
    lslsp = set_zero(lslsp)
    ltsp = set_zero(ltsp)
    rf = set_zero(rf)
    rsls = set_zero(rsls)
    rts = set_zero(rts)
    rslsp = set_zero(rslsp)
    rtsp = set_zero(rtsp)
    tf = set_zero(tf)
    lbb = set_zero(lbb)
    lk2t = set_zero(lk2t)
    lh = set_zero(lh)
    lrb = set_zero(lrb)
    lfs = set_zero(lfs)
    cs = set_zero(cs)
    rbb = set_zero(rbb)
    rk2t = set_zero(rk2t)
    rh = set_zero(rh)
    rrb = set_zero(rrb)
    rfs = set_zero(rfs)
    cs2 = set_zero(cs2)
    lat1 = set_zero(lat1)
    lat2 = set_zero(lat2)
    lat3 = set_zero(lat3)
    laas = set_zero(laas)
    larrd = set_zero(larrd)
    lacrd = set_zero(lacrd)
    lpt1 = set_zero(lpt1)
    lpt2 = set_zero(lpt2)
    lpt3 = set_zero(lpt3)
    lpas = set_zero(lpas)
    lprrd = set_zero(lprrd)
    lpcrd = set_zero(lpcrd)
    lpt21 = set_zero(lpt21)
    lpt22 = set_zero(lpt22)
    lpt23 = set_zero(lpt23)
    lpas2 = set_zero(lpas2)
    lprrd2 = set_zero(lprrd2)
    lpcrd2 = set_zero(lpcrd2)
    cs3 = set_zero(cs3)
    rat1 = set_zero(rat1)
    rat2 = set_zero(rat2)
    rat3 = set_zero(rat3)
    raas = set_zero(raas)
    rarrd = set_zero(rarrd)
    racrd = set_zero(racrd)
    rpt1 = set_zero(rpt1)
    rpt2 = set_zero(rpt2)
    rpt3 = set_zero(rpt3)
    rpas = set_zero(rpas)
    rprrd = set_zero(rprrd)
    rpcrd = set_zero(rpcrd)
    rpt21 = set_zero(rpt21)
    rpt22 = set_zero(rpt22)
    rpt23 = set_zero(rpt23)
    rpas2 = set_zero(rpas2)
    rprrd2 = set_zero(rprrd2)
    rpcrd2 = set_zero(rpcrd2)
    cs4 = set_zero(cs4)
    lkup = set_zero(lkup)
    rkup = set_zero(rkup)

    # # print"rec", cs2, cs3

    # id, ft, dls, dlsp, lf, lsls, lts, lslsp, ltsp, rf, rsls, rts, rslsp, rtsp, tf, lbb, lk2t, lh, lrb, lfs, cs, rbb, rk2t, rh, rrb, rfs, cs2, lat1, lat2, lat3, laas, larrd, lacrd, lpt1, lpt2, lpt3, lpas, lprrd, lpcrd, lpt21, lpt22, lpt23, lpas2, lprrd2, lpcrd2, cs3, rat1, rat2, rat3, raas, rarrd, racrd, rpt1, rpt2, rpt3, rpas, rprrd, rpcrd, rpt21, rpt22, rpt23, rpas2, rprrd2, rpcrd2, cs4

    db, cursor = connDB()
    comm = "select * from Balance where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        # # print"user already exist"
        comm = "delete from Balance where id='%s';" % uname
        cursor.execute(comm)
    # return "user exist"

    # else:
    comm = "insert into Balance values('%s','%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
	'%s','%s');" % (uname, ft, dls, dlsp, lf, lsls, lts, lslsp, ltsp, rf, rsls, rts, rslsp,
                    rtsp, tf, lbb, lk2t, lh, lrb, lfs, cs, rbb, rk2t, rh, rrb, rfs, cs2,
                    lat1, lat2, lat3, laas, larrd, lacrd, lpt1, lpt2, lpt3, lpas, lprrd,
                    lpcrd, lpt21, lpt22, lpt23, lpas2, lprrd2, lpcrd2, cs3, rat1, rat2,
                    rat3, raas, rarrd, racrd, rpt1, rpt2, rpt3, rpas, rprrd, rpcrd, rpt21,
                    rpt22, rpt23, rpas2, rprrd2, rpcrd2, cs4, lkup, rkup)

    # # printcomm
    cursor.execute(comm)
    db.commit()

    # return render_template('balance.html', name="justin")
    # return "success"
    # return redirect("/cardiopulmonary_fitness_form?name=%s"%uname)
    return redirect("/general_form?name=%s" % uname)


# return render_template('balance.html', name="justin")


@app.route("/cardiopulmonary_fitness_form")
def CFFormHandler():
    current_user = request.cookies.get('uname')
    # uname = request.cookies.get('uname')
    uname = request.args.get("name")
    # username = request.form.get("username")

    age = rhr = None

    cf_list = ["uname", "ymca", "aphrm", "ghrm", "thr", "hrm", "sp60", "sp120", "aphrm50", "aphrm60", "aphrm70",
               "aphrm80", "aphrm90", "sp60_pre", "sp120_pre", "hrm_w"]
    cf_dict = dict()

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    userType = res[0]

    comm = "select * from CardiopulmonaryFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]
        for i in range(len(cf_list)):
            cf_dict[cf_list[i]] = data[i]
    else:
        for i in range(len(cf_list)):
            cf_dict[cf_list[i]] = ""

    comm = "select rhr from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()

    comm3 = "select user from History where test_id='%s';" % uname
    cursor.execute(comm3)
    res3 = cursor.fetchone()
    comm2 = "select age from User where id='%s';" % res3[0]
    cursor.execute(comm2)
    res2 = cursor.fetchone()
    # # printres[0], res2[0]

    if not res or not res2:
        # # print"user already exist"
        # return "fill Body Composition form first!"
        return render_template('warning.html', test_id=uname)
    else:
        rhr = res[0]
        age = res2[0]
        return render_template('cardiopulmonary_finess.html', userType=userType, username=current_user, dict=cf_dict,
                               name=uname, age=age, rhr=rhr)


@app.route("/cardiopulmonary_fitness_form_submit", methods=["get", "post"])
def CFFormSubHandler():
    # uname = request.cookies.get('uname')
    # uname = request.args.get("name")
    uname = request.form.get("Username")

    ymca = request.form.get("ymca")
    aphrm = request.form.get("aphrm")
    ghrm = request.form.get("ghrm")
    thr = request.form.get("thr")
    hrm = request.form.get("hrm")
    hrm_w = request.form.get("hrm_w")
    sp60 = request.form.get("sp60")
    sp120 = request.form.get("sp120")
    sp60_pre = request.form.get("sp60_pre")
    sp120_pre = request.form.get("sp120_pre")
    aphrm50 = request.form.get("aphrm50")
    aphrm60 = request.form.get("aphrm60")
    aphrm70 = request.form.get("aphrm70")
    aphrm80 = request.form.get("aphrm80")
    aphrm90 = request.form.get("aphrm90")

    ymca = set_zero(ymca)
    aphrm = set_zero(aphrm)
    ghrm = set_zero(ghrm)
    thr = set_zero(thr)
    hrm = set_zero(hrm)
    hrm_w = set_zero(hrm_w)
    sp60 = set_zero(sp60)
    sp120 = set_zero(sp120)
    sp60_pre = set_zero(sp60_pre)
    sp120_pre = set_zero(sp120_pre)
    aphrm50 = set_zero(aphrm50)
    aphrm60 = set_zero(aphrm60)
    aphrm70 = set_zero(aphrm70)
    aphrm80 = set_zero(aphrm80)
    aphrm90 = set_zero(aphrm90)

    # # printthr, "****"
    # id, ymca, aphrm, ghrm, thr, hrm, sp60, sp120, aphrm50, aphrm60, aphrm70, aphrm80, aphrm90
    db, cursor = connDB()
    comm = "select * from CardiopulmonaryFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        # # print"user already exist"
        # return "user exist"
        comm = "delete from CardiopulmonaryFitness where id='%s';" % uname
        cursor.execute(comm)

    # else:
    comm = "insert into CardiopulmonaryFitness values('%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s', '%s');" % (uname, ymca, aphrm, ghrm, \
                                                                         thr, hrm, sp60, sp120, aphrm50, aphrm60,
                                                                         aphrm70, aphrm80, aphrm90, sp60_pre, sp120_pre,
                                                                         hrm_w)

    # # printcomm
    cursor.execute(comm)
    db.commit()

    # return render_template('cardiopulmonary_finess.html', name="justin")
    # return "success"
    # return redirect("/muscular_fitness_form?name=%s"%uname)
    return redirect("/general_form?name=%s" % uname)


@app.route("/muscular_fitness_form")
def MFFormHandler():
    current_user = request.cookies.get('uname')
    # uname = request.cookies.get('uname')
    uname = request.args.get("name")
    # username = request.form.get("username")

    weight = None
    mf_list = ["uname", "rmp", "bpwr", "rmp2", "pwr", "rml", "lpwr", "rhd", "lhd", "cd", "pu", "kpu", "pu2", "squ"]
    mf_dict = dict()

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    userType = res[0]

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    user = cursor.fetchone()[0]
    comm = "select gender from User where id='%s';" % user
    cursor.execute(comm)
    mf = cursor.fetchone()[0]

    comm = "select * from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]
        for i in range(len(mf_list)):
            mf_dict[mf_list[i]] = data[i]
    else:
        for i in range(len(mf_list)):
            mf_dict[mf_list[i]] = ""

    comm = "select weight from General where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) == 0:
        # # print"user already exist"
        # return "fill Body Composition form first!"
        return render_template('warning.html', test_id=uname)
    else:
        weight = res[0][0]
        return render_template('muscular_fitness.html', mf=mf, userType=userType, username=current_user, dict=mf_dict,
                               name=uname, weight=weight)


@app.route("/muscular_fitness_form_submit", methods=["get", "post"])
def MFFormSubHandler():
    # uname = request.cookies.get('uname')
    # uname = request.args.get("name")
    uname = request.form.get("Username")

    rmp = request.form.get("rmp")
    bpwr = request.form.get("bpwr")
    rmp2 = request.form.get("rmp2")
    pwr = request.form.get("pwr")
    rml = request.form.get("rml")
    lpwr = request.form.get("lpwr")
    rhd = request.form.get("rhd")
    lhd = request.form.get("lhd")
    cd = request.form.get("cd")
    pu = request.form.get("pu")
    kpu = request.form.get("kpu")
    pu2 = request.form.get("pu2")
    squ = request.form.get("squ")

    rmp = set_zero(rmp)
    bpwr = set_zero(bpwr)
    rmp2 = set_zero(rmp2)
    pwr = set_zero(pwr)
    rml = set_zero(rml)
    lpwr = set_zero(lpwr)
    rhd = set_zero(rhd)
    lhd = set_zero(lhd)
    cd = set_zero(cd)
    pu = set_zero(pu)
    kpu = set_zero(kpu)
    pu2 = set_zero(pu2)
    squ = set_zero(squ)

    # # print"rec", bpwr, rmp

    # id, rmp, bpwr, rmp2, pwr, rml, lpwr, rhd, lhd, cd, pu, kpu, pu2, squ

    db, cursor = connDB()
    comm = "select * from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        # # print"user already exist"
        # return "user exist"
        comm = "delete from MuscularFitness where id='%s';" % uname
        cursor.execute(comm)

    # else:
    comm = "insert into MuscularFitness values('%s', '%s','%s','%s','%s',\
	'%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (uname, rmp, bpwr, rmp2, \
                                                       pwr, rml, lpwr, rhd, lhd, cd, pu, kpu, pu2, squ)

    # # printcomm
    cursor.execute(comm)
    db.commit()

    # return render_template('muscular_fitness.html', name="justin")
    # return "success"
    # return redirect("/range_of_motion_form?name=%s"%uname)
    return redirect("/general_form?name=%s" % uname)


@app.route("/range_of_motion_form")
def ROMFormHandler():
    current_user = request.cookies.get('uname')
    # uname = request.cookies.get('uname')
    uname = request.args.get("name")
    # username = request.form.get("username")

    rom_list = ["uname", "fle", "ext", "slrr", "slrl", "th", "hin", "fler", "flel", "extr", "extl", "abdr", "abdl",
                "lrr", "lrl", "lrr_c", "lrl_c", "fle_c", "ext_c", "fler_a", "flel_a", "extr_a", "extl_a", "fler_w",
                "flel_w", "extr_w", "extl_w", "fler_e", "flel_e", "extr_e", "extl_e", "pror_e", "prol_e", "supr_e",
                "supl_e", "fler_k", "flel_k", "extr_k", "extl_k", "fler_h", "flel_h", "hypr_h", "hypl_h", "abdr_h",
                "abdl_h"]
    rom_dict = dict()

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    userType = res[0]

    comm = "select * from RangeOfMotion where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]
        for i in range(len(rom_list)):
            rom_dict[rom_list[i]] = data[i]
    else:
        for i in range(len(rom_list)):
            rom_dict[rom_list[i]] = ""

    return render_template('range_of_motion.html', userType=userType, username=current_user, name=uname, dict=rom_dict)


@app.route("/range_of_motion_form_submit", methods=["get", "post"])
def ROMFormSubHandler():
    # uname = request.cookies.get('uname')
    # uname = request.args.get("name")
    uname = request.form.get("Username")

    # arrlist = ["fle", "ext","slrr","slrl", "th", "hin","fler","flel","extr","extl","abdr","abdl","lrr","lrl","lrr_c","lrl_c","fle_c","ext_c","fler_a","flel_a","extr_a","extl_a","fler_w","flel_w","extr_w","extl_w","fler_e","flel_e","extr_e","extl_e","pror_e","prol_e","supr_e","supl_e","fler_k","flel_k","extr_k","extl_k","fler_h","flel_h","hypr_h","hypl_h","abdr_h","abdl_h"]
    # for ele in arrlist:

    fle = request.form.get("fle")
    ext = request.form.get("ext", 0)
    slrr = request.form.get("slrr", 0)
    slrl = request.form.get("slrl", 0)
    th = request.form.get("th", 0)
    hin = request.form.get("hin", 0)
    fler = request.form.get("fler", 0)
    flel = request.form.get("flel", 0)
    extr = request.form.get("extr", 0)
    extl = request.form.get("extl", 0)
    abdr = request.form.get("abdr", 0)
    abdl = request.form.get("abdl", 0)
    lrr = request.form.get("lrr", 0)
    lrl = request.form.get("lrl", 0)
    lrr_c = request.form.get("lrr_c", 0)
    lrl_c = request.form.get("lrl_c", 0)
    fle_c = request.form.get("fle_c", 0)
    ext_c = request.form.get("ext_c", 0)
    fler_a = request.form.get("fler_a", 0)
    flel_a = request.form.get("flel_a", 0)
    extr_a = request.form.get("extr_a", 0)
    extl_a = request.form.get("extl_a", 0)
    fler_w = request.form.get("fler_w", 0)
    flel_w = request.form.get("flel_w", 0)
    extr_w = request.form.get("extr_w", 0)
    extl_w = request.form.get("extl_w", 0)
    fler_e = request.form.get("fler_e", 0)
    flel_e = request.form.get("flel_e", 0)
    extr_e = request.form.get("extr_e", 0)
    extl_e = request.form.get("extl_e", 0)
    pror_e = request.form.get("pror_e", 0)
    prol_e = request.form.get("prol_e", 0)
    supr_e = request.form.get("supr_e", 0)
    supl_e = request.form.get("supl_e", 0)
    fler_k = request.form.get("fler_k", 0)
    flel_k = request.form.get("flel_k", 0)
    extr_k = request.form.get("extr_k", 0)
    extl_k = request.form.get("extl_k", 0)
    fler_h = request.form.get("fler_h", 0)
    flel_h = request.form.get("flel_h", 0)
    hypr_h = request.form.get("hypr_h", 0)
    hypl_h = request.form.get("hypl_h", 0)
    abdr_h = request.form.get("abdr_h", 0)
    abdl_h = request.form.get("abdl_h", 0)

    fle = set_zero(fle)
    ext = set_zero(ext)
    slrr = set_zero(slrr)
    slrl = set_zero(slrl)
    th = set_zero(th)
    hin = set_zero(hin)
    fler = set_zero(fler)
    flel = set_zero(flel)
    extr = set_zero(extr)
    extl = set_zero(extl)
    abdr = set_zero(abdr)
    abdl = set_zero(abdl)
    lrr = set_zero(lrr)
    lrl = set_zero(lrl)
    lrr_c = set_zero(lrr_c)
    lrl_c = set_zero(lrl_c)
    fle_c = set_zero(fle_c)
    ext_c = set_zero(ext_c)
    fler_a = set_zero(fler_a)
    flel_a = set_zero(flel_a)
    extr_a = set_zero(extr_a)
    extl_a = set_zero(extl_a)
    fler_w = set_zero(fler_w)
    flel_w = set_zero(flel_w)
    extr_w = set_zero(extr_w)
    extl_w = set_zero(extl_w)
    fler_e = set_zero(fler_e)
    flel_e = set_zero(flel_e)
    extr_e = set_zero(extr_e)
    extl_e = set_zero(extl_e)
    pror_e = set_zero(pror_e)
    prol_e = set_zero(prol_e)
    supr_e = set_zero(supr_e)
    supl_e = set_zero(supl_e)
    fler_k = set_zero(fler_k)
    flel_k = set_zero(flel_k)
    extr_k = set_zero(extr_k)
    extl_k = set_zero(extl_k)
    fler_h = set_zero(fler_h)
    flel_h = set_zero(flel_h)
    hypr_h = set_zero(hypr_h)
    hypl_h = set_zero(hypl_h)
    abdr_h = set_zero(abdr_h)
    abdl_h = set_zero(abdl_h)

    # id, fle, ext, slrr, slrl, th, hin, fler, flel, extr, extl, abdr, abdl, lrr, lrl, lrr_c, lrl_c, fle_c, ext_c, fler_a, flel_a, extr_a, extl_a, fler_w, flel_w, extr_w, extl_w, fler_e, flel_e, extr_e, extl_e, pror_e, prol_e, supr_e, supl_e, fler_k, flel_k, extr_k, extl_k, fler_h, flel_h, hypr_h, hypl_h, abdr_h, abdl_h

    try:
        db, cursor = connDB()
        comm = "select * from RangeOfMotion where id='%s';" % uname
        cursor.execute(comm)
        res = cursor.fetchall()

        if len(res) > 0:
            # # print("user already exist")
            # return "user exist"

            ## update data
            comm = "delete from RangeOfMotion where id='%s';" % uname
            cursor.execute(comm)

        # # printlrr_c, "##@#"
        # else:
        comm = "insert into RangeOfMotion values('%s', '%s','%s','%s','%s',\
		'%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s',\
		'%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s',\
		'%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s');" % (
        uname, fle, ext, slrr, slrl, th, hin, fler, flel, extr, extl, abdr, abdl, lrr, lrl, lrr_c, lrl_c, fle_c, ext_c,
        fler_a, flel_a, extr_a, extl_a, fler_w, flel_w, extr_w, extl_w, fler_e, flel_e, extr_e, extl_e, pror_e, prol_e,
        supr_e, supl_e, fler_k, flel_k, extr_k, extl_k, fler_h, flel_h, hypr_h, hypl_h, abdr_h, abdl_h)
        # # printcomm
        cursor.execute(comm)

        comm = "update User set fin='1' where id='%s';" % uname
        cursor.execute(comm)
        db.commit()

        # return redirect("/patient_list")
        return redirect("/general_form?name=%s" % uname)


    except:
        return redirect("/range_of_motion_form")


@app.route("/addUser")
def AddUserHandler():
    return redirect("/basic_form?fr_doc=t")


@app.route("/delete_user")
def DeleteUserHandler():
    uname = request.args.get("name")
    db, cursor = connDB()
    comm = "delete from User where id='%s';" % (uname)
    cursor.execute(comm)
    db.commit()
    return redirect("/patient_list")


@app.route("/addReport")
def AddHandler():
    uname = request.args.get("name")
    now = datetime.datetime.now()
    hash_object = hashlib.sha256(str(now))
    test_id = hash_object.hexdigest()
    date = str(now).split(" ")[0].split("-")
    f_date = "%s/%s/%s" % (date[1], date[2], date[0])

    db, cursor = connDB()
    comm = "insert into History values('%s', '%s', '%s');" % (test_id, uname, f_date)
    cursor.execute(comm)
    db.commit()

    tar = "general_form?name=%s" % (test_id)
    return redirect(tar)


# return redirect("/patient_list")


@app.route("/delete")
def DelHandler():
    test_id = uname = request.args.get("name")
    db, cursor = connDB()

    comm = "delete from History where test_id='%s';" % uname
    cursor.execute(comm)

    # comm = "delete from BodyComposition where id='%s';"%uname
    # cursor.execute(comm)

    # comm = "delete from CardiopulmonaryFitness where id='%s';"%uname
    # cursor.execute(comm)

    # comm = "delete from Balance where id='%s';"%uname
    # cursor.execute(comm)

    # comm = "delete from MuscularFitness where id='%s';"%uname
    # cursor.execute(comm)

    # comm = "delete from RangeOfMotion where id='%s';"%uname
    # cursor.execute(comm)

    db.commit()

    return redirect("/patient_list")


@app.route("/result_m")
def ResMHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    # bc_table = load_bc()
    # car_table = load_car()
    # balance_table = load_balance()
    # rom_table = load_rom()
    # mf_table = load_mf()

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    test_id = uname = request.args.get("name")

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, test_id)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    # for ele in tabs:
    # 	comm = "select * from %s where id='%s';"%(ele, test_id)
    # 	cursor.execute(comm)
    # 	res = cursor.fetchall()
    # 	if len(res)==0:
    # 		return render_template('result_m.html', userType=ut, username=current_user, name=uname, score=None, fin=0)

    #  
    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    user = cursor.fetchone()[0]
    #  
    # #  
    # 	comm = "select user from History where test_id='%s';"%uname
    # 	cursor.execute(comm)
    # 	user = cursor.fetchone()[0]
    # #  

    comm = "select fin from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()

    comm = "select gender, age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    mf = "male"
    if len(res) > 0:
        mf = res[0][0]
        age = int(res[0][1])

    ## bc
    # for data in res:
    if True:
        score_bc = 0
        try:
            comm = "select * from BodyComposition where id='%s';" % test_id
            cursor.execute(comm)
            res = cursor.fetchall()
            data = None
            if len(res) > 0:
                data = res[0]

            basic_list = ["dob", "age", "gender"]
            bc_list = ["uname", "height", "weight", "bmi", "bp", "rhr", "neck", "chest", "waist", "abdomen", "armr",
                       "arml", "forearmr", "forearml", "buttocks", "midthighr", "midthighl", "calfr", "calfl", "foot",
                       "knee", "asis", "shoulder", "abdomen2", "triceps", "chest2", "midaxillary", "subscapular",
                       "suprailiac", "thigh", "sum7", "sum31", "sum32", "bd1", "bd2", "bd3", "bf1", "bf2", "bf3", "bf",
                       "fm", "lbm", "circumference", "wthr", "bmr", "act_level", "tdee", "hrm"]
            bc_dict = dict()
            for i in range(len(bc_list)):
                bc_dict[bc_list[i]] = data[i]

            # comm = "select hrm from CardiopulmonaryFitness where id='%s';"%test_id
            # cursor.execute(comm)
            # res = cursor.fetchone()
            # hrm = res[0]

            # # printtest_id, bc_dict["bf"]
            bf = float(bc_dict["bf"])
            wthr = float(bc_dict["wthr"])
            abf = bf
            bmi = float(bc_dict["bmi"])

            # age = int(bc_dict["age"])
            # mf = bc_dict["gender"]
            score = check_table_bc(mf, age, bf, wthr, abf, bmi, bc_table)
            # # printbc_table, age
            # # print[bf, wthr, abf, bmi]
            # # printscore
            score2 = []
            for ele in score:
                score2.append(ele * 1.0 / 10)

            score_bc = round(0.5 * score2[0] + 0.25 * score2[1] + 0.2 * score2[2] + 0.05 * score2[3], 2)

        except:
            score_bc = 0.0

        ## balance
        score_balance = 0
        try:
            comm = "select * from Balance where id='%s';" % test_id
            # # printcomm
            cursor.execute(comm)
            res = cursor.fetchall()
            data = None
            if len(res) > 0:
                data = res[0]

            balance_list = ["uname", "ft", "dls", "dlsp", "lf", "lsls", "lts", "lslsp", "ltsp", "rf", "rsls", "rts",
                            "rslsp", "rtsp", "tf", "lbb", "lk2t", "lh", "lrb", "lfs", "cs", "rbb", "rk2t", "rh", "rrb",
                            "rfs", "cs2", "lat1", "lat2", "lat3", "laas", "larrd", "lacrd", "lpt1", "lpt2", "lpt3",
                            "lpas", "lprrd", "lpcrd", "lpt21", "lpt22", "lpt23", "lpas2", "lprrd2", "lpcrd2", "cs3",
                            "rat1", "rat2", "rat3", "raas", "rarrd", "racrd", "rpt1", "rpt2", "rpt3", "rpas", "rprrd",
                            "rpcrd", "rpt21", "rpt22", "rpt23", "rpas2", "rprrd2", "rpcrd2", "cs4", "lkup", "rkup"]
            valid_list = []
            balance_dict = dict()
            for i in range(len(balance_list)):
                # # printdata[i], i, "##"
                balance_dict[balance_list[i]] = data[i]
            bess_lf = int(balance_dict['lf'])
            bess_rf = int(balance_dict['rf'])
            an_l = float(balance_dict['cs'])
            an_r = float(balance_dict['cs2'])
            y_l = float(balance_dict['cs3'])
            y_r = float(balance_dict['cs4'])

            # comm = "select gender, age from User where id='%s';"%uname
            # cursor.execute(comm)
            # res = cursor.fetchall()
            # age = 0
            # if len(res)>0:
            # 	mf = res[0][0]
            # 	age = int(res[0][1])

            # table = load_balance()
            score = check_table_balance(mf, age, bess_lf, bess_rf, an_l, an_r, y_l, y_r, balance_table)
            # # printscore, "$$"
            # # printbalance_table
            # # printmf, age,score
            # return ""
            score2 = []
            for ele in score:
                if ele > 0:
                    score2.append(round(ele * 1.0 / 10, 2))
                else:
                    score2.append(0.0)

            tot = 0
            count = 0
            s_11 = (score2[0] + score2[1]) / 2
            # s_22 = (score2[2]+score2[3])/2
            # s_33 = (score2[4]+score2[5])/2
            s_22 = (an_l + an_r) / 20
            s_33 = (y_l + y_r) / 20

            if s_11 > 0:
                tot += s_11
                count += 1
            if s_22 > 0:
                tot += s_22
                count += 1
            if s_33 > 0:
                tot += s_33
                count += 1

            if count > 0:
                score_balance = round(tot / count, 2)
        # score_balance = round((s_11+s_22)/2, 2)
        # # print"count", count, score_balance, s_11, s_22, s_33

        # score_balance = 0.33*(score2[0]+score2[1])*0.5+ 0.33*(score2[2]+score2[3])*0.5+0.33*(score2[4]+score2[5])*0.5
        # score_balance = round(score_balance, 2)
        except:
            score_balance = 0.0

        ## car
        score_cf = 0
        try:
            comm = "select * from CardiopulmonaryFitness where id='%s';" % test_id
            cursor.execute(comm)
            res = cursor.fetchall()
            data = None
            if len(res) > 0:
                data = res[0]

            cf_list = ["uname", "ymca", "aphrm", "ghrm", "thr", "hrm", "sp60", "sp120", "aphrm50", "aphrm60", "aphrm70",
                       "aphrm80", "aphrm90", "sp60_pre", "sp120_pre", "hrm_w"]
            cf_dict = dict()
            for i in range(len(cf_list)):
                cf_dict[cf_list[i]] = data[i]

            vo2max = float(cf_dict["ymca"])
            hrr = int(cf_dict["sp60_pre"]) - int(cf_dict["sp60"])

            # comm = "select gender, age from User where id='%s';"%uname
            # cursor.execute(comm)
            # res = cursor.fetchall()
            # age = 0
            # if len(res)>0:
            # 	mf = res[0][0]
            # 	age = int(res[0][1])

            # table = load_car()
            score = check_table_car(mf, age, vo2max, hrr, car_table)
            # # printcar_table, hrr
            score2 = []
            for ele in score:
                score2.append(ele * 1.0 / 10)
            # # printscore2
            score_cf = round(0.5 * score2[0] + 0.5 * score2[1], 2)

        except:
            score_cf = 0.0;

        ## mf
        score_mf = 0
        try:
            comm = "select * from MuscularFitness where id='%s';" % test_id
            cursor.execute(comm)
            res = cursor.fetchall()
            data = None
            if len(res) > 0:
                data = res[0]

            mf_list = ["uname", "rmp", "bpwr", "rmp2", "pwr", "rml", "lpwr", "rhd", "lhd", "cd", "pu", "kpu", "pu2",
                       "squ"]
            mf_dict = dict()
            for i in range(len(mf_list)):
                mf_dict[mf_list[i]] = data[i]

            push = float(mf_dict["bpwr"])
            pull = float(mf_dict["pwr"])
            leg = float(mf_dict["lpwr"])
            # grip_l = mf_dict["lhd"]
            # grip_r = mf_dict["rhd"]
            # endurance = mf_dict["pu"] # "pu", "kpu", "pu2", "squ" -> avg?
            # push = float(mf_dict["rmp"])
            # pull = float(mf_dict["rmp2"])
            # leg = float(mf_dict["rml"])
            grip_l = 2 * float(mf_dict["lhd"])
            grip_r = 2 * float(mf_dict["rhd"])
            grip = float(mf_dict["lhd"]) + float(mf_dict["rhd"])
            # endurance = float(mf_dict["pu"])
            # # printgrip_l, "^^$$"

            ## avg of 4
            # end = [float(mf_dict["pu"]), float(mf_dict["kpu"]), float(mf_dict["pu2"]), float(mf_dict["squ"])]
            # tot_rep = 0
            # tot_count = 0
            # for ele in end:
            # 	if ele>0:
            # 		tot_rep += ele
            # 		tot_count += 1
            # endurance = 0
            # if tot_count>0:
            # 	endurance = round(tot_rep/tot_count, 0)
            # endurance = max(end)
            endurance = float(mf_dict["pu"])
            if (mf == "female"):
                endurance = float(mf_dict["kpu"])

            # comm = "select gender, age from User where id='%s';"%uname
            # cursor.execute(comm)
            # res = cursor.fetchall()
            # age = 0
            # if len(res)>0:
            # 	mf = res[0][0]
            # 	age = int(res[0][1])

            # table = load_mf()
            # # printleg, "$$"
            score = check_table_mf(mf, age, pull, push, leg, grip_l, grip_r, grip, endurance, mf_table)
            tt = 0
            cc = 0
            if push > 0:
                tt += score[1]
                cc += 1
            if leg > 0:
                tt += score[2]
                cc += 1
            if cc > 0:
                tt = tt / cc
            score.append(tt)

            score2 = []
            for ele in score:
                score2.append(ele * 1.0 / 10)
            # # printpull, push, leg, grip_l, grip_r, endurance
            # # printscore2

            tot = 0
            count = 0
            # s_11 = (score2[0]+score2[1]+score2[2])/3
            s_11 = (score2[7])
            s_22 = (score2[5])
            s_33 = (score2[6])
            if s_11 > 0:
                tot += s_11
                count += 1
            if s_22 > 0:
                tot += s_22
                count += 1
            if s_33 > 0:
                tot += s_33
                count += 1
            score_mf = 0
            if count > 0:
                score_mf = round(tot / count, 2)

        # score_mf = round(0.33*(score2[0]+score2[1]+score2[2])/3 + 0.33*(score2[3]+score2[4])/2 + 0.33*score2[5],2)
        except:
            score_mf = 0.0

        ## rom
        score_rom = 0
        try:
            comm = "select * from RangeOfMotion where id='%s';" % test_id
            cursor.execute(comm)
            res = cursor.fetchall()
            data = None
            if len(res) > 0:
                data = res[0]

            rom_list = ["uname", "fle", "ext", "slrr", "slrl", "th", "hin", "fler", "flel", "extr", "extl", "abdr",
                        "abdl", "lrr", "lrl", "lrr_c", "lrl_c", "fle_c", "ext_c", "fler_a", "flel_a", "extr_a",
                        "extl_a", "fler_w", "flel_w", "extr_w", "extl_w", "fler_e", "flel_e", "extr_e", "extl_e",
                        "pror_e", "prol_e", "supr_e", "supl_e", "fler_k", "flel_k", "extr_k", "extl_k", "fler_h",
                        "flel_h", "hypr_h", "hypl_h", "abdr_h", "abdl_h"]
            rom_dict = dict()
            for i in range(len(rom_list)):
                # if data[i]=="0":
                # rom_dict[rom_list[i]] = "N"
                # else:
                rom_dict[rom_list[i]] = data[i]

            # comm = "select age from User where id='%s';"%uname
            # cursor.execute(comm)
            # res = cursor.fetchall()
            # age = 0
            # if len(res)>0:
            # 	age = int(res[0][0])

            # table = load_rom()
            s11 = float(rom_dict["flel_h"])
            s12 = float(rom_dict["hypl_h"])
            s13 = float(rom_dict["abdl_h"])
            s11r = float(rom_dict["fler_h"])
            s12r = float(rom_dict["hypr_h"])
            s13r = float(rom_dict["abdr_h"])

            s21 = float(rom_dict["flel_k"])
            s22 = float(rom_dict["extl_k"])
            s21r = float(rom_dict["fler_k"])
            s22r = float(rom_dict["extr_k"])

            s31 = float(rom_dict["flel_a"])
            s32 = float(rom_dict["extl_a"])
            s31r = float(rom_dict["fler_a"])
            s32r = float(rom_dict["extr_a"])

            s41 = float(rom_dict["flel"])
            s42 = float(rom_dict["extl"])
            s43 = float(rom_dict["abdl"])
            s44 = float(rom_dict["lrl"])
            s41r = float(rom_dict["fler"])
            s42r = float(rom_dict["extr"])
            s43r = float(rom_dict["abdr"])
            s44r = float(rom_dict["lrr"])

            s51 = float(rom_dict["flel_e"])
            s52 = float(rom_dict["extl_e"])
            s53 = float(rom_dict["prol_e"])
            s54 = float(rom_dict["supl_e"])
            s51r = float(rom_dict["fler_e"])
            s52r = float(rom_dict["extr_e"])
            s53r = float(rom_dict["pror_e"])
            s54r = float(rom_dict["supr_e"])

            s61 = float(rom_dict["flel_w"])
            s62 = float(rom_dict["extl_w"])
            s61r = float(rom_dict["fler_w"])
            s62r = float(rom_dict["extr_w"])

            s71 = float(rom_dict["fle"])
            s72 = float(rom_dict["ext"])

            s81 = float(rom_dict["fle_c"])
            s82 = float(rom_dict["ext_c"])
            s83 = float(rom_dict["lrl_c"])
            s83r = float(rom_dict["lrr_c"])

            ## get age first!
            arr = [[s11, s12, s13, s11r, s12r, s13r], [s21, s22, s21r, s22r], [s31, s32, s31r, s32r],
                   [s41, s42, s43, s44, s41r, s42r, s43r, s44r], [s51, s52, s53, s54, s51r, s52r, s53r, s54r],
                   [s61, s62, s61r, s62r], [s71, s72], [s81, s82, s83, s83r]]
            scores = check_table_rom(int(age), arr, rom_table)

            # # printarr
            # # printscore
            score_t = []

            # # printscores

            score_11 = sum([scores["1a"], scores["1b"], scores["1c"], scores["1ar"], scores["1br"], scores["1cr"]]) / 6
            score_22 = sum([scores['2a'], scores['2b'], scores['2ar'], scores['2br']]) / 4
            score_33 = sum([scores['3a'], scores['3b'], scores['3ar'], scores['3br']]) / 4
            score_44 = sum(
                [scores['4a'], scores['4b'], scores['4c'], scores['4d'], scores['4ar'], scores['4br'], scores['4cr'],
                 scores['4dr']]) / 8
            score_55 = sum(
                [scores['5a'], scores['5b'], scores['5c'], scores['5d'], scores['5ar'], scores['5br'], scores['5cr'],
                 scores['5dr']]) / 8
            score_66 = sum([scores['6a'], scores['6b'], scores['6ar'], scores['6br']]) / 4
            score_77 = sum([scores['7a'], scores['7b']]) / 2
            score_88 = sum([scores['8a'], scores['8b'], scores['8c'], scores['8cr']]) / 4

            score_rom = round(sum([score_11, score_22, score_33, score_44, score_55, score_66, score_77, score_88]) / 8,
                              2)
        except:
            score_rom = 0.0

        ## sum
        count = 0
        tot = 0
        for single_s in [score_bc, score_balance, score_cf, score_mf, score_rom]:
            if single_s > 0:
                tot += single_s
                count += 1
        score_sum = 0.0
        if count > 0:
            score_sum = round(tot / count, 2)
        score_cf_10 = round(score_cf * 10, 2)

        score = [score_bc, score_balance, score_cf, score_mf, score_rom, score_sum, score_cf_10]

        # test_result.append(score)

        return render_template('result_m.html', states=states, single='f', patient=user, userType=ut,username=current_user, name=uname, score=score, fin=1)


# else:
# score = [2,4,6,10,6,8]
# return render_template('result_m.html', name=uname, score=score_result, fin=0)


@app.route("/result_bc")
def ResBCHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]
    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'
    # if uname=="doc":
    # 	uname = request.args.get("name")

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    bc_list = ["uname", "height", "weight", "bmi", "bp", "rhr", "neck", "chest", "waist", "abdomen", "armr", "arml",
               "forearmr", "forearml", "buttocks", "midthighr", "midthighl", "calfr", "calfl", "foot", "knee", "asis",
               "shoulder", "abdomen2", "triceps", "chest2", "midaxillary", "subscapular", "suprailiac", "thigh", "sum7",
               "sum31", "sum32", "bd1", "bd2", "bd3", "bf1", "bf2", "bf3", "bf", "fm", "lbm", "circumference", "wthr",
               "bmr", "act_level", "tdee", "hrm"]
    bc_dict = dict()
    comm = "select * from BodyComposition where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    # # printcomm
    data = None
    if len(res) > 0:
        data = res[0]

    cir_list = ["neck", "arml", "armr", "forearml", "forearmr", "chest", "waist", "abdomen", "buttocks", "midthighl",
                "midthighr", "calfl", "calfr"]
    for i in range(len(bc_list)):
        if bc_list[i] in cir_list:
            bc_dict[bc_list[i]] = str(round(float(data[i]) / 2.54, 2))
        # # print"change"
        else:
            bc_dict[bc_list[i]] = data[i]

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    user = cursor.fetchone()[0]
    comm = "select dob,age,gender from User where id='%s';" % user
    cursor.execute(comm)
    data_pre = cursor.fetchone()
    basic_list = ["dob", "age", "gender"]
    for i in range(len(basic_list)):
        bc_dict[basic_list[i]] = data_pre[i]

    # comm = "select hrm from CardiopulmonaryFitness where id='%s';"%uname
    # cursor.execute(comm)
    # res = cursor.fetchone()
    # hrm = res[0]

    bf = float(bc_dict["bf"])
    wthr = float(bc_dict["wthr"])
    abf = bf
    bmi = float(bc_dict["bmi"])
    age = int(bc_dict["age"])
    mf = bc_dict["gender"]
    # bc_table = load_bc()
    score = check_table_bc(mf, age, bf, wthr, abf, bmi, bc_table)
    # # printbc_table, age
    # # print[bf, wthr, abf, bmi]

    # # printscore
    score2 = []
    for ele in score:
        score2.append(ele * 1.0 / 10)

    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    sick_user = cursor.fetchone()[0]
    
    return render_template('result_bc.html', states=states, single=single, patient=sick_user, userType=ut,username=current_user, name=uname, bc_dict=bc_dict, score=score2)


@app.route("/result_balance")
def ResBalanceHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    comm = "select * from Balance where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    balance_list = ["uname", "ft", "dls", "dlsp", "lf", "lsls", "lts", "lslsp", "ltsp", "rf", "rsls", "rts", "rslsp",
                    "rtsp", "tf", "lbb", "lk2t", "lh", "lrb", "lfs", "cs", "rbb", "rk2t", "rh", "rrb", "rfs", "cs2",
                    "lat1", "lat2", "lat3", "laas", "larrd", "lacrd", "lpt1", "lpt2", "lpt3", "lpas", "lprrd", "lpcrd",
                    "lpt21", "lpt22", "lpt23", "lpas2", "lprrd2", "lpcrd2", "cs3", "rat1", "rat2", "rat3", "raas",
                    "rarrd", "racrd", "rpt1", "rpt2", "rpt3", "rpas", "rprrd", "rpcrd", "rpt21", "rpt22", "rpt23",
                    "rpas2", "rprrd2", "rpcrd2", "cs4", "lkup", "rkup"]
    valid_list = []
    balance_dict = dict()
    for i in range(len(balance_list)):
        balance_dict[balance_list[i]] = data[i]
    bess_lf = int(balance_dict['lf'])
    bess_rf = int(balance_dict['rf'])
    an_l = float(balance_dict['cs'])
    an_r = float(balance_dict['cs2'])
    y_l = float(balance_dict['cs3'])
    y_r = float(balance_dict['cs4'])
    mf = "male"
    age = 0

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    user = res[0]

    comm = "select gender, age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    if len(res) > 0:
        mf = res[0][0]
        age = int(res[0][1])

    # balance_table = load_balance()
    score = check_table_balance(mf, age, bess_lf, bess_rf, an_l, an_r, y_l, y_r, balance_table)
    score[2] = float(balance_dict['cs'])
    score[3] = float(balance_dict['cs2'])
    score[4] = float(balance_dict['cs3'])
    score[5] = float(balance_dict['cs4'])
    score.append(round(score[4] * 10, 2))
    score.append(round(score[5] * 10, 2))

    # printscore[0], score[1], "$$$"
    # # printscore, "$$"
    # # printbalance_table
    # # printscore
    score2 = []
    for ele in score:
        if ele > 0:
            score2.append(round(ele * 1.0 / 10, 2))
        else:
            score2.append(0.0)
    print(score2)
    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    sick_user = cursor.fetchone()[0]
    return render_template('result_balance.html', states=states, single=single, patient=sick_user, userType=ut,
                       username=current_user, name=uname, dict=balance_dict, score=score2)


@app.route("/result_cf")
def ResCFHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    comm = "select * from CardiopulmonaryFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    cf_list = ["uname", "ymca", "aphrm", "ghrm", "thr", "hrm", "sp60", "sp120", "aphrm50", "aphrm60", "aphrm70",
               "aphrm80", "aphrm90", "sp60_pre", "sp120_pre", "hrm_w"]
    cf_dict = dict()
    for i in range(len(cf_list)):
        cf_dict[cf_list[i]] = data[i]

    vo2max = float(cf_dict["ymca"])
    # # printcf_dict["sp60_pre"], "$$$"
    hrr = int(cf_dict["sp60_pre"]) - int(cf_dict["sp60"])
    mf = "male"
    age = 0

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    user = res[0]

    comm = "select gender,age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    if len(res) > 0:
        mf = res[0][0]
        age = int(res[0][1])

    # table = load_car()
    # car_table = load_car()
    score = check_table_car(mf, age, vo2max, hrr, car_table)
    # # printcar_table, hrr, vo2max
    score2 = []
    for ele in score:
        score2.append(ele * 1.0 / 10)


# # printscore2

    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    sick_user = cursor.fetchone()[0]
    return render_template('result_car.html', states=states, single=single, patient=sick_user, userType=ut,
                       username=current_user, name=uname, dict=cf_dict, score=score2)


@app.route("/result_mf")
def ResMFHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    uid = res[0]

    comm = "select gender from User where id='%s';" % uid
    cursor.execute(comm)
    res = cursor.fetchone()
    mf = res[0]

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    comm = "select * from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    mf_list = ["uname", "rmp", "bpwr", "rmp2", "pwr", "rml", "lpwr", "rhd", "lhd", "cd", "pu", "kpu", "pu2", "squ"]
    mf_dict = dict()
    for i in range(len(mf_list)):
        mf_dict[mf_list[i]] = data[i]

    push = float(mf_dict["bpwr"])
    pull = float(mf_dict["pwr"])
    leg = float(mf_dict["lpwr"])
    # grip_l = mf_dict["lhd"]
    # grip_r = mf_dict["rhd"]
    # endurance = mf_dict["pu"] # "pu", "kpu", "pu2", "squ" -> avg?
    # push = float(mf_dict["rmp"])
    # pull = float(mf_dict["rmp2"])
    # leg = float(mf_dict["rml"])
    grip_l = 2 * float(mf_dict["lhd"])
    grip_r = 2 * float(mf_dict["rhd"])
    grip = float(mf_dict["lhd"]) + float(mf_dict["rhd"])
    # endurance = float(mf_dict["pu"])
    # end = [float(mf_dict["pu"]), float(mf_dict["kpu"]), float(mf_dict["pu2"]), float(mf_dict["squ"])]
    # tot_rep = 0
    # tot_count = 0
    # for ele in end:
    # 	if ele>0:
    # 		tot_rep += ele
    # 		tot_count += 1
    # endurance = 0
    # if tot_count>0:
    # 	endurance = round(tot_rep/tot_count, 0)
    # endurance = max(end)

    endurance = float(mf_dict["pu"])
    if (mf == "female"):
        endurance = float(mf_dict["kpu"])

    # # printgrip_l, "^^$$"

    mf = "female"
    age = 0

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    user = res[0]

    comm = "select gender, age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    if len(res) > 0:
        mf = res[0][0]
        age = int(res[0][1])

    # mf_table = load_mf()
    #  	return str(mf_table)

    # # printpull, push, leg, "$$"
    score = check_table_mf(mf, age, pull, push, leg, grip_l, grip_r, grip, endurance, mf_table)
    tt = 0
    cc = 0
    if push > 0:
        tt += score[1]
        cc += 1
    if leg > 0:
        tt += score[2]
        cc += 1
    if cc > 0:
        tt = tt / cc
    score.append(tt)

    score2 = []
    # 	return "abcddd"
    for ele in score:
        score2.append(ele * 1.0 / 10)


# # printpull, push, leg, grip_l, grip_r, endurance
# # printscore2
# render_template_to_pdf('result_mf.html', download=True, save=False, param='hello', states=states, single=single, userType=ut, username=current_user, name=uname, dict=mf_dict, score=score2)


    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    sick_user = cursor.fetchone()[0]
    return render_template('result_mf.html', states=states, single=single, patient=sick_user, userType=ut,
                       username=current_user, name=uname, dict=mf_dict, score=score2)


@app.route("/result_rom")
def ResROMHandler():
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()

    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    comm = "select * from RangeOfMotion where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    rom_list = ["uname", "fle", "ext", "slrr", "slrl", "th", "hin", "fler", "flel", "extr", "extl", "abdr", "abdl",
                "lrr", "lrl", "lrr_c", "lrl_c", "fle_c", "ext_c", "fler_a", "flel_a", "extr_a", "extl_a", "fler_w",
                "flel_w", "extr_w", "extl_w", "fler_e", "flel_e", "extr_e", "extl_e", "pror_e", "prol_e", "supr_e",
                "supl_e", "fler_k", "flel_k", "extr_k", "extl_k", "fler_h", "flel_h", "hypr_h", "hypl_h", "abdr_h",
                "abdl_h"]
    rom_dict = dict()
    for i in range(len(rom_list)):
        # if data[i]=="0":
        # rom_dict[rom_list[i]] = "N"
        # else:
        rom_dict[rom_list[i]] = data[i]

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    user = res[0]
    comm = "select age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    if len(res) > 0:
        age = int(res[0][0])

    # table = load_rom()
    s11 = float(rom_dict["flel_h"])
    s12 = float(rom_dict["hypl_h"])
    s13 = float(rom_dict["abdl_h"])
    s11r = float(rom_dict["fler_h"])
    s12r = float(rom_dict["hypr_h"])
    s13r = float(rom_dict["abdr_h"])

    s21 = float(rom_dict["flel_k"])
    s22 = float(rom_dict["extl_k"])
    s21r = float(rom_dict["fler_k"])
    s22r = float(rom_dict["extr_k"])

    s31 = float(rom_dict["flel_a"])
    s32 = float(rom_dict["extl_a"])
    s31r = float(rom_dict["fler_a"])
    s32r = float(rom_dict["extr_a"])

    s41 = float(rom_dict["flel"])
    s42 = float(rom_dict["extl"])
    s43 = float(rom_dict["abdl"])
    s44 = float(rom_dict["lrl"])
    s41r = float(rom_dict["fler"])
    s42r = float(rom_dict["extr"])
    s43r = float(rom_dict["abdr"])
    s44r = float(rom_dict["lrr"])

    s51 = float(rom_dict["flel_e"])
    s52 = float(rom_dict["extl_e"])
    s53 = float(rom_dict["prol_e"])
    s54 = float(rom_dict["supl_e"])
    s51r = float(rom_dict["fler_e"])
    s52r = float(rom_dict["extr_e"])
    s53r = float(rom_dict["pror_e"])
    s54r = float(rom_dict["supr_e"])

    s61 = float(rom_dict["flel_w"])
    s62 = float(rom_dict["extl_w"])
    s61r = float(rom_dict["fler_w"])
    s62r = float(rom_dict["extr_w"])

    s71 = float(rom_dict["fle"])
    s72 = float(rom_dict["ext"])

    s81 = float(rom_dict["fle_c"])
    s82 = float(rom_dict["ext_c"])
    s83 = float(rom_dict["lrl_c"])
    s83r = float(rom_dict["lrr_c"])

    ## get age first!
    arr = [[s11, s12, s13, s11r, s12r, s13r], [s21, s22, s21r, s22r], [s31, s32, s31r, s32r],
           [s41, s42, s43, s44, s41r, s42r, s43r, s44r], [s51, s52, s53, s54, s51r, s52r, s53r, s54r],
           [s61, s62, s61r, s62r], [s71, s72], [s81, s82, s83, s83r]]
    # rom_table = load_rom()
    score = check_table_rom(int(age), arr, rom_table)


# # printarr
# # printscore
# score2 = []
# for ele in score:
# 	score2.append(ele) ## done /10

    comm = "select user from History where test_id='%s';"%uname
    cursor.execute(comm)
    sick_user = cursor.fetchone()[0]
    return render_template('result_rom.html', states=states, single=single, patient=sick_user, userType=ut, name=uname,
                       username=current_user, dict=rom_dict, score_dict=score)


@app.route("/result")
def ResultHandler():
    uname = request.cookies.get('uname')
    db, cursor = connDB()

    bmi = bf = wthr = gender = None
    comm = "select bmi,bf,wthr,gender from BodyComposition where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        bmi, bf, wthr, gender = res[0]

    laas = lpas = lpas2 = cs2 = None
    raas = rpas = rpas2 = cs3 = None
    comm = "select laas,lpas,lpas2,cs2,raas,rpas,rpas2,cs3 from Balance where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        laas, lpas, lpas2, cs2, raas, rpas, rpas2, cs3 = res[0]

    data = None
    comm = "select * from CardiopulmonaryFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        data = res[0]

    bpwr = pwr = lpwr = cd = None
    comm = "select bpwr, pwr, lpwr, cd from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        bpwr, pwr, lpwr, cd = res[0]

    data2 = None
    comm = "select * from RangeOfMotion where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    if len(res) > 0:
        data2 = res[0]

    return render_template('result.html', name="justin", bmi=bmi, bf=bf, wthr=wthr, gender=gender, laas=laas, lpas=lpas,
                           lpas2=lpas2, cs2=cs2, raas=raas, rpas=rpas, rpas2=rpas2, cs3=cs3, bpwr=bpwr, pwr=pwr,
                           lpwr=lpwr, cd=cd)


@app.route("/print2")
def Print2Handler():
    # current_user = "doc"
    current_user = request.cookies.get('uname')
    if current_user == "":
        return redirect("./logout")

    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    uid = res[0]

    comm = "select gender from User where id='%s';" % uid
    cursor.execute(comm)
    res = cursor.fetchone()
    mf = res[0]

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    comm = "select * from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    mf_list = ["uname", "rmp", "bpwr", "rmp2", "pwr", "rml", "lpwr", "rhd", "lhd", "cd", "pu", "kpu", "pu2", "squ"]
    mf_dict = dict()
    for i in range(len(mf_list)):
        mf_dict[mf_list[i]] = data[i]

    push = float(mf_dict["bpwr"])
    pull = float(mf_dict["pwr"])
    leg = float(mf_dict["lpwr"])
    grip_l = 2 * float(mf_dict["lhd"])
    grip_r = 2 * float(mf_dict["rhd"])
    grip = float(mf_dict["lhd"]) + float(mf_dict["rhd"])

    endurance = float(mf_dict["pu"])
    if (mf == "female"):
        endurance = float(mf_dict["kpu"])

    # # printgrip_l, "^^$$"

    mf = "female"
    age = 0

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    user = res[0]

    comm = "select gender, age from User where id='%s';" % user
    cursor.execute(comm)
    res = cursor.fetchall()
    age = 0
    if len(res) > 0:
        mf = res[0][0]
        age = int(res[0][1])

    # mf_table = load_mf()
    #  	return str(mf_table)

    # # printpull, push, leg, "$$"
    score = check_table_mf(mf, age, pull, push, leg, grip_l, grip_r, grip, endurance, mf_table)
    tt = 0
    cc = 0
    if push > 0:
        tt += score[1]
        cc += 1
    if leg > 0:
        tt += score[2]
        cc += 1
    if cc > 0:
        tt = tt / cc
    score.append(tt)

    score2 = []
    # 	return "abcddd"
    for ele in score:
        score2.append(ele * 1.0 / 10)
    # # printpull, push, leg, grip_l, grip_r, endurance
    # # printscore2
    # render_template_to_pdf('result_mf.html', download=True, save=False, param='hello', states=states, single=single, userType=ut, username=current_user, name=uname, dict=mf_dict, score=score2)

    html = render_template('result_mf.html', states=states, single=single, userType=ut, username=current_user,
                           name=uname, dict=mf_dict, score=score2)
    css = ["./static/style/result_mf.css"]
    pdfkit.from_string(html, 'out_mf.pdf')
    # return render_template('result_mf.html', states=states, single=single, userType=ut, username=current_user, name=uname, dict=mf_dict, score=score2)
    return "done"


@app.route("/print")
def PrintHandler():
    # pdfkit.from_url('http://127.0.0.1:5000/result_mf?name=3', 'out.pdf')
    # pdfkit.from_url("https://micropyramid.com/blog/how-to-create-pdf-files-in-python-using-pdfkit/", "out.pdf")
    # pdfkit.from_url("http://127.0.0.1:5000/patient_list", "out.pdf")

    # pdfkit.from_file('templates/result_mf.html', 'out.pdf')
    patients = []
    current_user = request.cookies.get('uname')
    db, cursor = connDB()
    comm = "select id,rname,email,dob,gender from User where userType='patient';"
    cursor.execute(comm)
    res = cursor.fetchall()
    for data in res:
        patient = dict()
        patient["id"] = data[0]
        patient["rname"] = data[1]
        patient["email"] = data[2]
        patient["dob"] = data[3]
        patient["mf"] = data[4]
        patient['test_list'] = []
        try:

            comm = "select test_id, date from History where user='%s';" % data[0]
            cursor.execute(comm)
            res3 = cursor.fetchall()
            count = 1
            for ele in res3:
                # # printele
                patient['test_list'].append([count, ele[0], ele[1]])
                count += 1

        except:
            pass
        patients.append(patient)

    html = render_template("patient_list.html", patients=patients, username=current_user)
    css = ["./static/style/result_mf.css"]
    pdfkit.from_string(html, 'out.pdf', css=css)
    return "done"


@app.route("/print_w")
def PrintWHandler():
    current_user = "doc"
    db, cursor = connDB()
    comm = "select userType from User where id='%s';" % current_user
    cursor.execute(comm)
    res = cursor.fetchone()
    ut = res[0]

    uname = request.args.get("name")
    single = request.args.get("single")
    if not single == 't':
        single = 'f'

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchone()
    uid = res[0]

    comm = "select gender from User where id='%s';" % uid
    cursor.execute(comm)
    res = cursor.fetchone()
    mf = res[0]

    tabs = ["BodyComposition", "Balance", "CardiopulmonaryFitness", "MuscularFitness", "RangeOfMotion"]
    states = []  ## 5 form statues + 1 basic statues
    for fname in tabs:
        comm = "select * from %s where id='%s';" % (fname, uname)
        cursor.execute(comm)
        res = cursor.fetchall()
        if len(res) > 0:
            states.append('t')
        else:
            states.append('f')

    ## bc
    bc_list = ["uname", "height", "weight", "bmi", "bp", "rhr", "neck", "chest", "waist", "abdomen", "armr", "arml",
               "forearmr", "forearml", "buttocks", "midthighr", "midthighl", "calfr", "calfl", "foot", "knee", "asis",
               "shoulder", "abdomen2", "triceps", "chest2", "midaxillary", "subscapular", "suprailiac", "thigh", "sum7",
               "sum31", "sum32", "bd1", "bd2", "bd3", "bf1", "bf2", "bf3", "bf", "fm", "lbm", "circumference", "wthr",
               "bmr", "act_level", "tdee", "hrm"]
    bc_dict = dict()
    comm = "select * from BodyComposition where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    # # printcomm
    data = None
    if len(res) > 0:
        data = res[0]

    cir_list = ["neck", "arml", "armr", "forearml", "forearmr", "chest", "waist", "abdomen", "buttocks", "midthighl",
                "midthighr", "calfl", "calfr"]
    for i in range(len(bc_list)):
        if bc_list[i] in cir_list:
            bc_dict[bc_list[i]] = str(round(float(data[i]) / 2.54, 2))
        # # print"change"
        else:
            bc_dict[bc_list[i]] = data[i]

    comm = "select user from History where test_id='%s';" % uname
    cursor.execute(comm)
    user = cursor.fetchone()[0]
    comm = "select dob,age,gender from User where id='%s';" % user
    cursor.execute(comm)
    data_pre = cursor.fetchone()
    basic_list = ["dob", "age", "gender"]
    for i in range(len(basic_list)):
        bc_dict[basic_list[i]] = data_pre[i]

    bf = float(bc_dict["bf"])
    wthr = float(bc_dict["wthr"])
    abf = bf
    bmi = float(bc_dict["bmi"])
    age = int(bc_dict["age"])
    mf = bc_dict["gender"]
    # bc_table = load_bc()
    score_bc = check_table_bc(mf, age, bf, wthr, abf, bmi, bc_table)
    # # printbc_table, age
    # # print[bf, wthr, abf, bmi]

    # # printscore
    score_bc2 = []
    for ele in score_bc:
        score_bc2.append(ele * 1.0 / 10)

    score_m_bc = round(0.5 * score_bc2[0] + 0.25 * score_bc2[1] + 0.2 * score_bc2[2] + 0.05 * score_bc2[3], 2)

    # balance
    comm = "select * from Balance where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    balance_list = ["uname", "ft", "dls", "dlsp", "lf", "lsls", "lts", "lslsp", "ltsp", "rf", "rsls", "rts", "rslsp",
                    "rtsp", "tf", "lbb", "lk2t", "lh", "lrb", "lfs", "cs", "rbb", "rk2t", "rh", "rrb", "rfs", "cs2",
                    "lat1", "lat2", "lat3", "laas", "larrd", "lacrd", "lpt1", "lpt2", "lpt3", "lpas", "lprrd", "lpcrd",
                    "lpt21", "lpt22", "lpt23", "lpas2", "lprrd2", "lpcrd2", "cs3", "rat1", "rat2", "rat3", "raas",
                    "rarrd", "racrd", "rpt1", "rpt2", "rpt3", "rpas", "rprrd", "rpcrd", "rpt21", "rpt22", "rpt23",
                    "rpas2", "rprrd2", "rpcrd2", "cs4", "lkup", "rkup"]
    valid_list = []
    balance_dict = dict()
    for i in range(len(balance_list)):
        balance_dict[balance_list[i]] = data[i]
    bess_lf = int(balance_dict['lf'])
    bess_rf = int(balance_dict['rf'])
    an_l = float(balance_dict['cs'])
    an_r = float(balance_dict['cs2'])
    y_l = float(balance_dict['cs3'])
    y_r = float(balance_dict['cs4'])

    # balance_table = load_balance()
    score_balance = check_table_balance(mf, age, bess_lf, bess_rf, an_l, an_r, y_l, y_r, balance_table)
    score_balance[2] = float(balance_dict['cs'])
    score_balance[3] = float(balance_dict['cs2'])
    score_balance[4] = float(balance_dict['cs3'])
    score_balance[5] = float(balance_dict['cs4'])

    score_balance2 = []
    for ele in score_balance:
        if ele > 0:
            score_balance2.append(round(ele * 1.0 / 10, 2))
        else:
            score_balance2.append(0.0)

    tot = 0
    count = 0
    score_m_balance = 0.0
    s_11 = (score_balance2[0] + score_balance2[1]) / 2
    s_22 = (an_l + an_r) / 20
    s_33 = (y_l + y_r) / 20

    if s_11 > 0:
        tot += s_11
        count += 1
    if s_22 > 0:
        tot += s_22
        count += 1
    if s_33 > 0:
        tot += s_33
        count += 1

    if count > 0:
        score_m_balance = round(tot / count, 2)

    ## cf
    comm = "select * from CardiopulmonaryFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    cf_list = ["uname", "ymca", "aphrm", "ghrm", "thr", "hrm", "sp60", "sp120", "aphrm50", "aphrm60", "aphrm70",
               "aphrm80", "aphrm90", "sp60_pre", "sp120_pre", "hrm_w"]
    cf_dict = dict()
    for i in range(len(cf_list)):
        cf_dict[cf_list[i]] = data[i]

    vo2max = float(cf_dict["ymca"])
    # # printcf_dict["sp60_pre"], "$$$"
    hrr = int(cf_dict["sp60_pre"]) - int(cf_dict["sp60"])

    # car_table = load_car()
    score_car = check_table_car(mf, age, vo2max, hrr, car_table)
    # # printcar_table, hrr, vo2max
    score_car2 = []
    for ele in score_car:
        score_car2.append(ele * 1.0 / 10)
    # # printscore2

    score_m_cf = round(0.5 * score_car2[0] + 0.5 * score_car2[1], 2)

    ## mf
    comm = "select * from MuscularFitness where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    mf_list = ["uname", "rmp", "bpwr", "rmp2", "pwr", "rml", "lpwr", "rhd", "lhd", "cd", "pu", "kpu", "pu2", "squ"]
    mf_dict = dict()
    for i in range(len(mf_list)):
        mf_dict[mf_list[i]] = data[i]

    push = float(mf_dict["bpwr"])
    pull = float(mf_dict["pwr"])
    leg = float(mf_dict["lpwr"])
    grip_l = 2 * float(mf_dict["lhd"])
    grip_r = 2 * float(mf_dict["rhd"])
    grip = float(mf_dict["lhd"]) + float(mf_dict["rhd"])

    endurance = float(mf_dict["pu"])
    if (mf == "female"):
        endurance = float(mf_dict["kpu"])

    score_mf = check_table_mf(mf, age, pull, push, leg, grip_l, grip_r, grip, endurance, mf_table)
    tt = 0
    cc = 0
    if push > 0:
        tt += score_mf[1]
        cc += 1
    if leg > 0:
        tt += score_mf[2]
        cc += 1
    if cc > 0:
        tt = tt / cc
    score_mf.append(tt)

    score_mf2 = []
    for ele in score_mf:
        score_mf2.append(ele * 1.0 / 10)

    tot = 0
    count = 0
    s_11 = (score_mf2[7])
    s_22 = (score_mf2[5])
    s_33 = (score_mf2[6])
    if s_11 > 0:
        tot += s_11
        count += 1
    if s_22 > 0:
        tot += s_22
        count += 1
    if s_33 > 0:
        tot += s_33
        count += 1

    score_m_mf = 0.0
    if count > 0:
        score_m_mf = round(tot / count, 2)

    ## rom
    comm = "select * from RangeOfMotion where id='%s';" % uname
    cursor.execute(comm)
    res = cursor.fetchall()
    data = None
    if len(res) > 0:
        data = res[0]

    rom_list = ["uname", "fle", "ext", "slrr", "slrl", "th", "hin", "fler", "flel", "extr", "extl", "abdr", "abdl",
                "lrr", "lrl", "lrr_c", "lrl_c", "fle_c", "ext_c", "fler_a", "flel_a", "extr_a", "extl_a", "fler_w",
                "flel_w", "extr_w", "extl_w", "fler_e", "flel_e", "extr_e", "extl_e", "pror_e", "prol_e", "supr_e",
                "supl_e", "fler_k", "flel_k", "extr_k", "extl_k", "fler_h", "flel_h", "hypr_h", "hypl_h", "abdr_h",
                "abdl_h"]
    rom_dict = dict()
    for i in range(len(rom_list)):
        # if data[i]=="0":
        # rom_dict[rom_list[i]] = "N"
        # else:
        rom_dict[rom_list[i]] = data[i]

    # table = load_rom()
    s11 = float(rom_dict["flel_h"])
    s12 = float(rom_dict["hypl_h"])
    s13 = float(rom_dict["abdl_h"])
    s11r = float(rom_dict["fler_h"])
    s12r = float(rom_dict["hypr_h"])
    s13r = float(rom_dict["abdr_h"])

    s21 = float(rom_dict["flel_k"])
    s22 = float(rom_dict["extl_k"])
    s21r = float(rom_dict["fler_k"])
    s22r = float(rom_dict["extr_k"])

    s31 = float(rom_dict["flel_a"])
    s32 = float(rom_dict["extl_a"])
    s31r = float(rom_dict["fler_a"])
    s32r = float(rom_dict["extr_a"])

    s41 = float(rom_dict["flel"])
    s42 = float(rom_dict["extl"])
    s43 = float(rom_dict["abdl"])
    s44 = float(rom_dict["lrl"])
    s41r = float(rom_dict["fler"])
    s42r = float(rom_dict["extr"])
    s43r = float(rom_dict["abdr"])
    s44r = float(rom_dict["lrr"])

    s51 = float(rom_dict["flel_e"])
    s52 = float(rom_dict["extl_e"])
    s53 = float(rom_dict["prol_e"])
    s54 = float(rom_dict["supl_e"])
    s51r = float(rom_dict["fler_e"])
    s52r = float(rom_dict["extr_e"])
    s53r = float(rom_dict["pror_e"])
    s54r = float(rom_dict["supr_e"])

    s61 = float(rom_dict["flel_w"])
    s62 = float(rom_dict["extl_w"])
    s61r = float(rom_dict["fler_w"])
    s62r = float(rom_dict["extr_w"])

    s71 = float(rom_dict["fle"])
    s72 = float(rom_dict["ext"])

    s81 = float(rom_dict["fle_c"])
    s82 = float(rom_dict["ext_c"])
    s83 = float(rom_dict["lrl_c"])
    s83r = float(rom_dict["lrr_c"])

    ## get age first!
    arr = [[s11, s12, s13, s11r, s12r, s13r], [s21, s22, s21r, s22r], [s31, s32, s31r, s32r],
           [s41, s42, s43, s44, s41r, s42r, s43r, s44r], [s51, s52, s53, s54, s51r, s52r, s53r, s54r],
           [s61, s62, s61r, s62r], [s71, s72], [s81, s82, s83, s83r]]
    # rom_table = load_rom()
    score_rom = check_table_rom(int(age), arr, rom_table)

    score_t = []
    score_m_rom = 0

    score_11 = sum(
        [score_rom["1a"], score_rom["1b"], score_rom["1c"], score_rom["1ar"], score_rom["1br"], score_rom["1cr"]]) / 6
    score_22 = sum([score_rom['2a'], score_rom['2b'], score_rom['2ar'], score_rom['2br']]) / 4
    score_33 = sum([score_rom['3a'], score_rom['3b'], score_rom['3ar'], score_rom['3br']]) / 4
    score_44 = sum(
        [score_rom['4a'], score_rom['4b'], score_rom['4c'], score_rom['4d'], score_rom['4ar'], score_rom['4br'],
         score_rom['4cr'], score_rom['4dr']]) / 8
    score_55 = sum(
        [score_rom['5a'], score_rom['5b'], score_rom['5c'], score_rom['5d'], score_rom['5ar'], score_rom['5br'],
         score_rom['5cr'], score_rom['5dr']]) / 8
    score_66 = sum([score_rom['6a'], score_rom['6b'], score_rom['6ar'], score_rom['6br']]) / 4
    score_77 = sum([score_rom['7a'], score_rom['7b']]) / 2
    score_88 = sum([score_rom['8a'], score_rom['8b'], score_rom['8c'], score_rom['8cr']]) / 4

    score_m_rom = round(sum([score_11, score_22, score_33, score_44, score_55, score_66, score_77, score_88]) / 8, 2)

    ## main
    count = 0
    tot = 0
    for single_s in [score_m_bc, score_m_balance, score_m_cf, score_m_mf, score_m_rom]:
        if single_s > 0:
            tot += single_s
            count += 1
    score_sum = 0.0
    if count > 0:
        score_sum = round(tot / count, 2)

    score = [score_m_bc, score_m_balance, score_m_cf, score_m_mf, score_m_rom, score_sum]

    html = render_template('result_print.html', states=states, single=single, userType=ut, patient=user,
                           username=current_user, name=uname, mf_dict=mf_dict, score_mf=score_mf2, rom_dict=rom_dict,
                           score_dict=score_rom, cf_dict=cf_dict, score_car=score_car2, balance_dict=balance_dict,
                           score_balance=score_balance2, bc_dict=bc_dict, score_bc=score_bc2, score=score)
    return html


################# tables ################

###### main #####
if __name__ == "__main__":
    ## SCORE table
    bc_table = load_bc()
    balance_table = load_balance()
    car_table = load_car()
    mf_table = load_mf()
    rom_table = load_rom()
    # 	key = Fernet.generate_key()

    app.run(debug=True, host="0.0.0.0", port=80)
    # app.run(debug=True, host="0.0.0.0", port=5000)
