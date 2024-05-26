#cat sgjp.tab | sed -En "s/^sie[^a-zA-zćńś]/\0/p"
cat sgjp.tab | sed -E "/^sie[^a-zA-zćńś]/d" > sgjp.mod.tab
echo "się " >> sgjp.mod.tab
split --number=l/32 sgjp.mod.tab słownik_podzielony/slownik-