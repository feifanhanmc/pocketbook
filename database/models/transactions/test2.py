def date_format(date, target_format='yyyymmdd'):
    def date_fill(date_part):
        if len(date_part) == 1:
            date_part = '0%s' % date_part
        return date_part[:2]

    for seg in ['-', '/']:
        if seg in date:
            y, m, d = date.split(' ')[0].split(seg)[:3]
            m = date_fill(m)
            d = date_fill(d)
            date = '%s%s%s' % (y, m, d)
            break
    return date[:8]


print(date_format('20200211'))
# print(date_format('2020-02-11'))
# print(date_format('2020-2-11'))
# print(date_format('2020/02/11'))
# print(date_format('2020/2/3'))
print(date_format('2020/2/3 12:3:2'))
