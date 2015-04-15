vector=$1
width=$2
height=$3
for f in ../kaskade\!/*.xml
do
	echo $f| tee -a $1.data
	./testing.py $f $vector ../negativi $width $height| tee -a $1.data
	echo ""| tee -a $1.data
done
