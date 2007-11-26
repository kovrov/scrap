from datetime import datetime
import sqlalchemy, sqlalchemy.orm


engine = sqlalchemy.create_engine('sqlite:////temp/sqlite.db', echo=True)
metadata = sqlalchemy.MetaData()
session = sqlalchemy.orm.sessionmaker(engine)()

class BlogEntry(object):
	def __init__(self, title=None, content=None):
		self.title = title
		self.content = content
		self.date = datetime.now()

	def load():
		pass

	def save():
		session.save(self)
# I want class decorators!
BlogEntry.table = sqlalchemy.Table('entries', metadata,
	sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
	sqlalchemy.Column('title', sqlalchemy.String(1024)),
	sqlalchemy.Column('content', sqlalchemy.TEXT()),
	sqlalchemy.Column('date', sqlalchemy.DateTime()))
BlogEntry.mapper = sqlalchemy.orm.mapper(BlogEntry, BlogEntry.table)
BlogEntry.query = session.query(BlogEntry)

if __name__ == "__main__":
	# create sql tables
	metadata.create_all(engine)
	#tests
	print BlogEntry.query
