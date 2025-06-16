// aes128_top.v
module aes128_top (
    input  wire        clk,
    input  wire        rst,
    input  wire        start,
    input  wire [127:0] plaintext,
    input  wire [127:0] key,
    output reg  [127:0] ciphertext,
    output reg         done
);
    wire [127:0] rk[0:10], next_state;
    reg  [3:0]   round;
    reg  [127:0] state;

    key_expansion ke(.key(key), .round_key(rk));
    aes_round    ar(.clk(clk), .state_in(state), .round_key(rk[round]), .round_num(round), .state_out(next_state));

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state     <= 128'b0;
            round     <= 4'd0;
            done      <= 1'b0;
        end else if (start) begin
            if (round==0)
                state <= plaintext ^ rk[0];
            else begin
                state <= next_state;
                if (round==10) begin
                    ciphertext <= next_state;
                    done       <= 1'b1;
                end
            end
            round <= round + 1;
        end
    end
endmodule
