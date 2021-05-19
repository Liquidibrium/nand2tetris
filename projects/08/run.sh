python vm_translator.py --target ./ProgramFlow/BasicLoop/BasicLoop.vm
../../tools/CPUEmulator.sh ./ProgramFlow/BasicLoop/BasicLoop.tst 

python vm_translator.py --target ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm
../../tools/CPUEmulator.sh ./ProgramFlow/FibonacciSeries/FibonacciSeries.tst 

python vm_translator.py --target FunctionCalls/FibonacciElement/
../../tools/CPUEmulator.sh ./FunctionCalls/FibonacciElement/FibonacciElement.tst

python vm_translator.py --target FunctionCalls/NestedCall/Sys.vm
../../tools/CPUEmulator.sh FunctionCalls/NestedCall/NestedCall.tst

python vm_translator.py --target FunctionCalls/SimpleFunction/SimpleFunction.vm
../../tools/CPUEmulator.sh FunctionCalls/SimpleFunction/SimpleFunction.tst
