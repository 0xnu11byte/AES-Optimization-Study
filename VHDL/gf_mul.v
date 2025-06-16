// gf_mul.v
module gf_mul (
    input  wire [7:0] a, b,
    output wire [7:0] p
);
    reg [7:0] aa, bb, rr;
    integer i;
    always @(*) begin
        aa = a; bb = b; rr = 8'h00;
        for (i=0; i<8; i=i+1) begin
            if (bb[0]) rr = rr ^ aa;
            bb = bb >> 1;
            if (aa[7]) aa = (aa << 1) ^ 8'h1b;
            else       aa = aa << 1;
        end
    end
    assign p = rr;
endmodule