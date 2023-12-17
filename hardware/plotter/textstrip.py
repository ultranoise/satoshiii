

#s = "<Run|WPos:98.000,-303.840,1.498|Bf:0,111|FS:1800,0>"
s = "<Run|WPos:-0.00,-303.840,-10.498|Bf:0,111|FS:1800,0>"
print(s)

x = s.split("|")

print(x)

y = x[1]

print(y)

z = y.split(":")
print(z)

pos = z[1]
print(pos)

coords = pos.split(",")
print(coords)