python jack_analyzer.py  --target ArrayTest
../../tools/TextComparer.sh ./ArrayTest/Main.xml ./ArrayTest/Main2.xml

python jack_analyzer.py  --target ExpressionLessSquare
../../tools/TextComparer.sh ./ExpressionLessSquare/Main.xml ./ExpressionLessSquare/Main2.xml
../../tools/TextComparer.sh ./ExpressionLessSquare/Square.xml ./ExpressionLessSquare/Square2.xml
../../tools/TextComparer.sh ./ExpressionLessSquare/SquareGame.xml ./ExpressionLessSquare/SquareGame2.xml



python jack_analyzer.py  --target Square
../../tools/TextComparer.sh ./Square/Main.xml ./Square/Main2.xml
../../tools/TextComparer.sh ./Square/Square.xml ./Square/Square2.xml
../../tools/TextComparer.sh ./Square/SquareGame.xml ./Square/SquareGame2.xml


