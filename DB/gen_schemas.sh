#!/bin/sh

# for every subfolfer of .
## this will fail on whitespaces!
## TODO: fix witespaces fail
importstring="var mongoose=require('mongoose');\n"
compilestring=""
for D in $(find . -type d)
do
# for every .yaml in subfolder
	for y  in $D/*.yaml
	do
		# if there are no matching files 
		# print a warning 
		if [ -f "$y" ]
		then
# generate schema file with yaml2mongoose.py
			file="$(./yaml2mongoose.py $y)"
			## probably wo'nt work if there's no file ext
			filename=$(basename -- "$y")
			name="${filename%.*}"
# save it in this subdir at the same name
			echo "$file" > $D/$name.js
			jsfile=${y%%yaml}js
			importstring=$importstring"var "$name"Schem =require(\"$jsfile\");\n"
			compilestring=$compilestring"\n $name:mongoose.model('$name',"$name"Schem),"

		else
			echo "No yaml file in $D!"
			break
		fi
	done
done

# generate Schemas.js that aggregates all subshemas
 
res="// This code was generated with ProjectBoot"
res=$res"\n\n"$importstring'\n'
res=$res"\nmodule.exports={$compilestring\n}"
echo $res > Schem.js

echo OUTPUT: $res
echo "Generated the file. testing via nodejs "
$(nodejs Schem.js) && echo Good.

