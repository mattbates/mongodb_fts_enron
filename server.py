import tornado.web, tornado.ioloop
import motor
import pymongo
from tornado import gen
import json
from bson import json_util

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish()

class HomeHandler(tornado.web.RequestHandler):
    @gen.engine
    @tornado.web.asynchronous
    def get(self):
	print self.settings['db']
        self.write('<form action="/"><input type="text" name="keywords"/></form>')
	if self.get_argument('keywords',''):
		q = self.get_argument('keywords', '')
		results = yield motor.Op(db.command, 'text', 'emails', search=q, limit=20, skip=5)
		print results
		self.write('<h3>%d results for "%s" in %dms</h3>' % (results['stats']['nscanned'],q,results['stats']['timeMicros']/1000))
		for doc in results['results']:
			self.write(json.dumps(doc, default = json_util.default))
			self.write('<br><br>')
	self.finish()

db = motor.MotorClient().open_sync().enron

application = tornado.web.Application([
        (r'/search', SearchHandler),
        (r'/', HomeHandler)
    ], db=db
)

print 'Listening on http://localhost:8888'
application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
