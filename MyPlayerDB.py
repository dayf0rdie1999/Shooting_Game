import mysql.connector


def main():
    mydb = MyPlayerDB()

class MyPlayerDB():

    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="Relive19$", database="gameshooting")
        self.mycursor = self.mydb.cursor()
        self.arrayData = None
        self.studentData = None
        self.playerList = []

    # def createUserTable(self):
    # self.mycursor.execute("CREATE TABLE user(username varchar(200), password varchar(200))")

    def insertPlayer(self, playername):
        sqlform = "Insert into player(playername,score) values (%s,%s)"
        player = (playername, 0)
        self.mycursor.execute(sqlform, player)
        self.mydb.commit()

    def readPlayer(self):
        self.mycursor.execute("SELECT * FROM player")
        self.arrayData = self.mycursor.fetchall()

    def printStudent(self):
        for row in self.arrayData:
            print(row)

    def updatePlayer(self, newPlayerName, oldPlayerName):
        sqlForm = "UPDATE player SET playername= %s WHERE playername= %s"
        player = (newPlayerName, oldPlayerName)
        self.mycursor.execute(sqlForm, player)
        self.mydb.commit()

    def updateScore(self, newScore, oldScore):
        sqlForm = "UPDATE player SET score= %s WHERE score= %s"
        player = (newScore, oldScore)
        self.mycursor.execute(sqlForm, player)
        self.mydb.commit()

    def deletePlayer(self, playerName, score):
        sqlForm = "DELETE FROM player WHERE playername= %s AND score = %s"
        player = (playerName, score)
        self.mycursor.execute(sqlForm, player)
        self.mydb.commit()

    def checkPlayer(self, playerName, score):
        self.readPlayer()
        for row in self.arrayData:
            if row[0] == playerName and row[1] == score:
                return True
            else:
                pass

        return False

    def listPlayer(self):
        self.mycursor.execute("SELECT * FROM player")
        self.playerData = self.mycursor.fetchall()

        for row in self.playerData:
            playerName = row[0] + "        " + str(row[1])
            self.playerList.append(playerName)

        return self.playerList


if __name__ == "__main__":
    main()
