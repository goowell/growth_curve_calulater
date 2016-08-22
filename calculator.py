# -*- coding: gbk -*-
from .pygrowup import Calculator, exceptions

from datetime import datetime
import csv
from os import listdir, path

def d(data_str):
    return datetime.strptime(data_str, '%Y/%m/%d')

data_folder = 'growup/data/'


def calculate_to_file(data_folder, filename):
    print(filename)
    with open(path.join(data_folder, filename)) as f:
        reader = csv.DictReader(f)
        zscore_in = ['入科Z值']
        zscore_out = ['出科Z值']
        for l in reader:
            gender = 'M' if l['性别'] == '1' else 'F'
            try:
                weight_in = l['入科体重']
                months_in = (d(l['入科日期']) - d(l['出生日期'])).days / 30

                if weight_in not in ['', ' ', None]:
                    zscore_in.append(str(calculator.wfa(weight_in, months_in, gender)))
                else:
                    zscore_in.append('Invalid')
            except ValueError as e:
                # print(e)
                print(l['序号'], l['姓名'])
                zscore_in.append('Invalid')
            except exceptions.DataNotFound as e:
                # print(e)
                print(l['序号'], l['姓名'])
                zscore_in.append('Invalid')
            try:
                weight_out = l['出科体重']
                months_out = (d(l['出科日期']) - d(l['出生日期'])).days / 30
                if weight_out not in ['', ' ', None]:
                    zscore_out.append(str(calculator.wfa(weight_out, months_out, gender)))
                else:
                    zscore_out.append('Invalid')
            except ValueError as e:
                # print(e)
                print(l['序号'], l['姓名'])
                zscore_out.append('Invalid')
            except Exception as e:
                print(l['序号'], l['姓名'])
                print(e)
                zscore_out.append('Invalid')
        with open(path.join(data_folder, 'calculated_' + filename), 'w') as cf:
            cf.write(','.join(zscore_in))
            cf.write('\n')
            cf.write(','.join(zscore_out))


if __name__ == '__main__':
    calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')
    print('hello')
    print(listdir(data_folder))
    for f in listdir(data_folder):
        if not f.startswith('calculated_'):
            calculate_to_file(data_folder, f)
