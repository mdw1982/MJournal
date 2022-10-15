# with open('ldb_config.json', 'r') as j:
#     lc = json.load(j)
#
# conn = sl.connect(lc['database'])
# data = pd.read_sql("select id, title, month, day, year, time from entries", conn)
# sorted_by_year = pd.DataFrame(data, columns=['id', 'title', 'month', 'day', 'year', 'time'])
# sorted_by_year.sort_values(by='year', inplace=True, ascending=False)
# conn.close()
# print(sorted_by_year)