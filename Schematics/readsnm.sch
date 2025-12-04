v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -240 -10 -240 100 {lab=qb2}
N -240 50 -130 50 {lab=qb2}
N -320 -40 -320 130 {lab=q2}
N -320 -40 -280 -40 {lab=q2}
N -320 130 -280 130 {lab=q2}
N -420 50 -320 50 {lab=q2}
N -420 50 -420 60 {lab=q2}
N -420 120 -420 200 {lab=GND}
N -420 200 -240 200 {lab=GND}
N -240 160 -240 200 {lab=GND}
N -330 200 -330 220 {lab=GND}
N -240 130 -150 130 {lab=GND}
N -240 160 -150 160 {lab=GND}
N -240 -120 -240 -70 {lab=VCC}
N -240 -40 -160 -40 {lab=VCC}
N -240 -70 -160 -70 {lab=VCC}
N -160 -70 -160 -40 {lab=VCC}
N -150 130 -150 160 {lab=GND}
N -50 -120 -50 10 {lab=VCC}
N 70 -120 70 10 {lab=VCC}
N -20 50 -20 210 {lab=VCC}
N 40 50 40 210 {lab=VCC}
N -50 50 -50 110 {lab=GND}
N 70 50 70 130 {lab=GND}
N -50 110 -50 130 {lab=GND}
N -50 10 -20 10 {lab=VCC}
N -20 10 -20 50 {lab=VCC}
N 40 10 70 10 {lab=VCC}
N 40 10 40 50 {lab=VCC}
N 250 0 250 110 {lab=q1}
N 150 50 250 50 {lab=q1}
N 290 -30 320 -30 {lab=qb1}
N 320 -30 320 140 {lab=qb1}
N 290 140 320 140 {lab=qb1}
N 320 50 420 50 {lab=qb1}
N 420 50 420 60 {lab=qb1}
N 420 120 420 210 {lab=GND}
N 250 210 420 210 {lab=GND}
N 250 170 250 210 {lab=GND}
N 340 210 340 230 {lab=GND}
N 170 140 250 140 {lab=GND}
N 170 140 170 170 {lab=GND}
N 170 170 250 170 {lab=GND}
N 250 -120 250 -60 {lab=VCC}
N 170 -30 250 -30 {lab=VCC}
N 170 -60 170 -30 {lab=VCC}
N 170 -60 250 -60 {lab=VCC}
N 450 -50 450 -20 {lab=GND}
N 450 -140 450 -110 {lab=VCC}
N -130 50 -80 50 {lab=qb2}
N 100 50 150 50 {lab=q1}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 270 -30 2 0 {name=M1
W=0.42
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {code.sym} -480 -210 0 0 {name=Readsnm only_toplevel=false value=".lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.param temp=27
.param supl=1.8

.dc V1 0 1.8 0.01 V2 0 1.8 0.01
.control
run
setplot
setplot dc1
plot q1 vs qb1 q2 vs qb2
wrdata /home/scholes33/Projects/PreLayout/Xschem/readsnm.txt q1 qb1 q2 qb2
.endc
.end
"
}
C {sky130_fd_pr/nfet_01v8.sym} 270 140 2 0 {name=M2
W=0.84
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -260 -40 0 0 {name=M3
W=0.42
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -260 130 0 0 {name=M4
W=0.84
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 70 30 1 0 {name=M5
W=0.42
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -50 30 1 0 {name=M6
W=0.42
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {vsource.sym} -420 90 0 0 {name=V2 value=1.8V savecurrent=false}
C {gnd.sym} -330 220 0 0 {name=l1 lab=GND}
C {lab_wire.sym} -240 -120 0 0 {name=p1 sig_type=std_logic lab=VCC}
C {lab_wire.sym} -320 50 0 0 {name=p2 sig_type=std_logic lab=q2}
C {lab_wire.sym} -130 50 0 0 {name=p3 sig_type=std_logic lab=qb2}
C {lab_wire.sym} -50 -120 0 0 {name=p4 sig_type=std_logic lab=VCC}
C {lab_wire.sym} 70 -120 0 0 {name=p5 sig_type=std_logic lab=VCC}
C {lab_wire.sym} 150 50 0 0 {name=p8 sig_type=std_logic lab=q1}
C {vsource.sym} 420 90 0 0 {name=V1 value=1.8V savecurrent=false}
C {gnd.sym} 340 230 0 0 {name=l2 lab=GND}
C {lab_wire.sym} 320 50 0 0 {name=p9 sig_type=std_logic lab=qb1}
C {lab_wire.sym} 250 -120 0 0 {name=p10 sig_type=std_logic lab=VCC}
C {lab_wire.sym} -20 210 0 0 {name=p6 sig_type=std_logic lab=bl}
C {lab_wire.sym} 40 210 0 0 {name=p7 sig_type=std_logic lab=blbar
}
C {vsource.sym} 450 -80 0 0 {name=VCC value=\{supl\} savecurrent=false}
C {gnd.sym} 450 -20 0 0 {name=l3 lab=GND}
C {lab_wire.sym} 450 -140 0 0 {name=p11 sig_type=std_logic lab=VCC}
C {gnd.sym} 70 130 0 0 {name=l4 lab=GND}
C {gnd.sym} -50 130 0 0 {name=l5 lab=GND}
