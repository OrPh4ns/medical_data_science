from django.shortcuts import render, redirect
from Core import MongoDatabase as mdb
import Core.Controller
import datetime
from django.contrib.auth import login, authenticate, logout


class HomeController(Core.Controller.Controller):

    def index(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve documents from the collection
            docs = mdb.collection.find()
            # Create an empty list to store values
            values = []
            # Iterate through each retrieved document
            for doc in docs:
                # Split the filename by "/"
                parts = doc['file']['filename'].split("/")
                # Get the last part of the filename
                last_part = parts[-1]
                # Split the last part by "_"
                code_parts = last_part.split("_")
                # Extract the code as an integer
                code = int(code_parts[0])
                # Convert the code to a date object
                date = datetime.datetime.fromtimestamp(code)
                # Get the year and month from the date object
                year = date.strftime("%Y")
                month = date.strftime("%m")
                # Check whether the values list is empty
                if len(values) != 0:
                    # Iterate through each value in the list
                    for val in values:
                        # Check if the year and month match
                        if val[0] == year and val[1] == month:
                            # Increment the count
                            val[2] = val[2]+1
                            # If they don't match add a new entry to the values list
                        else:
                            values.append([year, month, 1])
                else:
                    # If it's empty add a new entry to the values list
                    values.append([year, month, 1])
            # Count the total number of documents in the collection
            documents_count = mdb.collection.count_documents({})

            # Render the home.html template with the documents count and values
            return render(request, 'home.html', {"documents_count": documents_count, "values":values})
        else:
            # Redirect the user to the login page if not authenticated
            return redirect('/login')