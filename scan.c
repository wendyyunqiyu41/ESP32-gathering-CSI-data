/* Scan Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

/*
    This example shows how to use the All Channel Scan or Fast Scan to connect
    to a Wi-Fi network.

    In the Fast Scan mode, the scan will stop as soon as the first network matching
    the SSID is found. In this mode, an application can set threshold for the
    authentication mode and the Signal strength. Networks that do not meet the
    threshold requirements will be ignored.

    In the All Channel Scan mode, the scan will end only after all the channels
    are scanned, and connection will start with the best network. The networks
    can be sorted based on Authentication Mode or Signal Strength. The priority
    for the Authentication mode is:  WPA2 > WPA > WEP > Open
*/
//my includes
#include <stdint.h>
#include <inttypes.h>
#include <math.h>   //need to calculate the phase (But cause fragmentation dumb)
#include <string.h> //need for the string compare
#include <stdio.h>  //TO put into a file

//Original includes
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_event_loop.h"
#include "nvs_flash.h"

//Timer includes
#include "esp_types.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "soc/timer_group_struct.h"
#include "driver/periph_ctrl.h"
#include "driver/timer.h"

#define TIMER_DIVIDER         16  //  Hardware timer clock divider
#define TIMER_SCALE           (TIMER_BASE_CLK / TIMER_DIVIDER)  // convert counter value to seconds

#define LEN_MAC_ADDR 20

#if CONFIG_WIFI_ALL_CHANNEL_SCAN
#define DEFAULT_SCAN_METHOD WIFI_ALL_CHANNEL_SCAN
#elif CONFIG_WIFI_FAST_SCAN
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN
#else
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN
#endif /*CONFIG_SCAN_METHOD*/

#if CONFIG_WIFI_CONNECT_AP_BY_SIGNAL
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL
#elif CONFIG_WIFI_CONNECT_AP_BY_SECURITY
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SECURITY
#else
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL
#endif /*CONFIG_SORT_METHOD*/

#if CONFIG_FAST_SCAN_THRESHOLD
#define DEFAULT_RSSI CONFIG_FAST_SCAN_MINIMUM_SIGNAL
#if CONFIG_EXAMPLE_OPEN
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#elif CONFIG_EXAMPLE_WEP
#define DEFAULT_AUTHMODE WIFI_AUTH_WEP
#elif CONFIG_EXAMPLE_WPA
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA_PSK
#elif CONFIG_EXAMPLE_WPA2
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA2_PSK
#else
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#endif
#else
#define DEFAULT_RSSI -127
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#endif /*CONFIG_FAST_SCAN_THRESHOLD*/

static const char *TAG = "scan";

static esp_err_t event_handler(void *ctx, system_event_t *event)
{
    switch (event->event_id) {
        case SYSTEM_EVENT_STA_START:
            ESP_LOGI(TAG, "SYSTEM_EVENT_STA_START");
            ESP_ERROR_CHECK(esp_wifi_connect());
            break;
        case SYSTEM_EVENT_STA_GOT_IP:
            ESP_LOGI(TAG, "SYSTEM_EVENT_STA_GOT_IP");
            ESP_LOGI(TAG, "Got IP: %s\n",
                     ip4addr_ntoa(&event->event_info.got_ip.ip_info.ip));
            break;
        case SYSTEM_EVENT_STA_DISCONNECTED:
            ESP_LOGI(TAG, "SYSTEM_EVENT_STA_DISCONNECTED");
            ESP_ERROR_CHECK(esp_wifi_connect());
            break;
        default:
            break;
    }
    return ESP_OK;
}

/*
 * Goal : Get Channel State Information Packets and fill fields accordingly
 * In : Contexte (null), CSI packet
 * Out : Null, Fill fields of corresponding AP
*/
void receive_csi_cb(void *ctx, wifi_csi_info_t *data) {

    //Setting up the timer
	double time;
    timer_get_counter_time_sec(TIMER_GROUP_0, TIMER_0, &time);	

    //Accessing the csi datatype
	wifi_csi_info_t received = data[0];		//	THIS ONE

	char senddMacChr[LEN_MAC_ADDR] = {0}; // Sender	THIS ONE

	//creates the source mac address and puts in variable senddmacchar
	sprintf(senddMacChr, "%02X:%02X:%02X:%02X:%02X:%02X", received.mac[0], received.mac[1], received.mac[2], received.mac[3], received.mac[4], received.mac[5]);		//THIS ONE

    //Creates the sig filter and the channel filter
	if (strcmp(senddMacChr, "24:FD:52:CB:5D:D3") == 0 && received.rx_ctrl.sig_mode == 1) 		{		
		printf ("%f \n", time);
		int i = 0;	
		for (i = 0; i < data[0].len; i++) {	
			printf("%d\t", data[0].buf[i]);		
		}
		printf("\n");		
	}
	//sleep(1);
}

//Anything with // at the end of the code means it is in the original scan also would have its location
void app_main()
{
    // Initialize NVS
    esp_err_t ret = nvs_flash_init();// main


    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {// main
		ESP_ERROR_CHECK(nvs_flash_erase());// main
		ret = nvs_flash_init();// main
	}// main

	ESP_ERROR_CHECK( ret );// main
    
	tcpip_adapter_init();//scan

	ESP_ERROR_CHECK(esp_event_loop_init(event_handler, NULL));//scan
	wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();//scan

	cfg.csi_enable = 1;	
	
	ESP_ERROR_CHECK(esp_wifi_init(&cfg));
	ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
	ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA)); // Forced to be in AP mode to send frame ...

	//wifi_config_t wifi_configST;
	//wifi_configST.sta.ssid = "HELLO";
	//wifi_configST.sta.password = 1;

    //ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_configST) );
	
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous(true));


	ESP_ERROR_CHECK(esp_wifi_set_csi(1));

	//Configurating the esp32 for channel state info
	wifi_csi_config_t configuration_csi; // CSI = Channel State Information
	configuration_csi.lltf_en = 1;
	configuration_csi.htltf_en = 1;
	configuration_csi.stbc_htltf2_en = 1;
	configuration_csi.channel_filter_en = 0;
	configuration_csi.manu_scale = 0; // Automatic scalling
	//configuration_csi.shift=15; // 0->15
	
	ESP_ERROR_CHECK(esp_wifi_set_csi_config(&configuration_csi));

	ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(&receive_csi_cb, NULL));

	//printf("CSI data setup is done!\n");

	//Timer setup
	timer_config_t config;
	config.divider = TIMER_DIVIDER;
	config.counter_dir = TIMER_COUNT_UP;
	config.counter_en = TIMER_START;
	timer_init(TIMER_GROUP_0, TIMER_0, &config);

	ESP_ERROR_CHECK(timer_start(TIMER_GROUP_0, TIMER_0));
	
	while(1) {
        //Channel Filter
		ESP_ERROR_CHECK(esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE));
		sleep(1);
	}	
}














