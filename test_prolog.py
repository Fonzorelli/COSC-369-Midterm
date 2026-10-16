from pyswip import Prolog

prolog = Prolog()

prolog.assertz("parent(john, mary)")
prolog.assertz("parent(mary, steve)")

prolog.assertz(
    "grandparent(X, Z) :- parent(X, Y), parent(Y, Z)"
)

for result in prolog.query("grandparent(john, X)"):
    print(result)

