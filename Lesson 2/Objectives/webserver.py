from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys

sys.path.insert(0,'/home/akash/github/ud088-Full-Stack-Foundations/Lesson 1')

# import CRUD operations from Lesson 1
from database_setup import Base,Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>First Page.</h1>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><a href = '/restaurants/new'>Make a New Restaurant Here</a><br/><br/>List all the restaurants names in the database"
                # Query all the restaurants and return the results in any order
                result = session.query(Restaurant).all()
                print result
                # print the result with the restaurant name only
                for item in result:
                    # print item[0]
                    output += item.name
                    output += "<br/><a href = '#'>Edit</a><br/>"
                    output += "<a href = '#'>Delete</a></br/>"
                    output += "<br/><br/><br/>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html>"
                output += "<body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype = 'multipart/form-data' action='/restaurants/new'><input name="restaurant-name" type="text" placeholder = "New Restaurant Name" ><input type="submit" value="Create"> </form>'''
                output += "</body>"
                output += "</html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                # self.end_headers()
                ctype,pdict = cgi.parse_header(
                    self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('restaurant-name')

                    # create a new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_header('Location','/restaurants')
                    self.end_headers()
                # output = ""
                # output += "<html><body>"
                # output += " <h2> Okay, how about this: </h2>"
                # output += "<h1> %s </h1>" % messagecontent[0]
                # output += '''<form method='POST' enctype = 'multipart/form-data' action='/restaurant/new'><input name="restaurant-name" type="text" placeholder = "New Restaurant Name"><input type="submit" value="Create"> </form>'''
                # output += "</body></html>"
                self.wfile.write(output)
                print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
