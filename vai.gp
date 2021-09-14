set terminal pngcairo size 2000, 600 font "Helvetica,30" linewidth 10 dashed
set output "vai.png"

p = 1.561892578827941
q1(z) =  p * z - (p-2)/2;
q2(z) = -p * z + (p+2)/2;

Q1(z) = 2.922315236129668*z-1.383472854194501*z*z
Q2(z) =  0.3727369040519853*z*z-1.574667302616667*z+1.663088016624338

unset grid
set key bottom center
set border 3
set xlabel "bias"
set ylabel "probability density"
set xtics axis nomirror
set ytics 0.5 axis nomirror
plot  [0:1][0:] q1(x) dashtype 2 lc 1 t "", \
                q2(x) dashtype 2 lc 2 t "", \
		Q1(x) lc 1 t "Head-Tail coin", \
		Q2(x) lc 2 t "Tail-Tail coin"
