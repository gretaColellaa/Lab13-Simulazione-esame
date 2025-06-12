from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct s.`year` 
                    from formula1.seasons s  """

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getCose(a):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r.driverId , r.raceId , r.`position` 
                    from formula1.results r 
                    join formula1.races r2 on r2.raceId = r.raceId 
                    where r.`position` is not NULL
                    and r2.`year` = %s"""

        cursor.execute(query, (a,))

        for row in cursor:
            result.append((row["driverId"],row["raceId"], row["position"] ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getDrivers(a):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.driverId 
                            from formula1.results r 
                            join formula1.races r2 on r2.raceId = r.raceId 
                            where r.`position` is not NULL
                            and r2.`year` = %s"""

        cursor.execute(query, (a,))

        for row in cursor:
            result.append(row["driverId"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRaces(a):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.raceId
                                from formula1.results r 
                                join formula1.races r2 on r2.raceId = r.raceId 
                                where r.`position` is not NULL
                                and r2.`year` = %s"""

        cursor.execute(query, (a,))

        for row in cursor:
            result.append(row["raceId"])

        cursor.close()
        conn.close()
        return result



