import json

data1 = '{"course":{"logic":"and", "filters": ["CPE101", "CPE102"]}}'
data2 = '{"course":{"logic":"and", "filters": ["CPE101", "CPE102"]}, "faculty":{"logic":"or", "filters": ["tkearns@calpoly.edu"]}}'
data3 = '{"course":{"logic":"and", "filters": ["CPE101", "CPE102"]}, "faculty":{"logic":"or", "filters": ["tkearns@calpoly.edu"]}, "time":{"logic": "and", "filters":{"MWF":[["10:00AM", "12:00PM"], ["2:00PM", "3:00PM"]], "TR":[["11:00AM", "1:00PM"], ["5:00PM", "6:00PM"]]}}}'
data4 = '{}'


# # DATA1 EXAMPLE 
# filter_dict = json.loads(data1)
# array = filter_dict['course']
# # print logic
# print array['logic']
# # print filters
# for f in array['filters']:
#     print f

# # DATA2 EXAMPLE 
# filter_dict = json.loads(data2)
# for key,filters in filter_dict.iteritems():
#     for k,v in filters.iteritems():
#         # print logic
#         if k == 'logic':
#             print 'logic: ' + v
#         # print filters
#         elif k == 'filters':
#             for f in v:
#                 print 'filter: ' + f

# if no filters are chosen - return none
# if any filters are chosen - return only those filters
# if all filters are chosen - return all filters

# DATA3 EXAMPLE --- FINAL ---


filter_dict = json.loads(data3)
prevLogic = ''
for key,tags in filter_dict.iteritems():
    if prevLogic is not '':
        print prevLogic
    # if 'or' in prevLogic or prevLogic is '':
    #     print 'new section = Section.objects'
    # elif 'and' in prevLogic:
    #     print prevLogic
    filters = tags['filters']
    if key == "time":
        for k,v in filters.iteritems():
            if k == "MWF" or k == "TR":
                print "   filter(days=" + k + ")"
                for times in range(len(v)):
                    print '      filter(start_time >=' + v[times][0] + ', end_time <=' +  v[times][1] + ')'
    else:
        print "   filter(" + key + "=" + ', '.join(filters) + ")"
    prevLogic = tags['logic'] + " "