---------------------------------------------------------------
---------------------------------------------------------------
-------------Juhan got lost in the Paris Catacombs-------------
---------------------------------------------------------------
---------------------------------------------------------------

T��tamiseks vajab 32-bitist p��tonit ja t��tab Windowsis.
64-bitise p��toni puhul on (vist) vaja 64-bitist SDL2.dll
ja (vist) peaks t��tama. (vb on vaja ka teist libtcod versiooni)

Linuxil on vaja ise ehitada libtcod ja SDL2.dll (vist).
Ubuntu 14.04 ja Fedora 22 puhul on asi lihtne, teistel juhtudel
lihtsalt edu.

https://github.com/libtcod/libtcod/tree/master/build/autotools?fbclid=IwAR3pjMEkTz-H-cSJuWscRfWdL7cy9SXCiTiCAKJDjrIEIymrA4_P8fXlKJM

Kui m�ne bugi leiad siis t�en�oliselt on see hoopis feature.
Nii t��tab t�nap�eva m�ngudisain.

---------------------------------------------------------------
-------------------Kuidas k�ivitada, m�ngida-------------------
---------------------------------------------------------------

V�ta Thonnys v�i kusiganes main.py lahti ja pane k�ima. Kasutab
teeke libtcodpy, mis on juba failides olemas, ja pygame, mis
peab kasutajal endal olemas olema.

ESC - Men��
WASD - liikumine(s.h. kirstude avamine ja vastastele haiget tegemine)
I - avab seljakoti men��, kus n�itab ka mida iga nupp teeb.
E - l�heb redelist alla j�rgmisesse tasemesse v�i v�tab �les maas oleva eseme
SPACE - k�es eseme funktsiooni kasutamine (shoot bow / cast spell)

Spell staffid hakkavad spawnima alates 3. tasemest, kuid vibud
tekivad juba varem. Et spelli castida pead veenduma, et ese on
�ldse k�tte v�etud.

M�ng save'ib progressi ka, ehk kui m�ngust quit paned siis
j�rgmine kord saad continue game nupust edasi m�ngida.

---------------------------------------------------------------
-----------------------------Vihjed----------------------------
---------------------------------------------------------------

*Seljakotti mahub kuni 10 asja, k�es hoitud ese mitte kaasaarvatud,
seega korja v�imalikult palju j�ujooke, et elusid taastada ja
enda omadusi ajutiselt tugevdada.

*Kirstud v�ivad vahest hoopis kollid olla, seega �ra neid ava, kui
sul on v�he elusid.

*Staffid, mis annavad flat bonuse, ja staffid, mis omavad spelli
funktsiooni, n�evad samasugused v�lja, seega tasub alates 3. tasemest
k�iki kontrollida. Varem tasub ka, kuna iga staffi flat bonused on erinevad.

*Iga tasemega muutuvad kollid tiba tugevamaks.

*Buff potioneid saab korraga juua nii palju kui seljakotis on ja palju
E t�hte jaksad vajutada.

*Osad kollid pillavad oma relva maha, mis on tavaliselt v�ga n�rk aga
k�ige esimesel tasemel v�ib kasuks tulla.

*M�ngul puudub niinimetatud win condition, kuna kui poolpurjus eestlane
koperdub pimedates tunnelites aina s�gavamale ja s�gavamale (ja veel
sellised tunnelid kust ka kaine m�istusega inimesed on j��nud
teadmata kadunuks) siis annab loogiliselt tuletada et ega sellises
olukorras otseselt v�ita ei saagi. K�ll on aga floor counter, kui 
s�braga m�ngid ja saad �he taseme v�rra kaugemale siis saad talle
n�kku m��rida.

*Kui sa tahad kuskile YT gameplay vms millegi p�rast �les panna siis
v�ta muusika maha, ei m�leta litsentsi tingimusi. 

---------------------------------------------------------------
-----------------------------Intro-----------------------------
---------------------------------------------------------------

Aasta on 1972 ja Eesti eksiilvalitsusest Juhan Juhansson* (nimi
muudetud, arendajatele teada) on Pariisis seoses v�liseestlaste
kokkusaamisega, et arutada hetke olukorda maailmas, ja ka lihtsalt
eesti keele elus hoidmiseks. Kuna aga Pariisis on iga p�eva kohta
2/3 t�en�osus, et samal p�eval leiab aset protest, siis kahjuks
Juhan oma rahvuskaaslasteni ei j�udnudki. Selle asemel pidi ta
s�jalaadsest olukorrast pagema, ning k�ige rahulikum koht selleks
sattus olema Montparnasse'i surnuaed. Olles ka p�eva jooksul
alkoholi tarbinud, nagu eestlased ikka, otsustab ta minna seal m��da
tunnelit alla, kuni m�rkab, et ei teagi kus ta enam on. Tuleb
v�lja, et ta on j�udnud Pariisi katakombidesse, ning ta ei ole seal
�ksi. Siit algabki m�ng, kus Juhan v�itleb kollidega ja, nagu iga
vaimselt kohal inimene teeks, l�heb aina s�gavamale katakombidesse.
