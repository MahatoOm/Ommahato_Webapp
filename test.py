


afterdate = "2025-01-25"
startdate = "2025-01-20"
distance_day = int(afterdate[-2:]) - int(startdate[-2:])
distance_month = 
print(int(afterdate[-2:]))
print(startdate[-2:])
print(distance)



# import database
# from datetime import datetime, timedelta, date 
# def habitTracker(username, email):
    
#     print(username, email)
#     global list_item
#     list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]
    
#     todays_date = date.today()
#     totalweek = []
#     # print("in tracker",username, email)
#     last_date = todays_date + timedelta(3)
#     if email != "":
#         for i in range(7, -1, -1):

#             day = str(last_date - timedelta(i))

#             docs = database.find_by_date(email, day)

#             day_data = {}

#             for d in docs:
#                 day_data[d["habit"]] = {
#                     "status": d["data"].get("status", ""),
#                     "note": d["data"].get("note", "")
#                 }

#             totalweek.append({
#                 "date": day,
#                 "habits": day_data
#             })
#     # print(username, email)
#     # print(totalweek)
#     print(totalweek)

# # habitTracker("ompro", "omprakashmahato0010@gmail.com")


# def retrieve_data(email , start, end , days, movement = 1):
#     # global email, username
#     print(email,  "username email")

#     # start = request.args.get("start")
#     # end = request.args.get("end")
#     # days = int(request.args.get("day"))
#     # start_date = datetime.fromisoformat(start.replace("Z", ""))
#     # end_date = datetime.fromisoformat(end.replace("Z", ""))
    
#     if movement == -1:
#         end_date = start + timedelta(days-4 -7)
#     else:
#         end_date = start + timedelta(days - 4)  
#     print(email,  "username email")
#     print(start, end_date , days , "this is retrive function")

#     totalweek = []
#     for i in range(days, -1, -1):
#         day_str = str((end_date - timedelta(days=i)).strftime("%Y-%m-%d"))

#         docs = database.find_by_date(email, day_str)
#         # print(docs)
#         # print(list(docs))
#         day_data = {}
#         for d in docs:
#             day_data[d["habit"]] = {
#                 "status": d["data"].get("status", ""),
#                 "note": d["data"].get("note", "")
#             }

#         totalweek.append({
#             "date": day_str,
#             "habits": day_data
#         })

#     print(totalweek)
    

# start = date.today()
# end = start 
# # retrieve_data("omprakashmahato0010@gmail.com", start, end , 14, -1)

# '''
# condition 2: 
# movement add next week
# days = +7


#  '''


# '''
# Adding next week and previous week data to the page as when user his next week or previous week 
# '''

# def week_data(email , start, end , days, movement = 1):
#     # global email, username
#     print(email,  "username email")

#     # start = request.args.get("start")
#     # end = request.args.get("end")
#     # days = int(request.args.get("day"))
#     # start_date = datetime.fromisoformat(start.replace("Z", ""))
#     # end_date = datetime.fromisoformat(end.replace("Z", ""))
    
#     if movement == -1:
#         end_date = end + timedelta(-7)
#     else:
#         end_date = end + timedelta(7)  
#     print(email,  "username email")
#     print(start, end_date , days , "this is retrive function")

#     totalweek = []
#     for i in range(days, -1, -1):
#         day_str = str((end_date - timedelta(days=i)).strftime("%Y-%m-%d"))

#         docs = database.find_by_date(email, day_str)
#         # print(docs)
#         # print(list(docs))
#         day_data = {}
#         for d in docs:
#             day_data[d["habit"]] = {
#                 "status": d["data"].get("status", ""),
#                 "note": d["data"].get("note", "")
#             }

#         totalweek.append({
#             "date": day_str,
#             "habits": day_data
#         })

#     print(totalweek)

# start = date.today()
# end = start + timedelta(3) 
# week_data("omprakashmahato0010@gmial.com" ,start , end , 7 , -1 )