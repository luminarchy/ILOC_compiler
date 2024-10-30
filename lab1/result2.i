loadI  204 => r0              // rematerialize vr57 => pr0
load   r0 => r0               // Mem[vr57] => vr3
loadI  200 => r1              // rematerialize vr56 => pr1
load   r1 => r1               // Mem[vr56] => vr5
loadI  65536 => r2            // spill pr0 (vr3) => Mem[65536]
store  r0 => r2 
loadI  196 => r2              // rematerialize vr55 => pr2
load   r2 => r0               // Mem[vr55] => vr7
loadI  65540 => r2            // spill pr1 (vr5) => Mem[65540]
store  r1 => r2 
loadI  192 => r2              // rematerialize vr54 => pr2
load   r2 => r1               // Mem[vr54] => vr9
loadI  65544 => r2            // spill pr0 (vr7) => Mem[65544]
store  r0 => r2 
loadI  188 => r2              // rematerialize vr53 => pr2
load   r2 => r0               // Mem[vr53] => vr11
loadI  65548 => r2            // spill pr1 (vr9) => Mem[65548]
store  r1 => r2 
loadI  184 => r2              // rematerialize vr52 => pr2
load   r2 => r1               // Mem[vr52] => vr13
loadI  65552 => r2            // spill pr0 (vr11) => Mem[65552]
store  r0 => r2 
loadI  180 => r2              // rematerialize vr51 => pr2
load   r2 => r0               // Mem[vr51] => vr50
loadI  164 => r0              // rematerialize vr45 => pr0
loadI  176 => r2              // rematerialize vr49 => pr2
store  r0 => r2               // vr45 => Mem[vr49]
loadI  65556 => r2            // spill pr1 (vr13) => Mem[65556]
store  r1 => r2 
loadI  176 => r2              // rematerialize vr49 => pr2
load   r2 => r1               // Mem[vr49] => vr48
loadI  172 => r1              // rematerialize vr47 => pr1
load   r1 => r1               // Mem[vr47] => vr15
loadI  65560 => r2            // spill pr1 (vr15) => Mem[65560]
store  r1 => r2 
loadI  168 => r2              // rematerialize vr46 => pr2
load   r2 => r1               // Mem[vr46] => vr17
load   r0 => r0               // Mem[vr45] => vr19
loadI  65564 => r2            // spill pr1 (vr17) => Mem[65564]
store  r1 => r2 
loadI  160 => r2              // rematerialize vr44 => pr2
load   r2 => r1               // Mem[vr44] => vr21
loadI  65568 => r2            // spill pr0 (vr19) => Mem[65568]
store  r0 => r2 
loadI  156 => r2              // rematerialize vr43 => pr2
load   r2 => r0               // Mem[vr43] => vr23
loadI  65572 => r2            // spill pr1 (vr21) => Mem[65572]
store  r1 => r2 
loadI  152 => r2              // rematerialize vr42 => pr2
load   r2 => r1               // Mem[vr42] => vr25
loadI  65576 => r2            // spill pr0 (vr23) => Mem[65576]
store  r0 => r2 
loadI  148 => r2              // rematerialize vr41 => pr2
load   r2 => r0               // Mem[vr41] => vr27
loadI  65580 => r2            // spill pr1 (vr25) => Mem[65580]
store  r1 => r2 
loadI  144 => r2              // rematerialize vr40 => pr2
load   r2 => r1               // Mem[vr40] => vr29
loadI  65584 => r2            // spill pr0 (vr27) => Mem[65584]
store  r0 => r2 
loadI  140 => r2              // rematerialize vr39 => pr2
load   r2 => r0               // Mem[vr39] => vr31
loadI  65588 => r2            // spill pr1 (vr29) => Mem[65588]
store  r1 => r2 
loadI  136 => r2              // rematerialize vr38 => pr2
load   r2 => r1               // Mem[vr38] => vr33
loadI  65592 => r2            // spill pr0 (vr31) => Mem[65592]
store  r0 => r2 
loadI  132 => r2              // rematerialize vr37 => pr2
load   r2 => r0               // Mem[vr37] => vr35
loadI  65596 => r2            // spill pr1 (vr33) => Mem[65596]
store  r1 => r2 
loadI  128 => r2              // rematerialize vr36 => pr2
load   r2 => r1               // Mem[vr36] => vr34
add    r1, r0  => r0          // vr34, vr35 => vr32
loadI  65596 => r1            // restore  Mem[65596] (vr33) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr32, vr33 => vr30
loadI  65592 => r0            // restore  Mem[65592] (vr31) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr30, vr31 => vr28
loadI  65588 => r1            // restore  Mem[65588] (vr29) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr28, vr29 => vr26
loadI  65584 => r0            // restore  Mem[65584] (vr27) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr26, vr27 => vr24
loadI  65580 => r1            // restore  Mem[65580] (vr25) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr24, vr25 => vr22
loadI  65576 => r0            // restore  Mem[65576] (vr23) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr22, vr23 => vr20
loadI  65572 => r1            // restore  Mem[65572] (vr21) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr20, vr21 => vr18
loadI  65568 => r0            // restore  Mem[65568] (vr19) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr18, vr19 => vr16
loadI  65564 => r1            // restore  Mem[65564] (vr17) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr16, vr17 => vr14
loadI  65560 => r0            // restore  Mem[65560] (vr15) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr14, vr15 => vr12
loadI  65556 => r1            // restore  Mem[65556] (vr13) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr12, vr13 => vr10
loadI  65552 => r0            // restore  Mem[65552] (vr11) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr10, vr11 => vr8
loadI  65548 => r1            // restore  Mem[65548] (vr9) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr8, vr9 => vr6
loadI  65544 => r0            // restore  Mem[65544] (vr7) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr6, vr7 => vr4
loadI  65540 => r1            // restore  Mem[65540] (vr5) => pr 1
load   r1 => r1 
add    r0, r1  => r1          // vr4, vr5 => vr2
loadI  65536 => r0            // restore  Mem[65536] (vr3) => pr 0
load   r0 => r0 
add    r1, r0  => r0          // vr2, vr3 => vr1
loadI  1024 => r1             // rematerialize vr0 => pr1
store  r0 => r1               // vr1 => Mem[vr0]
output 1024                   // as in the input
output 176                    // as in the input