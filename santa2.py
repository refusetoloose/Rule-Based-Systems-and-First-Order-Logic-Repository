# %%
from pathlib import Path

from nltk import Prover9, Prover9Command
from nltk.sem import Expression

read_expr = Expression.fromstring

p = Prover9()
p._binary_location = r"C:\Program Files (x86)\Prover9-Mace4\bin-win32"


# %%
assumptions = [
    read_expr(p)
    for p in [
        # Every child loves anyone who gives the child any present.
        """
        all x y z.(child(x) & present(y) & gives(z,y,x) -> loves(x,z))
        """,
        # Every child will be given some present by Santa if Santa can travel on Christmas eve.
        """
        travels(Santa,Christmas_eve)->(all x.(child(x)->(exists y.(present(y) & gives(Santa,y,x)))))
        """,
        # It is foggy on Christmas eve.
        """
        foggy(Christmas_eve)
        """,
        # Anytime it is foggy, anyone can travel if he has some source of light.
        """
        all x t.(foggy(t)->(exists y.(light(y) & has(x,y))->travels(x,t)))
        """,
        # Any reindeer with a red nose is a source of light.
        """
        all x.(rednose_reindeer(x) -> light(x))
        """,
    ]
]

goal = read_expr(
    # If Santa has some reindeer with a red nose, then every child loves Santa.
    """
    exists x.(rednose_reindeer(x) & has(Santa, x))->all y.(child(y) -> loves(y,Santa))
    """
)



# %%
prover = Prover9Command(goal=goal, assumptions=assumptions, prover=p)

prover.print_assumptions()

print()
is_proved = prover.prove()

if is_proved:
    print("It can be proved.\nSee below:\n")
    print(prover.proof())
else:
    print("It cannot be proved")

# %%
