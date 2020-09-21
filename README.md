# Flask_StudentEnrolment
Full stack Student Enrolment web application

This is a University enrollment application. This web application developed using Flask.
Here user can register in the application using email address, name and password. Passwords
are stored in a hashed format inside database. This is a secured way to use password so that
even admin can't retrieve the password of the user. Once user try to login flask uses its
algorithm to compare the hashed password. And it is dynamic in nature. In the backend i have used
Mongo DB database and flask mongo db engine. This is an efficient no sql database where we can store and
retrieve data in json format. I have exposed api of the application. So using api call user can create, update
and delete data.
