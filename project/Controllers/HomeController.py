from django.shortcuts import render, redirect
from Core import MongoDatabase as mdb
import Core.Controller
import datetime
from django.contrib.auth import login, authenticate, logout


class HomeController(Core.Controller.Controller):

    def index(self, request):
        if request.user.is_authenticated:
            docs = mdb.collection.find()
            values = []
            for doc in docs:
                parts = doc['file']['filename'].split("/")
                last_part = parts[-1]
                code_parts = last_part.split("_")
                code = int(code_parts[0])
                date = datetime.datetime.fromtimestamp(code)
                year = date.strftime("%Y")
                month = date.strftime("%m")
                if len(values) != 0:
                    for val in values:
                        if val[0] == year and val[1] == month:
                            val[2] = val[2]+1
                        else:
                            values.append([year, month, 1])
                else:
                    values.append([year, month, 1])
                print(values)
            print("end")
            print(values)
            documents_count = mdb.collection.count_documents({})

            return render(request, 'home.html', {"documents_count": documents_count, "values":values})
        else:
            return redirect('/login')