// key_expansion.v
module key_expansion (
    input  wire [127:0] key,
    output wire [127:0] round_key [0:10]
);
    reg [31:0] words [0:43];
    integer i;
    wire [31:0] temp;
    wire [7:0] rc [0:10];
    assign rc[0]=8'h01; assign rc[1]=8'h02; assign rc[2]=8'h04; assign rc[3]=8'h08;
    assign rc[4]=8'h10; assign rc[5]=8'h20; assign rc[6]=8'h40; assign rc[7]=8'h80;
    assign rc[8]=8'h1B; assign rc[9]=8'h36; assign rc[10]=8'h6C;

    function [31:0] sub_word;
        input [31:0] w;
        begin
            sub_word = { sbox(w[23:16]), sbox(w[15:8]),
                         sbox(w[7:0]),     sbox(w[31:24]) };
        end
    endfunction

    function [7:0] sbox;
        input [7:0] b; begin
            aes_sbox u(.in(b), .out(sbox));
        end endfunction

    always @(*) begin
        for (i=0; i<4; i=i+1)
            words[i] = key[127 - i*32 -:32];
        for (i=4; i<44; i=i+1) begin
            if (i % 4 == 0)
                temp = sub_word(words[i-1]) ^ {rc[(i/4)-1],24'h000000};
            else
                temp = words[i-1];
            words[i] = words[i-4] ^ temp;
        end
        for (i=0; i<11; i=i+1)
            round_key[i] = {words[4*i], words[4*i+1], words[4*i+2], words[4*i+3]};
    end
endmodule