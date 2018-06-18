#-----------------------COMMENT EXAMPLE -------------------
#this is comment, nothing to see here
echo --------------------RUN PROCESS ls-------------------
ls


echo --------------------RUN PROCESS WITH ARGUMENT-------------------
ls -al


echo --------------------RUN TWO INLINE PROCESSES WITH SEPARATOR-------------------
echo command1; echo command2


echo -------------------- PIPE-------------------
ls -l | grep py | grep ast


echo -------------------- REDIRECT OUTPUT TO FILE-------------------
ls -l | grep py | grep ast > /home/wisnienka/interpreterek/file
echo output redirected to file
echo inside of file
cat /home/wisnienka/interpreterek/file


echo ---------------------ASSIGN VARIABLE
x=1
echo variable x has been assigned with value 1


echo -------------------GET VARIABLE VALUE USING DOLLAR SIGN
echo value x is $x
HOME=/home/wisnienka/
echo $HOME


echo --------------------IF EXAMPLE with multiple bash operators
if [ 1 -eq 1 ]
then
    echo 1 equals 1
fi
#-------------------------------------
if [ 1 -ne 2 ]
then
    echo 1 dont equals 2
fi
#-------------------------------------
if [ 1 -lt 2 ]
then
    echo 1 is less than 2
fi
#-------------------------------------
if [ 2 -gt 1 ]
then
    echo 2 is greather than 1
fi


echo --------------------IF-ELSE EXAMPLE with variables
x=1
y=2
if [ $x -eq $y ]
then
  echo x equals y
else
  echo x is NOT equal y
fi