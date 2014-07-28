from hostessapp import models

db = models.db
db.drop_all()
db.create_all()


a = models.BumpGroup("A")
b = models.BumpGroup("B")
c = models.BumpGroup("C")

db.session.add(a)
db.session.add(b)
db.session.add(c)

anna = models.Sister("Anna")
elsa = models.Sister("Elsa")
mary = models.Sister("Mary")
kate = models.Sister("Ashley")
emma = models.Sister("Emma")
dawn = models.Sister("Dawn")
alice = models.Sister("Alice")
amelia = models.Sister("Amelia")

anna.is_crib = True

anna.bump_group = a
elsa.bump_group = a
mary.bump_group = a
kate.bump_group = b
emma.bump_group = b
dawn.bump_group = b
alice.bump_group = c
amelia.bump_group = c

db.session.add(anna)
db.session.add(elsa)
db.session.add(mary)
db.session.add(kate)
db.session.add(emma)
db.session.add(dawn)
db.session.add(alice)
db.session.add(amelia)

#pnms

i = models.Pnm("Irma", "CS", "atown", 1, "writing, ponies")
j = models.Pnm("Allysa", "Bio", "btown", 2, "all kinds of dance")
k = models.Pnm("Lydia", "Chemistry", "ctown", 1, "stagecraft, singing")
l = models.Pnm("Jamie", "Philosophy", "dtown", 1, "veganism, acro")
m = models.Pnm("Vera", "History", "etown", 2, "ren fairs, crafts of all kinds")
n = models.Pnm("Liz", "Mech-e", "dtown", 1, "hip-hop")
o = models.Pnm("Michelle", "EE", "etown", 2, "robotics")
p = models.Pnm("Taylor", "Physics", "atown", 1, "art history")

db.session.add(i)
db.session.add(j)
db.session.add(k)
db.session.add(l)
db.session.add(m)
db.session.add(n)
db.session.add(o)
db.session.add(p)

db.session.add(models.Meta())

db.session.commit()
