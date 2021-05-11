#!/bin/bash

echo ""
echo ":: Building FasterCode"
echo ""

cd ./source/irina
gcc -Wall -fPIC -O3 -c lc.c board.c data.c eval.c hash.c loop.c makemove.c movegen.c movegen_piece_to.c search.c util.c pgn.c parser.c polyglot.c -DNDEBUG
ar cr ../libirina.a lc.o board.o data.o eval.o hash.o loop.o makemove.o movegen.o movegen_piece_to.o search.o util.o pgn.o parser.o polyglot.o
rm *.o

cd ..

cat Faster_Irina.pyx Faster_Polyglot.pyx > FasterCode.pyx

python3 setup_linux.py build_ext --inplace --verbose

cp FasterCode.cpython-3* ../../OS/linux

echo ""
echo ":: Building Complete"
echo ""

echo ":: Making all engines executable"
echo ""
echo ">> Alouette" && chmod 755 ../../OS/linux/Engines/alouette/Alouette-0.1.4
echo ">> Amoeba" && chmod 755 ../../OS/linux/Engines/amoeba/Amoeba-2.6
echo ">> Andscacs" && chmod 755 ../../OS/linux/Engines/andscacs/Andscacs-0.95
echo ">> Arasan" && chmod 755 ../../OS/linux/Engines/arasan/Arasan-22.2
echo ">> Asymptote" && chmod 755 ../../OS/linux/Engines/asymptote/Asymptote-0.8
echo ">> Beef" && chmod 755 ../../OS/linux/Engines/beef/Beef-0.36
echo ">> Cassandre" && chmod 755 ../../OS/linux/Engines/cassandre/Cassandre-0.24
echo ">> CeeChess" && chmod 755 ../../OS/linux/Engines/ceeChess/CeeChess-1.3.2
echo ">> Cheng" && chmod 755 ../../OS/linux/Engines/cheng/Cheng-4.40
echo ">> Chessika" && chmod 755 ../../OS/linux/Engines/chessika/Chessika-2.21
echo ">> Cinnamon" && chmod 755 ../../OS/linux/Engines/cinnamon/Cinnamon-1.2b
echo ">> Clarabit" && chmod 755 ../../OS/linux/Engines/clarabit/Clarabit-1.00
echo ">> Counter" && chmod 755 ../../OS/linux/Engines/counter/Counter-3.7
echo ">> Critter" && chmod 755 ../../OS/linux/Engines/critter/Critter-1.6a
echo ">> CT800" && chmod 755 ../../OS/linux/Engines/cT800/CT800-1.42
echo ">> Daydreamer" && chmod 755 ../../OS/linux/Engines/daydreamer/Daydreamer-1.75
echo ">> Delocto" && chmod 755 ../../OS/linux/Engines/delocto/Delocto-0.61n
echo ">> Discocheck" && chmod 755 ../../OS/linux/Engines/discocheck/Discocheck-5.2.1
echo ">> Dragontooth" && chmod 755 ../../OS/linux/Engines/dragontooth/Dragontooth-0.2
echo ">> Drofa" && chmod 755 ../../OS/linux/Engines/drofa/Drofa-2.2.0
echo ">> Ethereal" && chmod 755 ../../OS/linux/Engines/ethereal/Ethereal-12.75
echo ">> FracTal" && chmod 755 ../../OS/linux/Engines/fracTal/FracTal-1.0
echo ">> Fruit" && chmod 755 ../../OS/linux/Engines/fruit/Fruit-2.1
echo ">> Gaviota" && chmod 755 ../../OS/linux/Engines/gaviota/Gaviota-0.84
echo ">> Glaurung" && chmod 755 ../../OS/linux/Engines/glaurung/Glaurung-2.2
echo ">> Godel" && chmod 755 ../../OS/linux/Engines/godel/Godel-7.0
echo ">> Goldfish" && chmod 755 ../../OS/linux/Engines/goldfish/Goldfish-1.13.0
echo ">> Greko" && chmod 755 ../../OS/linux/Engines/greko/GreKo-2020.03
echo ">> Gunborg" && chmod 755 ../../OS/linux/Engines/gunborg/Gunborg-1.35
echo ">> Hactar" && chmod 755 ../../OS/linux/Engines/hactar/Hactar-0.9.0
echo ">> Igel" && chmod 755 ../../OS/linux/Engines/igel/Igel-3.0.0
echo ">> Irina" && chmod 755 ../../OS/linux/Engines/irina/Irina-0.15
echo ">> Jabba" && chmod 755 ../../OS/linux/Engines/jabba/Jabba-1.0
echo ">> K2" && chmod 755 ../../OS/linux/Engines/k2/K2-0.99
echo ">> Komodo" && chmod 755 ../../OS/linux/Engines/komodo/Komodo-12.1.1-bmi2
echo ">> Laser" && chmod 755 ../../OS/linux/Engines/laser/Laser-1.17
echo ">> Lc0" && chmod 755 ../../OS/linux/Engines/lc0/Lc0-0.27.0
echo ">> Maia" && chmod 755 ../../OS/linux/Engines/maia/Lc0-0.27.0
echo ">> Marvin" && chmod 755 ../../OS/linux/Engines/marvin/Marvin-5.0.0
echo ">> Monochrome" && chmod 755 ../../OS/linux/Engines/monochrome/Monochrome
echo ">> Monolith" && chmod 755 ../../OS/linux/Engines/monolith/Monolith-2.01
echo ">> Octochess" && chmod 755 ../../OS/linux/Engines/octochess/Octochess-r5190
echo ">> Pawny" && chmod 755 ../../OS/linux/Engines/pawny/Pawny-1.2
echo ">> Pigeon" && chmod 755 ../../OS/linux/Engines/pigeon/Pigeon-1.5.1
echo ">> Pulse" && chmod 755 ../../OS/linux/Engines/pulse/Pulse-1.6.1
echo ">> Quokka" && chmod 755 ../../OS/linux/Engines/quokka/Quokka-2.1
echo ">> Rocinante" && chmod 755 ../../OS/linux/Engines/rocinante/Rocinante-2.0
echo ">> RodentII" && chmod 755 ../../OS/linux/Engines/rodentII/RodentII-0.9.64
echo ">> Shallow-blue" && chmod 755 ../../OS/linux/Engines/shallow-blue/Shallow-blue-2.0.0
echo ">> Simplex" && chmod 755 ../../OS/linux/Engines/simplex/Simplex-0.9.8
echo ">> Sissa" && chmod 755 ../../OS/linux/Engines/sissa/Sissa-2.0
echo ">> SpaceDog" && chmod 755 ../../OS/linux/Engines/spaceDog/SpaceDog-0.97.7
echo ">> Stash" && chmod 755 ../../OS/linux/Engines/stash/Stash-29.0
echo ">> Stockfish" && chmod 755 ../../OS/linux/Engines/stockfish/Stockfish-13
echo ">> Supernova" && chmod 755 ../../OS/linux/Engines/supernova/Supernova-2.3
echo ">> Teki" && chmod 755 ../../OS/linux/Engines/teki/Teki-2
echo ">> Texel" && chmod 755 ../../OS/linux/Engines/texel/Texel-1.06
echo ">> Tucano" && chmod 755 ../../OS/linux/Engines/tucano/Tucano-9.00
echo ">> Tunguska" && chmod 755 ../../OS/linux/Engines/tunguska/Tunguska-1.1
echo ">> Velvet" && chmod 755 ../../OS/linux/Engines/velvet/Velvet-1.2.0
echo ">> Weiss" && chmod 755 ../../OS/linux/Engines/weiss/Weiss-1.2
echo ">> Wowl" && chmod 755 ../../OS/linux/Engines/wowl/Wowl-1.3.7
echo ">> WyldChess" && chmod 755 ../../OS/linux/Engines/wyldChess/WyldChess-1.51
echo ">> Zappa" && chmod 755 ../../OS/linux/Engines/zappa/Zappa-1.1
echo ">> Zurichess" && chmod 755 ../../OS/linux/Engines/zurichess/Zurichess-1.7.4
echo ""
echo ":: All done!"

