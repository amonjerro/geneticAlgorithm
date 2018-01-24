import psycopg2 as pg

class DB:
	"""Wrapper for a pg database CRUD handler. Uses a Singleton Pattern"""

	#Inner Class - Holds the important parameters and produces the connection instance
	class __DB:
		def __init__(self, dbPath, maxConn):
			self.dbPath = dbPath
			self.maxConn = maxConn
			self.currConn = 0
			self.error = ''
			self.count = 0
			self.results = 0

		def __str__(self):
			return repr(self) + self.dbPath

		def query(self,sql,values=[],commitable=False,fetchable=False):
			#Debug query
			# print(sql)
			# print(values)

			con = pg.connect(self.dbPath)
			self.maxConn += 1
			cursor = con.cursor()
			try:
				if len(values)>0:
					cursor.execute(sql,values)
				else:
					cursor.execute(sql)
				if fetchable:
					self.results = cursor.fetchall()
					self.count = len(self.results)
				if commitable:
					con.commit()
				con.close()
				self.maxConn -= 1
				return True
			except Exception as e:
				print('Error')
				self.error = e
				con.close()
				return False
		def prepare(self,sql,where=None,priorParams=[],commitable=False,fetchable=False):
			if not where:
				self.query(sql,None,commitable,fetchable)
			else:
				sql += ' WHERE '
				if len(where) > 3:
					for i in range((len(where)//4)+1):
						sql += where[i*4] + ' '
						if where[i*4+1] == 'IN' or where[i*4+1] == 'NOT IN':
							#IN/NOT IN bullshit
							sql += where[i*4+1] + ' ('
							for i in range(len(where[i*4+2])):
								if i == len(where[i*4+2]) - 1:
									sql += ' %s)'
								else:
									sql += ' %s,'
						else:
							#Add operator and placeholder
							sql += where[i*4+1] + ' %s'
							priorParams.append(where[i*4+2])
						if (i*4+3) < len(where) - 1:
							sql += ' ' + where[i*4+3]+ ' '
					return self.query(sql,tuple(priorParams),commitable,fetchable)
				elif len(where) == 3:
					if where[1] == 'IN' or where[1] == 'NOT IN':
						#Working
						sql += where[0] + ' ' + where[1] + ' ('
						for i in range(len(where[2])):
							if i == len(where[2]) - 1:
								sql += ' %s)'
							else:
								sql += ' %s,'
						priorParams.append(where[2])
						return self.query(sql,tuple(priorParams),commitable,fetchable)
					else:
						#Working
						sql += where[0] + ' ' + where[1] + ' %s';
						priorParams.append(where[2])
						return self.query(sql,tuple(priorParams),commitable,fetchable)
				elif len(where) < 3:
					#Working
					self.error = 'Incorrect where statement values'
					return False


	#External Class - Exposes methods that call the methods of the internal class.
	instance = None
	def __init__(self, dbPath,maxconn):
		# print('Instantiating')
		if not DB.instance:
			DB.instance = DB.__DB(dbPath,maxconn)
		else:
			DB.instance.dbPath = dbPath

	def results(self):
		return self.instance.results

	def insert(self,table, content):
		columns = content.keys();
		value_string = 'VALUES ('
		values = []
		sql = 'INSERT INTO '+table+'('
		sub = ''
		for i in columns:
			sub += i+','
			value_string += '%s,'
			values.append(content[i])
		sql += sub.rstrip(',')+') ' + value_string.rstrip(',') + ');'
		DB.instance.query(sql,values,[],True)
		
	def get(self, table, fields=None, where=None):
		sql = 'SELECT '
		if fields:
			for i in fields:
				sql += i+','
			sql = sql.rstrip(',') + ' FROM ' + table
		else:
			sql += '* FROM ' + table
		if not where:
			sql += ';'
			if DB.instance.query(sql):
				print(DB.instance.results)
			else:
				print(DB.instance.error)
		else:
			if DB.instance.prepare(sql,where,[],False,True):
				return DB.instance.results
			else:
				print(DB.instance.error)
	def update(self,table,updateHash,conditions):
		sql = 'UPDATE '+table+' SET '
		updateFields = list(updateHash.keys())
		updateValues = list(updateHash.values())
		for i in range(len(updateFields)):
			if i == len(updateFields) -1 :
				sql += updateFields[i] + ' = %s '
			else:
				sql += updateFields[i] + ' = %s,'
		if DB.instance.prepare(sql,conditions,updateValues,True,False):
			print('Update succesfull')
		else:
			print(DB.instance.error)
	def delete(self,table,conditions):
		sql = 'DELETE FROM '+tables
		DB.instance.prepare(sql,conditions,[],True)