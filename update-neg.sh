rm -f neg.txt
for f in ../negativi/*/*.*
do
	echo $f>>neg.txt
done
