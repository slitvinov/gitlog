set terminal pngcairo size 2000, 600 font "Helvetica,30" linewidth 15
set output "var.png"

E = 13/24.0
f(q) = (-q*log(q))-log(3)*q-log(1-q)*(1-q)-log(6)*(1-q)
lE = log(E)

unset grid
set key center
set xlabel "parameter of Q"
set xtics axis nomirror
set ytics 0.5 axis nomirror
set border 3
plot [-0.001:1.001][:-0.5] f(x) t "evidence lower bound", lE t "log-evidence", "<echo 0.66667 -0.693147" w p ps 6 pt 7 lc 1 t ""