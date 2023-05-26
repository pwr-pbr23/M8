cd DeepLineDP\script\line-level-baseline\

echo Generating results for N-gram line-level baseline...
cd ngram
javac n_gram.java
java n_gram
xcopy /E /I n_gram_result\ ..\..\..\output\

echo Generating results for ErrorProne line-level baseline...
cd ..\ErrorProne
jupyter run run_ErrorProne.ipynb
xcopy /E /I ErrorProne_result\ ..\..\..\output\
