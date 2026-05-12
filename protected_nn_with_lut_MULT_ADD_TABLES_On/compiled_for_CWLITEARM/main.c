#include "hal.h"
#include "simpleserial.h"
#include "network.h"          
#include "network_config.h"   
#include <stdint.h>

#define NOP_SLED_50() do { \
    for(int i=0; i<200; i++) { __asm__ __volatile__ ("nop"); } \
} while(0)

// verify data integrity by echoing back the 20 bytes
uint8_t debug_handle(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{
    simpleserial_put('d', len, buf);
    return 0;
}

uint8_t handle(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{
    // if input sent less than 20 bytes, program execution stops 
    // prevent program to read random memory
    if (len < 20) {
        uint8_t error_code = 0xEE; 
        simpleserial_put('e', 1, &error_code);
        return 0x01;
    }

    trigger_high();
    
    NOP_SLED_50(); 

    uint16_t *inputs_16bit = (uint16_t *)buf;
    int32_t result = network_forward(inputs_16bit);
    
    NOP_SLED_50(); 
    
    trigger_low();

    // return the 4-byte result
    simpleserial_put('r', sizeof(int32_t), (uint8_t*)&result);
    return 0;
}

int main(void)
{
    platform_init();
    init_uart();
    trigger_setup();
    simpleserial_init();

    // 10 inputs * 2 bytes each = 20 bytes
    simpleserial_addcmd('p', 20, handle);
    simpleserial_addcmd('d', 20, debug_handle);

    while(1) simpleserial_get();
}