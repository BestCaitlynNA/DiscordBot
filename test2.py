from Naked.toolshed.shell import execute_js, muterun_js
import sys
string = "var x = 10;\n"\
"x = 10 - 5;\n"\
"console.log(x);\n"\
"function greet() {\n"\
"      console.log('Hello World!');\n"\
"}\n"\
"greet()\n"

with open('temp.js', 'w') as f:
    f.write(string)

response = muterun_js('temp.js')
if response.exitcode == 0:
    print(response.stdout)
else:
    sys.stderr.write(response.stderr)
