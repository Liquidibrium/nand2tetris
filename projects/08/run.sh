echo 1
python vm_translator.py --target ./ProgramFlow/BasicLoop/BasicLoop.vm
../../tools/CPUEmulator.sh ./ProgramFlow/BasicLoop/BasicLoop.tst
echo 2
python vm_translator.py --target ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm
../../tools/CPUEmulator.sh ./ProgramFlow/FibonacciSeries/FibonacciSeries.tst 
echo 3
python vm_translator.py --target FunctionCalls/SimpleFunction/SimpleFunction.vm
../../tools/CPUEmulator.sh FunctionCalls/SimpleFunction/SimpleFunction.tst
echo 4
python vm_translator.py --target FunctionCalls/NestedCall/
../../tools/CPUEmulator.sh FunctionCalls/NestedCall/NestedCall.tst
echo 5
python vm_translator.py --target FunctionCalls/FibonacciElement/
../../tools/CPUEmulator.sh ./FunctionCalls/FibonacciElement/FibonacciElement.tst
echo 6
python vm_translator.py --target FunctionCalls/StaticsTest/
../../tools/CPUEmulator.sh FunctionCalls/StaticsTest/StaticsTest.tst