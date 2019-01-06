#Table specifications and simple queries goes here

from extensions import db

class audit_trail(db.Model):

	id = db.Column(db.INT, primary_key=True)
	user_id = db.Column(db.INT)
	affected_id = db.Column(db.INT, nullable=False)
	target_table = db.Column(db.VARCHAR(25), nullable=False)
	date_created = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.CHAR(1), nullable=False)

	#def query_sample():

		#value = audit_trail(id='1',user_id='2',affected_id='3',target_table='event_information',date_created='2018-01-21',type='5')
		#db.session.add(value)
		#db.session.commit()