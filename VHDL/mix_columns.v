// mix_columns.v
module mix_columns (
    input  wire [127:0] state_in,
    output wire [127:0] state_out
);
    wire [7:0] s[0:15], m[0:15];
    genvar i;
    for (i=0; i<16; i=i+1)
        assign s[i] = state_in[i*8 +:8];

    wire [7:0] t0 = gf2(s[0],s[1],s[2],s[3]);
    wire [7:0] t1 = gf2(s[1],s[2],s[3],s[0]);
    wire [7:0] t2 = gf2(s[2],s[3],s[0],s[1]);
    wire [7:0] t3 = gf2(s[3],s[0],s[1],s[2]);
    wire [7:0] t4 = gf2(s[4],s[5],s[6],s[7]);
    wire [7:0] t5 = gf2(s[5],s[6],s[7],s[4]);
    wire [7:0] t6 = gf2(s[6],s[7],s[4],s[5]);
    wire [7:0] t7 = gf2(s[7],s[4],s[5],s[6]);
    wire [7:0] t8 = gf2(s[8],s[9],s[10],s[11]);
    wire [7:0] t9 = gf2(s[9],s[10],s[11],s[8]);
    wire [7:0] ta = gf2(s[10],s[11],s[8],s[9]);
    wire [7:0] tb = gf2(s[11],s[8],s[9],s[10]);
    wire [7:0] tc = gf2(s[12],s[13],s[14],s[15]);
    wire [7:0] td = gf2(s[13],s[14],s[15],s[12]);
    wire [7:0] te = gf2(s[14],s[15],s[12],s[13]);
    wire [7:0] tf = gf2(s[15],s[12],s[13],s[14]);

    assign state_out = {t0,t1,t2,t3, t4,t5,t6,t7, t8,t9,ta,tb, tc,td,te,tf};

    function [7:0] gf2;
        input [7:0] a0,a1,a2,a3;
        wire [7:0] x2 = gf_mul_inst(a0, 8'h02);
        wire [7:0] x3 = gf_mul_inst(a1, 8'h03);
        begin
            gf2 = x2 ^ x3 ^ a2 ^ a3;
        end
    endfunction

    function [7:0] gf_mul_inst;
        input [7:0] x; input [7:0] y;
        begin
            gf_mul mul_u(.a(x), .b(y), .p(gf_mul_inst));
        end
    endfunction
endmodule