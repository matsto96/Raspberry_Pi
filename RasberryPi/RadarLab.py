import drivers

file_name = "radar.bin"

drivers.run_adc(file_name)
drivers.transfer_data_from_pi(file_name)

