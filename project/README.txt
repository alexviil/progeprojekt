---------------------------------------------------------------
---------------------------------------------------------------
-------------Juhan got lost in the Paris Catacombs-------------
---------------------------------------------------------------
---------------------------------------------------------------

Töötamiseks vajab 32-bitist püütonit ja töötab Windowsis.
64-bitise püütoni puhul on (vist) vaja 64-bitist SDL2.dll
ja (vist) peaks töötama. (vb on vaja ka teist libtcod versiooni)

Linuxil on vaja ise ehitada libtcod ja SDL2.dll (vist).
Ubuntu 14.04 ja Fedora 22 puhul on asi lihtne, teistel juhtudel
lihtsalt edu.

https://github.com/libtcod/libtcod/tree/master/build/autotools?fbclid=IwAR3pjMEkTz-H-cSJuWscRfWdL7cy9SXCiTiCAKJDjrIEIymrA4_P8fXlKJM

Kui mõne bugi leiad siis tõenäoliselt on see hoopis feature.
Nii töötab tänapäeva mängudisain.

---------------------------------------------------------------
-------------------Kuidas käivitada, mängida-------------------
---------------------------------------------------------------

Võta Thonnys või kusiganes main.py lahti ja pane käima. Kasutab
teeke libtcodpy, mis on juba failides olemas, ja pygame, mis
peab kasutajal endal olemas olema.

ESC - Menüü
WASD - liikumine(s.h. kirstude avamine ja vastastele haiget tegemine)
I - avab seljakoti menüü, kus näitab ka mida iga nupp teeb.
E - läheb redelist alla järgmisesse tasemesse või võtab üles maas oleva eseme
SPACE - käes eseme funktsiooni kasutamine (shoot bow / cast spell)

Spell staffid hakkavad spawnima alates 3. tasemest, kuid vibud
tekivad juba varem. Et spelli castida pead veenduma, et ese on
üldse kätte võetud.

Mäng save'ib progressi ka, ehk kui mängust quit paned siis
järgmine kord saad continue game nupust edasi mängida.

---------------------------------------------------------------
-----------------------------Vihjed----------------------------
---------------------------------------------------------------

*Seljakotti mahub kuni 10 asja, käes hoitud ese mitte kaasaarvatud,
seega korja võimalikult palju jõujooke, et elusid taastada ja
enda omadusi ajutiselt tugevdada.

*Kirstud võivad vahest hoopis kollid olla, seega ära neid ava, kui
sul on vähe elusid.

*Staffid, mis annavad flat bonuse, ja staffid, mis omavad spelli
funktsiooni, näevad samasugused välja, seega tasub alates 3. tasemest
kõiki kontrollida. Varem tasub ka, kuna iga staffi flat bonused on erinevad.

*Iga tasemega muutuvad kollid tiba tugevamaks.

*Buff potioneid saab korraga juua nii palju kui seljakotis on ja palju
E tähte jaksad vajutada.

*Osad kollid pillavad oma relva maha, mis on tavaliselt väga nõrk aga
kõige esimesel tasemel võib kasuks tulla.

*Mängul puudub niinimetatud win condition, kuna kui poolpurjus eestlane
koperdub pimedates tunnelites aina sügavamale ja sügavamale (ja veel
sellised tunnelid kust ka kaine mõistusega inimesed on jäänud
teadmata kadunuks) siis annab loogiliselt tuletada et ega sellises
olukorras otseselt võita ei saagi. Küll on aga floor counter, kui 
sõbraga mängid ja saad ühe taseme võrra kaugemale siis saad talle
näkku määrida.

*Kui sa tahad kuskile YT gameplay vms millegi pärast üles panna siis
võta muusika maha, ei mäleta litsentsi tingimusi. 

---------------------------------------------------------------
-----------------------------Intro-----------------------------
---------------------------------------------------------------

Aasta on 1972 ja Eesti eksiilvalitsusest Juhan Juhansson* (nimi
muudetud, arendajatele teada) on Pariisis seoses väliseestlaste
kokkusaamisega, et arutada hetke olukorda maailmas, ja ka lihtsalt
eesti keele elus hoidmiseks. Kuna aga Pariisis on iga päeva kohta
2/3 tõenäosus, et samal päeval leiab aset protest, siis kahjuks
Juhan oma rahvuskaaslasteni ei jõudnudki. Selle asemel pidi ta
sõjalaadsest olukorrast pagema, ning kõige rahulikum koht selleks
sattus olema Montparnasse'i surnuaed. Olles ka päeva jooksul
alkoholi tarbinud, nagu eestlased ikka, otsustab ta minna seal mööda
tunnelit alla, kuni märkab, et ei teagi kus ta enam on. Tuleb
välja, et ta on jõudnud Pariisi katakombidesse, ning ta ei ole seal
üksi. Siit algabki mäng, kus Juhan võitleb kollidega ja, nagu iga
vaimselt kohal inimene teeks, läheb aina sügavamale katakombidesse.
