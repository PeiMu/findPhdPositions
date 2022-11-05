def get_link(conf, year):
    url = ''
    is_specific = False
    if conf.find('code generation and optimization') != -1:
        if year == '2021':
            url = 'https://conf.researchr.org/track/cgo-2021/cgo-2021-papers?#event-overview'
            is_specific = True
        elif year == '2022':
            url = 'https://conf.researchr.org/track/cgo-2022/cgo-2022-main-conference#event-overview'
            is_specific = True
    elif conf.find('compiler construction') != -1:
        if year == '2021':
            url = 'https://conf.researchr.org/track/CC-2021/cc-research-papers?#event-overview'
            is_specific = True
        elif year == '2022':
            url = 'https://conf.researchr.org/track/CC-2022/CC-2022-research-papers#event-overview'
            is_specific = True
    else:
        conf_name = conf.split(' ')
        url_pre = 'https://scholar.google.com/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors' \
                  '=&as_publication='
        url_year = '&as_ylo=' + year + '&as_yhi=' + year + '&hl=en&as_sdt=0%2C5'
        url_name = ''
        for c_name in conf_name:
            if c_name != '':
                url_name += '+' + c_name
        url = url_pre + url_name[1:] + url_year
    return [url, is_specific]
