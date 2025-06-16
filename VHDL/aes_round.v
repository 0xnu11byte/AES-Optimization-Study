// aes_round.v
module aes_round (
    input  wire        clk,
    input  wire [127:0] state_in,
    input  wire [127:0] round_key,
    input  wire [3:0]   round_num,
    output reg  [127:0] state_out
);
    wire [127:0] sb, sr, mc, ark;
    sbox_layer sbm(.in(state_in), .out(sb));
    shift_rows shr(.state_in(sb), .state_out(sr));
    mix_columns mcm(.state_in(sr), .state_out(mc));
    assign ark = (round_num<10) ? mc ^ round_key : sr ^ round_key;

    always @(posedge clk)
        state_out <= ark;
endmodule