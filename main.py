# Arthor: B.X. Weinstein Xiao
# Contact: rchopin@outlook.com, bangxi_xiao@brown.edu

from sse import *
from szse import *
from text_tools import *
import pandas as pd
import time
import os


if __name__ == '__main__':
    # Handling data from SSE
    sse_t_pages = 141  # total pages of target websites
    sse = SSE()  # Initialize SSE scrapper
    sse_data_gathered = []
    for i in range(1, sse_t_pages + 1):
        print('Executing page {}.'.format(i))
        page_result = sse.get_page(p=i, shuffle_id=False)
        page_result = sse.extract_info(page_result)
        sse_data_gathered += sse.extract_info(page_result)
    # Executing pdf files
    pdf_data_gathered = []
    for u in [x[-2] for x in sse_data_gathered]:
        print('Executing url {}'.format(u))
        try:
            pdf_data_gathered.append(sse.get_pdf_content('http://' + u))  # In case of losing connection
        except:
            time.sleep(5)
            pdf_data_gathered.append(sse.get_pdf_content('http://' + u))
    df_sse = pd.DataFrame(sse_data_gathered, columns=sse.rc)
    df_sse['pdf_content'] = pdf_data_gathered
    df_sse['compname'] = df_sse['docTitle'].apply(process_text).apply(process_compname)
    df_sse.to_csv('sse_data.csv', encoding='utf_8_sig', index=False)  # save to local

    # Handling data from SZSE
    page_dict = {'主板': 100, '中小企业板': 130, '创业板': 124}  # Number of Pages of each block
    szse = SZSE()  # Initialize SZSE scrapper
    data_gathered = []
    for j in ['主板', '中小企业板', '创业板']:
        l = page_dict[j]
        for i in range(1, 1 + l):
            print('Executing page {} in block {}.'.format(i, j))
            data_gathered += szse.get_page(i, j)
    ck_fp = 'C:\\Users\\acegodness\\Desktop\\FMC Research Intern\\download\\szse\\ck'
    for i, j in [(k.get('ck'), k.get('unique_id')) for k in data_gathered]:
        try:
            szse.download_all(i, j, ck_fp)
        except:
            time.sleep(np.random.randint(1, 5))
            szse.download_all(i, j, ck_fp)
    ck_content = []
    fn = os.listdir('.\\download\\szse\\{}'.format('ck'))
    for fmt, func in zip(['pdf', 'ocx', 'doc'],
                         [szse.get_local_pdf_content, szse.get_local_docx_content, szse.get_local_doc_content]):
        fn_subset = list(filter(lambda x: fmt == x[-3:], fn))
        ck_content += [func(x, ck_fp) for x in fn_subset]
    szse_data = pd.DataFrame(data_gathered, columns=szse.rc)
    szse_inq_data = pd.DataFrame(ck_content, columns=['ck_content', 'unique_id'])
    szse_data = pd.merge(szse_data, szse_inq_data, on='unique_id', how='inner')
    # process company names
    szse_data['compname'] = szse_inq_data['ck_content'].apply(process_text).apply(process_compname)
    szse_data.to_csv('szse_data.csv', index=False, encoding='utf_8_sig')
